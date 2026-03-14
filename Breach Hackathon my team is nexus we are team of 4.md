<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# Breach Hackathon my team is nexus we are team of 4 we have github student dev pack give us proper documenation and methology frameswork to build this to its finest

Here’s a full methodology and documentation framework tailored for Team Nexus to build the Unified AI-Powered Recruitment Platform for the Breach Hackathon, plus how to leverage your GitHub Student Developer Pack along the way.[^1][^2][^3]

## 1. Overall game plan

- Build a clean **end-to-end slice**: ingest → parse → dedup → semantic search → recruiter UI, even if each block is slightly simplified.[^1]
- Optimize for **demo-ability and clarity of story** more than raw feature count: judges should “get it” in 2 minutes.
- Use **Student Pack infra** so you can have a live URL and not just “runs on localhost.”[^2][^3]

A good team split (4 people):

- Dev 1: Backend + integrations (email, HRMS/LinkedIn simulation).
- Dev 2: NLP/resume parsing + dedup + embeddings.
- Dev 3: Frontend UX and search experience.
- Dev 4: DevOps + documentation + pitch + glue work.

***

## 2. Architecture you should aim for

### Core components

- **Ingestion layer**
    - Resume upload API (file upload).
    - Email connector (Gmail/Outlook API) for resumes in a specific label/folder.[^1]
    - HRMS/LinkedIn simulator: CSV/JSON upload that pretends to be an HRMS or LinkedIn integration.[^1]
- **Processing \& NLP**
    - Text extraction from PDF/DOCX.
    - Resume parsing (experience, skills, location).
    - Skill normalization and experience summarization.
    - Dedup logic to unify multiple sources into one candidate.[^1]
- **Search \& ranking**
    - Embedding generation for each candidate profile.
    - Vector similarity + filters (location, years of experience, skills).[^1]
- **Backend API**
    - CRUD for candidates.
    - `/search` with natural-language query and filters.
    - Endpoints to configure integrations (e.g., connect inbox, upload HRMS dump).
- **Frontend**
    - Dashboard, candidate list, candidate profile view.
    - Search bar with NL queries.
    - Shortlist / pipeline board.[^1]
- **Storage**
    - Main DB (PostgreSQL or MongoDB Atlas).[^4][^3]
    - Vector index (pgvector or embeddings table).
- **Infra**
    - Repo on GitHub, CI with GitHub Actions, deployment to Azure/DigitalOcean via Student Pack.[^5][^3][^6][^2]

***

## 3. Suggested tech choices (hackathon-friendly)

- **Frontend**: React or Next.js for fast DX and good ecosystem.
- **Backend**:
    - Option A: Node.js + Express/NestJS.
    - Option B: Python + FastAPI.
- **Database**:
    - If you like documents: MongoDB Atlas (you get credits with the Student Pack).[^3][^4]
    - If you like relational: PostgreSQL (and pgvector for embeddings).
- **NLP / LLM**:
    - Hosted embedding API (for semantic search).
    - Ready-made resume parsing libs or a simple “LLM-assisted parsing” prompt.
- **Hosting using Student Pack**:
    - Backend + DB: Azure/DigitalOcean credits from the GitHub Student Developer Pack.[^6][^2][^5][^3]
    - Frontend: GitHub Pages / static host from the Pack.[^2][^3]
    - Tooling: JetBrains IDEs, design tools, etc., from the Pack.[^7][^8][^9][^3]

***

## 4. Phase-wise methodology (you can map this to a 24–48h timeline)

### Phase 1 – Clarify scope \& stories (2–3 hours)

Lock these **high-priority user stories** (and put them in your PRD):

- Upload a resume → see a parsed candidate profile.
- Connect email label/folder → auto-ingest resumes from new emails.
- Import HRMS/LinkedIn-like CSV → candidates show up unified with existing ones.[^1]
- Search with a natural-language query → relevant candidates with explanation of why they matched.[^1]
- View a single candidate profile aggregated from many sources; shortlist them and change their stage.

Explicitly **de-scope** things like full ATS, interview scheduling, offer letters. Mention them only as “future work.”

***

### Phase 2 – Data model \& dedup design (2–3 hours)

Design a simple schema first (even on a whiteboard), then codify it:

- `Candidate`
    - id
    - name
    - emails []
    - phones []
    - location
    - current_title
    - total_experience_years
    - skills [] (normalized)
    - sources [] (list of source records)
    - embedding (vector)
- `SourceRecord`
    - source_type (EMAIL, HRMS, LINKEDIN, UPLOAD, REFERRAL)
    - source_id (e.g., email message-id, HRMS ID)
    - raw_resume_path
    - parsed_at
- `ExperienceItem`
    - company, title, start_date, end_date
- `Skill`
    - name_normalized
    - confidence, maybe level

**Dedup strategy**:

- Primary: normalized email address.
- Secondary: name + phone OR name + high similarity of parsed profile text.
- When you detect duplicate:
    - Merge skills (union).
    - Merge contacts (union).
    - Add to `sources[]` list.
    - Prefer newest data when conflicts.

Keep this design in a **System Design Doc**.

***

### Phase 3 – Ingestion connectors (4–6 hours)

Build **three ingestion paths** end-to-end:

1. **Resume upload**
    - Simple `POST /upload` with a form in frontend.
    - Backend saves file, invokes parser, writes candidate.
2. **Email (Gmail/Outlook)**
    - Choose one provider; set up OAuth/scopes only for a labeled folder (e.g., “Candidates”).[^1]
    - A scheduled job or manual “Sync now” button:
        - Reads that folder, downloads attachments, passes them into the same parsing pipeline.
3. **HRMS / LinkedIn simulation**
    - Prepare a sample CSV/JSON of candidates (HRMS export / fake LinkedIn profiles).
    - UI button: “Import from HRMS/LinkedIn”.
    - Backend reads file, maps fields to internal schema, runs through dedup and save.

Document integration details in an **Integrations Spec** (endpoints, data formats, example payloads).

***

### Phase 4 – Parsing \& NLP (4–6 hours)

Pipeline:

1. **Extract text**:
    - Use libraries/services to get plain text from PDF/DOCX.
2. **Segment content**:
    - Split into sections: Experience, Education, Skills.
3. **Entity extraction**:
    - Skills: fuzzy match against a curated list of 100–200 skills (React, Node, SQL, AWS, etc.).
    - Experience: simple regex or LLM to pull company, role, date ranges.
    - Location: search for city/country patterns.

Focus on **good-enough heuristics**; aim for robust demos over perfect parsing.

Write an **AI/NLP Design Note** with:

- Which models/APIs you used and why.
- How you build the candidate text used for embeddings.
- Known limitations and “future improvements” sections.

***

### Phase 5 – Semantic search (4–6 hours)

1. **Indexing**
    - For each candidate, build a text summary like:
`\"Senior React developer with 5 years experience at fintech companies in Bangalore, skills: React, Node, AWS, PostgreSQL\"`
    - Generate embedding vector and store it against the candidate record.
2. **Query handling**
    - Take recruiter query string, embed it, run vector similarity search.
    - Filter results with:
        - Must-have skills (if they appear explicitly).
        - Location constraints.
        - Minimum years of experience.
3. **Ranking \& explanation**
    - Primary sort by similarity score.
    - Show “Why this matched” on the UI:
        - Highlight overlapping skills.
        - Show matching location / experience.

Describe all of this under “Search \& Ranking” in your System Design Doc.

***

### Phase 6 – Frontend UX (4–6 hours)

Build **four main screens**:

1. **Dashboard**
    - Total candidates, number of sources, last sync status.
2. **Candidate list**
    - Table/cards: name, title, location, key skills, sources count.
    - Filters on the side (skills, location, experience).
3. **Candidate profile**
    - Aggregated info: parsed resume text, skill chips, experience timeline.
    - “Sources” section listing email/HRMS/LinkedIn upload details.
    - Actions: shortlist, add note, move stage.
4. **Search page**
    - Prominent natural-language search bar.
    - Results list with “why matched” explanations.

Use design tools from the Student Pack (e.g., Canva/Figma) to sketch quick mockups and also to create nice slides for the final pitch.[^7][^3]

***

### Phase 7 – Testing, demo data, and story (3–4 hours)

- Create a **demo dataset**:
    - Same candidate appears via email + HRMS + LinkedIn → shows off dedup.
    - Multiple roles (backend, frontend, data) across locations.
- Define **demo script**:
    - Start with “before” pain (multiple systems, spreadsheets).[^1]
    - Connect an inbox / import HRMS.
    - Show candidate profiles auto-appearing, deduplicated.
    - Run 2–3 natural-language searches and explain why the results make sense.
    - Shortlist a candidate and move them through stages.

Have this written out; one teammate should rehearse this fully.

***

## 5. Documentation framework (what you should actually write)

### A. Product Requirements Document (PRD)

Sections:

- Problem \& context – 1 page summarizing the hackathon brief and pain points.[^1]
- Goals – unified candidate DB, semantic search, dedup, reduced manual work, better time-to-hire.[^1]
- User personas – recruiter, HR lead, agency recruiter, high-volume enterprise.[^1]
- User stories – list with priorities and acceptance criteria.
- Non-functional – performance, latency targets for search, basic security.
- Success metrics – at least qualitative metrics for the hackathon.


### B. System Design Document

Include:

- High-level architecture diagram.
- Component descriptions (ingestion, parsing, dedup, search, UI).
- Data model diagrams (ERD or similar).
- API specs (table of endpoints with brief description \& example JSON).
- Deployment architecture (how GitHub → CI → cloud → running app).


### C. AI/NLP Design Note

Short, focused doc describing:

- Models/APIs used, reasons.
- Parsing strategy (heuristics, prompts).
- Embedding/search strategy.
- Limitations and next steps (multi-language, better skill ontologies, etc.).


### D. Integration Specifications

For each integration:

- Email:
    - Provider, scopes, how you limit access to a label/folder.
    - Polling/webhook strategy.
- HRMS:
    - Example payload structure, mapping to internal schema.
- LinkedIn simulation:
    - CSV/JSON format, mapping rules.


### E. Testing \& Evaluation Plan

- Unit tests: parsing helpers, dedup matcher, search scoring.
- Integration tests: ingestion → parsing → DB → search path.
- Manual evaluation: curated queries + expected top candidates.


### F. README (GitHub)

Your main README should cover:

- What the project does in 4–5 lines.
- Architecture overview diagram.
- Tech stack.
- Setup (local + Docker).
- Deployment steps (how to deploy using your chosen Student Pack cloud credits).
- Screenshots/GIFs of core flows.

***

## 6. Using GitHub Student Developer Pack intelligently

Leverage your pack not just for free stuff, but to **show judges you understand production-style setups**.[^10][^9][^3][^7][^2]

- **Repo \& workflow**
    - Private GitHub Pro repo with clear branching and PR reviews.[^8][^9][^7][^2]
    - GitHub Actions:
        - Run tests on every push.
        - Build \& deploy to cloud on main-branch merges.
- **Cloud hosting**
    - Pick one: Azure or DigitalOcean credits from the Pack.[^5][^3][^6]
    - Host backend + DB there; put URL in README and slides.
- **Database**
    - Use MongoDB Atlas credits from the Pack if you go document-based.[^4]
    - Nice talking point: “We used MongoDB Atlas from the GitHub Student Developer Pack to quickly spin up a secure managed DB.”
- **Tooling**
    - JetBrains IDEs, design tools (Canva/Figma alternatives) to speed up dev and make your final UI and slides polished.[^3][^8][^7]

***

## 7. Pitch narrative for judges

Frame your demo like this (and bake it into your slides):

- **Context**: Hiring is fragmented across emails, HRMS, LinkedIn, and spreadsheets; recruiters waste time in admin rather than talking to people.[^1]
- **Our solution**: A unified AI-powered recruitment workspace that:
    - Aggregates all candidates across channels.
    - Parses and cleans resumes automatically.
    - Deduplicates candidates and keeps a single source of truth.
    - Supports natural-language search (“Senior backend dev in Mumbai with Go and Kubernetes”).[^1]
- **Impact**:
    - Less manual copy-paste.
    - Higher-quality shortlists, faster.
    - Recruiters can focus on candidates, not systems.[^1]

End with **future roadmap** (learning-to-rank, bias checks, full ATS capabilities) so they see you’ve thought beyond the hackathon MVP.

***

If you want, next step I can:

- Draft a concrete PRD template pre-filled for your project, or
- Give you a repo structure (folders + README skeleton + example API spec) tailored to your chosen stack.
<span style="display:none">[^11][^12][^13][^14][^15][^16]</span>

<div align="center">⁂</div>

[^1]: Problem-Statement-1.pdf

[^2]: https://github.com/education/students

[^3]: https://www.geeksforgeeks.org/blogs/what-is-github-student-developer-pack-and-how-to-get-it/

[^4]: https://github.com/github-education-resources/Student-Developer-Pack-Current-Partners-FAQ/blob/main/README.md

[^5]: https://www.mongodb.com/company/blog/news/mongodb-joins-the-github-student-developer-pack

[^6]: https://www.reddit.com/r/github/comments/gxc59v/the_github_student_developer_pack_has_lots_of/

[^7]: https://www.reddit.com/r/webdev/comments/fdfq2s/github_student_developer_pack/

[^8]: https://dev.to/jliter/why-every-college-student-learning-to-code-needs-a-github-student-developer-pack-1nhb

[^9]: https://github.blog/developer-skills/career-growth/get-over-100k-worth-of-tools-with-the-github-student-developer-pack/

[^10]: https://dev.to/pratik_kale/github-student-developer-pack-overview-1jld

[^11]: https://www.linkedin.com/pulse/how-get-1-year-free-n8n-hosting-github-student-pack-digitalocean-m--d6cgf

[^12]: https://www.reddit.com/r/learnprogramming/comments/soemqv/github_student_developer_packimportant_offers_to/

[^13]: https://www.reddit.com/r/learnprogramming/comments/exuh5w/if_youre_a_student_you_should_be_taking_full/

[^14]: https://www.reddit.com/r/developersIndia/comments/1ggh62q/github_student_developer_pack_benefits_and_vps/

[^15]: https://github.com/ShreyamMaity/student-offers

[^16]: https://github.blog/developer-skills/github/over-100-partners-to-help-you-succeed-with-the-github-student-developer-pack/

