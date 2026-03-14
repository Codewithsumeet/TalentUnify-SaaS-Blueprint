# TalentUnify — Revised Implementation Guide
**Breach 2026 Hackathon | 48 Hours | 4 Engineers**

---

## Engineer Roles & Ownership

| Engineer | Role | Primary Ownership |
|---|---|---|
| Eng-1 | Frontend | React UI, all pages & components |
| Eng-2 | Backend | FastAPI, DB models, REST routes |
| Eng-3 | AI / NLP | Resume parsing, embeddings, semantic search |
| Eng-4 | DevOps / Integrations | Docker, CI/CD, Gmail, HRMS mock, LinkedIn sim |

---

## Architecture Overview

```
[Sources]                  [Ingestion Layer]           [Core Backend]           [Frontend]
Email (Gmail)   ──────►   Celery Task Queue   ──────►  FastAPI (Python)  ──►  React 18 + Vite
Resume Upload   ──────►   Parser Orchestrator ──────►  PostgreSQL DB     ──►  Tailwind + shadcn
LinkedIn Sim    ──────►   NLP Pipeline        ──────►  Pinecone (Vector) ──►  Single Recruiter UI
HRMS Mock API   ──────►   Deduplicator        ──────►  Redis (Cache)
```

---

## Phase 0 — Pre-Work Checklist (Before Clock Starts)

All engineers complete before the 48-hour timer begins.

- [ ] GitHub repo created, all engineers have access
- [ ] API keys obtained: OpenAI, Pinecone (free tier)
- [ ] Google Cloud project created, Gmail OAuth credentials downloaded
- [ ] `.env.example` committed with all required keys documented
- [ ] Docker Desktop confirmed working on all machines
- [ ] Node.js 20+, Python 3.11, npm confirmed installed

---

## Phase 1 — Setup & Foundation (Hours 0–6)

**Goal:** All four services running locally. Engineers unblocked to work in parallel.

### Eng-1 (Frontend)
```
frontend/
├── src/
│   ├── components/
│   │   ├── layout/
│   │   │   ├── Navbar.tsx
│   │   │   └── Sidebar.tsx
│   │   └── ui/                    # shadcn/ui base components
│   ├── pages/
│   │   ├── DashboardPage.tsx      # Stub with placeholder stats
│   │   ├── CandidatesPage.tsx     # Stub
│   │   ├── SearchPage.tsx         # Stub
│   │   ├── ComparePage.tsx        # NEW — stub for comparison view
│   │   └── IntegrationsPage.tsx   # Stub
│   ├── lib/
│   │   └── api.ts                 # Axios instance with base URL + JWT interceptor
│   └── App.tsx                    # React Router with all routes wired
```

**Setup commands:**
```bash
npm create vite@latest frontend -- --template react-ts
cd frontend && npm install
npm install tailwindcss @shadcn/ui axios react-router-dom lucide-react
npx shadcn-ui@latest init
```

### Eng-2 (Backend)
```
backend/
├── main.py                        # FastAPI app factory, CORS, router includes
├── config.py                      # Settings from env (pydantic-settings)
├── database.py                    # SQLAlchemy engine + SessionLocal
├── models/
│   ├── candidate.py               # Candidate, Resume, Skill models
│   └── user.py                    # User model (JWT auth)
├── alembic/                       # DB migrations
└── requirements.txt
```

**Base models:**
```python
# models/candidate.py
class Candidate(Base):
    __tablename__ = "candidates"
    id           = Column(UUID, primary_key=True, default=uuid4)
    name         = Column(String)
    email        = Column(String, unique=True, index=True)
    phone        = Column(String)
    location     = Column(String)
    linkedin_url = Column(String)             # NEW — for LinkedIn sim data
    source       = Column(String)            # "upload" | "gmail" | "hrms" | "linkedin"
    raw_text     = Column(Text)
    pinecone_id  = Column(String)
    created_at   = Column(DateTime, default=datetime.utcnow)
    skills       = relationship("CandidateSkill", back_populates="candidate")
    experiences  = relationship("Experience", back_populates="candidate")

class Experience(Base):
    __tablename__ = "experiences"
    id           = Column(UUID, primary_key=True, default=uuid4)
    candidate_id = Column(UUID, ForeignKey("candidates.id"))
    company      = Column(String)
    title        = Column(String)
    start_date   = Column(String)
    end_date     = Column(String)
    years        = Column(Float)             # computed duration
```

**Setup commands:**
```bash
pip install fastapi uvicorn sqlalchemy alembic psycopg2-binary pydantic-settings python-jose passlib
alembic init alembic && alembic revision --autogenerate -m "init"
alembic upgrade head
```

### Eng-3 (AI / NLP)
```
backend/ai/
├── __init__.py
├── text_extractor.py              # extract_text(file_bytes, mime_type) -> str
├── nlp/
│   ├── spacy_nlp.py               # NER: name, email, phone, location
│   └── skill_extractor.py         # Taxonomy match + zero-shot fallback
└── embeddings/
    └── client.py                  # get_embedding(text) -> List[float]
```

**Setup commands:**
```bash
pip install spacy transformers torch pypdf python-docx openai pinecone-client sentence-transformers
python -m spacy download en_core_web_sm
```

### Eng-4 (DevOps / Integrations)
```
docker/
├── docker-compose.yml             # postgres, redis, backend, frontend, celery-worker
├── Dockerfile.backend
└── Dockerfile.frontend

.github/workflows/
└── ci.yml                         # Black, ESLint, pytest, vitest on PR
```

**docker-compose.yml (core services):**
```yaml
services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: talentunify
      POSTGRES_USER: tu_user
      POSTGRES_PASSWORD: tu_pass
    ports: ["5432:5432"]
    volumes: [postgres_data:/var/lib/postgresql/data]

  redis:
    image: redis:7-alpine
    ports: ["6379:6379"]

  backend:
    build: ./backend
    env_file: .env
    depends_on: [postgres, redis]
    ports: ["8000:8000"]

  celery-worker:
    build: ./backend
    command: celery -A tasks.celery_app worker --loglevel=info
    env_file: .env
    depends_on: [postgres, redis]

  frontend:
    build: ./frontend
    ports: ["5173:5173"]
```

**Phase 1 Checkpoint (Hour 6):**
- `docker compose up` starts all services with no errors
- `GET /health` returns `{"status": "ok"}`
- Frontend loads at `localhost:5173` with nav and routing working
- All engineers can push/pull to shared repo

---

## Phase 2 — Core Build: Resume Parsing & Database (Hours 6–18)

**Goal:** A resume can be uploaded and its parsed data appears in the database.

### Eng-3: NLP Pipeline

**text_extractor.py:**
```python
def extract_text(file_bytes: bytes, mime_type: str) -> str:
    if mime_type == "application/pdf":
        reader = PdfReader(io.BytesIO(file_bytes))
        return "\n".join(page.extract_text() for page in reader.pages)
    elif mime_type in ("application/vnd.openxmlformats...wordprocessingml", "application/msword"):
        doc = Document(io.BytesIO(file_bytes))
        return "\n".join(p.text for p in doc.paragraphs)
    raise ValueError(f"Unsupported mime type: {mime_type}")
```

**spacy_nlp.py — NER extraction:**
```python
nlp = spacy.load("en_core_web_sm")

def extract_entities(text: str) -> dict:
    doc = nlp(text)
    email = re.findall(r"[\w.+-]+@[\w-]+\.[a-zA-Z]{2,}", text)
    phone = re.findall(r"[\+]?[(]?[0-9]{1,4}[)]?[\s\-.]?[0-9]{3,5}[\s\-.]?[0-9]{4,6}", text)
    name  = next((ent.text for ent in doc.ents if ent.label_ == "PERSON"), None)
    loc   = next((ent.text for ent in doc.ents if ent.label_ in ["GPE","LOC"]), None)
    return {"name": name, "email": email[0] if email else None,
            "phone": phone[0] if phone else None, "location": loc}
```

**skill_extractor.py — 2-phase extraction:**
```python
SKILL_TAXONOMY = [
    "Python","JavaScript","TypeScript","React","Node.js","FastAPI","Django",
    "PostgreSQL","MongoDB","Redis","Docker","Kubernetes","AWS","GCP","Azure",
    "Machine Learning","Deep Learning","NLP","Data Science","SQL","GraphQL",
    "REST APIs","Git","CI/CD","Agile","Scrum","Java","Go","Rust","C++","C#"
]

classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

def extract_skills(text: str) -> List[str]:
    # Phase 1: fast keyword taxonomy match
    found = [s for s in SKILL_TAXONOMY if s.lower() in text.lower()]
    # Phase 2: zero-shot fallback for anything not in taxonomy
    if len(found) < 3:
        result = classifier(text[:512], candidate_labels=SKILL_TAXONOMY, multi_label=True)
        found += [l for l, s in zip(result["labels"], result["scores"]) if s > 0.75]
    return list(set(found))
```

### Eng-2: Resume Routes

**resume/routes.py:**
```python
@router.post("/resume/upload")
async def upload_resume(
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks = BackgroundTasks(),
    db: Session = Depends(get_db)
):
    file_bytes = await file.read()
    task = parse_resume_task.delay(file_bytes, file.content_type, source="upload")
    return {"task_id": task.id, "status": "queued"}

@router.get("/resume/status/{task_id}")
async def get_parse_status(task_id: str):
    result = AsyncResult(task_id)
    return {"task_id": task_id, "status": result.status,
            "result": result.result if result.ready() else None}
```

**tasks/resume_tasks.py (Celery):**
```python
@celery_app.task(bind=True, max_retries=3)
def parse_resume_task(self, file_bytes: bytes, mime_type: str, source: str):
    try:
        text      = extract_text(file_bytes, mime_type)
        entities  = extract_entities(text)
        skills    = extract_skills(text)
        candidate = upsert_candidate(entities, skills, text, source)  # handles dedup
        embedding = get_embedding(build_profile_text(candidate))
        index_to_pinecone(candidate.id, embedding)
        return {"candidate_id": str(candidate.id), "status": "parsed"}
    except Exception as exc:
        raise self.retry(exc=exc, countdown=5)
```

### Eng-1: Upload UI

**components/Resume/ResumeUploadZone.tsx:**
- Drag-and-drop zone (react-dropzone)
- Accept PDF and DOCX only
- POST to `/resume/upload` → poll `/resume/status/{task_id}` every 2s
- Show parsing progress: Queued → Extracting → Parsed → ✅ Added to database
- On success, show extracted name + skills preview before redirect

**Phase 2 Checkpoint (Hour 18):**
- Upload a PDF resume → parsed candidate appears in `/candidates` DB table
- Name, email, skills extracted with >85% accuracy on 5 test resumes
- Celery worker processes tasks asynchronously (no request timeout)

---

## Phase 3 — Semantic Search (Hours 18–30)

**Goal:** Recruiter types natural language query → ranked candidates returned.

### Eng-3: Embeddings & Pinecone

**embeddings/client.py:**
```python
openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)

# Fallback: sentence-transformers if OpenAI is unavailable
try:
    def get_embedding(text: str) -> List[float]:
        response = openai_client.embeddings.create(
            input=text, model="text-embedding-3-small"
        )
        return response.data[0].embedding
except Exception:
    from sentence_transformers import SentenceTransformer
    _local_model = SentenceTransformer("all-MiniLM-L6-v2")
    def get_embedding(text: str) -> List[float]:
        return _local_model.encode(text).tolist()
```

**Profile text builder (for richer embeddings):**
```python
def build_profile_text(candidate: Candidate) -> str:
    skills_str = ", ".join(s.name for s in candidate.skills)
    exp_str    = " | ".join(
        f"{e.title} at {e.company} ({e.years}yr)" for e in candidate.experiences
    )
    return (
        f"Name: {candidate.name}. Location: {candidate.location}. "
        f"Skills: {skills_str}. Experience: {exp_str}."
    )
```

**search/semantic_search.py:**
```python
pc    = Pinecone(api_key=settings.PINECONE_API_KEY)
index = pc.Index("candidates")

def semantic_search(query: str, top_k: int = 20, filters: dict = None) -> List[dict]:
    query_embedding = get_embedding(query)
    results = index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True,
        filter=filters   # e.g., {"location": {"$eq": "San Francisco"}}
    )
    return [
        {"candidate_id": m.id, "score": round(m.score * 100, 1), "metadata": m.metadata}
        for m in results.matches
    ]
```

### Eng-2: Search Routes

```python
@router.post("/search")
async def search_candidates(
    payload: SearchRequest,   # { "query": str, "limit": int, "filters": dict }
    db: Session = Depends(get_db)
):
    matches      = semantic_search(payload.query, top_k=payload.limit or 10)
    candidate_ids = [m["candidate_id"] for m in matches]
    candidates   = db.query(Candidate).filter(Candidate.id.in_(candidate_ids)).all()
    # Merge match scores with DB records
    score_map    = {m["candidate_id"]: m["score"] for m in matches}
    return [
        {**CandidateSchema.from_orm(c).dict(), "match_score": score_map.get(str(c.id), 0)}
        for c in sorted(candidates, key=lambda c: score_map.get(str(c.id), 0), reverse=True)
    ]
```

### Eng-1: Search UI

**pages/SearchPage.tsx:**
- Full-width natural language input: `"Senior React developers in Bangalore with 5+ years"`
- Filter chips: Location | Skills | Years of Experience | Source
- Results grid: CandidateCard with match score badge (🟢 >85%, 🟡 70–85%, 🔴 <70%)
- Each card: name, location, top 5 skills, match %, source badge, "View Profile" + "Add to Compare" buttons

**Phase 3 Checkpoint (Hour 30):**
- Query "Python backend engineers with FastAPI experience" returns relevant candidates
- Match scores are displayed correctly
- Search completes in < 2 seconds

---

## Phase 4 — Integrations (Hours 30–36)

**Goal:** Three ingestion sources beyond manual upload — Gmail, mock HRMS, LinkedIn simulation.

### Eng-4: Gmail Integration

**integrations/gmail/oauth.py:**
```python
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

def get_auth_url() -> str:
    flow = Flow.from_client_secrets_file("credentials.json", scopes=SCOPES,
           redirect_uri=settings.GMAIL_REDIRECT_URI)
    url, _ = flow.authorization_url(prompt="consent")
    return url

def exchange_code(code: str) -> Credentials:
    flow = Flow.from_client_secrets_file("credentials.json", scopes=SCOPES,
           redirect_uri=settings.GMAIL_REDIRECT_URI)
    flow.fetch_token(code=code)
    return flow.credentials
```

**integrations/gmail/service.py:**
```python
def sync_resume_attachments(credentials: Credentials, label: str = "Recruitment"):
    service   = build("gmail", "v1", credentials=credentials)
    messages  = service.users().messages().list(userId="me", labelIds=[label]).execute()
    queued    = 0
    for msg in messages.get("messages", []):
        full_msg = service.users().messages().get(userId="me", id=msg["id"]).execute()
        for part in full_msg["payload"].get("parts", []):
            if part["filename"].endswith((".pdf", ".docx")):
                data = part["body"].get("data", "")
                file_bytes = base64.urlsafe_b64decode(data)
                parse_resume_task.delay(file_bytes, part["mimeType"], source="gmail")
                queued += 1
    return {"queued": queued}
```

**Routes:**
```
GET  /integration/gmail/connect    → returns OAuth URL
GET  /integration/gmail/callback   → exchanges code, stores token
POST /integration/gmail/sync       → triggers attachment fetch
GET  /integration/gmail/status     → returns sync stats
```

---

### Eng-4: Mock HRMS Integration (NEW — fills critical gap)

Simulates pulling candidates from an external HRMS via REST. Allows demo without real HRMS credentials.

**integrations/hrms/mock_data.json:**
```json
[
  {
    "id": "hrms-001",
    "full_name": "Priya Sharma",
    "email": "priya.sharma@example.com",
    "phone": "+91-9876543210",
    "location": "Bengaluru, India",
    "current_title": "Senior Software Engineer",
    "years_experience": 6,
    "skills": ["Python", "Django", "PostgreSQL", "Docker", "AWS"],
    "applied_role": "Backend Engineer",
    "applied_date": "2026-03-01"
  }
  // ... 15-20 realistic entries across roles and locations
]
```

**integrations/hrms/service.py:**
```python
def fetch_hrms_candidates() -> List[dict]:
    """
    In production: replace with actual HRMS REST call.
    e.g., requests.get(f"{settings.HRMS_BASE_URL}/candidates",
                       headers={"Authorization": f"Bearer {settings.HRMS_API_KEY}"})
    """
    with open("integrations/hrms/mock_data.json") as f:
        return json.load(f)

def sync_hrms():
    candidates = fetch_hrms_candidates()
    queued = 0
    for c in candidates:
        ingest_structured_candidate.delay(c, source="hrms")
        queued += 1
    return {"synced": queued, "source": "hrms"}
```

**New Celery task for structured (non-resume) data:**
```python
@celery_app.task
def ingest_structured_candidate(data: dict, source: str):
    """For pre-structured data from HRMS or LinkedIn sim — skips NER, goes straight to upsert."""
    candidate = upsert_candidate_structured(data, source)
    embedding = get_embedding(build_profile_text(candidate))
    index_to_pinecone(candidate.id, embedding)
```

**Routes:**
```
GET  /integration/hrms/status    → connection status (always "connected" for mock)
POST /integration/hrms/sync      → triggers pull from mock data
GET  /integration/hrms/preview   → returns raw mock data for demo visibility
```

---

### Eng-4: LinkedIn Profile Simulation (NEW — fills critical gap)

**integrations/linkedin/simulator.py:**
```python
SIMULATED_PROFILES = [
    {
        "linkedin_url": "https://linkedin.com/in/arjun-mehta-dev",
        "full_name": "Arjun Mehta",
        "headline": "Full Stack Engineer | React | Node.js | 4 years",
        "location": "Mumbai, India",
        "summary": "Passionate engineer with experience building scalable web apps...",
        "skills": ["React", "Node.js", "TypeScript", "MongoDB", "AWS"],
        "experience": [
            {"company": "Infosys", "title": "Software Engineer", "duration_years": 2},
            {"company": "StartupXYZ", "title": "Frontend Lead", "duration_years": 2}
        ]
    }
    // ... 10+ profiles
]

def get_simulated_profiles(limit: int = 10) -> List[dict]:
    return SIMULATED_PROFILES[:limit]
```

**Routes:**
```
GET  /integration/linkedin/profiles          → returns simulated profiles
POST /integration/linkedin/ingest            → ingests all simulated profiles into DB
GET  /integration/linkedin/status            → ingestion statistics
```

**UI note (Eng-1):** Add a "LinkedIn (Simulated)" badge on all candidate cards ingested from this source, making it obvious in the demo.

---

## Phase 5 — Deduplication & Candidate Comparison (Hours 36–42)

**Goal:** No duplicate candidates. Recruiters can compare two candidates side-by-side.

### Eng-2 + Eng-3: Deduplication

**candidate/deduplicator.py:**
```python
def upsert_candidate(entities: dict, skills: List[str], raw_text: str, source: str) -> Candidate:
    db = next(get_db())

    # Layer 1: Exact email match
    if entities.get("email"):
        existing = db.query(Candidate).filter_by(email=entities["email"]).first()
        if existing:
            merge_candidate_data(existing, entities, skills, source)
            return existing

    # Layer 2: Fuzzy name match (Levenshtein distance < 3)
    if entities.get("name"):
        all_candidates = db.query(Candidate).all()
        for c in all_candidates:
            if c.name and Levenshtein.distance(entities["name"].lower(), c.name.lower()) <= 2:
                merge_candidate_data(c, entities, skills, source)
                return c

    # Layer 3: Cosine similarity via Pinecone (>0.92 = same person)
    temp_embedding = get_embedding(raw_text[:512])
    results = index.query(vector=temp_embedding, top_k=1, include_metadata=True)
    if results.matches and results.matches[0].score > 0.92:
        candidate_id = results.matches[0].id
        existing = db.query(Candidate).filter_by(id=candidate_id).first()
        if existing:
            merge_candidate_data(existing, entities, skills, source)
            return existing

    # No duplicate found — create new
    return create_new_candidate(entities, skills, raw_text, source, db)

def merge_candidate_data(existing: Candidate, new_entities: dict, new_skills: List[str], source: str):
    """Merge: fill missing fields, add new skills, append source to source list."""
    for field in ["phone", "location", "linkedin_url"]:
        if not getattr(existing, field) and new_entities.get(field):
            setattr(existing, field, new_entities[field])
    existing_skill_names = {s.name for s in existing.skills}
    for skill in new_skills:
        if skill not in existing_skill_names:
            existing.skills.append(CandidateSkill(name=skill))
    # Track all sources for this candidate
    sources = set(existing.source.split(",") if existing.source else [])
    sources.add(source)
    existing.source = ",".join(sources)
```

### Eng-1: Candidate Comparison Page (NEW — fills critical gap)

**pages/ComparePage.tsx:**
```
Layout: Two-column panel (50/50 split)

Left Panel                          Right Panel
──────────────────────────────────  ──────────────────────────────────
[Search / Select Candidate A]       [Search / Select Candidate B]
Name: Arjun Mehta                   Name: Priya Sharma
Location: Mumbai                    Location: Bengaluru
Match Score: 92%                    Match Score: 88%

Skills:                             Skills:
  ✅ React          ✅ React         ──   ✅ Django
  ✅ Node.js        ──               ✅ PostgreSQL
  ✅ TypeScript     ──               ✅ Docker

Experience: 4 years                 Experience: 6 years
Source: LinkedIn Sim                Source: HRMS

[Add to Shortlist]                  [Add to Shortlist]
```

- Skills highlighted green if shared, amber if unique to that candidate
- "Add to Shortlist" button updates candidate status in DB
- "Export Comparison" button generates a downloadable PDF summary
- URL params: `/compare?a={id}&b={id}` for shareable comparison links

---

## Phase 6 — Polish, Testing & Deployment (Hours 42–48)

**Hour 42–44: Bug fixes & UI polish**
- Eng-1: Responsive layout check (mobile breakpoints), loading skeletons, error states
- Eng-2: API response time audit — all endpoints < 500ms
- Eng-3: Run NLP accuracy suite against 10 sample resumes
- Eng-4: Final Docker build validation

**Hour 44–46: End-to-End Demo Flow**

Execute this exact flow before submission:

1. Open app at production URL
2. Navigate to **Integrations** → Connect Gmail (use test account) → Sync → verify candidates ingested
3. Navigate to **Integrations** → HRMS → Sync → verify 15+ candidates appear
4. Navigate to **Integrations** → LinkedIn → Ingest → verify simulated profiles appear
5. Navigate to **Upload** → drag and drop 3 test resumes → verify all parse correctly
6. Navigate to **Candidates** → verify deduplication (upload same resume twice → only 1 record)
7. Navigate to **Search** → query: `"Senior Python engineers in Bangalore"` → verify relevant results
8. Navigate to **Search** → query: `"React developer with 3+ years TypeScript"` → verify results
9. Navigate to **Compare** → select two candidates → verify side-by-side diff renders
10. Navigate to **Dashboard** → verify stats reflect all ingested candidates

**Hour 46–48: Deployment & Submission**
- Eng-4: Deploy backend to Railway, frontend to Vercel
- Eng-4: Set all production env vars in Railway/Vercel dashboards
- Eng-1: Smoke test production URL with demo flow steps 1–10
- All: Record 3-minute demo video as backup

---

## Environment Variables Reference

```env
# Database
DATABASE_URL=postgresql://tu_user:tu_pass@localhost:5432/talentunify

# Redis / Celery
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/0

# OpenAI
OPENAI_API_KEY=sk-...

# Pinecone
PINECONE_API_KEY=...
PINECONE_ENV=us-east-1
PINECONE_INDEX=candidates

# Gmail OAuth
GMAIL_CLIENT_ID=...
GMAIL_CLIENT_SECRET=...
GMAIL_REDIRECT_URI=http://localhost:8000/integration/gmail/callback

# JWT
JWT_SECRET_KEY=...
JWT_ALGORITHM=HS256

# HRMS Mock (no real keys needed for mock)
HRMS_MOCK_ENABLED=true
```

---

## API Endpoint Summary

| Method | Endpoint | Description |
|---|---|---|
| POST | `/resume/upload` | Upload resume file |
| GET | `/resume/status/{task_id}` | Poll parse status |
| POST | `/search` | Natural language candidate search |
| GET | `/candidates` | List all candidates (paginated) |
| GET | `/candidates/{id}` | Get single candidate profile |
| POST | `/candidates/compare` | Get comparison data for two IDs |
| GET | `/integration/gmail/connect` | Get Gmail OAuth URL |
| GET | `/integration/gmail/callback` | OAuth callback handler |
| POST | `/integration/gmail/sync` | Trigger Gmail sync |
| GET | `/integration/hrms/status` | HRMS connection status |
| POST | `/integration/hrms/sync` | Pull from mock HRMS |
| GET | `/integration/hrms/preview` | View raw HRMS mock data |
| GET | `/integration/linkedin/profiles` | View simulated profiles |
| POST | `/integration/linkedin/ingest` | Ingest LinkedIn simulations |
| GET | `/health` | Health check |

---

## Accuracy & Performance Targets

| Metric | Target | Measurement |
|---|---|---|
| Name extraction accuracy | > 96% | 10-resume test suite |
| Skill extraction accuracy | > 85% | 10-resume test suite |
| API response time (non-search) | < 500ms | manual timing |
| Search response time | < 2 seconds | manual timing |
| Resume parse time (async) | < 10 seconds | Celery task duration |
| Dedup false positive rate | < 5% | manual verification |

---

## Risk Register & Mitigations

| Risk | Probability | Mitigation |
|---|---|---|
| OpenAI API rate limit during demo | Medium | sentence-transformers fallback pre-loaded |
| Pinecone free tier limit hit | Low | seed with ≤ 100 candidates for demo |
| Gmail OAuth flow breaks in prod | Medium | pre-authorize test account before demo |
| NLP accuracy below target | Low | expand SKILL_TAXONOMY to 60+ entries |
| Docker build fails on deploy | Low | test Railway deploy by Hour 44 |
| HRMS/LinkedIn gap visible to judges | Mitigated | both now fully implemented in Phase 4 |
| Candidate comparison not built | Mitigated | now fully scoped in Phase 5 |
