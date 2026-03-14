"""
LinkedIn Simulation Integration.

Generates realistic fintech LinkedIn profiles and feeds them into the
TalentFlow pipeline as if they came from a LinkedIn data source.

In production: replace with LinkedIn OAuth + Profile API.
For hackathon: provides /api/v1/intake/linkedin-import to demo the source.
"""
import random
import uuid
from typing import Optional

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/api/v1/intake")

# ── Realistic profile data pools ──────────────────────────────────────────────

_FIRST = ["Aditya","Sneha","Vikram","Pooja","Rahul","Meera","Arjun","Nisha",
          "Kiran","Tanvi","Siddharth","Kavya","Manish","Swati","Deepak"]
_LAST  = ["Sharma","Patel","Singh","Kumar","Joshi","Rao","Nair","Mehta",
          "Gupta","Iyer","Bose","Reddy","Agarwal","Shah","Das"]

_ROLES = [
    ("Senior Software Engineer",   "Razorpay"),
    ("ML Engineer",                "PhonePe"),
    ("Backend Engineer",           "CRED"),
    ("Full Stack Developer",       "Zepto"),
    ("DevOps Engineer",            "Groww"),
    ("Data Scientist",             "Slice"),
    ("Blockchain Developer",       "Polygon"),
    ("Platform Engineer",          "BharatPe"),
    ("Security Engineer",          "Paytm"),
    ("Mobile Engineer",            "Jupiter"),
]

_SKILL_POOLS = {
    "Senior Software Engineer":  ["Go","Python","Kafka","PostgreSQL","Redis","Docker","Kubernetes","gRPC"],
    "ML Engineer":               ["Python","PyTorch","TensorFlow","LangChain","FastAPI","Pinecone","HuggingFace"],
    "Backend Engineer":          ["Python","FastAPI","PostgreSQL","Redis","Celery","Docker","SQLAlchemy"],
    "Full Stack Developer":      ["React","Node.js","TypeScript","MongoDB","AWS","Next.js","Tailwind"],
    "DevOps Engineer":           ["Kubernetes","Docker","Terraform","GitHub Actions","AWS","Prometheus","Grafana"],
    "Data Scientist":            ["Python","Pandas","NumPy","Scikit-learn","PyTorch","Tableau","Jupyter"],
    "Blockchain Developer":      ["Solidity","Web3","Rust","Go","DeFi","Ethereum","Hardhat"],
    "Platform Engineer":         ["Go","Kubernetes","Terraform","AWS","Prometheus","Redis","PostgreSQL"],
    "Security Engineer":         ["Python","Go","AWS","Kubernetes","Penetration Testing","SIEM","IAM"],
    "Mobile Engineer":           ["Swift","Kotlin","React Native","Firebase","iOS","Android","REST API"],
}

_LOCATIONS = ["Bangalore","Mumbai","Hyderabad","Pune","Chennai","Delhi","Gurgaon","Noida","Kochi"]


def _generate_profile() -> dict:
    first      = random.choice(_FIRST)
    last       = random.choice(_LAST)
    name       = f"{first} {last}"
    role, company = random.choice(_ROLES)
    location   = random.choice(_LOCATIONS)
    exp_years  = round(random.uniform(1.5, 10.0), 1)
    skills     = random.sample(_SKILL_POOLS.get(role, ["Python","Docker"]),
                               k=min(6, len(_SKILL_POOLS.get(role, []))))
    email      = f"{first.lower()}.{last.lower()}{random.randint(10,99)}@linkedin-sim.talentflow.dev"

    markdown = f"""# {name}

**{role}** at **{company}**
📍 {location} | {exp_years} years experience

## Contact
- Email: {email}
- LinkedIn: https://linkedin.com/in/{first.lower()}-{last.lower()}-{uuid.uuid4().hex[:6]}

## Experience

### {role} — {company}
*{max(1, int(exp_years) - 2)} years*

Working on core fintech infrastructure and scaling distributed systems.

### Junior Engineer — Previous Company
*{min(2, int(exp_years))} years*

Built and maintained production services handling high transaction volumes.

## Skills
{', '.join(skills)}

## Education
B.Tech in Computer Science — IIT/NIT ({2024 - int(exp_years) - 4})
"""
    return {
        "name": name, "email": email, "location": location,
        "role": role, "company": company, "exp_years": exp_years,
        "skills": skills, "markdown": markdown,
    }


class LinkedInImportRequest(BaseModel):
    count:   int                = 3    # how many profiles to generate
    query:   Optional[str]      = None # filter hint (not used in sim, logged only)


@router.post("/linkedin-import")
async def linkedin_import(req: LinkedInImportRequest):
    """
    Generates `count` realistic LinkedIn profiles and queues them for parsing.
    Simulates what a LinkedIn API integration would provide.
    """
    count    = min(req.count, 10)   # cap at 10 per request
    task_ids = []
    from tasks.resume_tasks import parse_resume

    for _ in range(count):
        profile  = _generate_profile()
        md_bytes = profile["markdown"].encode("utf-8")

        task = parse_resume.delay(
            file_bytes = md_bytes,
            mime_type  = "text/markdown",
            source     = "linkedin",
            filename   = f"{profile['name'].replace(' ','_')}_linkedin.md",
            metadata   = {
                "source_system": "linkedin_sim",
                "query_hint":    req.query,
                "pre_extracted": {
                    "name":             profile["name"],
                    "email":            profile["email"],
                    "location":         profile["location"],
                    "current_role":     profile["role"],
                    "current_company":  profile["company"],
                    "experience_years": profile["exp_years"],
                    "skills_phase2":    profile["skills"],
                },
            },
        )
        task_ids.append({"name": profile["name"], "task_id": task.id})

    return {
        "imported": len(task_ids),
        "source":   "linkedin_sim",
        "tasks":    task_ids,
        "status":   "queued",
    }
