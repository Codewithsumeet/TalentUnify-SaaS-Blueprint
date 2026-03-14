"""
Optional post-pipeline GitHub profile enrichment.
Fired by parse_resume_task after successful Tier 5B write if github_url is present.
Non-blocking: runs as a separate Celery task. Failure is silently logged.
Does NOT affect the candidate record if it fails.
"""
import asyncio
import httpx
from tasks.celery_app import celery_app


@celery_app.task(max_retries=1, default_retry_delay=10)
def enrich_github_profile(candidate_id: str, github_url: str) -> dict:
    """
    Fetches public GitHub data and writes it to the candidate record.
    Uses asyncio.run() for Python 3.11 compatibility in sync Celery context.
    """
    async def _fetch() -> dict | None:
        username = github_url.rstrip("/").split("/")[-1]
        if not username or "/" in username:
            return None

        async with httpx.AsyncClient(timeout=5.0) as client:
            try:
                user_r  = await client.get(
                    f"https://api.github.com/users/{username}",
                    headers={"Accept": "application/vnd.github.v3+json"},
                )
                repos_r = await client.get(
                    f"https://api.github.com/users/{username}/repos?sort=stars&per_page=5",
                )
                if user_r.status_code != 200:
                    return None

                user  = user_r.json()
                repos = repos_r.json() if repos_r.status_code == 200 else []

                return {
                    "github_public_repos":  user.get("public_repos", 0),
                    "github_followers":     user.get("followers", 0),
                    "github_top_languages": list({
                        r["language"] for r in repos if r.get("language")
                    }),
                    "github_top_repos": [
                        {
                            "name":        r["name"],
                            "stars":       r["stargazers_count"],
                            "language":    r.get("language"),
                            "description": (r.get("description") or "")[:100],
                        }
                        for r in repos[:3]
                    ],
                    "github_bio": user.get("bio"),
                }
            except Exception:
                return None

    enrichment = asyncio.run(_fetch())
    if not enrichment:
        return {"enriched": False}

    from database import get_db_session
    from models.candidate import Candidate

    with get_db_session() as db:
        cand = db.query(Candidate).filter_by(id=candidate_id).first()
        if cand:
            cand.github_enrichment = enrichment
            db.commit()

    return {"enriched": True, "data": enrichment}
