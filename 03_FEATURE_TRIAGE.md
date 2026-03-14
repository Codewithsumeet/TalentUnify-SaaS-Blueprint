# 03 — FEATURE PRIORITIZATION & SCOPE
## What to Build, What to Skip, and Why

---

> [!CAUTION]
> **Scope is the #1 killer of hackathon projects.** The original prompt estimated 400+ hours of work for a 192-hour team capacity (4 × 48h). This triage brings it down to a realistic ~140 hours across Tier 1 + 1 optional Tier 2 feature.

---

## 🔴 TIER 1 — Must Ship (Demo-Critical)

**Deadline: Hour 36 | Total Effort: ~36h across 4 engineers**

These 5 features define the demo. No compromises, no half-implementations.

### 1. Resume Upload & Parsing (8h)
- Upload `.pdf` / `.docx` resumes via drag-and-drop UI
- AI extracts: name, email, phone, skills, work experience, education
- Store parsed data in PostgreSQL
- Show extraction confidence score on UI
- **Acceptance Criteria:** Upload a PDF → see parsed candidate profile in < 10 seconds

### 2. Candidate Database (4h)
- Store all candidates with structured data
- CRUD operations (create, read, update, list)
- Paginated candidate list with search/filter
- **Acceptance Criteria:** View list of 100+ candidates with filters working

### 3. Natural Language Candidate Search (10h)
- Search bar accepting English queries: *"Find Python developers with 5+ years in SF"*
- AI converts query to semantic embedding → searches Pinecone vector DB
- Returns ranked candidates with match percentage + explanation
- Results in < 2 seconds
- **Acceptance Criteria:** Type a natural language query → get semantically relevant ranked results

### 4. Recruiter Dashboard (8h)
- Dashboard with stats: total candidates, sources, recent activity
- Navigation: Dashboard, Search, Candidates, Integrations
- Candidate cards with key info (name, skills, source)
- Quick actions: Upload Resume, Connect Gmail
- **Acceptance Criteria:** Dashboard loads with real data, no console errors

### 5. Gmail Integration via OAuth (6h)
- "Connect Gmail" button → OAuth2 popup
- Fetch emails with resume attachments from labeled folder
- Auto-parse resumes and add to candidate DB
- Show sync status (connected, last sync, candidates imported)
- **Acceptance Criteria:** Connect Gmail → auto-import 5+ resumes → see new candidates in DB

---

## 🟡 TIER 2 — Judge-Wow Features (If Time Permits)

**Window: Hours 36-42 | Pick only 1-2 features maximum**

### Option A: Candidate Deduplication (4h) ⭐ Recommended
- Detect duplicate candidates using email match + embedding similarity
- Flag duplicates with confidence score
- Merge duplicate profiles
- **Why pick this:** Demonstrates AI sophistication with minimal UI work

### Option B: Candidate Comparison (6h)
- Select 2-3 candidates → side-by-side comparison view
- Skill comparison table, experience timeline
- **Why pick this:** Visually impressive for demo, clear judge-appeal

### Option C: Candidate Ranking/Scoring (4h)
- AI ranks candidates for a specific job description
- Weighted scoring: 30% skills, 25% experience, 20% location, 15% education, 10% recency
- Explainable scores
- **Why pick this:** Shows AI depth, useful feature

### Option D: Pipeline/Kanban Board (6h)
- Status tracking: Applied → Screening → Interview → Offer → Hired
- Drag-and-drop kanban board
- **Why skip this:** High UI effort for moderate demo impact

### Option E: Analytics Dashboard (6h)
- Hiring metrics, skill heatmaps, source attribution charts
- **Why skip this:** Charts don't demo as well as AI features

---

## 🔵 TIER 3 — Post-Hackathon Roadmap

**DO NOT build any of these during the hackathon.** Mention as "future work" in the pitch.

| Feature | Estimated Effort | Why Deferred |
|---------|-----------------|-------------|
| HRMS API integration (Workday, ADP, BambooHR) | 20h | Each API is different, enterprise-only |
| Real LinkedIn API | 15h | Requires business account ($0-5K/month) |
| Outlook email integration | 8h | OAuth completely different from Gmail |
| Advanced ML ranking models | 12h | Requires training data |
| Bulk CSV import | 4h | Low demo impact |
| Interview scheduling | 10h | Requires calendar API |
| Offer letter generation | 6h | Not differentiating |
| Team collaboration | 8h | Multi-user is complex |
| Mobile app | 40h | Completely different codebase |
| Candidate communication portal | 12h | Requires email/SMS integration |

---

## ⚖️ Scope Decision Framework

When deciding whether to add a feature, ask:

```
1. Does it demo well in < 30 seconds?     → Yes → Consider it
2. Can it be built in < 4 hours?           → Yes → Consider it
3. Does it show AI/ML sophistication?      → Yes → Higher priority
4. Is it visible during the 5-min demo?    → No  → Skip it
5. Does it require external API access?    → Yes → Mock it or skip it
```

---

## 🧩 Feature Dependencies

```
Resume Upload + Parsing ────────┐
                                ├── Candidate Database ──── Dashboard
Gmail Integration ──────────────┘        │
                                         │
                              Natural Language Search
                                         │
                            ┌────────────┤
                            │            │
                     Deduplication   Comparison
                       (Tier 2)      (Tier 2)
```

**Critical path:** Resume Parsing → Database → Search → Demo-ready

---

## 🚫 What We Explicitly Do NOT Build

- ❌ Full ATS (applicant tracking system) — too broad
- ❌ Video interviews — overkill for hackathon
- ❌ Calendar integration — complex third-party API
- ❌ Background checks — requires third-party service
- ❌ Offer letters — not differentiating
- ❌ Real LinkedIn integration — enterprise-only API
- ❌ Multi-language support — English only for MVP

---

## 🔗 Cross-References
- **How to build each feature:** → [04_AI_AND_NLP_PIPELINE.md](./04_AI_AND_NLP_PIPELINE.md) (AI features), [05_DATABASE_AND_API.md](./05_DATABASE_AND_API.md) (backend), [06_FRONTEND_AND_UX.md](./06_FRONTEND_AND_UX.md) (UI)
- **Timeline per feature:** → [08_DEVELOPMENT_TIMELINE.md](./08_DEVELOPMENT_TIMELINE.md)
- **What to demo:** → [10_DEMO_AND_PRESENTATION.md](./10_DEMO_AND_PRESENTATION.md)

---

*Source: ERROR_ANALYSIS_AND_CORRECTIONS.md (Error #4), REFINED_CTO_BLUEPRINT_PROMPT.md (Section 2-3), QUICK_REFERENCE_INDEX.md*
