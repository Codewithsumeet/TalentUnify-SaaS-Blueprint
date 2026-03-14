"""
Optional post-pipeline GitHub enrichment.
Non-blocking Celery task. Failure does NOT affect the candidate record.
Uses asyncio.run() — correct for Python 3.11+ sync Celery workers.
"""
import asyncio

import httpx

from .celery_app import celery_app


@celery_app.task(max_retries=1, default_retry_delay=10, ignore_result=True)
def enrich_github(candidate_id: str, github_url: str) -> dict:
    """
    Fetches public GitHub profile data and writes it to the candidate record.
    Returns {"enriched": True} on success, {"enriched": False} on any failure.
    """

    async def _fetch() -> dict | None:
        username = github_url.rstrip("/").split("/")[-1]
        if not username or "/" in username:
            return None

        async with httpx.AsyncClient(timeout=5.0) as client:
            try:
                user_resp  = await client.get(
                    f"https://api.github.com/users/{username}",
                    headers={"Accept": "application/vnd.github.v3+json"},
                )
                repos_resp = await client.get(
                    f"https://api.github.com/users/{username}/repos"
                    "?sort=stars&per_page=5",
                )
                if user_resp.status_code != 200:
                    return None

                user  = user_resp.json()
                repos = repos_resp.json() if repos_resp.status_code == 200 else []

                return {
                    "github_public_repos":  user.get("public_repos", 0),
                    "github_followers":     user.get("followers", 0),
                    "github_bio":           user.get("bio"),
                    "github_top_languages": list({
                        repo["language"]
                        for repo in repos
                        if repo.get("language")
                    }),
                    "github_top_repos": [
                        {
                            "name":        repo["name"],
                            "stars":       repo["stargazers_count"],
                            "language":    repo.get("language"),
                            "description": (repo.get("description") or "")[:100],
                        }
                        for repo in repos[:3]
                    ],
                }
            except Exception:
                return None

    enrichment = asyncio.run(_fetch())

    if not enrichment:
        return {"enriched": False}

    from database import get_db_session
    from models.candidate import Candidate

    with get_db_session() as db:
        candidate = db.query(Candidate).filter_by(id=candidate_id).first()
        if candidate:
            candidate.github_enrichment = enrichment
            db.commit()

    return {"enriched": True, "repos": len(enrichment.get("github_top_repos", []))}
