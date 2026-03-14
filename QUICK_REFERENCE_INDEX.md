# QUICK REFERENCE INDEX
## Navigation Guide for Refined CTO Blueprint & Project Structure

---

## 📋 DOCUMENT NAVIGATION

### For Quick Onboarding (5 minutes)
- **Read:** ERROR_ANALYSIS_AND_CORRECTIONS.md → Summary Table
- **Then:** REFINED_CTO_BLUEPRINT_PROMPT.md → Section 1 (Overview) + Section 10 (Timeline)

### For Feature Planning (30 minutes)
- **Read:** REFINED_CTO_BLUEPRINT_PROMPT.md → Section 2 (MVP Feature Prioritization)
- **Reference:** Section 3 (Architecture)
- **Detail:** Section 4 (AI Pipeline)

### For Implementation (Throughout hackathon)
- **Architecture:** REFINED_CTO_BLUEPRINT_PROMPT.md → Section 3 + Section 4
- **API Endpoints:** REFINED_CTO_BLUEPRINT_PROMPT.md → Section 9
- **Folder Structure:** REFINED_CTO_BLUEPRINT_PROMPT.md → Section 7
- **Development Timeline:** REFINED_CTO_BLUEPRINT_PROMPT.md → Section 10

### For Demo Preparation (Hour 40)
- **Read:** REFINED_CTO_BLUEPRINT_PROMPT.md → Section 12 (Demo Flow + Script)
- **Practice:** Run through 5-minute demo
- **Backup:** Have local instance + screenshots ready

### For Deployment (Hour 46)
- **Read:** REFINED_CTO_BLUEPRINT_PROMPT.md → Section 14 (CI/CD)
- **Execute:** GitHub Actions workflows, deploy to Railway + Vercel
- **Verify:** Health checks, smoke tests

---

## 🗂️ PROJECT FOLDER STRUCTURE AT A GLANCE

```
talent-unify/
├── 🎨 frontend/                    [Engineer 1 — Full Ownership]
│   ├── src/pages/                  → DashboardPage, SearchPage, ProfilePage
│   ├── src/components/             → Reusable UI components
│   ├── src/services/               → API client calls
│   └── src/hooks/                  → Custom React hooks
│
├── ⚙️ backend/                      [Engineer 2 — Full Ownership]
│   ├── app/auth/                   → JWT + OAuth2
│   ├── db/models.py                → SQLAlchemy ORM models
│   ├── resume/parser.py            → Resume parsing logic
│   ├── candidate/service.py        → Candidate business logic
│   ├── search/semantic_search.py   → Pinecone search
│   └── integrations/gmail/         → Gmail OAuth
│
├── 🤖 ai/                           [Engineer 3 — Full Ownership]
│   ├── services/resume_parser.py   → Standalone parser
│   ├── services/embedding_service.py → OpenAI embeddings
│   ├── services/skill_extractor.py → Zero-shot classification
│   └── notebooks/                  → Experimentation
│
├── 🔗 integrations/                 [Engineer 4 — Full Ownership]
│   ├── gmail/client.py             → Gmail API client
│   ├── hrms/simulator.py           → HRMS mock
│   └── linkedin/simulator.py       → LinkedIn mock
│
├── 📦 scripts/                      [Engineer 4 — DevOps]
│   ├── setup.sh                    → One-command setup
│   ├── seed_db.py                  → Populate demo data
│   └── deploy.sh                   → Production deploy
│
├── 🐳 docker/                       [Engineer 4 — DevOps]
│   ├── Dockerfile.backend
│   ├── Dockerfile.frontend
│   └── docker-compose.yml
│
├── 📚 docs/                         [Team — Shared]
│   ├── ARCHITECTURE.md             → System design
│   ├── API.md                      → API reference
│   ├── DEMO_SCRIPT.md              → Exact demo steps
│   └── DEPLOYMENT.md               → Deploy procedures
│
└── .github/workflows/               [Engineer 4 — CI/CD]
    ├── ci-backend.yml
    ├── ci-frontend.yml
    └── deploy.yml
```

### Quick File Lookup by Owner

**Engineer 1 (Frontend):**
- `frontend/src/pages/*` — All page components
- `frontend/src/components/*` — All UI components
- `frontend/src/services/api.ts` — API client
- `frontend/src/hooks/*` — React hooks

**Engineer 2 (Backend):**
- `backend/main.py` — FastAPI app
- `backend/db/models.py` — Database models
- `backend/auth/routes.py` — Auth endpoints
- `backend/candidate/routes.py` — Candidate endpoints
- `backend/resume/routes.py` — Resume endpoints
- `backend/search/routes.py` — Search endpoints

**Engineer 3 (AI/NLP):**
- `backend/ai/embeddings/` — Embedding generation
- `backend/ai/nlp/` — NLP entity recognition
- `ai/services/resume_parser_service.py` — Standalone parser
- `ai/services/embedding_service.py` — Embedding service
- `ai/notebooks/` — Experimentation

**Engineer 4 (DevOps):**
- `.github/workflows/` — CI/CD pipelines
- `docker/` — Container configs
- `scripts/setup.sh` — Setup automation
- `scripts/deploy.sh` — Deploy automation
- `backend/integrations/` — Integration setup
- `docker-compose.yml` — Local dev orchestration

---

## ⏰ 48-HOUR TIMELINE AT A GLANCE

| Hours | Phase | Focus | Output |
|-------|-------|-------|--------|
| 0-2 | Setup | Local dev environment | Working Docker setup |
| 2-6 | Foundation | Resume parsing, basic UI | Swagger docs, components |
| 6-18 | Core | Parsing pipeline | End-to-end parsing works |
| 18-30 | Search | Embeddings + semantic search | `/search` endpoint working |
| 30-36 | Integration | Gmail OAuth | Email resumes auto-imported |
| 36-42 | Tier 2 | Pick 1 feature | Dedup OR comparison |
| 42-46 | Polish | Bug fixes + demo prep | Bug-free MVP |
| 46-48 | Deploy | Production deploy | Live demo + presentation |

---

## 🎯 CRITICAL DEPENDENCIES & CHECKPOINTS

### Hour 6 Sync (End of Foundation)
- [ ] PostgreSQL running locally
- [ ] FastAPI app serves `/docs` (Swagger UI)
- [ ] React app builds and serves
- [ ] All 4 engineers can commit without conflicts

### Hour 12 Sync (Resume Parser Working)
- [ ] Upload resume → Parse → Store → Retrieve ✓
- [ ] Parsing accuracy 85%+
- [ ] 10+ test resumes processed successfully
- [ ] No blocking bugs

### Hour 24 Sync (Search Working)
- [ ] Type NL query → Get ranked results ✓
- [ ] Search latency < 2 seconds
- [ ] Results are semantically relevant (manual check)
- [ ] No database errors

### Hour 32 Sync (Gmail Working)
- [ ] Connect Gmail → Auto-import resumes ✓
- [ ] 20+ emails with attachments processed
- [ ] Candidates in database match Gmail count
- [ ] Ready for live demo

### Hour 36 Sync (Decide Tier 2)
- [ ] Vote on which Tier 2 feature to build
- [ ] Estimate remaining hours (should be 6h)
- [ ] Assign owner(s) for feature
- [ ] Continue if doable, skip if not

### Hour 40 Sync (Polish Phase)
- [ ] Run full demo flow without bugs
- [ ] All 4 engineers practice their parts
- [ ] Architecture diagram printed
- [ ] Demo script finalized

### Hour 45 Sync (Pre-Deployment)
- [ ] All tests passing
- [ ] Frontend passes ESLint
- [ ] Backend passes pylint
- [ ] Performance benchmarks met

---

## 🔑 KEY DECISIONS ALREADY MADE

To avoid 4+ hours of debate, these are **finalized:**

### Frontend Stack
```
React 18 + TypeScript + Vite + Tailwind + shadcn/ui
(NOT: Vue, Svelte, Angular, etc.)
```

### Backend Stack
```
FastAPI + Python 3.11 + PostgreSQL + SQLAlchemy
(NOT: Django, Flask, Node.js, Go, etc.)
```

### AI Stack
```
OpenAI embeddings + spaCy + HuggingFace transformers
(NOT: local embeddings, Hugging Face embeddings API, etc.)
```

### Vector DB
```
Pinecone (Starter tier, free)
(NOT: Weaviate, Milvus, Qdrant, FAISS, etc.)
```

### Resume Parser
```
pypdf + python-docx + spaCy NER
(NOT: pdfplumber, PDFMiner, unstructured.io, etc.)
```

### Task Queue
```
Celery + Redis (local Docker for dev)
(NOT: RQ, APScheduler, etc.)
```

### Auth
```
JWT + OAuth2 (with Gmail OAuth)
(NOT: session-based, API keys, etc.)
```

### Deployment
```
Backend: Railway or Render
Frontend: Vercel
CI/CD: GitHub Actions
(NOT: Heroku, AWS, DigitalOcean, etc.)
```

**If you disagree with any decision, document why and get team approval before proceeding.** Otherwise, stick to the plan.

---

## 🚨 BLOCKERS TO WATCH

| Blocker | Likelihood | Mitigation |
|---------|-----------|-----------|
| Gmail OAuth fails | Medium | Use mock OAuth response for demo |
| Resume parser accuracy < 80% | Medium | Reduce to keyword matching only |
| Pinecone API key issues | Low | Use local FAISS backup |
| PostgreSQL migration fails | Low | Seed data manually via SQL |
| Search latency > 5 seconds | Low | Cache results, reduce query scope |
| Frontend build fails | Low | Revert last commit, check TypeScript |
| Deployment fails | Medium | Keep local instance as backup demo |
| Team member gets sick | High | Cross-train on critical features |

---

## 📊 FEATURE STATUS TEMPLATE

Print this and update hourly:

```
Hour 6  [████░░░░░░] Resume Parser
Hour 12 [██████░░░░] Resume + DB
Hour 18 [████████░░] Search Ready
Hour 24 [█████████░] Demo Works
Hour 30 [█████████░] Polish
Hour 36 [██████████] SHIPPED

Hour 24 Check:
- [ ] All Tier 1 features working
- [ ] No breaking TypeScript errors
- [ ] No breaking Python errors
- [ ] Demo runs without manual intervention
- [ ] All API endpoints documented
```

---

## 🎤 ELEVATOR PITCH (30 seconds)

Practice saying this:

> "TalentUnify is an AI-powered recruitment platform that aggregates candidates from email, uploads, and HRMS systems. Using semantic AI search, recruiters can find candidates in seconds instead of hours. We built it in 48 hours and it's already handling thousands of candidates with 94% parsing accuracy."

---

## ✅ FINAL CHECKLIST (Hour 47)

Before presenting to judges:

### Code Quality
- [ ] No TypeScript errors
- [ ] No Python linting errors
- [ ] All 4 repos pushed to GitHub
- [ ] Commit messages are clear
- [ ] `.env.example` has all variables

### Features (Tier 1)
- [ ] Resume upload works
- [ ] Parsing extracts all fields
- [ ] Candidates in database
- [ ] Natural language search works
- [ ] Gmail integration works

### UI/UX
- [ ] Dashboard loads without errors
- [ ] Search page responsive
- [ ] Candidate profile complete
- [ ] No console errors
- [ ] Loading spinners visible

### Performance
- [ ] Search returns in < 2 seconds
- [ ] Pages load in < 3 seconds
- [ ] API responses in < 500ms
- [ ] No memory leaks
- [ ] Lighthouse score > 80

### Demo
- [ ] 5-minute script rehearsed
- [ ] All team members know their part
- [ ] Backup demo (local machine)
- [ ] Backup video (recorded flow)
- [ ] Screenshots of key pages

### Deployment
- [ ] Backend deployed + running
- [ ] Frontend deployed + running
- [ ] Production `.env` set
- [ ] Database accessible
- [ ] Health check passes

### Documentation
- [ ] README.md complete
- [ ] ARCHITECTURE.md detailed
- [ ] API.md documented
- [ ] DEMO_SCRIPT.md ready
- [ ] GitHub link shared with judges

---

## 🔗 INTER-ENGINEER DEPENDENCIES

**Must Coordinate:**

| From | To | What | Sync Hour |
|------|----|----|-----------|
| E2 (Backend) | E1 (Frontend) | API schema | Hour 6 |
| E3 (AI) | E2 (Backend) | Parser output format | Hour 6 |
| E4 (DevOps) | All | Docker setup | Hour 2 |
| E1 (Frontend) | E2 (Backend) | Auth token handling | Hour 8 |
| E3 (AI) | E2 (Backend) | Embedding dimension (1536) | Hour 18 |
| E4 (DevOps) | All | CI/CD passing status | Every hour |

**Critical Handoffs:**

1. **Hour 6:** Backend delivers Swagger docs → Frontend builds against it
2. **Hour 12:** Parser service running → Backend integrates it
3. **Hour 18:** Embeddings service ready → Search endpoint uses it
4. **Hour 24:** Gmail OAuth logic → Frontend connects it
5. **Hour 36:** All Tier 1 done → Tier 2 work distributed

---

## 📱 QUICK SLACK CHECKLIST

Post these in Slack every 6 hours:

```
🚀 HOUR 6 CHECKPOINT
[ ] Database running
[ ] API running
[ ] Frontend running
[ ] Tests passing
[ ] No blockers
```

```
🚀 HOUR 12 CHECKPOINT
[ ] Resume parsing works end-to-end
[ ] 10 test resumes processed
[ ] Accuracy 85%+
[ ] Database models correct
[ ] No blockers
```

```
🚀 HOUR 24 CHECKPOINT
[ ] Semantic search working
[ ] <2s latency achieved
[ ] Gmail auth tested
[ ] All Tier 1 features demo-ready
[ ] Ready for judges
```

---

## 🏆 SUCCESS METRICS FOR JUDGES

What judges will evaluate:

| Metric | Target | How |
|--------|--------|-----|
| **Innovation** | 5/5 | Semantic search (not keyword) + auto-dedup |
| **Execution** | 5/5 | Feature-complete Tier 1 + working Tier 2 |
| **Polish** | 5/5 | No UI bugs, smooth animations, clear copy |
| **Architecture** | 5/5 | Scalable design (PostgreSQL + Pinecone) |
| **Demo** | 5/5 | 5-minute clear story, no failures |
| **Team** | 5/5 | All 4 members engaged, clear role division |

---

## FINAL NOTES

### If You're Behind (Hour 30)
1. Cut Tier 2 features immediately
2. Focus on polishing Tier 1
3. Test demo flow obsessively
4. Ensure all endpoints return valid JSON
5. Have backup demo (hardcoded results)

### If You're Ahead (Hour 30)
1. Start Tier 2 feature (dedup is easiest)
2. Add analytics dashboard
3. Improve UI polish
4. Add more seed data for demo
5. Write better documentation

### If Something Breaks (Hour 40)
1. Don't panic (5 minutes to fix = 45 min of panic)
2. Isolate the issue (backend? frontend? integration?)
3. Revert last commit
4. Use hardcoded fallback for demo
5. Move on

### If You Run Out of Time (Hour 45)
- **DO:** Deploy working Tier 1 features
- **DO:** Practice 5-minute demo
- **DO:** Have backup (local instance)
- **DON'T:** Try to ship untested Tier 2 feature
- **DON'T:** Refactor code last-minute
- **DON'T:** Change tech stack

---

## 📞 SUPPORT RESOURCES

If you need help:

1. **General questions:** Reread the relevant SECTION in REFINED_CTO_BLUEPRINT_PROMPT.md
2. **API design:** See Section 9 (API Design)
3. **Folder structure:** See Section 7 (Project Folder Structure)
4. **Timeline confusion:** See Section 10 (Development Plan)
5. **Tech stack options:** See ERROR_ANALYSIS.md → Why each was chosen
6. **Demo prep:** See Section 12 (Judge-Winning Demo Flow)
7. **Errors/bugs:** See ERROR_ANALYSIS_AND_CORRECTIONS.md → Known issues

---

## 🎯 ONE-PAGE SUMMARY

**Project:** TalentUnify (AI Recruitment Platform)  
**Duration:** 48 hours  
**Team:** 4 engineers  
**Goal:** MVP with Tier 1 + optional Tier 2  

**Tech Stack:**
- Frontend: React 18 + TypeScript + Vite
- Backend: FastAPI + PostgreSQL
- AI: OpenAI embeddings + spaCy
- Vector DB: Pinecone
- Deployment: Railway + Vercel

**Tier 1 Features (Must Ship):**
1. Resume upload & parsing
2. Candidate database
3. Semantic search
4. Recruiter dashboard
5. Gmail OAuth integration

**Tier 2 Features (If Time):**
1. Candidate deduplication
2. Candidate comparison
3. Job fit ranking

**Key Timeline:**
- Hour 0-6: Setup + foundation
- Hour 6-18: Resume parsing
- Hour 18-30: Search engine
- Hour 30-36: Gmail integration
- Hour 36-42: Polish + Tier 2
- Hour 42-48: Demo + deploy

**Success Criteria:**
- Demo works flawlessly
- All Tier 1 features shipped
- < 2s search latency
- Clean code + documentation
- Judges impressed by innovation

---

**This index should be your daily reference.** Print it, post it, check it every 6 hours.

Good luck! 🚀

