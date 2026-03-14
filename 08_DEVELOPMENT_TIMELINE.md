# 08 — 48-HOUR DEVELOPMENT TIMELINE
## Hour-by-Hour Plan with Engineer Assignments & Sync Points

---

## ⏰ Timeline Overview

| Hours | Phase | Primary Focus | Output |
|-------|-------|---------------|--------|
| **0-2** | 🔧 Setup | Local dev environment | Docker, DB, all services running |
| **2-6** | 🧱 Foundation | Basic UI + API + Parser | Swagger docs, basic components |
| **6-18** | 🏗️ Core Build | Resume parsing pipeline | End-to-end upload → parse → store |
| **18-30** | 🔍 Search | Embeddings + semantic search | `/search` returning ranked results |
| **30-36** | 📧 Integration | Gmail OAuth connection | Email resumes auto-imported |
| **36-42** | ✨ Polish | Tier 2 feature + bug fixes | Bug-free MVP |
| **42-46** | 🧪 Testing | Full demo flow testing | Demo-ready system |
| **46-48** | 🚀 Deploy | Production deploy + present | Live URL + presentation |

---

## 🕐 HOURS 0-2: Project Setup & Architecture Alignment

**All 4 Engineers Together**

- [ ] Clone repo & set up local environment
- [ ] Run `scripts/setup.sh` to bootstrap project
- [ ] Create `.env` files with API keys (OpenAI, Pinecone, etc.)
- [ ] Start PostgreSQL + Redis via Docker
- [ ] Verify all 4 services can start locally
- [ ] Review architecture docs together (15 min)
- [ ] Set up team communication (Slack channel for blockers)
- [ ] Set up Git workflow: `main` → `develop` → `feature/*`

**✅ Deliverable:** Working local dev environment for all 4 engineers

---

## 🕑 HOURS 2-6: Foundation (Tier 1 Features Begin)

### Engineer 1 — Frontend
- [ ] Set up React 18 + TypeScript + Vite + Tailwind
- [ ] Create Navbar + Sidebar layout components
- [ ] Build Dashboard page with hardcoded stats
- [ ] Build ResumeUploadZone (drag-and-drop)
- [ ] Create CandidateCard component
- [ ] Set up React Router

### Engineer 2 — Backend
- [ ] Initialize FastAPI project
- [ ] Create database models (User, Candidate, Resume, Skills)
- [ ] Set up SQLAlchemy ORM + Alembic migrations
- [ ] Build JWT authentication (register, login)
- [ ] Create `/candidate` GET/POST endpoints
- [ ] Set up error handling & logging middleware
- [ ] **Generate Swagger docs** (critical for E1)

### Engineer 3 — AI/NLP
- [ ] Validate OpenAI API key works
- [ ] Install spaCy (`en_core_web_sm`) + transformers + pypdf
- [ ] Build `extract_text()` function (PDF/DOCX)
- [ ] Build spaCy NER for name/email/phone/location
- [ ] Build keyword-based skill extraction
- [ ] Create ParsedResume Pydantic schema
- [ ] Test with 5 sample resumes

### Engineer 4 — DevOps
- [ ] Set up Docker + `docker-compose.yml`
- [ ] Create Dockerfiles for backend + frontend
- [ ] Set up GitHub repo + branch protection
- [ ] Create CI pipelines (`.github/workflows/`)
- [ ] Set up PostgreSQL + Redis in Docker
- [ ] Test: `docker-compose up` works

### 🔄 SYNC POINT — Hour 6
- [ ] PostgreSQL running locally
- [ ] FastAPI serves `/docs` (Swagger UI)
- [ ] React app builds and serves
- [ ] All 4 engineers can commit without conflicts

---

## 🕕 HOURS 6-18: Resume Parsing Pipeline

### Engineer 3 (AI) — PRIMARY
- [ ] Integrate spaCy NER into full parsing pipeline
- [ ] Implement zero-shot skill extraction (HuggingFace)
- [ ] Create `/ai/extract-skills` endpoint
- [ ] Build skill normalization (e.g., "Python3" → "Python")
- [ ] Test with 20+ real resumes
- [ ] Measure accuracy → target 85%+
- [ ] Document edge cases

### Engineer 2 (Backend) — SUPPORTING
- [ ] Create `/resume/upload` endpoint
- [ ] Create `/resume/parse` endpoint
- [ ] Integrate with AI parser service
- [ ] Store parsed data in PostgreSQL
- [ ] Build resume versioning (multiple uploads per candidate)
- [ ] Set up Celery task for async parsing

### Engineer 1 (Frontend) — SUPPORTING
- [ ] Build ResumeUploadZone with file drag-drop
- [ ] Add upload progress indicator
- [ ] Display parsed resume data
- [ ] Show extraction confidence score
- [ ] Connect to `/resume/upload` API
- [ ] Add loading spinners

### Engineer 4 (DevOps) — SUPPORTING
- [ ] Set up Celery + Redis for task queuing
- [ ] Monitor Celery task execution
- [ ] Set up file storage (local or MinIO)

### 🔄 SYNC POINT — Hour 12
- [ ] Upload resume → Parse → Store → Retrieve ✅
- [ ] Parsing accuracy 85%+
- [ ] 10+ test resumes processed successfully

---

## 🕕 HOURS 18-30: Candidate Search & Embeddings

### Engineer 3 (AI) — PRIMARY
- [ ] Set up Pinecone account + API key
- [ ] Create Pinecone index `"candidates"` (1536 dims, cosine)
- [ ] Implement OpenAI embedding generation
- [ ] Build embedding pipeline for candidate profiles
- [ ] Build semantic search function
- [ ] Test with real queries:
  - "Find Python developers"
  - "AWS architects with 5+ years"
  - "React engineers in San Francisco"
- [ ] Manual relevance evaluation

### Engineer 2 (Backend) — PRIMARY
- [ ] Create `/search` endpoint (natural language)
- [ ] Integrate AI embeddings service
- [ ] Build query parser (NL → structured filters)
- [ ] Implement result ranking algorithm
- [ ] Create `/search/history` endpoint
- [ ] Set up search caching (Redis)

### Engineer 1 (Frontend) — SUPPORTING
- [ ] Build SearchBar component with autocomplete
- [ ] Create SearchResults component
- [ ] Build FilterPanel (skills, years, location)
- [ ] Build result cards with match score + explanation
- [ ] Connect to `/search` API
- [ ] Add keyboard shortcut (Ctrl+K)

### Engineer 4 (DevOps) — SUPPORTING
- [ ] Set up Pinecone CLI tools
- [ ] Create smoke test for embeddings
- [ ] Monitor API performance

### 🔄 SYNC POINT — Hour 24
- [ ] Type NL query → Get ranked results ✅
- [ ] Search latency < 2 seconds
- [ ] Results are semantically relevant

---

## 🕕 HOURS 30-36: Gmail Integration (Tier 1)

### Engineer 4 (DevOps) — PRIMARY
- [ ] Set up Gmail OAuth app (Google Cloud Console)
- [ ] Implement OAuth2 flow in FastAPI
- [ ] Create `/integration/gmail/connect` endpoint
- [ ] Create `/integration/gmail/callback` endpoint
- [ ] Fetch emails with attachments
- [ ] Queue attachments for async parsing (Celery)

### Engineer 2 (Backend) — SUPPORTING
- [ ] Create IntegrationToken model
- [ ] Store OAuth tokens (encrypted)
- [ ] Build `/integration/gmail/status` endpoint
- [ ] Build `/integration/gmail/sync` endpoint
- [ ] Error recovery (retry failed emails)

### Engineer 1 (Frontend) — SUPPORTING
- [ ] Build GmailConnectButton
- [ ] Show OAuth flow (popup window)
- [ ] Display connection status
- [ ] Build sync progress indicator
- [ ] Add manual "Sync Now" button

### 🔄 SYNC POINT — Hour 32
- [ ] Connect Gmail → Fetch resumes → Auto-parse → DB ✅
- [ ] 20+ emails with attachments processed

---

## 🕕 HOURS 36-42: Polish & Tier 2 Feature

### ALL ENGINEERS — DECIDE TIER 2 FEATURE

> **Recommended:** Candidate Deduplication (4h, lowest risk, shows AI depth)

### Polish Tasks (ALL)
- [ ] Fix TypeScript errors
- [ ] Fix ESLint warnings
- [ ] Test responsive design
- [ ] Fix slow API responses
- [ ] Set up error boundaries in React
- [ ] Improve loading states
- [ ] Write basic tests (5-10 per engineer)
- [ ] Test all integrations end-to-end

---

## 🕕 HOURS 42-46: Demo Prep & Testing

### ALL ENGINEERS
- [ ] Test full demo flow (10 steps):
  1. Login → 2. Dashboard → 3. Upload resume → 4. See parsed data
  5. Connect Gmail → 6. NL search → 7. View results
  8. Candidate profile → 9. Compare → 10. Architecture slide
- [ ] Prepare 5-minute demo script
- [ ] Create 3-4 test candidates in seed data
- [ ] Test on clean database
- [ ] Screenshot key flows
- [ ] Fix visual bugs
- [ ] Performance test: search < 2s, page load < 3s

---

## 🕕 HOURS 46-48: Final Deploy & Presentation

### Engineer 4 (DevOps) — PRIMARY
- [ ] Deploy backend to Railway/Render
- [ ] Deploy frontend to Vercel
- [ ] Configure production `.env`
- [ ] Run smoke tests on production
- [ ] Set up monitoring

### Engineers 1, 2, 3
- [ ] Practice demo (5 minutes)
- [ ] Prepare talking points
- [ ] Have backup demo (local machine)
- [ ] Prepare GitHub repo link + live demo link

---

## 🚨 If You're Behind Schedule

| Situation | Action |
|-----------|--------|
| **Behind at Hour 24** | Cut all Tier 2 features, focus on Tier 1 polish |
| **Behind at Hour 36** | Use mock data for Gmail, hardcode search results |
| **Behind at Hour 42** | Deploy what works, prepare backup screenshots |
| **Something breaks at Hour 44** | Revert last commit, use hardcoded fallbacks |

---

## 🔗 Cross-References
- **Feature list for each phase:** → [03_FEATURE_TRIAGE.md](./03_FEATURE_TRIAGE.md)
- **Which files each engineer builds:** → [07_PROJECT_STRUCTURE_AND_OWNERSHIP.md](./07_PROJECT_STRUCTURE_AND_OWNERSHIP.md)
- **Deployment procedures:** → [09_DEVOPS_AND_DEPLOYMENT.md](./09_DEVOPS_AND_DEPLOYMENT.md)
- **Demo script to rehearse:** → [10_DEMO_AND_PRESENTATION.md](./10_DEMO_AND_PRESENTATION.md)

---

*Source: REFINED_CTO_BLUEPRINT_PROMPT.md (Section 11), QUICK_REFERENCE_INDEX.md, Deep Research Report*
