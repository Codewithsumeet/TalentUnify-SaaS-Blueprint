# 07 — PROJECT STRUCTURE & TEAM OWNERSHIP
## Folder Hierarchy, File Ownership Matrix & Dependency Map

---

## 📂 Complete Project Directory

```
talent-unify/
│
├── 📋 ROOT FILES
│   ├── .env.example                     # Template for env vars
│   ├── .gitignore                       # Ignore patterns
│   ├── docker-compose.yml               # Local dev orchestration
│   ├── README.md                        # Project overview
│   ├── ARCHITECTURE.md                  # System design doc
│   ├── LICENSE                          # MIT license
│   └── .pre-commit-config.yaml          # Auto-format on commit
│
├── 🎨 frontend/                          [ENGINEER 1 OWNS]
│   ├── public/
│   │   ├── favicon.ico
│   │   └── logo.svg
│   ├── src/
│   │   ├── main.tsx                     # Entry point
│   │   ├── App.tsx                      # Root component + router
│   │   ├── auth/
│   │   │   ├── AuthContext.tsx          # Auth state provider
│   │   │   ├── useAuth.ts              # Auth hook
│   │   │   └── LoginPage.tsx
│   │   ├── pages/
│   │   │   ├── DashboardPage.tsx
│   │   │   ├── CandidateSearchPage.tsx
│   │   │   ├── CandidateProfilePage.tsx
│   │   │   ├── ComparisonPage.tsx       # Tier 2
│   │   │   ├── IntegrationsPage.tsx
│   │   │   └── NotFoundPage.tsx
│   │   ├── components/
│   │   │   ├── Navigation/              # Navbar, Sidebar
│   │   │   ├── Candidate/              # CandidateCard, List, SkillBadge
│   │   │   ├── Search/                 # SearchBar, Results, Filters
│   │   │   ├── Resume/                 # UploadZone, ParseProgress
│   │   │   ├── Integration/            # GmailConnectButton, Status
│   │   │   └── UI/                     # shadcn/ui components
│   │   ├── services/
│   │   │   ├── api.ts                  # Axios instance
│   │   │   ├── candidateService.ts
│   │   │   ├── searchService.ts
│   │   │   └── authService.ts
│   │   ├── hooks/
│   │   │   ├── useAuth.ts
│   │   │   ├── useCandidates.ts
│   │   │   └── useDebounce.ts
│   │   ├── types/
│   │   │   ├── candidate.ts
│   │   │   ├── search.ts
│   │   │   └── api.ts
│   │   └── styles/
│   │       ├── globals.css
│   │       └── variables.css
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   └── tailwind.config.js
│
├── ⚙️ backend/                           [ENGINEER 2 OWNS]
│   ├── main.py                          # FastAPI entry point
│   ├── requirements.txt
│   ├── requirements-dev.txt
│   ├── app/
│   │   ├── __init__.py
│   │   ├── config.py                    # Environment config
│   │   ├── exceptions.py
│   │   ├── dependencies.py              # DB, auth dependencies
│   │   └── logger.py
│   ├── auth/
│   │   ├── jwt_handler.py               # JWT create/validate
│   │   ├── oauth.py                     # Gmail OAuth2 flow
│   │   ├── models.py                    # User/Token schemas
│   │   ├── routes.py                    # /auth endpoints
│   │   └── dependencies.py              # get_current_user()
│   ├── db/
│   │   ├── database.py                  # SQLAlchemy connection
│   │   ├── models.py                    # ORM models
│   │   ├── schemas.py                   # Pydantic schemas
│   │   └── migrations/                  # Alembic
│   │       └── versions/
│   ├── resume/
│   │   ├── parser.py                    # Resume parsing logic
│   │   ├── extractor.py                 # Skill/experience extraction
│   │   ├── models.py
│   │   ├── routes.py                    # /resume endpoints
│   │   └── validators.py
│   ├── candidate/
│   │   ├── service.py                   # Business logic
│   │   ├── models.py
│   │   ├── routes.py                    # /candidate endpoints
│   │   ├── deduplicator.py              # Duplicate detection
│   │   └── matcher.py                   # Job fit (Tier 2)
│   ├── search/
│   │   ├── semantic_search.py           # Pinecone search
│   │   ├── query_parser.py              # NL → structured
│   │   ├── models.py
│   │   ├── routes.py                    # /search endpoints
│   │   └── ranker.py
│   ├── integrations/
│   │   ├── gmail/
│   │   │   ├── client.py
│   │   │   ├── service.py
│   │   │   └── routes.py
│   │   ├── hrms/simulator.py
│   │   └── linkedin/simulator.py
│   ├── ai/
│   │   ├── embeddings/
│   │   │   ├── client.py                # OpenAI embeddings
│   │   │   └── service.py
│   │   ├── nlp/
│   │   │   ├── spacy_nlp.py             # spaCy NER
│   │   │   ├── skill_extractor.py       # Zero-shot extraction
│   │   │   └── text_processor.py
│   │   └── ranking/scorer.py
│   ├── tasks/
│   │   ├── celery_app.py                # Celery config
│   │   ├── resume_parsing_task.py
│   │   └── email_ingestion_task.py
│   ├── middleware/
│   │   ├── error_handler.py
│   │   ├── cors.py
│   │   └── rate_limiter.py
│   └── tests/
│       ├── conftest.py
│       ├── test_auth.py
│       ├── test_candidate.py
│       ├── test_resume.py
│       └── test_search.py
│
├── 🗄️ data/
│   ├── skills_taxonomy.json             # 500+ skill definitions
│   ├── seed_data.sql                    # Demo data
│   └── sample_resumes/                  # 10+ test resumes
│
├── 📜 scripts/
│   ├── setup.sh                         # One-command local setup
│   ├── seed_db.py                       # Populate demo data
│   ├── generate_embeddings.py           # Batch embedding generation
│   └── deploy.sh                        # Deploy to production
│
├── 🐳 docker/
│   ├── Dockerfile.backend
│   ├── Dockerfile.frontend
│   └── docker-compose.yml
│
├── 📚 docs/
│   ├── ARCHITECTURE.md
│   ├── API.md
│   ├── DEMO_SCRIPT.md
│   └── DEPLOYMENT.md
│
└── .github/workflows/                    [ENGINEER 4 OWNS]
    ├── ci-backend.yml
    ├── ci-frontend.yml
    └── deploy.yml
```

---

## 👷 Ownership Matrix

| Engineer | Owns | Files | Depends On |
|----------|------|-------|-----------|
| **E1: Frontend Lead** | All React UI | `frontend/src/**` | Backend API (E2) |
| **E2: Backend Lead** | FastAPI + DB | `backend/**` (except `ai/`) | PostgreSQL, Redis |
| **E3: AI/ML Engineer** | NLP pipelines | `backend/ai/**`, `data/skills_taxonomy.json` | OpenAI API, Pinecone, spaCy |
| **E4: DevOps Lead** | Infra + Integrations | `.github/`, `docker/`, `scripts/`, `backend/integrations/` | All services |

### Conflict-Free Zones
Each engineer owns separate directories to **prevent merge conflicts**:

```
E1 touches: frontend/src/
E2 touches: backend/app/, backend/auth/, backend/db/, backend/resume/, backend/candidate/, backend/search/
E3 touches: backend/ai/, data/
E4 touches: .github/, docker/, scripts/, backend/integrations/, backend/tasks/
```

---

## 🔄 Inter-Engineer Dependencies

| From | To | What | When |
|------|----|------|------|
| E2 (Backend) | E1 (Frontend) | API schema/Swagger docs | Hour 6 |
| E3 (AI) | E2 (Backend) | Parser output format (Pydantic schema) | Hour 6 |
| E4 (DevOps) | All | Docker setup working | Hour 2 |
| E1 (Frontend) | E2 (Backend) | Auth token handling format | Hour 8 |
| E3 (AI) | E2 (Backend) | Embedding dimension (1536) | Hour 18 |
| E4 (DevOps) | All | CI/CD passing status | Every commit |

### Critical Handoffs
1. **Hour 6:** E2 delivers Swagger docs → E1 builds frontend against them
2. **Hour 12:** E3's parser service running → E2 integrates it
3. **Hour 18:** E3's embeddings ready → E2's search endpoint uses them
4. **Hour 24:** E4's Gmail OAuth → E1 connects the button
5. **Hour 36:** All Tier 1 done → Tier 2 work distributed

---

## 📝 Naming Conventions

| Type | Convention | Example |
|------|-----------|---------|
| Python files | snake_case | `resume_parser.py` |
| TypeScript files | PascalCase (components), camelCase (utils) | `SearchBar.tsx`, `candidateService.ts` |
| API endpoints | kebab-case | `/candidate/deduplicate` |
| DB tables | snake_case plural | `candidate_skills` |
| Environment vars | SCREAMING_SNAKE_CASE | `OPENAI_API_KEY` |
| Git branches | feature/kebab-case | `feature/dashboard` |

---

## 🔗 Cross-References
- **What each file implements:** → [04_AI_AND_NLP_PIPELINE.md](./04_AI_AND_NLP_PIPELINE.md) (AI), [05_DATABASE_AND_API.md](./05_DATABASE_AND_API.md) (Backend/DB), [06_FRONTEND_AND_UX.md](./06_FRONTEND_AND_UX.md) (Frontend)
- **When to build which file:** → [08_DEVELOPMENT_TIMELINE.md](./08_DEVELOPMENT_TIMELINE.md)
- **CI/CD for these files:** → [09_DEVOPS_AND_DEPLOYMENT.md](./09_DEVOPS_AND_DEPLOYMENT.md)

---

*Source: REFINED_CTO_BLUEPRINT_PROMPT.md (Section 7), ERROR_ANALYSIS (Error #9), QUICK_REFERENCE_INDEX.md*
