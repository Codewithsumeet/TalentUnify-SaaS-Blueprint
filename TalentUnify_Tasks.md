# TalentUnify Hackathon Task Tracker

This file serves as the master task list derived from the `TalentUnify_Implementation_Guide.md` for the 48-hour Breach 2026 Hackathon.

## Phase 0 — Pre-Work Checklist (Before Clock Starts)
- [ ] **All Engineers:** Create GitHub repo and ensure everyone has access
- [ ] **All Engineers:** Obtain API keys (OpenAI, Pinecone free tier)
- [ ] **All Engineers:** Create Google Cloud project; download Gmail OAuth credentials
- [ ] **All Engineers:** Commit `.env.example` with all required keys documented
- [ ] **All Engineers:** Confirm Docker Desktop is working on all machines
- [ ] **All Engineers:** Verify Node.js 20+, Python 3.11, and npm are installed

---

## Phase 1 — Setup & Foundation (Hours 0–6)
*Goal: All four services running locally. Engineers unblocked to work in parallel.*

### Eng-1 (Frontend)
- [ ] Initialize React 18 + Vite frontend app (`npm create vite@latest frontend -- --template react-ts`)
- [ ] Install frontend dependencies (`tailwindcss`, `@shadcn/ui`, `axios`, `react-router-dom`, `lucide-react`)
- [ ] Initialize `shadcn-ui`
- [ ] Scaffold folder structure (`src/components/layout`, `src/components/ui`, `src/pages`, `src/lib`)
- [ ] Create stub pages (`DashboardPage.tsx`, `CandidatesPage.tsx`, `SearchPage.tsx`, `ComparePage.tsx`, `IntegrationsPage.tsx`)
- [ ] Configure base Axios instance (`lib/api.ts`) with JWT interceptor
- [ ] Set up React Router in `App.tsx` and wire up basic navigation (`Navbar.tsx`, `Sidebar.tsx`)

### Eng-2 (Backend)
- [ ] Initialize Python FastAPI backend environment
- [ ] Install backend dependencies (FastAPI, uvicorn, sqlalchemy, alembic, psycopg2-binary, pydantic-settings, python-jose, passlib)
- [ ] Set up `main.py` factory, CORS, and route includes
- [ ] Implement config management using `pydantic-settings` (`config.py`)
- [ ] Set up database engine and connection pool (`database.py`)
- [ ] Define initial base SQLAlchemy models (`models/candidate.py`, `models/user.py`)
- [ ] Initialize Alembic, generate first migration, and upgrade DB head

### Eng-3 (AI / NLP)
- [ ] Initialize Python environment for AI/NLP tasks
- [ ] Install dependencies (`spacy`, `transformers`, `torch`, `pypdf`, `python-docx`, `openai`, `pinecone-client`, `sentence-transformers`)
- [ ] Download spacy NLP model (`python -m spacy download en_core_web_sm`)
- [ ] Add `backend/ai/text_extractor.py` skeleton
- [ ] Add `backend/ai/nlp/spacy_nlp.py` and `skill_extractor.py` skeletons
- [ ] Add `backend/ai/embeddings/client.py` skeleton

### Eng-4 (DevOps / Integrations)
- [ ] Create root `docker-compose.yml` for `postgres`, `redis`, `backend`, `frontend`, `celery-worker`
- [ ] Write `Dockerfile.backend` and `Dockerfile.frontend`
- [ ] Set up GitHub Actions CI workflow for Black, ESLint, pytest, and vitest
- [ ] **Phase 1 Checkpoint:** 
  - [ ] `docker compose up` starts without errors
  - [ ] `GET /health` returns `{"status": "ok"}`
  - [ ] Frontend successfully loads on port `5173`

---

## Phase 2 — Core Build: Resume Parsing & Database (Hours 6–18)
*Goal: A resume can be uploaded and its parsed data appears in the database.*

### Eng-3 (AI / NLP)
- [ ] Implement `extract_text` parsing logic for `.pdf` and `.docx` (`text_extractor.py`)
- [ ] Build Named Entity Recognition (NER) to extract name, email, phone, location (`spacy_nlp.py`)
- [ ] Complete `skill_extractor.py` combining fast keyword taxonomy extraction and zero-shot fallback

### Eng-2 (Backend)
- [ ] Create `POST /resume/upload` route to trigger Celery task
- [ ] Create `GET /resume/status/{task_id}` for clients to poll parsing progress
- [ ] Develop `parse_resume_task` Celery task (`tasks/resume_tasks.py`) 
- [ ] Ensure Celery task orchestrates text extraction, NLP, skill extraction, database insertion, and vector index updates

### Eng-1 (Frontend)
- [ ] Build `ResumeUploadZone.tsx` supporting drag-and-drop (`react-dropzone`)
- [ ] Wire upload component to `POST /resume/upload` and start polling `GET /resume/status/{task_id}`
- [ ] Implement parsing progress visuals (Queued → Extracting → Parsed → Added)
- [ ] Show parsed candidate preview prior to redirection
- [ ] **Phase 2 Checkpoint:** Uploading a PDF successfully creates a parsed candidate record in the DB asynchronously.

---

## Phase 3 — Semantic Search (Hours 18–30)
*Goal: Recruiter types natural language query → ranked candidates returned.*

### Eng-3 (AI / NLP)
- [ ] Implement `get_embedding` with OpenAI and hook up `sentence-transformers` fallback (`client.py`)
- [ ] Write `build_profile_text` function to assemble a candidate’s textual representation for vectorization
- [ ] Integrate with Pinecone cluster; implement `semantic_search` lookup (`search/semantic_search.py`)

### Eng-2 (Backend)
- [ ] Expose `POST /search` route accepting `{ "query": str, "limit": int, "filters": dict }`
- [ ] Ensure `POST /search` fetches top Pinecone matches and joins with DB candidate data returning match scores

### Eng-1 (Frontend)
- [ ] Construct `SearchPage.tsx` featuring a prominent natural language input
- [ ] Add Filter chips for location, skills, experience, and source
- [ ] Build Result Grid containing `CandidateCard` components
- [ ] Define Match Score badges in `CandidateCard` (🟢 >85%, 🟡 70–85%, 🔴 <70%)
- [ ] **Phase 3 Checkpoint:** Example queries return expected candidate items accurately within 2 seconds.

---

## Phase 4 — Integrations (Hours 30–36)
*Goal: Implement three ingestion sources beyond manual upload.*

### Eng-4 (DevOps / Integrations)
- [ ] **Gmail Integration:**
  - [ ] Implement `get_auth_url` and `exchange_code` (`integrations/gmail/oauth.py`)
  - [ ] Build `sync_resume_attachments` fetching recent .pdf/.docx files and dispatching `parse_resume_task` (`service.py`)
  - [ ] Add Gmail endpoints (`/connect`, `/callback`, `/sync`, `/status`)
- [ ] **Mock HRMS Integration:**
  - [ ] Create mock JSON dataset spanning 15-20 candidates (`integrations/hrms/mock_data.json`)
  - [ ] Develop `sync_hrms` utilizing `ingest_structured_candidate.delay()` (`service.py`)
  - [ ] Expose HRMS routes (`/status`, `/sync`, `/preview`)
- [ ] **LinkedIn Simulation:**
  - [ ] Seed 10+ detailed fallback profiles (`integrations/linkedin/simulator.py`)
  - [ ] Provide endpoints to expose and trigger LinkedIn ingestion (`/profiles`, `/ingest`, `/status`)

### Eng-1 (Frontend)
- [ ] Update frontend UI to show unique "LinkedIn (Simulated)" labels on appropriate candidate cards

---

## Phase 5 — Deduplication & Candidate Comparison (Hours 36–42)
*Goal: Prevent duplications and allow visual side-by-side analysis.*

### Eng-2 & Eng-3 (Backend / Context matching)
- [ ] Rewrite `upsert_candidate` in `deduplicator.py` combining three layers:
  1. Exact Email match
  2. Fuzzy Name match (Levenshtein distance <= 2)
  3. Context/Embedding duplicate detection (Cosine similarity > 0.92)
- [ ] Create robust `merge_candidate_data` logic to unify fields and append multiple sources without clobbering existing DB records

### Eng-1 (Frontend)
- [ ] Complete `ComparePage.tsx` using a 50/50 vertical division layout
- [ ] Develop visual diff logic for highlighting shared vs. unique skills
- [ ] Implement "Add to Shortlist" and "Export Comparison" functionality
- [ ] Configure React Router config to ingest standard `?a={id}&b={id}` parameter payloads

---

## Phase 6 — Polish, Testing & Deployment (Hours 42–48)
*Goal: End-to-end verification, bug-squashing, UI cleanup, and production deployment.*

### Hours 42–44 (Polish)
- [ ] **Eng-1:** Run through a responsive layout check (mobile breaking rules), and examine all skeleton loading states.
- [ ] **Eng-2:** Code review API response times (Hard limit: <500ms for standard requests).
- [ ] **Eng-3:** Audit NLP extraction with a minimum of 10 test suite resumes targeting >96% name extraction and >85% skill extraction.
- [ ] **Eng-4:** Finalize and validate local Docker build.

### Hours 44–46 (End-to-End Testing)
- [ ] **All Engineers:** Step-by-step verification of Demo Flow (Steps 1 through 10 listed in Implementation Guide)

### Hours 46–48 (Deployment)
- [ ] **Eng-4:** Deploy Backend onto Railway and Frontend onto Vercel.
- [ ] **Eng-4:** Replicate `.env` securely across Railway/Vercel dashboards.
- [ ] **Eng-1:** Conduct quick smoke testing on live Production URLs.
- [ ] **All Engineers:** Record fallback 3-minute video presentation.
