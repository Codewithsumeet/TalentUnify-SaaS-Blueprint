# REFINED CTO BLUEPRINT PROMPT
## AI-Powered Recruitment Platform - 24/48-Hour Hackathon MVP

---

## EXECUTIVE SUMMARY

This prompt guides a 4-person engineering team to build a **production-grade SaaS MVP** for unified AI-powered recruitment. The refined version addresses:

✅ **Error Corrections** from original prompt  
✅ **Organized Directory Indexing** with clear hierarchies  
✅ **Structured File Organization** with ownership & dependencies  
✅ **Timeline Alignment** with realistic 48-hour execution  
✅ **Deliverable Clarity** with specific output formats  

---

# SECTION 1: ERRORS IN ORIGINAL PROMPT

## Critical Errors Identified

| Error | Location | Impact | Fix |
|-------|----------|--------|-----|
| **"Antigravity framework"** - undefined, unknown framework | Section 7 | Vague tech stack choice | Replace with clear tech stack: FastAPI + React + Pinecone/Weaviate |
| **Markdown spec auto-generation unclear** | Section 7 | How does .md generate project? | Clarify: Markdown is documentation blueprint; use CLI tools (cookiecutter/scaffolder) |
| **4-person team scope vs 48 hours unrealistic** | Section 10 | Too many features for timeline | Prioritize: Focus Tier 1 + 1 Tier 2 feature max |
| **"Vector database OR semantic search"** - vague | Section 4 | Unclear implementation path | Specify: Use Pinecone (vector DB) + OpenAI embeddings |
| **No clear API authentication model** | Section 9 | Security gap | Add: JWT + OAuth2 for email integrations |
| **Resume parsing "library" unspecified** | Section 4 | Unknown dependencies | Specify: `pydantic`, `spacy`, `transformers` for NLP |
| **"Simulated LinkedIn"** - unclear scope | Hackathon problem | Unclear deliverable | Clarify: Mock API, not actual LinkedIn integration |
| **Folder structure lacks file-level organization** | Section 6 | Unclear file ownership | Add: File-level indexing with ownership matrix |
| **No database choice specified (SQL/NoSQL/Vector)** | Section 5 | Architecture ambiguity | Specify: PostgreSQL + Pinecone (hybrid approach) |
| **CI/CD platform unspecified** | Section 13 | Unclear deployment path | Specify: GitHub Actions + Docker + Vercel/Railway |

---

# SECTION 2: REFINED SYSTEM OVERVIEW

## Product Vision

**TalentUnify**: A unified AI-powered recruitment platform that aggregates candidate data from disparate sources (email, HRMS, resume uploads, LinkedIn simulation) and enables recruiters to discover, compare, and manage candidates using natural language search powered by semantic AI.

## Target Users

- **Primary**: Mid-market recruitment teams (2-50 recruiters)
- **Secondary**: HR managers at SMBs
- **Use Case**: Volume hiring, diverse candidate sourcing, skills-based matching

## Key Differentiating Innovation

1. **Semantic candidate search** (not keyword-based)
2. **Automatic resume parsing + skill extraction** with ML
3. **Intelligent candidate deduplication** using embeddings
4. **Multi-source data aggregation** (email, HRMS, uploads)
5. **Real-time candidate insights** via AI-powered dashboard

## Why This Wins Hackathons

✨ **Technical Depth**: NLP pipelines, vector databases, ML embeddings  
✨ **User Experience**: Polished dashboard with live search  
✨ **Integration**: Real APIs (Gmail), realistic data ingestion  
✨ **Innovation**: AI-powered features judges rarely see in hackathons  
✨ **Scalability Story**: Architecture ready for growth  

---

# SECTION 3: REFINED MVP FEATURE PRIORITIZATION

## Tier 1 — Demo Critical (MUST HAVE by Hour 36)

**These 5 features define the demo. No compromises.**

1. **Resume Upload & Parsing**
   - Upload .pdf/.docx resumés
   - AI extracts: name, email, phone, skills, experience
   - Store parsed data in database

2. **Candidate Database**
   - Store candidates with parsed resume data
   - Search candidates by name/skills

3. **Natural Language Candidate Search**
   - Query: "Find Python developers with 5+ years experience"
   - AI converts to semantic search via embeddings
   - Returns ranked candidates

4. **Recruiter Dashboard**
   - Simple HTML/React UI
   - View uploaded candidates
   - Live search bar
   - Candidate list with basic info

5. **Integration: Email Resume Ingestion**
   - Connect Gmail (OAuth)
   - Parse resumes from email attachments
   - Auto-import into candidate DB

---

## Tier 2 — Judge-Wow Features (IF TIME PERMITS by Hour 42)

**Pick 1-2 maximum in 48 hours.**

1. **Candidate Comparison View**
   - Side-by-side skill comparison
   - Experience timeline
   - Salary expectations

2. **Automatic Deduplication**
   - Identify duplicate candidates
   - Merge profiles
   - Flag potential matches

3. **Candidate Ranking & Scoring**
   - AI ranks candidates by job fit
   - Explainable scoring
   - Custom weightings

4. **Pipeline Management**
   - Status tracking (Applied → Interview → Offer)
   - Drag-and-drop kanban board
   - Activity timeline

5. **Analytics Dashboard**
   - Hiring metrics (time-to-hire, conversion rates)
   - Candidate source attribution
   - Skill heatmaps

---

## Tier 3 — Post-Hackathon Expansion

**These are roadmap items—do NOT build during hackathon.**

- [ ] HRMS API integration (ADP, BambooHR)
- [ ] LinkedIn profile simulation with real API
- [ ] Advanced ML ranking models
- [ ] Bulk candidate import (CSV)
- [ ] Interview scheduling
- [ ] Offer generation templates
- [ ] Team collaboration features
- [ ] Advanced analytics & reporting
- [ ] Mobile app
- [ ] Candidate communication portal

---

# SECTION 4: COMPLETE SAAS ARCHITECTURE

## 4.1 Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     RECRUITER DASHBOARD                      │
│                    (React + TypeScript)                      │
└────────────────┬────────────────────────────────────────────┘
                 │
         ┌───────┴──────────┐
         │                  │
    ┌────▼─────┐      ┌─────▼────┐
    │  Next.js  │      │  WebSocket│
    │  Frontend │      │   Events  │
    └────┬─────┘      └─────┬────┘
         │                  │
    ┌────▼──────────────────▼────┐
    │   API GATEWAY (FastAPI)    │
    │  /candidate /resume /search │
    └────┬──────────────────┬────┘
         │                  │
    ┌────▼─────────────────▼─────┐
    │    BACKEND SERVICES         │
    │ ┌─────────┐  ┌──────────┐  │
    │ │Candidate│  │Resume    │  │
    │ │Service  │  │Parser    │  │
    │ │         │  │Service   │  │
    │ └─────────┘  └──────────┘  │
    │ ┌─────────┐  ┌──────────┐  │
    │ │Search   │  │Dedup     │  │
    │ │Service  │  │Service   │  │
    │ └─────────┘  └──────────┘  │
    └────┬──────────────────┬────┘
         │                  │
    ┌────▼──────────────────▼────┐
    │   DATA LAYER               │
    │ ┌────────┐  ┌────────────┐ │
    │ │PostgreSQL│ │Pinecone    │ │
    │ │(Relational)│ (Vector DB)│ │
    │ └────────┘  └────────────┘ │
    └────┬──────────────────┬────┘
         │                  │
    ┌────▼──────────────────▼────┐
    │   INTEGRATIONS              │
    │ ┌──────┐ ┌───────┐ ┌──────┐│
    │ │Gmail │ │HRMS   │ │Resume││
    │ │OAuth │ │Sim    │ │Parser││
    │ └──────┘ └───────┘ └──────┘│
    └────────────────────────────┘

    ┌────────────────────────────┐
    │   AI/NLP SERVICES          │
    │ ┌──────┐  ┌────────────┐   │
    │ │OpenAI│  │SpaCy/HF    │   │
    │ │ API  │  │Transformers│   │
    │ └──────┘  └────────────┘   │
    └────────────────────────────┘
```

## 4.2 Technology Stack Decisions

### Frontend Layer
| Component | Technology | Reasoning |
|-----------|-----------|-----------|
| **Framework** | React 18 + TypeScript | Type safety, component reusability, fast iteration |
| **Build Tool** | Vite | 10x faster than Webpack for hackathons |
| **Styling** | Tailwind CSS | Rapid UI prototyping, production-grade components |
| **Components** | shadcn/ui | Pre-built, accessible React components |
| **State Mgmt** | TanStack Query + Zustand | Simple, lightweight, perfect for 48h |
| **Search UX** | React Aria | Accessible autocomplete search |

### Backend Layer
| Component | Technology | Reasoning |
|-----------|-----------|-----------|
| **Framework** | FastAPI | Fastest Python async framework, auto OpenAPI docs |
| **Auth** | JWT + OAuth2 | Built-in FastAPI support, stateless, scalable |
| **Task Queue** | Celery + Redis | Async resume parsing, email ingestion |
| **API Docs** | Swagger UI | Auto-generated, zero config with FastAPI |

### AI/NLP Layer
| Component | Technology | Reasoning |
|-----------|-----------|-----------|
| **Resume Parsing** | Pydantic + spaCy | Structured extraction, NLP entity recognition |
| **Embeddings** | OpenAI API (text-embedding-3-small) | Fast, accurate, no local GPU needed |
| **Skill Extraction** | HuggingFace Transformers | Zero-shot classification for job skills |
| **Semantic Search** | Pinecone + OpenAI embeddings | Managed vector DB, no DevOps overhead |
| **Deduplication** | Cosine similarity on embeddings | Deterministic, interpretable |

### Data Layer
| Component | Technology | Reasoning |
|-----------|-----------|-----------|
| **Relational DB** | PostgreSQL | ACID compliance, complex queries, free tier available |
| **Vector DB** | Pinecone (Starter Tier) | Free for hackathons, serverless, managed service |
| **Caching** | Redis | Fast candidate lookups, session cache |
| **ORM** | SQLAlchemy | Type hints, migrations, relationship management |

### DevOps/Deployment
| Component | Technology | Reasoning |
|-----------|-----------|-----------|
| **Containerization** | Docker | Reproducible deployments, local dev parity |
| **Frontend Hosting** | Vercel | 1-click Next.js deployment, free tier, fast CDN |
| **Backend Hosting** | Railway / Render | Simple deployment, GitHub integration, free credits |
| **CI/CD** | GitHub Actions | Free, integrated with GitHub, no external config |
| **Secrets Mgmt** | GitHub Secrets | Simple for hackathons, secure |

---

# SECTION 5: AI PIPELINE DESIGN

## 5.1 Resume Parsing Pipeline

```
Resume (PDF/DOCX)
    ↓
[PDF/DOCX Extraction] (pypdf, python-docx)
    ↓
[Raw Text]
    ↓
[spaCy NER] → Extract: Name, Email, Phone, Location
    ↓
[Pydantic Validation] → Enforce schema
    ↓
[Structured Candidate Data]
{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+1234567890",
  "location": "San Francisco, CA",
  "skills": [...],
  "experience": [...]
}
```

### Implementation Details

**Resume Parser Service** (`services/resume_parser.py`)

```python
from pydantic import BaseModel
import spacy
from pypdf import PdfReader
import json

class ParsedResume(BaseModel):
    name: str
    email: str
    phone: str
    location: str
    skills: list[str]
    experience: list[dict]
    education: list[dict]
    summary: str

async def parse_resume(file_path: str) -> ParsedResume:
    # 1. Extract text from PDF/DOCX
    text = extract_text(file_path)
    
    # 2. Use spaCy for NER
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    
    # 3. Extract entities: PERSON, ORG, GPE, DATE
    entities = extract_entities(doc)
    
    # 4. Extract skills using keyword matching + ML
    skills = extract_skills(text)
    
    # 5. Parse experience section
    experience = parse_experience_section(text)
    
    # 6. Return structured data
    return ParsedResume(
        name=entities.get("name"),
        email=extract_email(text),
        phone=extract_phone(text),
        skills=skills,
        experience=experience
    )
```

## 5.2 Skill Extraction

**Methods (in priority order):**

1. **Keyword Matching** (fast, deterministic)
   - Maintain skill taxonomy file: `data/skills_taxonomy.json`
   - Match against 500+ tech skills
   - Examples: Python, AWS, React, SQL

2. **Zero-Shot Classification** (HuggingFace)
   - Model: `facebook/bart-large-mnli`
   - Question: "Does candidate have Python experience?"
   - Lower latency than fine-tuned models

3. **NER with Transformers** (if time permits)
   - Model: `dslim/distilbert-NER`
   - Extract skill entities directly

**Implementation:**

```python
from transformers import pipeline

def extract_skills(resume_text: str) -> list[str]:
    # Keyword matching (fast path)
    skills = match_skills_from_taxonomy(resume_text)
    
    # If < 5 skills found, use zero-shot classification
    if len(skills) < 5:
        classifier = pipeline("zero-shot-classification", 
                            model="facebook/bart-large-mnli")
        candidate_labels = TECH_SKILLS_LIST  # 500+ skills
        
        results = classifier(resume_text, candidate_labels, 
                           multi_class=True)
        skills.extend([r['labels'][0] for r in results if r['scores'][0] > 0.5])
    
    return list(set(skills))
```

## 5.3 Candidate Embeddings & Semantic Search

**Architecture:**

```
Candidate Profile
    ↓
[Text Aggregation]
"John Doe: Python, 5 years, AWS, React, ..."
    ↓
[OpenAI Embeddings API]
text-embedding-3-small (1536 dims, $0.02/1M tokens)
    ↓
[Vector Embedding]
[0.023, -0.145, 0.891, ..., 0.234]
    ↓
[Pinecone Vector DB]
Index: "candidates"
    ↓
[Semantic Search]
Query: "Find Python developers with AWS experience"
    ↓
[Cosine Similarity Ranking]
Results: [Candidate A, Candidate B, Candidate C]
```

**Implementation:**

```python
from openai import OpenAI
import pinecone

client = OpenAI()
pc = pinecone.Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index("candidates")

async def embed_candidate(candidate_id: str, profile_text: str):
    # 1. Create embedding via OpenAI
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=profile_text
    )
    embedding = response.data[0].embedding
    
    # 2. Store in Pinecone
    index.upsert(
        vectors=[
            (
                candidate_id,
                embedding,
                {
                    "candidate_id": candidate_id,
                    "profile_text": profile_text
                }
            )
        ]
    )

async def semantic_search(query: str, top_k: int = 10):
    # 1. Embed the query
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=query
    )
    query_embedding = response.data[0].embedding
    
    # 2. Search Pinecone
    results = index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True
    )
    
    return results
```

## 5.4 Automatic Deduplication

**Algorithm:**

```
New Candidate Upload
    ↓
[Extract Name + Email]
    ↓
[Search existing candidates]
Query: name + email
    ↓
[Exact Match Found?]
├─ YES → Flag as duplicate, suggest merge
├─ NO → Check embedding similarity
    ↓
[Cosine Similarity > 0.92?]
├─ YES → Likely duplicate (different name variant?)
├─ NO → New candidate
```

**Implementation:**

```python
async def find_duplicates(candidate_id: str) -> list[dict]:
    candidate = db.get_candidate(candidate_id)
    
    # 1. Exact match on name + email
    exact = db.query_candidates(
        name=candidate.name,
        email=candidate.email
    )
    if exact:
        return exact
    
    # 2. Fuzzy match on name
    fuzzy = db.fuzzy_search_name(candidate.name)
    
    # 3. Embedding similarity
    embedding = await get_candidate_embedding(candidate_id)
    similar = index.query(vector=embedding, top_k=5)
    
    # 4. Filter by similarity threshold
    duplicates = [
        s for s in similar 
        if s['score'] > 0.92 and s['id'] != candidate_id
    ]
    
    return duplicates

async def merge_candidates(primary_id: str, duplicate_ids: list[str]):
    primary = db.get_candidate(primary_id)
    
    for dup_id in duplicate_ids:
        duplicate = db.get_candidate(dup_id)
        
        # Merge skills, experience, education
        primary.skills = list(set(primary.skills + duplicate.skills))
        
        # Mark duplicate as merged
        db.update_candidate(dup_id, status="merged", merged_into=primary_id)
    
    db.save(primary)
```

## 5.5 Candidate Ranking for Job Fit

**Scoring Formula (Tier 2 feature):**

```
Job Requirements: Python, AWS, 5+ years, San Francisco
Candidate A: Python ✓, AWS ✓, 7 years ✓, SF ✓ → Score: 95
Candidate B: Python ✓, AWS ✗, 3 years ✗, Remote ✗ → Score: 45
Candidate C: Java ✗, AWS ✓, 6 years ✓, NY ✗ → Score: 35

Score = 
  0.30 * skill_match_score +
  0.25 * experience_years_score +
  0.20 * location_match_score +
  0.15 * education_score +
  0.10 * activity_recency_score
```

---

# SECTION 6: DATABASE ARCHITECTURE

## 6.1 Entity Relationship Diagram

```
┌─────────────────┐
│     Users       │
├─────────────────┤
│ id (PK)         │
│ email (UNIQUE)  │
│ password_hash   │
│ full_name       │
│ created_at      │
└────────┬────────┘
         │ 1:N
         │
┌────────▼────────────────┐
│    Recruiters           │
├─────────────────────────┤
│ id (PK)                 │
│ user_id (FK)            │
│ company_name            │
│ team_id                 │
│ created_at              │
└────────┬────────────────┘
         │ 1:N
         │
┌────────▼──────────────────────┐
│    Candidates                  │
├────────────────────────────────┤
│ id (PK)                        │
│ recruiter_id (FK)              │
│ name                           │
│ email                          │
│ phone                          │
│ location                       │
│ status (applied/interviewed..)│
│ source (email/upload/linkedin) │
│ created_at                     │
│ embedding_id (FK Pinecone)    │
└────────┬───────────────────────┘
         │ 1:N
         │
┌────────▼──────────────────┐
│    Resumes                │
├───────────────────────────┤
│ id (PK)                   │
│ candidate_id (FK)         │
│ file_path                 │
│ raw_text                  │
│ parsed_json               │
│ version                   │
│ created_at                │
└───────────────────────────┘

┌─────────────────────────┐
│    Skills               │
├─────────────────────────┤
│ id (PK)                 │
│ skill_name              │
│ category (lang/tool/..) │
│ taxonomy_id             │
└────────┬────────────────┘
         │ N:M
         │
┌────────▼──────────────────┐
│    CandidateSkills       │
├───────────────────────────┤
│ candidate_id (FK)         │
│ skill_id (FK)             │
│ proficiency_level         │
│ years_of_experience       │
│ last_used                 │
└───────────────────────────┘

┌────────────────────────────┐
│    Applications            │
├────────────────────────────┤
│ id (PK)                    │
│ recruiter_id (FK)          │
│ candidate_id (FK)          │
│ job_id                     │
│ status (applied/screened..)│
│ rating (1-5 stars)         │
│ notes                      │
│ created_at                 │
└────────────────────────────┘

┌────────────────────────────┐
│    CandidateEmbeddings     │
├────────────────────────────┤
│ id (PK)                    │
│ candidate_id (FK)          │
│ embedding_vector_id        │ → Pinecone
│ embedding_model            │
│ created_at                 │
│ updated_at                 │
└────────────────────────────┘

┌────────────────────────────┐
│    ActivityLogs            │
├────────────────────────────┤
│ id (PK)                    │
│ recruiter_id (FK)          │
│ action_type                │
│ entity_id                  │
│ metadata_json              │
│ created_at                 │
└────────────────────────────┘

┌────────────────────────────┐
│    IntegrationTokens       │
├────────────────────────────┤
│ id (PK)                    │
│ recruiter_id (FK)          │
│ integration_type (gmail..) │
│ access_token (encrypted)   │
│ refresh_token              │
│ expires_at                 │
│ created_at                 │
└────────────────────────────┘
```

## 6.2 Database Choices

### PostgreSQL (Relational)

**Why PostgreSQL?**
- ACID compliance for consistency
- Complex joins (candidates + skills + applications)
- Free tier (Render.com provides free PostgreSQL)
- Full-text search capabilities
- JSON support for flexible metadata

**Schema Location:** `db/migrations/001_init.sql`

### Pinecone (Vector Database)

**Why Pinecone?**
- Serverless vector search (no DevOps)
- Free starter tier (1M vectors)
- Integration with OpenAI embeddings
- Built-in cosine similarity
- No local GPU needed

**Index Configuration:**

```json
{
  "name": "candidates",
  "metric": "cosine",
  "dimension": 1536,
  "spec": {
    "serverless": {
      "cloud": "aws",
      "region": "us-east-1"
    }
  }
}
```

## 6.3 Indexing Strategy

### PostgreSQL Indexes

```sql
-- Candidates table
CREATE INDEX idx_candidates_recruiter_id ON candidates(recruiter_id);
CREATE INDEX idx_candidates_email ON candidates(email);
CREATE INDEX idx_candidates_status ON candidates(status);
CREATE INDEX idx_candidates_created_at ON candidates(created_at DESC);

-- Skills
CREATE INDEX idx_candidate_skills_candidate_id ON candidate_skills(candidate_id);
CREATE INDEX idx_candidate_skills_skill_id ON candidate_skills(skill_id);

-- Applications
CREATE INDEX idx_applications_recruiter_id ON applications(recruiter_id);
CREATE INDEX idx_applications_candidate_id ON applications(candidate_id);
CREATE INDEX idx_applications_status ON applications(status);

-- Full-text search on resume text
CREATE INDEX idx_resumes_text_search ON resumes USING GIN(to_tsvector('english', raw_text));
```

### Pinecone Indexes

```python
# Namespace strategy for multi-tenant isolation
index.query(
    vector=embedding,
    namespace=f"recruiter_{recruiter_id}",
    top_k=10
)
```

---

# SECTION 7: ORGANIZED PROJECT FOLDER STRUCTURE

## 7.1 Directory Hierarchy with Ownership Matrix

```
talent-unify/
│
├── 📋 ROOT CONFIGURATION FILES
│   ├── .env.example                    # [Backend Owner] Template for env vars
│   ├── .env.test                       # [DevOps Owner] Test environment
│   ├── .github/workflows/
│   │   ├── ci-backend.yml              # [DevOps Owner] Backend CI pipeline
│   │   ├── ci-frontend.yml             # [DevOps Owner] Frontend CI pipeline
│   │   └── deploy.yml                  # [DevOps Owner] Deployment pipeline
│   ├── docker-compose.yml              # [DevOps Owner] Local dev environment
│   ├── README.md                       # [Team Lead] Project overview
│   ├── CONTRIBUTING.md                 # [Team Lead] Contribution guidelines
│   ├── ARCHITECTURE.md                 # [Tech Lead] This document
│   └── package.json                    # [Frontend Owner] Monorepo root
│
├── 🎨 FRONTEND/ (React + TypeScript)   [Engineer 1]
│   ├── public/
│   │   ├── favicon.ico
│   │   ├── logo.svg
│   │   └── manifest.json
│   ├── src/
│   │   ├── index.html
│   │   ├── main.tsx                    # Entry point
│   │   ├── App.tsx                     # Root component
│   │   │
│   │   ├── 🔐 auth/
│   │   │   ├── AuthContext.tsx         # Authentication state
│   │   │   ├── useAuth.ts              # Auth hook
│   │   │   ├── LoginPage.tsx
│   │   │   └── LogoutButton.tsx
│   │   │
│   │   ├── 📄 pages/
│   │   │   ├── DashboardPage.tsx       # Main recruiter dashboard
│   │   │   ├── CandidateSearchPage.tsx # Natural language search
│   │   │   ├── CandidateProfilePage.tsx # Individual candidate view
│   │   │   ├── ComparisonPage.tsx      # Side-by-side comparison
│   │   │   ├── PipelinePage.tsx        # Kanban board (Tier 2)
│   │   │   ├── AnalyticsPage.tsx       # Analytics (Tier 2)
│   │   │   └── NotFoundPage.tsx
│   │   │
│   │   ├── 🧩 components/
│   │   │   ├── Navigation/
│   │   │   │   ├── Navbar.tsx
│   │   │   │   ├── Sidebar.tsx
│   │   │   │   └── Breadcrumbs.tsx
│   │   │   │
│   │   │   ├── Candidate/
│   │   │   │   ├── CandidateCard.tsx
│   │   │   │   ├── CandidateList.tsx
│   │   │   │   ├── SkillBadge.tsx
│   │   │   │   ├── CandidateDetails.tsx
│   │   │   │   └── DuplicateWarning.tsx
│   │   │   │
│   │   │   ├── Search/
│   │   │   │   ├── SearchBar.tsx       # Natural language input
│   │   │   │   ├── SearchResults.tsx
│   │   │   │   ├── FilterPanel.tsx
│   │   │   │   └── SearchHistory.tsx
│   │   │   │
│   │   │   ├── Resume/
│   │   │   │   ├── ResumeUploadZone.tsx # Drag-drop upload
│   │   │   │   ├── ResumeViewer.tsx
│   │   │   │   └── ParseProgress.tsx
│   │   │   │
│   │   │   ├── Integration/
│   │   │   │   ├── GmailConnectButton.tsx
│   │   │   │   ├── HrmsConnectButton.tsx
│   │   │   │   └── IntegrationStatus.tsx
│   │   │   │
│   │   │   ├── Comparison/
│   │   │   │   ├── ComparisonTable.tsx
│   │   │   │   ├── SkillComparison.tsx
│   │   │   │   └── ExperienceTimeline.tsx
│   │   │   │
│   │   │   └── UI/ (shadcn/ui)
│   │   │       ├── Button.tsx
│   │   │       ├── Modal.tsx
│   │   │       ├── Input.tsx
│   │   │       ├── Card.tsx
│   │   │       ├── Table.tsx
│   │   │       ├── Badge.tsx
│   │   │       └── Spinner.tsx
│   │   │
│   │   ├── 🔗 services/
│   │   │   ├── api.ts                  # Axios instance + base config
│   │   │   ├── candidateService.ts     # /candidate endpoints
│   │   │   ├── resumeService.ts        # /resume endpoints
│   │   │   ├── searchService.ts        # /search endpoints
│   │   │   ├── integrationService.ts   # /integration endpoints
│   │   │   └── authService.ts          # Authentication
│   │   │
│   │   ├── 🎣 hooks/
│   │   │   ├── useAuth.ts
│   │   │   ├── useFetch.ts
│   │   │   ├── useDebounce.ts
│   │   │   ├── useLocalStorage.ts
│   │   │   └── useCandidates.ts
│   │   │
│   │   ├── 🎨 styles/
│   │   │   ├── globals.css             # Tailwind + global styles
│   │   │   ├── variables.css           # CSS variables
│   │   │   └── themes.css              # Dark/light mode
│   │   │
│   │   ├── 🛠️ utils/
│   │   │   ├── formatters.ts           # Date, currency, skill formatting
│   │   │   ├── validators.ts           # Email, phone validation
│   │   │   ├── constants.ts            # App-wide constants
│   │   │   ├── skillTaxonomy.ts        # Skill list
│   │   │   └── errorHandler.ts
│   │   │
│   │   ├── 📦 types/
│   │   │   ├── index.ts                # Export all types
│   │   │   ├── candidate.ts
│   │   │   ├── resume.ts
│   │   │   ├── user.ts
│   │   │   ├── api.ts
│   │   │   └── search.ts
│   │   │
│   │   └── 📝 config/
│   │       ├── apiConfig.ts
│   │       └── featureFlags.ts
│   │
│   ├── package.json                    # Frontend dependencies
│   ├── tsconfig.json                   # TypeScript config
│   ├── vite.config.ts                  # Vite config
│   ├── tailwind.config.js              # Tailwind config
│   ├── .eslintrc.json                  # ESLint rules
│   └── .prettierrc                     # Code formatting
│
├── ⚙️ BACKEND/ (FastAPI + Python)      [Engineer 2]
│   ├── main.py                         # FastAPI app entry point
│   ├── requirements.txt                # Python dependencies
│   ├── requirements-dev.txt            # Dev dependencies
│   ├── pyproject.toml                  # Python project config
│   │
│   ├── 🔧 app/
│   │   ├── __init__.py
│   │   ├── config.py                   # Environment config, API keys
│   │   ├── exceptions.py               # Custom exceptions
│   │   ├── dependencies.py             # FastAPI dependencies (DB, auth)
│   │   └── logger.py                   # Logging config
│   │
│   ├── 🔐 auth/
│   │   ├── __init__.py
│   │   ├── jwt_handler.py              # JWT token creation/validation
│   │   ├── oauth.py                    # OAuth2 flow for Gmail
│   │   ├── models.py                   # User, Token schemas
│   │   ├── routes.py                   # /auth endpoints
│   │   └── dependencies.py             # get_current_user(), etc
│   │
│   ├── 🗄️ db/
│   │   ├── __init__.py
│   │   ├── database.py                 # SQLAlchemy connection
│   │   ├── models.py                   # ORM models (User, Candidate, Resume..)
│   │   ├── schemas.py                  # Pydantic schemas for API
│   │   │
│   │   └── migrations/                 # Alembic migrations
│   │       ├── env.py
│   │       ├── script.py.mako
│   │       └── versions/
│   │           ├── 001_init.py
│   │           ├── 002_add_embeddings.py
│   │           └── README.md
│   │
│   ├── 📧 integrations/
│   │   ├── __init__.py
│   │   ├── gmail/
│   │   │   ├── client.py               # Gmail API client
│   │   │   ├── service.py              # Email ingestion logic
│   │   │   ├── models.py               # GmailMessage schema
│   │   │   └── routes.py               # /integration/gmail endpoints
│   │   │
│   │   ├── hrms/
│   │   │   ├── client.py               # HRMS simulator
│   │   │   ├── service.py
│   │   │   └── routes.py
│   │   │
│   │   └── linkedin/
│   │       ├── simulator.py            # LinkedIn mock API
│   │       └── routes.py
│   │
│   ├── 🤖 ai/
│   │   ├── __init__.py
│   │   ├── embeddings/
│   │   │   ├── client.py               # OpenAI embeddings client
│   │   │   ├── service.py              # Embedding generation
│   │   │   └── models.py
│   │   │
│   │   ├── nlp/
│   │   │   ├── spacy_nlp.py            # spaCy entity recognition
│   │   │   ├── skill_extractor.py      # Zero-shot skill extraction
│   │   │   └── text_processor.py       # Tokenization, cleaning
│   │   │
│   │   └── ranking/
│   │       ├── scorer.py               # Candidate scoring algorithm
│   │       └── models.py
│   │
│   ├── 📄 resume/
│   │   ├── __init__.py
│   │   ├── parser.py                   # Resume parsing logic
│   │   ├── extractor.py                # Skill/experience extraction
│   │   ├── models.py                   # ParsedResume schema
│   │   ├── routes.py                   # /resume endpoints
│   │   └── validators.py
│   │
│   ├── 🎯 candidate/
│   │   ├── __init__.py
│   │   ├── service.py                  # Candidate business logic
│   │   ├── models.py                   # Pydantic candidate schemas
│   │   ├── routes.py                   # /candidate endpoints
│   │   ├── deduplicator.py             # Duplicate detection
│   │   └── matcher.py                  # Job fit matching (Tier 2)
│   │
│   ├── 🔍 search/
│   │   ├── __init__.py
│   │   ├── semantic_search.py          # Pinecone search logic
│   │   ├── query_parser.py             # NL query → structured search
│   │   ├── models.py                   # SearchQuery, SearchResult schemas
│   │   ├── routes.py                   # /search endpoints
│   │   └── ranker.py                   # Result ranking & filtering
│   │
│   ├── 🔄 tasks/
│   │   ├── __init__.py
│   │   ├── celery_app.py               # Celery config
│   │   ├── resume_parsing_task.py      # Async resume parsing
│   │   ├── email_ingestion_task.py     # Async email fetching
│   │   └── embedding_task.py           # Async embedding generation
│   │
│   ├── 📊 analytics/
│   │   ├── __init__.py
│   │   ├── service.py                  # Metrics calculation
│   │   ├── models.py                   # Analytics schemas
│   │   └── routes.py                   # /analytics endpoints
│   │
│   ├── 🛡️ middleware/
│   │   ├── __init__.py
│   │   ├── error_handler.py            # Global error handling
│   │   ├── request_logger.py           # Request/response logging
│   │   ├── cors.py                     # CORS configuration
│   │   └── rate_limiter.py             # Rate limiting
│   │
│   ├── 🧪 tests/
│   │   ├── __init__.py
│   │   ├── conftest.py                 # pytest config, fixtures
│   │   ├── test_auth.py
│   │   ├── test_candidate.py
│   │   ├── test_resume.py
│   │   ├── test_search.py
│   │   └── test_integrations.py
│   │
│   └── 📝 docs/
│       ├── API.md                      # API documentation
│       ├── DEVELOPMENT.md              # Dev setup guide
│       ├── AI_PIPELINE.md              # AI/ML architecture
│       └── DEPLOYMENT.md               # Deployment guide
│
├── 🧠 AI/ (Standalone AI Services)     [Engineer 3]
│   ├── requirements.txt
│   ├── main.py                         # FastAPI server for ML models
│   │
│   ├── services/
│   │   ├── resume_parser_service.py    # Standalone resume parsing
│   │   ├── embedding_service.py        # Standalone embedding service
│   │   ├── skill_extraction_service.py # Zero-shot classifier
│   │   └── dedup_service.py            # Similarity matching
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── resume_parser.pkl           # Trained models (if any)
│   │   └── skill_classifier.pkl
│   │
│   ├── notebooks/
│   │   ├── explore_embeddings.ipynb
│   │   ├── test_resume_parser.ipynb
│   │   └── skill_extraction_eval.ipynb
│   │
│   └── tests/
│       └── test_services.py
│
├── 🔗 INTEGRATIONS/                    [Engineer 4]
│   ├── gmail/
│   │   ├── config.py                   # OAuth credentials
│   │   ├── client.py                   # Gmail API client
│   │   └── tests/
│   │
│   ├── hrms/
│   │   ├── client.py                   # ADP/BambooHR mock
│   │   └── tests/
│   │
│   ├── linkedin/
│   │   ├── simulator.py                # LinkedIn mock data
│   │   └── tests/
│   │
│   └── webhooks/
│       ├── gmail_webhook_handler.py    # Handle Gmail push notifications
│       └── tests/
│
├── 🗄️ DATA/
│   ├── skills_taxonomy.json            # Skill database (500+)
│   ├── job_descriptions_samples.json   # Sample JDs for matching
│   ├── seed_data.sql                   # Test data for demo
│   └── migrations/
│       └── 001_init.sql                # Database schema
│
├── 📜 SCRIPTS/
│   ├── setup.sh                        # One-command local setup
│   ├── seed_db.py                      # Populate with demo data
│   ├── generate_embeddings.py          # Batch embed existing candidates
│   ├── test_integrations.py            # Integration tests
│   └── deploy.sh                       # Deploy to production
│
├── 📦 DOCKER/
│   ├── Dockerfile.backend              # Backend container
│   ├── Dockerfile.frontend             # Frontend container
│   ├── Dockerfile.ai                   # AI services container
│   └── docker-compose.yml              # Orchestration
│
├── 📚 DOCS/
│   ├── README.md                       # Quick start
│   ├── ARCHITECTURE.md                 # System design (this file)
│   ├── API.md                          # API reference
│   ├── DEVELOPMENT.md                  # Dev setup
│   ├── DEPLOYMENT.md                   # Deployment guide
│   ├── AI_MODELS.md                    # AI/ML details
│   ├── DATABASE.md                     # Database schema
│   ├── DEMO_SCRIPT.md                  # Exact demo steps
│   ├── TROUBLESHOOTING.md              # Common issues
│   └── GLOSSARY.md                     # Terms & definitions
│
└── 📋 CONFIG FILES (Root)
    ├── .env.example
    ├── .env.test
    ├── .gitignore
    ├── .github/
    │   ├── workflows/ci-backend.yml
    │   ├── workflows/ci-frontend.yml
    │   └── workflows/deploy.yml
    ├── docker-compose.yml
    ├── .editorconfig
    ├── LICENSE
    └── .pre-commit-config.yaml
```

## 7.2 File Ownership Matrix

| Owner | Component | Files | Dependencies |
|-------|-----------|-------|--------------|
| **Engineer 1: Frontend** | React UI | `frontend/src/**` | Backend API |
| **Engineer 2: Backend** | FastAPI API | `backend/app/**` | PostgreSQL, Redis |
| **Engineer 3: AI/NLP** | ML pipelines | `ai/**`, `backend/ai/**` | OpenAI API, Pinecone |
| **Engineer 4: DevOps** | Deployment | `.github/`, `docker/`, `scripts/` | All services |

---

# SECTION 8: ANTIGRAVITY PROJECT SETUP (CLARIFIED)

## 8.1 What is "Antigravity Framework"? (CORRECTED)

**Original Issue:** The prompt mentions "Antigravity framework" without definition.

**Clarification:**
- Antigravity is likely **not a real framework** for this hackathon
- **ASSUMED CORRECTION**: This refers to a **project scaffolding/templating tool**
- **Recommended replacement**: Use standard industry tools

## 8.2 Corrected Project Initialization Strategy

### Option A: Use Cookiecutter (Recommended for Hackathons)

**What:** Python template generator for reproducible project setup

**Setup Command:**
```bash
# Install cookiecutter
pip install cookiecutter

# Use Python FastAPI + React template
cookiecutter https://github.com/tiangolo/full-stack-fastapi-postgresql

# Or create custom template
cookiecutter ./templates/talent-unify-template/
```

**Template Structure:**
```
./templates/talent-unify-template/
├── cookiecutter.json
└── {{cookiecutter.project_slug}}/
    ├── backend/
    ├── frontend/
    ├── docker-compose.yml
    └── README.md
```

**cookiecutter.json:**
```json
{
    "project_name": "TalentUnify",
    "project_slug": "{{ cookiecutter.project_name.lower().replace(' ', '_') }}",
    "postgres_db": "talent_unify",
    "backend_port": 8000,
    "frontend_port": 3000
}
```

### Option B: Use Scaffolding CLI (Custom)

**Create a project initialization script:**

```bash
#!/bin/bash
# scripts/init_project.sh

PROJECT_NAME=${1:-"talent-unify"}

# 1. Create directory structure
mkdir -p $PROJECT_NAME/{frontend,backend,ai,integrations,data,scripts,docs,docker}

# 2. Clone boilerplate templates
git clone https://github.com/tiangolo/fastapi-template backend/
git clone https://github.com/vitejs/vite-plugin-react-template frontend/

# 3. Generate config files
cat > .env.example <<EOF
# PostgreSQL
DATABASE_URL=postgresql://user:password@localhost:5432/talent_unify
SQLALCHEMY_TRACK_MODIFICATIONS=False

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
EOF

# 4. Initialize Git
git init
git add .
git commit -m "Initial project structure"

echo "✅ Project initialized: $PROJECT_NAME"
```

**Usage:**
```bash
bash scripts/init_project.sh talent-unify
```

## 8.3 Markdown Specification File

**This is the architecture blueprint** that generates the project.

**File:** `PROJECT_SPECIFICATION.md` (at repo root)

**Format:**

```markdown
# TalentUnify MVP Specification

## 1. Project Metadata
- Name: TalentUnify
- Team: 4 Engineers
- Duration: 48 hours
- Status: In Development

## 2. Feature List
- [x] Resume Upload
- [x] Candidate Search
- [ ] Candidate Comparison (Tier 2)
- [ ] Pipeline Management (Tier 2)

## 3. Tech Stack
- Frontend: React 18 + TypeScript + Tailwind
- Backend: FastAPI + PostgreSQL + Redis
- AI: OpenAI Embeddings + spaCy
- Vector DB: Pinecone
- DevOps: Docker + GitHub Actions

## 4. Architecture
[Full architecture detailed above in SECTION 3]

## 5. Database Schema
[Tables listed in SECTION 6.1]

## 6. API Endpoints
[Defined in SECTION 9]

## 7. Development Tasks
[Broken down in SECTION 10]

## 8. Deployment Steps
[Listed in SECTION 13]
```

**This markdown file is the single source of truth** for the entire project.

---

# SECTION 9: UI/UX DESIGN PLAN

## 9.1 Design System Overview

**Color Palette:**
- Primary: #2563EB (Professional Blue)
- Secondary: #10B981 (Success Green)
- Danger: #EF4444 (Error Red)
- Background: #F9FAFB (Light Gray)
- Text: #1F2937 (Dark Gray)

**Typography:**
- Headlines: Inter Bold (18-32px)
- Body: Inter Regular (14-16px)
- Mono: JetBrains Mono (Code)

**Components:** Use shadcn/ui for consistency

## 9.2 Page Designs

### 9.2.1 Recruiter Dashboard (Landing Page)

**URL:** `/dashboard`

**Layout:**

```
┌─────────────────────────────────────────────────┐
│ Header: Logo | Search | User Menu               │
├──────────┬──────────────────────────────────────┤
│ Sidebar  │ Main Content                         │
│          │                                      │
│ Dashboard│ 📊 Quick Stats                       │
│ Search   │ ├─ 150 Candidates                   │
│ Pipeline │ ├─ 45 In Progress                   │
│ Analytics│ └─ 12 Offered                       │
│ Settings │                                      │
│          │ 🔝 Recently Added Candidates         │
│          │ ┌──────────────────────────────────┐ │
│          │ │ Name | Skills | Source | Date    │ │
│          │ ├──────────────────────────────────┤ │
│          │ │ John | Python,AWS | Email | 2h  │ │
│          │ │ Jane | React,JS  | Upload | 1h  │ │
│          │ └──────────────────────────────────┘ │
│          │                                      │
│          │ 🔗 Quick Actions                    │
│          │ [Upload Resume] [Connect Gmail]    │
│          │ [Import CSV] [Search Candidates]   │
│          │                                      │
└──────────┴──────────────────────────────────────┘
```

**Components:**
- `<StatsCard />` — Shows metrics
- `<CandidateTable />` — Recent candidates
- `<ActionButtons />` — Quick access
- `<ActivityFeed />` — Timeline of actions

### 9.2.2 Candidate Search Page

**URL:** `/search`

**Layout:**

```
┌─────────────────────────────────────────────────┐
│ Natural Language Search Bar                     │
│ ┌───────────────────────────────────────────┐  │
│ │ Find Python developers with 5+ years... │  │
│ └───────────────────────────────────────────┘  │
│                   [Search]                      │
├──────────────────────────────────────────────────┤
│                                                  │
│ Filters (Left)        │ Results (Right)         │
│                       │                         │
│ ☐ Skills              │ 🔍 Results: 12         │
│   ☐ Python            │                         │
│   ☐ AWS               │ ┌─────────────────────┐ │
│   ☐ React             │ │ Rank 1: 95% match   │ │
│                       │ │ John Doe             │ │
│ ☐ Years Exp.          │ │ Python ⭐⭐⭐⭐⭐ 8y │ │
│   ☐ 5-10 years        │ │ AWS    ⭐⭐⭐⭐  6y │ │
│   ☐ 10+ years         │ │ [View Profile]      │ │
│                       │ └─────────────────────┘ │
│ ☐ Location            │                         │
│   ☐ USA               │ ┌─────────────────────┐ │
│   ☐ Remote            │ │ Rank 2: 87% match   │ │
│                       │ │ Jane Smith           │ │
│ [Clear All]           │ │ Python ⭐⭐⭐⭐  5y │ │
│                       │ │ AWS    ⭐⭐⭐      3y │ │
│                       │ │ [View Profile]      │ │
│                       │ └─────────────────────┘ │
│                       │                         │
│                       │ [Load More...]          │
└──────────────────────┴─────────────────────────┘
```

**Components:**
- `<SearchBar />` — NL input with suggestions
- `<FilterPanel />` — Multi-select filters
- `<ResultCard />` — Candidate card with scoring
- `<ResultsList />` — Infinite scroll results

### 9.2.3 Candidate Profile Page

**URL:** `/candidates/:id`

**Layout:**

```
┌──────────────────────────────────────────────┐
│ ◀ Back | John Doe | ⭐ ⭐ ⭐ ⭐ ☆ (Rating)   │
├──────────────────────────────────────────────┤
│                                              │
│ 📋 Contact              │ 📊 Candidate       │
│ ├─ john@example.com     │ ├─ Applied: 2024   │
│ ├─ +1-234-567-8900      │ ├─ Status: Screened│
│ ├─ San Francisco, CA    │ ├─ Score: 92/100   │
│ └─ LinkedIn: [Link]     │ └─ Fit: 🟢 Excellent│
│                         │                    │
│ 💼 Experience           │ 🔧 Top Skills     │
│ ├─ Senior Engineer      │ ├─ Python ⭐⭐⭐⭐⭐│
│ │  Google (2020-2024)   │ ├─ AWS ⭐⭐⭐⭐  │
│ │  Built APIs, 8y       │ ├─ Docker ⭐⭐⭐  │
│ │                       │ ├─ PostgreSQL ⭐⭐⭐│
│ ├─ Software Engineer    │ └─ TypeScript ⭐⭐ │
│ │  Microsoft (2018-2020)│                    │
│ │  Full-stack, 4y       │ 🎓 Education      │
│ │                       │ ├─ BS Computer Sci │
│ └─ Intern               │ │  MIT, 2018       │
│    StartupX (2017)      │ └─ Bootcamp Cert   │
│                         │    Codecademy, 2017│
│                         │                    │
│ 📝 Resume               │ 📧 Email           │
│ [Download PDF]          │ [Send Message]     │
│ [View Parsed]           │ [Schedule Interview]│
│                         │ [Add to Pipeline]  │
│                         │ [Share with Team]  │
│                         │                    │
│ 💬 Notes (Recruiter)    │                    │
│ ┌──────────────────────┐│                    │
│ │ "Great fit for       ││                    │
│ │  Senior role. Strong ││                    │
│ │  AWS background."    ││                    │
│ │            — Jane    ││                    │
│ │         (2 hours ago)││                    │
│ └──────────────────────┘│                    │
│                                              │
│ 🔗 Related Candidates (Similar skills)      │
│ ┌──────────┐ ┌──────────┐ ┌──────────┐     │
│ │ Jane S.  │ │ Alex M.  │ │ Sarah L. │     │
│ │ 88% match│ │ 85% match│ │ 82% match│     │
│ └──────────┘ └──────────┘ └──────────┘     │
│                                              │
└──────────────────────────────────────────────┘
```

**Components:**
- `<ProfileHeader />` — Name, rating, actions
- `<ContactCard />` — Email, phone, location
- `<ExperienceTimeline />` — Work history
- `<SkillsPanel />` — Skill badges with ratings
- `<ResumeViewer />` — Embedded PDF viewer
- `<NotesSection />` — Recruiter comments
- `<RelatedCandidates />` — Similar candidates

### 9.2.4 Candidate Comparison Page (Tier 2)

**URL:** `/compare?candidates=id1,id2,id3`

**Layout:**

```
┌────────────────────────────────────────────────────────────┐
│ Comparing: John Doe | Jane Smith | Alex Miller             │
├────────────────────────────────────────────────────────────┤
│                                                             │
│            │ John Doe      │ Jane Smith     │ Alex Miller   │
│ ─────────────────────────────────────────────────────────── │
│ Match %    │ 95% 🟢        │ 87% 🟡        │ 78% 🟡       │
│ Experience │ 8 years       │ 5 years       │ 10 years      │
│ Location   │ SF            │ NYC (Remote)  │ Boston        │
│ Salary Exp │ $180-220k     │ $150-200k     │ $200-250k     │
│                                                             │
│ Python     │ ⭐⭐⭐⭐⭐  │ ⭐⭐⭐⭐   │ ⭐⭐⭐       │
│ AWS        │ ⭐⭐⭐⭐     │ ⭐⭐⭐⭐⭐  │ ⭐⭐⭐⭐   │
│ React      │ ⭐⭐⭐       │ ⭐⭐⭐⭐   │ ⭐⭐        │
│ Docker     │ ⭐⭐⭐⭐     │ ⭐⭐⭐      │ ⭐⭐⭐⭐⭐  │
│ PostgreSQL │ ⭐⭐⭐⭐⭐  │ ⭐⭐       │ ⭐⭐⭐⭐   │
│                                                             │
│ [View All Skills] [Download Comparison] [Export]           │
│                                                             │
└────────────────────────────────────────────────────────────┘
```

**Components:**
- `<ComparisonTable />` — Skills side-by-side
- `<RadarChart />` — Skill distribution (Recharts)
- `<ExperienceComparison />` — Timeline overlay
- `<ExportButton />` — PDF/CSV download

### 9.2.5 Integration Page

**URL:** `/settings/integrations`

**Layout:**

```
┌─────────────────────────────────────────────┐
│ Integrations & Data Sources                 │
├─────────────────────────────────────────────┤
│                                             │
│ 📧 Gmail                                   │
│ ├─ Status: ✅ Connected (john@company.com)│
│ ├─ Last Sync: 2 hours ago                  │
│ ├─ Resumes Found: 45                       │
│ └─ [Disconnect] [Sync Now]                 │
│                                             │
│ 💼 HRMS (BambooHR)                         │
│ ├─ Status: ⭕ Not Connected                │
│ └─ [Connect BambooHR]                      │
│                                             │
│ 💼 Workday                                 │
│ ├─ Status: ⭕ Not Connected                │
│ └─ [Connect Workday]                       │
│                                             │
│ 📁 LinkedIn (Simulation)                   │
│ ├─ Status: ✅ Connected                    │
│ ├─ Last Sync: 5 hours ago                  │
│ ├─ Candidates Imported: 120                │
│ └─ [Sync Now] [Settings]                   │
│                                             │
│ 📤 Manual Upload                           │
│ ├─ [Upload Resume] [Upload CSV]            │
│ └─ Max File Size: 25MB                     │
│                                             │
└─────────────────────────────────────────────┘
```

**Components:**
- `<IntegrationCard />` — Status, actions
- `<ConnectionModal />` — OAuth flow
- `<SyncButton />` — Trigger data fetch
- `<UploadZone />` — Drag-drop file upload

---

# SECTION 10: API DESIGN

## 10.1 Authentication Endpoints

### POST /auth/register
**Register a new recruiter account**

**Request:**
```json
{
  "email": "recruiter@company.com",
  "password": "SecurePassword123!",
  "full_name": "Jane Doe",
  "company_name": "TechCorp"
}
```

**Response:**
```json
{
  "id": "uuid-1234",
  "email": "recruiter@company.com",
  "full_name": "Jane Doe",
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "expires_in": 3600
}
```

### POST /auth/login
**Login with email/password**

**Request:**
```json
{
  "email": "recruiter@company.com",
  "password": "SecurePassword123!"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "expires_in": 3600,
  "user": {
    "id": "uuid-1234",
    "email": "recruiter@company.com",
    "full_name": "Jane Doe"
  }
}
```

### POST /auth/refresh
**Refresh JWT token**

**Request:**
```json
{
  "refresh_token": "eyJ0eXAiOiJKV1QiLC..."
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "expires_in": 3600
}
```

---

## 10.2 Resume Endpoints

### POST /resume/upload
**Upload and parse a resume**

**Request:** (multipart/form-data)
```
file: <binary PDF/DOCX>
candidate_name: "John Doe" (optional)
```

**Response:**
```json
{
  "resume_id": "uuid-5678",
  "candidate_id": "uuid-1234",
  "file_name": "john_doe_resume.pdf",
  "parsed_data": {
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "+1-234-567-8900",
    "location": "San Francisco, CA",
    "summary": "Senior Software Engineer with 8 years of experience...",
    "skills": ["Python", "AWS", "Docker", "PostgreSQL"],
    "experience": [
      {
        "title": "Senior Engineer",
        "company": "Google",
        "start_date": "2020-01-01",
        "end_date": "2024-01-01",
        "description": "Led backend infrastructure..."
      }
    ],
    "education": [
      {
        "degree": "BS",
        "field": "Computer Science",
        "school": "MIT",
        "year": 2018
      }
    ]
  },
  "parsing_status": "success",
  "extraction_confidence": 0.94,
  "duplicates_found": ["uuid-9999", "uuid-8888"],
  "created_at": "2024-01-15T10:30:00Z"
}
```

### POST /resume/parse
**Manually parse resume text (for email attachments)**

**Request:**
```json
{
  "text": "John Doe\njohn@example.com\n+1-234-567-8900\n\nPython Developer...",
  "source": "email",
  "source_metadata": {
    "sender_email": "hiring@company.com",
    "email_subject": "Resume: John Doe",
    "received_at": "2024-01-15T08:00:00Z"
  }
}
```

**Response:** (Same as POST /resume/upload)

### GET /resume/:resume_id
**Fetch parsed resume details**

**Response:**
```json
{
  "resume_id": "uuid-5678",
  "candidate_id": "uuid-1234",
  "parsed_data": { ... },
  "parsing_status": "success",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

---

## 10.3 Candidate Endpoints

### GET /candidate
**List all candidates for recruiter (paginated)**

**Query Parameters:**
```
?page=1&limit=20&sort=created_at&order=desc&status=applied
```

**Response:**
```json
{
  "candidates": [
    {
      "id": "uuid-1234",
      "name": "John Doe",
      "email": "john@example.com",
      "phone": "+1-234-567-8900",
      "location": "San Francisco, CA",
      "status": "applied",
      "skills": ["Python", "AWS"],
      "years_experience": 8,
      "source": "email",
      "created_at": "2024-01-15T10:30:00Z",
      "embedding_id": "candidate_uuid_1234_emb"
    }
  ],
  "total": 150,
  "page": 1,
  "limit": 20,
  "pages": 8
}
```

### GET /candidate/:candidate_id
**Fetch detailed candidate profile**

**Response:**
```json
{
  "id": "uuid-1234",
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+1-234-567-8900",
  "location": "San Francisco, CA",
  "status": "applied",
  "source": "email",
  "skills": [
    {
      "skill_id": "skill-001",
      "name": "Python",
      "proficiency": "expert",
      "years": 8
    }
  ],
  "experience": [
    {
      "title": "Senior Engineer",
      "company": "Google",
      "start_date": "2020-01-01",
      "end_date": "2024-01-01"
    }
  ],
  "education": [...],
  "resumes": ["uuid-5678", "uuid-5679"],
  "applications": [
    {
      "job_id": "job-001",
      "status": "in-progress",
      "rating": 4.5,
      "applied_at": "2024-01-15T10:30:00Z"
    }
  ],
  "recruiter_notes": "Strong Python background, great fit for role.",
  "last_activity": "2024-01-16T09:00:00Z",
  "created_at": "2024-01-15T10:30:00Z"
}
```

### PUT /candidate/:candidate_id
**Update candidate profile**

**Request:**
```json
{
  "status": "interview-scheduled",
  "recruiter_notes": "Scheduled for Friday 2pm",
  "rating": 5
}
```

**Response:** (Updated candidate object)

### POST /candidate/deduplicate
**Find and flag duplicate candidates**

**Request:**
```json
{
  "candidate_ids": ["uuid-1234", "uuid-5678", "uuid-9999"]
}
```

**Response:**
```json
{
  "analysis_id": "analysis-001",
  "duplicates": [
    {
      "primary_id": "uuid-1234",
      "duplicates": [
        {
          "id": "uuid-5678",
          "similarity_score": 0.95,
          "reason": "Same email address"
        },
        {
          "id": "uuid-9999",
          "similarity_score": 0.87,
          "reason": "Embedding similarity"
        }
      ]
    }
  ]
}
```

### POST /candidate/merge
**Merge duplicate candidate profiles**

**Request:**
```json
{
  "primary_id": "uuid-1234",
  "merge_ids": ["uuid-5678", "uuid-9999"]
}
```

**Response:**
```json
{
  "merge_id": "merge-001",
  "primary_candidate": { ... },
  "merged_count": 2,
  "status": "success"
}
```

---

## 10.4 Search Endpoints

### POST /search
**Natural language candidate search (AI-powered)**

**Request:**
```json
{
  "query": "Find Python developers with AWS experience and 5+ years",
  "limit": 10,
  "filters": {
    "min_years": 5,
    "location": "San Francisco",
    "remote_ok": true
  }
}
```

**Response:**
```json
{
  "query_id": "search-001",
  "original_query": "Find Python developers with AWS experience...",
  "parsed_query": {
    "skills": ["Python", "AWS"],
    "min_years": 5,
    "location": "San Francisco"
  },
  "results": [
    {
      "rank": 1,
      "candidate_id": "uuid-1234",
      "name": "John Doe",
      "match_score": 0.95,
      "match_explanation": "Expert Python (8y), Advanced AWS (6y), Remote OK",
      "skills": ["Python", "AWS", "Docker"],
      "years_experience": 8
    },
    {
      "rank": 2,
      "candidate_id": "uuid-5678",
      "name": "Jane Smith",
      "match_score": 0.87,
      "match_explanation": "Senior Python (5y), Good AWS (3y), NYC location",
      "skills": ["Python", "AWS", "React"],
      "years_experience": 5
    }
  ],
  "total_results": 12,
  "search_time_ms": 245
}
```

### GET /search/history
**Fetch search history for recruiter**

**Response:**
```json
{
  "searches": [
    {
      "search_id": "search-001",
      "query": "Python developers with AWS",
      "result_count": 12,
      "created_at": "2024-01-16T10:30:00Z"
    }
  ]
}
```

### POST /search/save
**Save search query for later**

**Request:**
```json
{
  "query": "Find Python developers with AWS experience",
  "name": "Python AWS Specialists",
  "filters": { ... }
}
```

**Response:**
```json
{
  "saved_search_id": "saved-001",
  "name": "Python AWS Specialists",
  "created_at": "2024-01-16T10:30:00Z"
}
```

---

## 10.5 Integration Endpoints

### POST /integration/gmail/connect
**Initiate Gmail OAuth flow**

**Response:**
```json
{
  "auth_url": "https://accounts.google.com/o/oauth2/v2/auth?...",
  "state": "random-state-token"
}
```

### POST /integration/gmail/callback
**Handle Gmail OAuth callback**

**Request:**
```json
{
  "code": "4/0AY-...",
  "state": "random-state-token"
}
```

**Response:**
```json
{
  "status": "connected",
  "email": "recruiter@company.com",
  "sync_status": "in-progress",
  "last_sync": null,
  "resumes_found": 0
}
```

### GET /integration/gmail/status
**Check Gmail integration status**

**Response:**
```json
{
  "status": "connected",
  "email": "recruiter@company.com",
  "last_sync": "2024-01-16T10:00:00Z",
  "resumes_found": 45,
  "candidates_imported": 42
}
```

### POST /integration/gmail/sync
**Manually trigger Gmail sync**

**Response:**
```json
{
  "sync_id": "sync-001",
  "status": "in-progress",
  "started_at": "2024-01-16T10:30:00Z",
  "estimated_duration_ms": 3000
}
```

### DELETE /integration/gmail
**Disconnect Gmail**

**Response:**
```json
{
  "status": "disconnected",
  "message": "Gmail integration removed. Previously imported candidates remain in database."
}
```

---

## 10.6 Webhook Endpoints

### POST /webhooks/gmail
**Receive Gmail push notifications (background sync)**

**Request (from Gmail API):**
```json
{
  "subscription": "gmail-push-001",
  "new_messages": [
    {
      "message_id": "msg-001",
      "from": "hiring@company.com",
      "subject": "Resume: John Doe",
      "has_attachments": true
    }
  ]
}
```

**Response:**
```json
{
  "status": "processing",
  "messages_queued": 1,
  "celery_task_id": "task-001"
}
```

---

# SECTION 11: DEVELOPMENT PLAN FOR 4-PERSON TEAM

## 11.1 Team Role Assignment

| Role | Engineer | Focus | Hours |
|------|----------|-------|-------|
| **Frontend Lead** | Engineer 1 | React UI, Dashboard | 48h |
| **Backend Lead** | Engineer 2 | FastAPI, Candidate DB, APIs | 48h |
| **AI/ML Engineer** | Engineer 3 | NLP, Embeddings, Search | 48h |
| **DevOps/Integration Lead** | Engineer 4 | Deployment, Gmail OAuth, DevOps | 48h |

## 11.2 48-Hour Execution Timeline

### Hour 0-2: Project Setup & Architecture Alignment

**All Engineers Together:**

- [ ] Clone repo & setup local environment
- [ ] Run `setup.sh` to bootstrap project
- [ ] Create `.env` files with API keys
- [ ] Start PostgreSQL + Redis locally
- [ ] Verify all 4 services can start
- [ ] Review ARCHITECTURE.md together
- [ ] Define Slack channel for blockers
- [ ] Setup git workflow (main, develop, feature branches)

**Deliverable:** Working local dev environment for all 4 engineers

---

### Hour 2-6: Foundation Tier 1 Features

**Engineer 1 (Frontend):**
- [ ] Setup React 18 + TypeScript + Tailwind project
- [ ] Create basic Navbar + Sidebar layout
- [ ] Build Dashboard page with hardcoded stats
- [ ] Build Resume Upload component with drag-drop
- [ ] Create Candidate Card component
- [ ] Setup React Router for navigation
- [ ] Export components to shared library

**Engineer 2 (Backend):**
- [ ] Initialize FastAPI project with FastAPI setup
- [ ] Create database models (User, Candidate, Resume)
- [ ] Setup SQLAlchemy ORM and migrations
- [ ] Build authentication (JWT + OAuth2)
- [ ] Create /auth endpoints (register, login)
- [ ] Create /candidate GET/POST endpoints
- [ ] Setup error handling & logging middleware
- [ ] Generate Swagger docs

**Engineer 3 (AI/NLP):**
- [ ] Setup OpenAI API key validation
- [ ] Install spaCy + transformers + pypdf
- [ ] Build resume text extraction function (PDF/DOCX)
- [ ] Build spaCy NER for name/email/phone extraction
- [ ] Build skill extraction function (keyword matching)
- [ ] Create ParsedResume Pydantic schema
- [ ] Test with 5 sample resumes
- [ ] Create `/ai/parse` FastAPI endpoint

**Engineer 4 (DevOps):**
- [ ] Setup Docker and docker-compose.yml
- [ ] Create Dockerfile for backend + frontend
- [ ] Setup GitHub repo with branch protection
- [ ] Create `.github/workflows/ci-backend.yml`
- [ ] Create `.github/workflows/ci-frontend.yml`
- [ ] Setup PostgreSQL in Docker
- [ ] Setup Redis in Docker
- [ ] Test local deployment: `docker-compose up`

**Sync Point (Hour 6):**
All engineers demo their progress. Resolve blockers.

---

### Hour 6-18: Resume Parsing Pipeline

**Engineer 3 (AI/NLP) — Primary:**
- [ ] Integrate spaCy entity recognition into resume parser
- [ ] Implement skill extraction with HuggingFace zero-shot
- [ ] Create `/ai/extract-skills` endpoint
- [ ] Build skill deduplication (normalize Python → python)
- [ ] Create training/test data for skill extraction
- [ ] Test with 20+ real resumes
- [ ] Measure extraction accuracy (aim for 85%+)
- [ ] Document edge cases

**Engineer 2 (Backend) — Supporting:**
- [ ] Create `/resume/upload` endpoint
- [ ] Create `/resume/parse` endpoint
- [ ] Integrate resume parser service calls
- [ ] Store parsed resume in PostgreSQL
- [ ] Create resume validation schema
- [ ] Build resume versioning (multiple uploads per candidate)
- [ ] Setup Celery task for async parsing
- [ ] Create `/resume/:id` GET endpoint

**Engineer 1 (Frontend) — Supporting:**
- [ ] Build ResumeUploadZone component
- [ ] Add upload progress indicator
- [ ] Display parsed resume data
- [ ] Show extraction confidence score
- [ ] Build error handling for failed parses
- [ ] Add drag-and-drop to upload component
- [ ] Connect to `/resume/upload` endpoint
- [ ] Add loading spinners

**Engineer 4 (DevOps) — Supporting:**
- [ ] Setup Celery + Redis for task queuing
- [ ] Monitor Celery tasks in local setup
- [ ] Configure Sentry for error tracking (optional)
- [ ] Setup AWS S3 mock (MinIO) for file storage
- [ ] Create deploy script for resume parser service

**Sync Point (Hour 12):**
Test end-to-end: Upload resume → Parse → Store → Retrieve

---

### Hour 18-30: Candidate Search & Embeddings

**Engineer 3 (AI/NLP) — Primary:**
- [ ] Setup Pinecone account + API key
- [ ] Create Pinecone index "candidates"
- [ ] Implement OpenAI embeddings function
- [ ] Create embedding pipeline for candidate profiles
- [ ] Build semantic search function
- [ ] Test search with real queries:
  - "Find Python developers"
  - "AWS architects with 5+ years"
  - "React engineers in San Francisco"
- [ ] Measure search relevance (manual eval)
- [ ] Optimize embedding model (try text-embedding-3-small vs -large)

**Engineer 2 (Backend) — Primary:**
- [ ] Create `/search` endpoint (NL search)
- [ ] Integrate AI embeddings service
- [ ] Build query parser (NL → structured filters)
- [ ] Implement result ranking algorithm
- [ ] Create `/search/history` endpoint
- [ ] Build `/search/save` endpoint
- [ ] Setup search caching (Redis)
- [ ] Rate-limit search endpoint

**Engineer 1 (Frontend) — Supporting:**
- [ ] Build SearchBar component with autocomplete
- [ ] Create SearchResults component
- [ ] Build FilterPanel (skills, years, location)
- [ ] Implement result pagination
- [ ] Add search history dropdown
- [ ] Build result cards with match score explanation
- [ ] Connect to `/search` endpoint
- [ ] Add keyboard shortcuts (Ctrl+K for search)

**Engineer 4 (DevOps) — Supporting:**
- [ ] Setup Pinecone CLI tools
- [ ] Backup Pinecone data strategy
- [ ] Monitor Pinecone usage
- [ ] Create smoke test for embeddings

**Sync Point (Hour 24):**
Live demo: Type natural language query → AI returns ranked candidates

---

### Hour 30-36: Email Integration (Tier 1)

**Engineer 4 (DevOps) — Primary:**
- [ ] Setup Gmail OAuth app (Google Cloud Console)
- [ ] Implement OAuth2 flow in FastAPI
- [ ] Create `/integration/gmail/connect` endpoint
- [ ] Create `/integration/gmail/callback` endpoint
- [ ] Fetch emails with attachments using Gmail API
- [ ] Extract attachments from emails
- [ ] Queue for async processing (Celery)
- [ ] Create `/integration/gmail/status` endpoint

**Engineer 2 (Backend) — Supporting:**
- [ ] Create IntegrationToken model
- [ ] Store OAuth tokens encrypted
- [ ] Build integration status dashboard
- [ ] Setup email attachment download + storage
- [ ] Create `/integration/gmail/sync` endpoint
- [ ] Implement sync rate limiting (avoid Gmail quota)
- [ ] Build error recovery (retry failed emails)

**Engineer 1 (Frontend) — Supporting:**
- [ ] Build GmailConnectButton component
- [ ] Show OAuth flow (popup window)
- [ ] Display connection status (connected/disconnected)
- [ ] Build sync progress indicator
- [ ] Show candidate count from Gmail
- [ ] Add manual "Sync Now" button
- [ ] Connection status in Integrations page

**Engineer 3 (AI/NLP) — Supporting:**
- [ ] Ensure resume parser handles email-extracted PDFs
- [ ] Test with 10+ real emails with resume attachments

**Sync Point (Hour 32):**
Demo: Connect Gmail → Fetch resumes → Auto-parse → Add to DB

---

### Hour 36-42: Polish & Tier 2 Feature (If Time)

**ALL ENGINEERS:**

**If time permits, pick ONE Tier 2 feature:**

**Option A: Candidate Deduplication**
- Engineer 3: Build deduplication algorithm (embedding similarity)
- Engineer 2: Create `/candidate/deduplicate` + `/candidate/merge` endpoints
- Engineer 1: Build deduplication UI with merge flows
- Engineer 4: Test deduplication at scale (100+ candidates)

**Option B: Candidate Comparison**
- Engineer 1: Build ComparisonPage with table + charts
- Engineer 2: Create `/candidate/compare` endpoint
- Engineer 3: Implement skill comparison logic
- Engineer 4: Optimize comparison queries

**Option C: Recruiter Dashboard Metrics**
- Engineer 1: Build Analytics page with charts
- Engineer 2: Create `/analytics` endpoint
- Engineer 3: Implement metric calculations
- Engineer 4: Monitor backend performance

**Polish (All):**
- [ ] Fix TypeScript errors
- [ ] Fix ESLint warnings
- [ ] Test responsive design (mobile, tablet, desktop)
- [ ] Fix slow API responses
- [ ] Setup error boundaries in React
- [ ] Improve loading states
- [ ] Test all integrations end-to-end
- [ ] Write basic tests (5-10 per engineer)

**Sync Point (Hour 36):**
Decide Tier 2 feature. Divide work.

---

### Hour 42-46: Demo Prep & Testing

**All Engineers:**

- [ ] **Test the full demo flow:**
  1. Login as recruiter
  2. Upload resume (PDF)
  3. See parsed candidate data
  4. Search with natural language
  5. View ranked results
  6. Click candidate profile
  7. Show related candidates
  8. Connect Gmail & sync

- [ ] **Prepare 5-minute demo script** (write to DEMO_SCRIPT.md)
- [ ] **Create 3-4 test candidates** in seed data
- [ ] **Test on fresh PostgreSQL** (clean DB)
- [ ] **Screenshot key flows** for presentation
- [ ] **Fix any visual bugs** (UI polish)
- [ ] **Test error cases:**
  - Invalid PDF
  - Missing fields
  - Search with no results
  - Gmail connection failure
- [ ] **Performance test:**
  - Search latency < 2 seconds
  - Candidate profile load < 1 second
  - File upload < 5 seconds
- [ ] **Load test basics** (Apache Bench or wrk)
  ```bash
  ab -n 100 -c 10 http://localhost:8000/candidate
  ```

**Deliverable:** Bug-free, polished demo system

---

### Hour 46-48: Final Deployment & Presentation

**Engineer 4 (DevOps) — Primary:**
- [ ] Deploy backend to Railway/Render
- [ ] Deploy frontend to Vercel
- [ ] Deploy PostgreSQL to managed service
- [ ] Setup Pinecone production index
- [ ] Configure production `.env` variables
- [ ] Run smoke tests on production
- [ ] Setup monitoring (error tracking, logs)
- [ ] Create runbook for judges

**Engineer 1, 2, 3:**
- [ ] Practice demo (5 minutes)
- [ ] Prepare talking points (innovation, architecture, challenges)
- [ ] Troubleshoot production issues
- [ ] Prepare technical Q&A

**Final 30 minutes:**
- [ ] Practice presentation with judges
- [ ] Have backup demo (local machine)
- [ ] Print out architecture diagram
- [ ] Prepare GitHub repo link + live demo link

---

## 11.3 Daily Standups (3x per day)

**Hour 8, 24, 40:**

**Each engineer (2 minutes):**
- What did I complete?
- What am I blocked on?
- What's next?

---

## 11.4 Git Workflow for Hackathon

```bash
# Initial setup
git clone <repo>
cd talent-unify
git checkout -b develop

# Engineer 1 (Frontend)
git checkout -b feature/dashboard
# ... make commits ...
git push origin feature/dashboard
# Create pull request (no review needed in hackathon)
git merge --squash feature/dashboard develop

# Engineer 2 (Backend)
git checkout -b feature/api-candidates
# ... make commits ...
git merge develop  # Pull latest
git push origin feature/api-candidates

# Main branch = production-ready code
# Develop branch = integration branch
# Feature branches for parallel work
```

---

# SECTION 12: JUDGE-WINNING DEMO FLOW

## 12.1 Demo Story (5-7 minutes)

### Scene: Recruiter Dashboard

> "Hi judges! I'm going to show you TalentUnify, an AI-powered recruitment platform. Imagine you're a recruiter at a fast-growing startup, and you need to hire 10 senior Python engineers. You've been managing resumes in email, spreadsheets, and LinkedIn. It's chaos."

**[Demo Step 1: Upload Resume]**

> "First, I'll upload a candidate's resume."

- Click [Upload Resume] button
- Drag-drop a PDF resume
- Show parsing in progress (spinner)
- Display extracted data:
  - Name: John Doe
  - Email: john@example.com
  - Skills: Python ⭐⭐⭐⭐⭐, AWS ⭐⭐⭐⭐, Docker ⭐⭐⭐
  - Experience: Senior Engineer at Google (8 years)

> "Behind the scenes, our AI instantly parsed this resume using spaCy and extracted structured data — no manual data entry. The extraction is 94% accurate."

---

**[Demo Step 2: Email Integration]**

> "But most of your candidates come through email. Let me connect your Gmail account."

- Click [Connect Gmail] in Settings
- Show OAuth popup (or walk through flow)
- Display: "Gmail connected ✅ — 45 resumes with attachments found"
- Show "Syncing..." with progress
- After sync: "42 new candidates imported automatically"

> "Now, every resume in your email inbox is automatically parsed and added to our system. We're doing the grunt work for you."

---

**[Demo Step 3: Natural Language Search (THE HERO MOMENT)]**

> "Now here's the magic. Instead of keyword searching or complex filters, I can search in natural language."

- Click on [Search] page
- Type in search bar: **"Find senior Python developers with AWS and Docker experience, located in San Francisco or willing to relocate, with 5+ years of experience"**
- Hit Enter

**[PAUSE FOR EFFECT — Show real-time results]**

> "Watch what happens..."

- Results appear instantly:
  1. **John Doe** — 95% match 🟢 (All skills, 8 years, SF)
  2. **Jane Smith** — 87% match 🟡 (Python + AWS strong, 5 years, NYC → Remote OK)
  3. **Alex Miller** — 78% match 🟡 (Has Python/AWS/Docker, 10 years, Boston)

> "Our AI understands intent. It's not keyword matching — it's semantic understanding. We converted your English sentence into skill embeddings and searched our vector database. This took 245 milliseconds."

---

**[Demo Step 4: Candidate Profile]**

> "Let me click on John, the top match."

- Click on John's candidate card
- Show full profile:
  - Skills breakdown with experience years
  - Work history timeline
  - Education
  - Contact info
  - Similarity to other candidates
  - Recruiter notes section

> "You get a complete 360-degree view. But here's the thing — John is listed as a potential duplicate with another candidate in the system. Our deduplication algorithm flagged it with 92% confidence."

- Show duplicate warning

> "Our system prevents you from contacting the same person twice."

---

**[Demo Step 5: Candidate Comparison]**

> "Let me compare the top 3 candidates side by side."

- Click [Compare] button (or navigate to compare page)
- Show comparison table:
  - John Doe: 95% match, Python ⭐⭐⭐⭐⭐, AWS ⭐⭐⭐⭐, 8y, $180-220k
  - Jane Smith: 87% match, Python ⭐⭐⭐⭐, AWS ⭐⭐⭐⭐⭐, 5y, $150-200k
  - Alex Miller: 78% match, Python ⭐⭐⭐, AWS ⭐⭐⭐⭐, 10y, $200-250k

> "In one view, you see the strengths and gaps of each candidate. John has the most balanced profile, but Jane has stronger AWS skills. Alex has the most experience but lower match on Python."

---

**[Demo Step 6: Technical Highlight]**

> "Let me show you the architecture. This isn't just a search app — it's a production-grade SaaS platform."

- Show architecture diagram on screen:
  - Frontend: React + TypeScript (semantic search, responsive)
  - Backend: FastAPI (async, high-performance)
  - AI Pipeline: OpenAI embeddings + spaCy NLP
  - Vector DB: Pinecone (1.5M-dimensional semantic search)
  - Data: PostgreSQL (ACID compliance)
  - Integrations: Gmail OAuth, HRMS simulation

> "Every component scales independently. The search endpoint handles 10K+ queries/day. We use Pinecone for vector search (no GPU overhead) and PostgreSQL for relational data. This is built for growth."

---

**[Demo Step 7: Speed & Polish]**

> "And it's fast. Let me run another search:"

- Type: "React engineers in New York"
- Show results in < 500ms
- Smooth animations, no lag

> "You'll notice there are no loading spinners, no lag. This is production-quality UX."

---

## 12.2 Key Talking Points

1. **"Natural Language Search"** — Judges love AI. Emphasize semantic understanding, not keyword matching.
2. **"Automated Resume Parsing"** — Saves hours per week. Mention accuracy rate (94%+).
3. **"Email Integration"** — Real Gmail OAuth, not faked. Show the auth flow.
4. **"Deduplication"** — Prevents duplicates using embeddings. Smart, not brute-force.
5. **"Scalable Architecture"** — PostgreSQL + Pinecone + FastAPI + React. Production-ready.
6. **"Multi-Source Data"** — Email, upload, HRMS simulation, LinkedIn simulation. Unified platform.
7. **"Built in 48 Hours"** — Emphasize speed & efficiency of team.

---

## 12.3 Demo Script (Write to DOCS/DEMO_SCRIPT.md)

```markdown
# TalentUnify Demo Script (5 minutes)

## Opening (30 seconds)
"Hi! We're TalentUnify. This is an AI-powered recruitment platform that solves a real problem: 
recruitment is broken. Recruiters are drowning in resumes from email, LinkedIn, HRMS systems. 
We aggregate all sources and let you find candidates in seconds using natural language."

## Demo Flow
1. [Show login] "Let's say I'm a recruiter."
2. [Show dashboard] "Here's my dashboard — 150 candidates, multiple sources."
3. [Upload resume] "I'll upload a candidate's resume. Behind the scenes, AI extracts structured data."
4. [Show parsed data] "Name, email, skills, experience — all automatic."
5. [Connect Gmail] "I'll connect Gmail to ingest all candidate resumes from email."
6. [Natural language search] "Now, the magic. I search in English: 'Senior Python developers with AWS, San Francisco'..."
7. [Show results] "Instant results, ranked by AI relevance. 95% match, 87% match, 78% match."
8. [Click candidate] "Full profile — work history, skills, education, similarity scoring."
9. [Compare] "I can compare 3 candidates side-by-side to make better decisions."
10. [Show architecture] "Under the hood: React frontend, FastAPI backend, OpenAI embeddings, Pinecone vector DB."

## Closing (30 seconds)
"This is production-grade SaaS built in 48 hours by 4 engineers. We're ready to scale."

## Backup: If internet fails
- Have a recorded demo video
- Have screenshots of all flows
- Have a local instance running
```

---

# SECTION 13: VIRAL/JUDGE-WINNING FEATURES

## Advanced Features That Impress (Tier 2+)

### Feature 1: Candidate Similarity Graph

**What:** Visual network showing related candidates

**Why Judges Love It:** 
- Novel visualization
- Shows AI sophistication
- Useful for recruitment (find similar candidates)

**Implementation (Optional):**
```javascript
// Frontend: React + D3.js or Vis.js
import { Network } from 'vis-network';

const nodes = candidates.map(c => ({ id: c.id, label: c.name }));
const edges = similarities.map(s => ({
  from: s.candidate1_id,
  to: s.candidate2_id,
  value: s.similarity_score  // Line thickness
}));

const network = new Network(container, { nodes, edges });
```

---

### Feature 2: Skill Heatmap

**What:** Visualization of skill distribution across candidates

**Why Judges Love It:**
- Data visualization + AI
- Shows market trends
- Actionable insights

**Implementation:**
```javascript
// Recharts heatmap
const skillHeatData = [
  { skill: "Python", junior: 10, mid: 20, senior: 15 },
  { skill: "AWS", junior: 5, mid: 18, senior: 22 },
  { skill: "React", junior: 25, mid: 30, senior: 5 }
];

<BarChart data={skillHeatData}.../>
```

---

### Feature 3: Hiring Analytics Dashboard

**What:** Metrics like time-to-hire, conversion rates, source attribution

**Why Judges Love It:**
- Shows product thinking
- Analytics for recruiters = ROI
- Measurable business value

**Metrics to Track:**
- Time-to-hire (days from application to offer)
- Conversion rate (applications → interviews → offers)
- Cost-per-hire by source (Gmail vs upload vs HRMS)
- Candidate quality (ratings distribution)
- Skill demand (top 10 skills)

---

### Feature 4: AI Recruiter Copilot (Chat Interface)

**What:** Chat interface with AI suggesting next steps

**Why Judges Love It:**
- Cutting-edge (LLMs)
- Shows AI sophistication
- "Copilot" is hot in tech

**Implementation:**
```python
# Backend: Use OpenAI chat API
from openai import OpenAI

client = OpenAI()

def get_recruiter_suggestion(candidate_id: str, context: str):
    candidate = db.get_candidate(candidate_id)
    
    prompt = f"""
    You are a recruitment advisor. 
    Candidate: {candidate.name}
    Skills: {', '.join(candidate.skills)}
    Experience: {candidate.years_experience} years
    
    Context: {context}
    
    What should this recruiter do next? (1-2 sentences)
    """
    
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.choices[0].message.content
```

---

### Feature 5: Resume Scoring & Feedback

**What:** AI rates resumes and suggests improvements

**Why Judges Love It:**
- B2B SaaS (recruiters use it)
- Adds value (helps candidates)
- Shows ML sophistication

---

## Features to Avoid (Waste of Time in Hackathon)

❌ Mobile app (focus on web)  
❌ Video interviews (overkill)  
❌ Calendar integration (too complex)  
❌ Offer letter generation (not differentiating)  
❌ Background checks (requires third-party)  

---

# SECTION 14: GITHUB REPO + CI/CD SETUP

## 14.1 Repository Structure

```
talent-unify/
├── .github/
│   ├── workflows/
│   │   ├── ci-backend.yml          ← GitHub Actions for backend tests
│   │   ├── ci-frontend.yml         ← GitHub Actions for frontend tests
│   │   ├── deploy-staging.yml      ← Deploy to staging environment
│   │   └── deploy-production.yml   ← Deploy to production
│   └── ISSUE_TEMPLATE/
│       ├── bug_report.md
│       └── feature_request.md
├── .gitignore                       ← Exclude .env, node_modules, __pycache__
├── .pre-commit-config.yaml         ← Auto-format on commit
├── docker-compose.yml              ← Local dev environment
├── LICENSE                         ← MIT license
└── README.md
```

## 14.2 Branch Strategy

```
main (production)
  ↑ (only merge after all tests pass)
  |
  └─ develop (integration branch)
      ↑
      ├─ feature/dashboard (Engineer 1)
      ├─ feature/api-candidates (Engineer 2)
      ├─ feature/embeddings (Engineer 3)
      └─ feature/gmail-oauth (Engineer 4)
```

**Rules:**
- `main`: Production-ready code only. Requires PR review + all tests passing.
- `develop`: Integration branch. PRs auto-merge after CI passes.
- `feature/*`: Individual engineer branches. Rebase before merge.

---

## 14.3 CI Pipeline (GitHub Actions)

### ci-backend.yml
```yaml
name: Backend CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install -r backend/requirements.txt
          pip install -r backend/requirements-dev.txt
      
      - name: Lint (pylint)
        run: pylint backend/app --fail-under=8.0
      
      - name: Format check (black)
        run: black backend/ --check
      
      - name: Type check (mypy)
        run: mypy backend/app
      
      - name: Run tests (pytest)
        run: pytest backend/tests -v --cov=backend/app
        env:
          DATABASE_URL: postgresql://postgres:postgres@localhost:5432/test_db
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

### ci-frontend.yml
```yaml
name: Frontend CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Node
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          cache: 'npm'
          cache-dependency-path: 'frontend/package-lock.json'
      
      - name: Install dependencies
        run: cd frontend && npm ci
      
      - name: Lint (ESLint)
        run: cd frontend && npm run lint
      
      - name: Format check (prettier)
        run: cd frontend && npm run format:check
      
      - name: Type check (tsc)
        run: cd frontend && npm run type-check
      
      - name: Build
        run: cd frontend && npm run build
      
      - name: Unit tests (vitest)
        run: cd frontend && npm run test
```

---

## 14.4 Deployment Pipeline

### deploy-staging.yml
```yaml
name: Deploy to Staging

on:
  push:
    branches: [develop]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Deploy backend to Railway
        uses: railway-app/deploy-action@v1
        with:
          service: backend
          token: ${{ secrets.RAILWAY_TOKEN }}
          environment: staging
      
      - name: Deploy frontend to Vercel
        uses: amondnet/vercel-action@v20
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          github-token: ${{ secrets.GITHUB_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
          scope: ${{ secrets.VERCEL_ORG_ID }}
          working-directory: ./frontend
      
      - name: Smoke test
        run: |
          curl https://staging-api.talentunify.io/health
          curl https://staging.talentunify.io/
```

---

## 14.5 Pre-Commit Hooks

### .pre-commit-config.yaml
```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
        args: ['--maxkb=500']
  
  - repo: https://github.com/psf/black
    rev: 23.1.0
    hooks:
      - id: black
        language_version: python3.11
  
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.0
    hooks:
      - id: ruff
```

---

## 14.6 Environment Secrets (GitHub Secrets)

```bash
# Backend
DATABASE_URL = postgresql://user:pass@localhost/db
REDIS_URL = redis://localhost:6379
OPENAI_API_KEY = sk-...
PINECONE_API_KEY = ...
GOOGLE_CLIENT_ID = ...
GOOGLE_CLIENT_SECRET = ...
SECRET_KEY = random-secret-key-here

# DevOps
RAILWAY_TOKEN = ...
VERCEL_TOKEN = ...
VERCEL_ORG_ID = ...
VERCEL_PROJECT_ID = ...
```

---

# SECTION 15: FINAL DELIVERABLES CHECKLIST

By end of hackathon, ensure:

## Code Quality
- [ ] All TypeScript files: 0 errors, 0 warnings
- [ ] All Python files: pylint score > 8.0
- [ ] All tests passing (backend: pytest, frontend: vitest)
- [ ] 70%+ code coverage on critical paths
- [ ] No hardcoded secrets in code
- [ ] `.env.example` has all needed vars

## Features Completed (Tier 1)
- [x] Resume upload & parsing
- [x] Candidate database
- [x] Natural language search
- [x] Recruiter dashboard
- [x] Gmail integration (OAuth)

## UI/UX
- [ ] Dashboard fully functional
- [ ] Search page responsive
- [ ] Candidate profile polished
- [ ] Mobile responsive (at least 80% same as desktop)
- [ ] No console errors
- [ ] Keyboard navigation working
- [ ] Accessibility score > 85 (Lighthouse)

## Performance
- [ ] Search latency < 2 seconds
- [ ] Page loads < 3 seconds
- [ ] Resume parsing < 10 seconds (async is OK)
- [ ] Lighthouse score > 80

## Documentation
- [ ] README.md with quick start
- [ ] ARCHITECTURE.md (complete)
- [ ] API.md with all endpoints
- [ ] DEMO_SCRIPT.md with exact steps
- [ ] DEPLOYMENT.md with deploy instructions
- [ ] Inline code comments for complex logic

## Deployment
- [ ] Backend deployed to Railway/Render
- [ ] Frontend deployed to Vercel
- [ ] Database accessible from production
- [ ] Pinecone index configured
- [ ] Production `.env` variables set
- [ ] Health check endpoint working (/health)
- [ ] Error logging enabled (Sentry or similar)

## Presentation
- [ ] 5-minute demo script written
- [ ] Architecture diagram prepared (print + digital)
- [ ] GitHub repo link ready
- [ ] Live demo link ready
- [ ] Backup local demo ready
- [ ] Team talking points prepared

---

# FINAL NOTES FOR TEAM

## Time Management
- Don't aim for perfection—aim for shipping
- Tier 1 features > polished Tier 2 features
- Demo works > everything else matters

## Common Pitfalls to Avoid
❌ Over-engineering database schema  
❌ Building perfect UI before functionality works  
❌ Trying to integrate real LinkedIn API (use simulation)  
❌ Over-scoping HRMS integrations (mock it)  
❌ Perfectionist testing (aim for 70% coverage, not 100%)  
❌ Spending time on deployment too early (do it on Hour 42)  

## Pro Tips
✅ Use mock data aggressively (don't wait for real integrations)  
✅ Pair program on bottlenecks (e.g., embedding generation)  
✅ Test demo flow constantly (every 6 hours)  
✅ Have a "judge-ready" version by Hour 40  
✅ Screenshot everything for slides  
✅ Write demo script early (helps clarify feature priority)  

---

# EPILOGUE: AFTER THE HACKATHON

**If you win/advance:**
- Refactor code (remove hacks)
- Add comprehensive tests
- Setup CI/CD properly
- Write proper documentation
- Build roadmap for Series A features

**Key metrics to measure for investor pitch:**
- Time-to-hire improvement (50% faster than alternatives)
- Cost-per-hire reduction (save $2K-5K per hire)
- Candidate time-to-fill (down to days, not weeks)
- AI accuracy (resume parsing 94%+, dedup 92%+)
- User satisfaction (4.5+ stars on demo)

**6-month roadmap:**
- [ ] Advanced HRMS integrations (Workday, ADP)
- [ ] Real LinkedIn API integration
- [ ] Candidate communication portal
- [ ] Interview scheduling
- [ ] Offer letter generation
- [ ] Team collaboration features
- [ ] Mobile app
- [ ] Advanced analytics & reporting
- [ ] Integrations marketplace (Slack, Teams, etc.)
- [ ] Custom ML models for better ranking

---

**END OF SPECIFICATION**

**Version:** 1.0  
**Last Updated:** January 2024  
**Status:** Ready for Hackathon Execution
