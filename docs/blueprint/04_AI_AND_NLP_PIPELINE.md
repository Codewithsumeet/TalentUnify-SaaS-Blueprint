# 04 — AI & NLP PIPELINE DESIGN
## Resume Parsing, Skill Extraction, Embeddings & Semantic Search

---

## 🧠 Pipeline Overview

```
Resume (PDF/DOCX)
    ↓
[1. Text Extraction] ─── pypdf / python-docx
    ↓
[2. NER Processing] ─── spaCy (en_core_web_sm)
    ↓
[3. Skill Extraction] ─── Keyword matching + HuggingFace zero-shot
    ↓
[4. Schema Validation] ─── Pydantic
    ↓
[5. Embedding Generation] ─── OpenAI text-embedding-3-small
    ↓
[6. Storage] ─── PostgreSQL (structured) + Pinecone (vector)
    ↓
[7. Semantic Search] ─── Cosine similarity via Pinecone
```

---

## 1️⃣ Resume Text Extraction

**Libraries:** `pypdf` for PDFs, `python-docx` for DOCX files

```python
from pypdf import PdfReader
from docx import Document

def extract_text(file_path: str) -> str:
    if file_path.endswith('.pdf'):
        reader = PdfReader(file_path)
        return "\n".join(page.extract_text() for page in reader.pages)
    elif file_path.endswith('.docx'):
        doc = Document(file_path)
        return "\n".join(para.text for para in doc.paragraphs)
    else:
        raise ValueError(f"Unsupported file type: {file_path}")
```

**Edge cases to handle:**
- Scanned PDFs (no text layer) → flag and return error message
- Password-protected PDFs → reject with user message
- Malformed DOCX → try-catch with graceful degradation

---

## 2️⃣ Named Entity Recognition (NER)

**Model:** `spaCy en_core_web_sm` (40MB, ~94% accuracy on standard text)

```python
import spacy
import re

nlp = spacy.load("en_core_web_sm")

def extract_entities(text: str) -> dict:
    doc = nlp(text)
    
    entities = {
        "name": None,
        "organizations": [],
        "locations": [],
        "dates": []
    }
    
    for ent in doc.ents:
        if ent.label_ == "PERSON" and not entities["name"]:
            entities["name"] = ent.text
        elif ent.label_ == "ORG":
            entities["organizations"].append(ent.text)
        elif ent.label_ == "GPE":
            entities["locations"].append(ent.text)
        elif ent.label_ == "DATE":
            entities["dates"].append(ent.text)
    
    return entities

def extract_email(text: str) -> str:
    match = re.search(r'[\w.+-]+@[\w-]+\.[\w.-]+', text)
    return match.group(0) if match else None  # 99%+ accuracy

def extract_phone(text: str) -> str:
    match = re.search(r'[\+]?[(]?[0-9]{1,4}[)]?[-\s\./0-9]{7,15}', text)
    return match.group(0) if match else None
```

**Accuracy targets:**
| Field | Method | Target Accuracy |
|-------|--------|----------------|
| Name | spaCy NER (PERSON) | 96%+ |
| Email | Regex | 99%+ |
| Phone | Regex | 95%+ |
| Location | spaCy NER (GPE) | 90%+ |
| Skills | Keyword + zero-shot | 85%+ |
| Experience | Heuristics + NER | 80%+ |

---

## 3️⃣ Skill Extraction (Two-Phase Approach)

### Phase 1: Keyword Matching (Fast Path)
- Maintain a skill taxonomy: `data/skills_taxonomy.json` with 500+ tech skills
- Case-insensitive fuzzy matching against resume text
- Returns immediately, deterministic results

### Phase 2: Zero-Shot Classification (Fallback)
- **Model:** `facebook/bart-large-mnli` (HuggingFace)
- Used when keyword matching returns < 5 skills
- Uses natural language inference to detect skills

```python
from transformers import pipeline

TECH_SKILLS = ["Python", "JavaScript", "React", "AWS", "Docker", 
               "PostgreSQL", "Node.js", "TypeScript", "Kubernetes", 
               "Machine Learning", ...]  # 500+ skills

def extract_skills(resume_text: str) -> list[str]:
    # Phase 1: Fast keyword matching
    skills = match_skills_from_taxonomy(resume_text)
    
    # Phase 2: Zero-shot if needed
    if len(skills) < 5:
        classifier = pipeline(
            "zero-shot-classification",
            model="facebook/bart-large-mnli"
        )
        results = classifier(
            resume_text[:1000],  # First 1000 chars
            TECH_SKILLS,
            multi_class=True
        )
        for label, score in zip(results['labels'], results['scores']):
            if score > 0.5:
                skills.append(label)
    
    return list(set(skills))
```

---

## 4️⃣ Structured Output Schema

```python
from pydantic import BaseModel
from typing import Optional

class ParsedResume(BaseModel):
    name: str
    email: Optional[str]
    phone: Optional[str]
    location: Optional[str]
    summary: str
    skills: list[str]
    experience: list[dict]   # [{title, company, start_date, end_date, description}]
    education: list[dict]    # [{degree, field, school, year}]
    extraction_confidence: float  # 0.0 - 1.0
```

---

## 5️⃣ Embedding Generation & Storage

**Model:** OpenAI `text-embedding-3-small`
- Dimensions: 1536
- Cost: $0.02 per 1M tokens
- No local GPU required

```python
from openai import OpenAI

client = OpenAI()

async def generate_embedding(profile_text: str) -> list[float]:
    """Generate 1536-dim embedding from candidate profile text."""
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=profile_text
    )
    return response.data[0].embedding

def build_profile_text(candidate: dict) -> str:
    """Create searchable text summary for embedding."""
    return (
        f"{candidate['name']}: "
        f"{', '.join(candidate['skills'])} developer with "
        f"{candidate.get('years_experience', 'N/A')} years experience. "
        f"Previously at {', '.join(org for exp in candidate.get('experience', []) for org in [exp.get('company', '')] if org)}. "
        f"Located in {candidate.get('location', 'Unknown')}."
    )
```

**Pinecone Index Configuration:**
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

---

## 6️⃣ Semantic Search

```python
import pinecone

pc = pinecone.Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index("candidates")

async def semantic_search(query: str, top_k: int = 10, 
                          recruiter_id: str = None) -> list[dict]:
    # 1. Embed the query
    query_embedding = await generate_embedding(query)
    
    # 2. Search Pinecone (with namespace for multi-tenant isolation)
    results = index.query(
        vector=query_embedding,
        namespace=f"recruiter_{recruiter_id}" if recruiter_id else None,
        top_k=top_k,
        include_metadata=True
    )
    
    # 3. Format results with match explanations
    return [
        {
            "candidate_id": match.id,
            "match_score": round(match.score, 2),
            "profile_text": match.metadata.get("profile_text", "")
        }
        for match in results.matches
    ]
```

---

## 7️⃣ Automatic Deduplication (Tier 2)

**Three-layer approach:**

| Layer | Method | Threshold | Speed |
|-------|--------|-----------|-------|
| 1 | Exact email match | 100% | Instant |
| 2 | Fuzzy name match | Levenshtein ≤ 2 | Fast |
| 3 | Embedding cosine similarity | > 0.92 | ~200ms |

```python
async def find_duplicates(candidate_id: str) -> list[dict]:
    candidate = db.get_candidate(candidate_id)
    
    # Layer 1: Exact email match
    exact = db.find_by_email(candidate.email)
    if exact and exact.id != candidate_id:
        return [{"id": exact.id, "score": 1.0, "reason": "Same email"}]
    
    # Layer 2: Fuzzy name match
    fuzzy = db.fuzzy_search_name(candidate.name, threshold=2)
    
    # Layer 3: Embedding similarity
    embedding = await get_candidate_embedding(candidate_id)
    similar = index.query(vector=embedding, top_k=5)
    
    duplicates = [
        {"id": s.id, "score": s.score, "reason": "Embedding similarity"}
        for s in similar.matches
        if s.score > 0.92 and s.id != candidate_id
    ]
    
    return duplicates
```

---

## 📦 Open-Source Building Blocks

For rapid implementation, reference these proven repositories:

| Resource | Use Case | Link |
|----------|----------|------|
| **Resume Semantic Search (BERT)** | Semantic search reference | KarthikAlagarsamy/Resume-Semantic-Search |
| **LLM Resume Parser** | Structured JSON output | Sajjad-Amjad/Resume-Parser |
| **Resume NER BERT v2** | NER model (90.9% F1) | yashpwr/resume-ner-bert-v2 (HuggingFace) |
| **LangGraph Resume Screener** | RAG-based screening | Ajithbalakrishnan/LangGraph_Based_Resume_Screener |
| **n8n Gmail → Parse Workflow** | Gmail ingestion pattern | Pragnakalp n8n workflow |
| **Agentic Resume Parser (HF)** | PDF→JSON service | csccorner/Agentic-Resume-Parser |

---

## ⚠️ Known Limitations

1. **Scanned PDFs** — Cannot extract text; requires OCR (out of scope for hackathon)
2. **Multi-language resumes** — English only for MVP
3. **Complex layouts** — Two-column resumes may parse poorly
4. **Skill taxonomy gaps** — 500 skills covers ~90% of tech roles; edge cases exist
5. **Zero-shot latency** — HuggingFace model adds ~2-3s on first call (model loading)

---

## 🔗 Cross-References
- **API endpoints for these services:** → [05_DATABASE_AND_API.md](./05_DATABASE_AND_API.md)
- **Where the AI code lives:** → [07_PROJECT_STRUCTURE_AND_OWNERSHIP.md](./07_PROJECT_STRUCTURE_AND_OWNERSHIP.md)
- **When to build each pipeline stage:** → [08_DEVELOPMENT_TIMELINE.md](./08_DEVELOPMENT_TIMELINE.md)

---

*Source: REFINED_CTO_BLUEPRINT_PROMPT.md (Section 5), ERROR_ANALYSIS (Errors #5, #8), GitHub repos & n8n workflows doc*
