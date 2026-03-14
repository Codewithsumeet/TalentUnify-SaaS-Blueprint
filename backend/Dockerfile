FROM python:3.11-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential libpq-dev curl && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

# Install Python deps
RUN pip install --no-cache-dir -r requirements.txt

# BUG FIX 4: Install CPU-only torch explicitly BEFORE transformers model downloads.
# transformers requires torch OR tensorflow. We use CPU torch (~200MB vs ~800MB GPU).
# Must use the CPU index to avoid pulling CUDA binaries.
RUN pip install --no-cache-dir \
    torch==2.3.0 \
    --index-url https://download.pytorch.org/whl/cpu

# BUG FIX 12: Pre-cache ALL HuggingFace models at build time.
# Without this, each container restart re-downloads 2GB+ of weights.
# Build-time cache = zero cold-start on demo day.

# spaCy — NOT a pip package, requires separate download
RUN python -m spacy download en_core_web_sm

# facebook/bart-large-mnli (~1.6 GB) — zero-shot skill classifier
RUN python -c "\
from transformers import pipeline; \
p = pipeline('zero-shot-classification', model='facebook/bart-large-mnli', device=-1); \
print('OK: bart-large-mnli')"

# all-MiniLM-L6-v2 (~80 MB) — local embedding fallback
RUN python -c "\
from sentence_transformers import SentenceTransformer; \
SentenceTransformer('all-MiniLM-L6-v2'); \
print('OK: all-MiniLM-L6-v2')"

# yashpwr/resume-ner-bert-v2 (~400 MB) — BERT NER fallback
RUN python -c "\
from transformers import pipeline; \
pipeline('token-classification', model='yashpwr/resume-ner-bert-v2', \
aggregation_strategy='simple', device=-1); \
print('OK: resume-ner-bert-v2')"

# TechWolf/JobBERT-v3 (~140 MB) — job title normalizer
RUN python -c "\
from sentence_transformers import SentenceTransformer; \
SentenceTransformer('TechWolf/JobBERT-v3'); \
print('OK: JobBERT-v3')"

COPY . .

# Default: Celery worker
# Override in docker-compose for the API process
CMD ["celery", "-A", "tasks.celery_app:celery_app", "worker", \
     "--loglevel=info", "--concurrency=2", "-Q", "default"]
