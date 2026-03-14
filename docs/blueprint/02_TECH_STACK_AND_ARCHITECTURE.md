# 02 — TECHNOLOGY STACK & SYSTEM ARCHITECTURE
## Finalized Decisions & Architecture Diagram

---

> [!IMPORTANT]
> These technology choices are **finalized**. Do not debate alternatives — they were selected based on hackathon constraints (48h, 4 people, free tiers, demo-ability). See the Error Analysis source doc for reasoning behind each rejection of alternatives.

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     RECRUITER DASHBOARD                      │
│                    (React + TypeScript)                      │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTPS
                ┌────────▼──────────┐
                │  API GATEWAY       │
                │  (FastAPI)         │
                │  /auth /candidate  │
                │  /resume /search   │
                └────────┬──────────┘
                         │
          ┌──────────────┼──────────────┐
          │              │              │
    ┌─────▼─────┐ ┌─────▼─────┐ ┌─────▼─────┐
    │ Candidate │ │  Resume   │ │  Search   │
    │ Service   │ │  Parser   │ │  Service  │
    └─────┬─────┘ └─────┬─────┘ └─────┬─────┘
          │              │              │
    ┌─────▼──────────────▼──────────────▼─────┐
    │            DATA LAYER                    │
    │  ┌────────────┐    ┌───────────────┐    │
    │  │ PostgreSQL │    │   Pinecone    │    │
    │  │ (Relational)│   │  (Vector DB)  │    │
    │  └────────────┘    └───────────────┘    │
    └─────────────────────────────────────────┘

    ┌─────────────────────────────────────────┐
    │         AI / NLP SERVICES               │
    │  ┌──────────┐  ┌──────────────────┐    │
    │  │ OpenAI   │  │ spaCy + HF       │    │
    │  │ Embed API│  │ Transformers     │    │
    │  └──────────┘  └──────────────────┘    │
    └─────────────────────────────────────────┘

    ┌─────────────────────────────────────────┐
    │         INTEGRATIONS                     │
    │  ┌──────┐  ┌──────┐  ┌────────────┐    │
    │  │Gmail │  │ HRMS │  │ LinkedIn   │    │
    │  │OAuth │  │ Mock │  │ Simulator  │    │
    │  └──────┘  └──────┘  └────────────┘    │
    └─────────────────────────────────────────┘
```

---

## 📋 Complete Technology Stack

### Frontend

| Component | Technology | Why This Choice |
|-----------|-----------|----------------|
| Framework | **React 18 + TypeScript** | Type safety, massive ecosystem, fast iteration |
| Build Tool | **Vite** | 10x faster HMR than Webpack, perfect for hackathons |
| Styling | **Tailwind CSS** | Utility-first, rapid UI prototyping |
| Component Library | **shadcn/ui** | Pre-built, accessible, customizable React components |
| State Management | **TanStack Query + Zustand** | Lightweight, covers server + client state |
| Search UX | **React Aria** | Accessible autocomplete/combobox patterns |
| Charts | **Recharts** | Simple charting for analytics (Tier 2) |

### Backend

| Component | Technology | Why This Choice |
|-----------|-----------|----------------|
| Framework | **FastAPI (Python 3.11)** | Fastest Python async framework, auto OpenAPI/Swagger docs |
| ORM | **SQLAlchemy** | Type hints, migrations (Alembic), relationship management |
| Auth | **JWT + OAuth2** | Built-in FastAPI support, stateless, scalable |
| Task Queue | **Celery + Redis** | Async resume parsing, email ingestion |
| Validation | **Pydantic** | Data validation, serialization, schema enforcement |
| API Docs | **Swagger UI** | Auto-generated from FastAPI, zero config |

### AI / NLP

| Component | Technology | Why This Choice |
|-----------|-----------|----------------|
| Resume Parsing | **pypdf + python-docx** | PDF/DOCX text extraction |
| NER | **spaCy (en_core_web_sm)** | Entity recognition: name, org, location (40MB, 94% acc) |
| Skill Extraction | **HuggingFace Transformers** | Zero-shot classification (`facebook/bart-large-mnli`) |
| Embeddings | **OpenAI API (text-embedding-3-small)** | 1536 dims, $0.02/1M tokens, no local GPU |
| Semantic Search | **Pinecone** | Managed vector DB, serverless, free starter tier |
| Deduplication | **Cosine similarity** | Deterministic, interpretable, fast |

### Data Layer

| Component | Technology | Why This Choice |
|-----------|-----------|----------------|
| Relational DB | **PostgreSQL** | ACID compliance, complex joins, free tier on Render |
| Vector DB | **Pinecone (Starter Tier)** | Free 1M vectors, serverless, managed, cosine similarity |
| Cache | **Redis** | Session cache, Celery broker, search result caching |

### DevOps & Deployment

| Component | Technology | Why This Choice |
|-----------|-----------|----------------|
| Containers | **Docker** | Local dev parity, reproducible builds |
| Frontend Hosting | **Vercel** | 1-click deploy, free tier, fast CDN |
| Backend Hosting | **Railway / Render** | Simple deploy, GitHub integration, free credits |
| CI/CD | **GitHub Actions** | Free, integrated with GitHub, no external config |
| Secrets | **GitHub Secrets** | Simple for hackathons, secure |

---

## ❌ Explicitly Rejected Alternatives

| Rejected | Reason |
|----------|--------|
| Vue / Svelte / Angular | React has larger ecosystem and team familiarity |
| Django / Flask | FastAPI is async-first with built-in OpenAPI docs |
| Node.js / Express | Python needed for AI/NLP libraries (spaCy, transformers) |
| MongoDB | PostgreSQL better for complex joins + team already knows SQL |
| Weaviate / Milvus / FAISS | Pinecone is serverless (no DevOps), free tier |
| pdfplumber / PDFMiner | pypdf is simpler and sufficient for hackathon |
| Heroku | Railway has better free tier and GitHub integration |
| AWS / DigitalOcean | Too complex for 48h; Railway/Vercel are simpler |

---

## 🔧 Environment Variables Required

```bash
# PostgreSQL
DATABASE_URL=postgresql://user:password@localhost:5432/talent_unify

# Redis
REDIS_URL=redis://localhost:6379

# OpenAI
OPENAI_API_KEY=sk-...

# Pinecone
PINECONE_API_KEY=...
PINECONE_ENVIRONMENT=gcp-starter

# Gmail OAuth
GOOGLE_CLIENT_ID=...
GOOGLE_CLIENT_SECRET=...

# App
SECRET_KEY=your-secret-key-here
ENVIRONMENT=development
```

---

## 🔗 Cross-References
- **AI pipeline details:** → [04_AI_AND_NLP_PIPELINE.md](./04_AI_AND_NLP_PIPELINE.md)
- **Database schema:** → [05_DATABASE_AND_API.md](./05_DATABASE_AND_API.md)
- **Frontend design:** → [06_FRONTEND_AND_UX.md](./06_FRONTEND_AND_UX.md)
- **Deployment config:** → [09_DEVOPS_AND_DEPLOYMENT.md](./09_DEVOPS_AND_DEPLOYMENT.md)

---

*Source: REFINED_CTO_BLUEPRINT_PROMPT.md (Sections 3-4), ERROR_ANALYSIS_AND_CORRECTIONS.md (Errors #3, #5, #6)*
