# 05 — DATABASE SCHEMA & API DESIGN
## PostgreSQL Schema, Pinecone Index & Complete API Reference

---

## 🗄️ Entity Relationship Diagram

```
┌─────────────────┐
│     Users       │
│─────────────────│
│ id (PK, UUID)   │
│ email (UNIQUE)  │
│ password_hash   │
│ full_name       │
│ created_at      │
└────────┬────────┘
         │ 1:N
┌────────▼────────────────┐
│     Recruiters          │
│─────────────────────────│
│ id (PK, UUID)           │
│ user_id (FK → Users)    │
│ company_name            │
│ team_id                 │
│ created_at              │
└────────┬────────────────┘
         │ 1:N
┌────────▼────────────────────────┐       ┌────────────────────────┐
│     Candidates                  │       │    Skills              │
│─────────────────────────────────│       │────────────────────────│
│ id (PK, UUID)                   │       │ id (PK)                │
│ recruiter_id (FK → Recruiters)  │  N:M  │ skill_name             │
│ name                            │◄─────►│ category               │
│ email                           │       │ taxonomy_id            │
│ phone                           │       └────────────────────────┘
│ location                        │              ↕ (via CandidateSkills)
│ status                          │       ┌────────────────────────┐
│ source (email/upload/linkedin)  │       │  CandidateSkills       │
│ embedding_id → Pinecone         │       │────────────────────────│
│ created_at                      │       │ candidate_id (FK)      │
└────────┬────────────────────────┘       │ skill_id (FK)          │
         │ 1:N                            │ proficiency_level      │
┌────────▼──────────────────┐             │ years_of_experience    │
│     Resumes               │             └────────────────────────┘
│───────────────────────────│
│ id (PK, UUID)             │     ┌─────────────────────────────┐
│ candidate_id (FK)         │     │  IntegrationTokens          │
│ file_path                 │     │─────────────────────────────│
│ raw_text                  │     │ id (PK, UUID)               │
│ parsed_json (JSONB)       │     │ recruiter_id (FK)           │
│ version                   │     │ integration_type (gmail...) │
│ created_at                │     │ access_token (encrypted)    │
└───────────────────────────┘     │ refresh_token               │
                                  │ expires_at                  │
┌───────────────────────────┐     └─────────────────────────────┘
│  Applications             │
│───────────────────────────│     ┌─────────────────────────────┐
│ id (PK, UUID)             │     │  ActivityLogs               │
│ recruiter_id (FK)         │     │─────────────────────────────│
│ candidate_id (FK)         │     │ id (PK, UUID)               │
│ job_id                    │     │ recruiter_id (FK)           │
│ status                    │     │ action_type                 │
│ rating (1-5)              │     │ entity_id                   │
│ notes                     │     │ metadata_json               │
│ created_at                │     │ created_at                  │
└───────────────────────────┘     └─────────────────────────────┘
```

---

## 📐 SQL Schema

```sql
-- Core Tables
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE recruiters (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id),
    company_name VARCHAR(255),
    team_id VARCHAR(100),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE candidates (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    recruiter_id UUID NOT NULL REFERENCES recruiters(id),
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    phone VARCHAR(50),
    location VARCHAR(255),
    status VARCHAR(50) DEFAULT 'applied',  -- applied/screened/interviewed/offered/hired
    source VARCHAR(50),                     -- email/upload/linkedin/hrms
    embedding_id VARCHAR(255),              -- References Pinecone vector
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE resumes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    candidate_id UUID NOT NULL REFERENCES candidates(id),
    file_path VARCHAR(500),
    raw_text TEXT,
    parsed_json JSONB,
    version INT DEFAULT 1,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE skills (
    id SERIAL PRIMARY KEY,
    skill_name VARCHAR(100) UNIQUE NOT NULL,
    category VARCHAR(50)   -- language/framework/cloud/database/tool
);

CREATE TABLE candidate_skills (
    candidate_id UUID REFERENCES candidates(id),
    skill_id INT REFERENCES skills(id),
    proficiency_level VARCHAR(20),  -- beginner/intermediate/advanced/expert
    years_of_experience FLOAT,
    PRIMARY KEY (candidate_id, skill_id)
);

CREATE TABLE integration_tokens (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    recruiter_id UUID NOT NULL REFERENCES recruiters(id),
    integration_type VARCHAR(50) NOT NULL,  -- gmail/outlook/hrms
    access_token TEXT NOT NULL,
    refresh_token TEXT,
    expires_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX idx_candidates_recruiter ON candidates(recruiter_id);
CREATE INDEX idx_candidates_email ON candidates(email);
CREATE INDEX idx_candidates_status ON candidates(status);
CREATE INDEX idx_candidates_created ON candidates(created_at DESC);
CREATE INDEX idx_candidate_skills_cid ON candidate_skills(candidate_id);
CREATE INDEX idx_resumes_text_search ON resumes USING GIN(to_tsvector('english', raw_text));
```

---

## 🌐 API Endpoint Reference

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/auth/register` | Register new recruiter |
| `POST` | `/auth/login` | Login with email/password → JWT |
| `POST` | `/auth/refresh` | Refresh JWT token |

**All subsequent endpoints require `Authorization: Bearer <JWT>` header.**

---

### Resume Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/resume/upload` | Upload & parse resume (multipart/form-data) |
| `POST` | `/resume/parse` | Parse raw text (for email attachments) |
| `GET` | `/resume/:id` | Fetch parsed resume details |

**Upload Response Example:**
```json
{
    "resume_id": "uuid-5678",
    "candidate_id": "uuid-1234",
    "parsed_data": {
        "name": "John Doe",
        "email": "john@example.com",
        "skills": ["Python", "AWS", "Docker"],
        "experience": [
            {"title": "Senior Engineer", "company": "Google", "start_date": "2020-01-01"}
        ]
    },
    "extraction_confidence": 0.94,
    "duplicates_found": ["uuid-9999"]
}
```

---

### Candidate Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/candidate` | List all candidates (paginated) |
| `GET` | `/candidate/:id` | Fetch detailed candidate profile |
| `PUT` | `/candidate/:id` | Update candidate (status, notes, rating) |
| `POST` | `/candidate/deduplicate` | Find duplicate candidates |
| `POST` | `/candidate/merge` | Merge duplicate profiles |

**List Query Parameters:** `?page=1&limit=20&sort=created_at&order=desc&status=applied`

---

### Search Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/search` | Natural language semantic search |
| `GET` | `/search/history` | Fetch past searches |
| `POST` | `/search/save` | Save a search query |

**Search Request:**
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

**Search Response:**
```json
{
    "results": [
        {
            "rank": 1,
            "candidate_id": "uuid-1234",
            "name": "John Doe",
            "match_score": 0.95,
            "match_explanation": "Expert Python (8y), Advanced AWS (6y), in SF"
        }
    ],
    "total_results": 12,
    "search_time_ms": 245
}
```

---

### Integration Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/integration/gmail/connect` | Initiate Gmail OAuth → returns auth URL |
| `POST` | `/integration/gmail/callback` | Handle OAuth callback |
| `GET` | `/integration/gmail/status` | Connection status |
| `POST` | `/integration/gmail/sync` | Manual sync trigger |
| `DELETE` | `/integration/gmail` | Disconnect Gmail |

---

### Authentication Model

```python
# All endpoints use JWT + OAuth2
# Header: Authorization: Bearer eyJhbGciOiJIUzI1NiIs...

# FastAPI dependency:
async def get_current_recruiter(token: str = Depends(oauth2_scheme)):
    recruiter = verify_jwt_token(token)
    if not recruiter:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return recruiter

# File upload security:
# - Max file size: 25MB
# - Allowed types: .pdf, .docx
# - JWT token required
```

---

## ⚡ Performance Targets

| Metric | Target |
|--------|--------|
| Search latency | < 2 seconds |
| API response time | < 500ms |
| Page load time | < 3 seconds |
| Resume parsing | < 10 seconds (async OK) |
| Lighthouse score | > 80 |

---

## 🔗 Cross-References
- **How AI processes these requests:** → [04_AI_AND_NLP_PIPELINE.md](./04_AI_AND_NLP_PIPELINE.md)
- **Frontend that consumes these APIs:** → [06_FRONTEND_AND_UX.md](./06_FRONTEND_AND_UX.md)
- **Backend file structure:** → [07_PROJECT_STRUCTURE_AND_OWNERSHIP.md](./07_PROJECT_STRUCTURE_AND_OWNERSHIP.md)

---

*Source: REFINED_CTO_BLUEPRINT_PROMPT.md (Sections 6, 10), ERROR_ANALYSIS (Errors #6, #7)*
