# 09 — DEVOPS, CI/CD & DEPLOYMENT
## Docker, GitHub Actions, Railway/Vercel Deployment & Secrets

---

## 🐳 Docker Setup (Local Development)

### docker-compose.yml
```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15
    ports:
      - "5432:5432"
    environment:
      POSTGRES_USER: talent_user
      POSTGRES_PASSWORD: talent_pass
      POSTGRES_DB: talent_unify
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  backend:
    build:
      context: ./backend
      dockerfile: ../docker/Dockerfile.backend
    ports:
      - "8000:8000"
    depends_on:
      - postgres
      - redis
    env_file:
      - .env
    volumes:
      - ./backend:/app

  frontend:
    build:
      context: ./frontend
      dockerfile: ../docker/Dockerfile.frontend
    ports:
      - "3000:3000"
    volumes:
      - ./frontend:/app
      - /app/node_modules

  celery_worker:
    build:
      context: ./backend
      dockerfile: ../docker/Dockerfile.backend
    command: celery -A tasks.celery_app worker --loglevel=info
    depends_on:
      - redis
      - postgres
    env_file:
      - .env

volumes:
  postgres_data:
```

### Dockerfile.backend
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m spacy download en_core_web_sm

COPY . .

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```

### Dockerfile.frontend
```dockerfile
FROM node:18-alpine

WORKDIR /app
COPY package*.json ./
RUN npm ci

COPY . .

EXPOSE 3000
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
```

### One-Command Setup
```bash
# scripts/setup.sh
#!/bin/bash
set -e

echo "🚀 Setting up TalentUnify..."

# 1. Check prerequisites
command -v docker >/dev/null 2>&1 || { echo "Docker required"; exit 1; }

# 2. Copy env template
cp .env.example .env
echo "📝 Edit .env with your API keys before proceeding"

# 3. Start services
docker-compose up -d postgres redis

# 4. Install backend deps
cd backend && pip install -r requirements.txt
python -m spacy download en_core_web_sm

# 5. Run migrations
alembic upgrade head

# 6. Seed demo data
python ../scripts/seed_db.py

# 7. Install frontend deps
cd ../frontend && npm install

echo "✅ Setup complete! Run: docker-compose up"
```

---

## 🔄 GitHub Actions CI/CD

### Backend CI (`.github/workflows/ci-backend.yml`)
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
      - name: Set up Python 3.11
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
      - name: Run tests (pytest)
        run: pytest backend/tests -v --cov=backend/app
        env:
          DATABASE_URL: postgresql://postgres:postgres@localhost:5432/test_db
```

### Frontend CI (`.github/workflows/ci-frontend.yml`)
```yaml
name: Frontend CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Node 18
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          cache: 'npm'
          cache-dependency-path: 'frontend/package-lock.json'
      - name: Install dependencies
        run: cd frontend && npm ci
      - name: Lint (ESLint)
        run: cd frontend && npm run lint
      - name: Type check (tsc)
        run: cd frontend && npm run type-check
      - name: Build
        run: cd frontend && npm run build
      - name: Unit tests (vitest)
        run: cd frontend && npm run test
```

### Deploy Pipeline (`.github/workflows/deploy.yml`)
```yaml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Deploy to Railway
        uses: railway-app/deploy-action@v1
        with:
          service: backend
          token: ${{ secrets.RAILWAY_TOKEN }}
      - name: Smoke test
        run: curl -f https://api.talentunify.io/health

  deploy-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Deploy to Vercel
        uses: amondnet/vercel-action@v20
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          github-token: ${{ secrets.GITHUB_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
          working-directory: ./frontend
```

---

## 🌲 Git Branch Strategy

```
main (production — deploy on merge)
  ↑ PR required, tests must pass
  │
  └── develop (integration branch)
        ↑ PRs auto-merge after CI
        ├── feature/dashboard         (Engineer 1)
        ├── feature/api-candidates    (Engineer 2)
        ├── feature/resume-parser     (Engineer 3)
        └── feature/gmail-oauth       (Engineer 4)
```

**Rules:**
- `main`: Production-ready only. Requires PR + all CI passing
- `develop`: Integration branch. PRs auto-merge after CI
- `feature/*`: Individual branches. Rebase before merge

**Quick commands:**
```bash
# Start a feature
git checkout develop && git pull
git checkout -b feature/your-feature

# Merge to develop
git checkout develop && git merge --squash feature/your-feature
git push origin develop

# Deploy to production
git checkout main && git merge develop
git push origin main  # Triggers deploy pipeline
```

---

## 🔐 Secrets Management

### GitHub Secrets to Configure

```bash
# Backend
DATABASE_URL           # PostgreSQL connection string
REDIS_URL              # Redis connection string
OPENAI_API_KEY         # OpenAI API key
PINECONE_API_KEY       # Pinecone API key
PINECONE_ENVIRONMENT   # Pinecone region
GOOGLE_CLIENT_ID       # Gmail OAuth client ID
GOOGLE_CLIENT_SECRET   # Gmail OAuth client secret
SECRET_KEY             # JWT signing key

# Deployment
RAILWAY_TOKEN          # Railway deployment token
VERCEL_TOKEN           # Vercel deployment token
VERCEL_ORG_ID          # Vercel org ID
VERCEL_PROJECT_ID      # Vercel project ID
```

### `.env.example` Template
Include in repo root — never commit actual `.env` files.

---

## 🚀 Deployment Checklist (Hour 46)

### Backend (Railway/Render)
- [ ] Push to `main` branch
- [ ] Verify Railway builds successfully
- [ ] Set all environment variables in Railway dashboard
- [ ] Verify `/health` endpoint returns 200
- [ ] Verify `/docs` (Swagger) loads
- [ ] Test API response times < 500ms

### Frontend (Vercel)
- [ ] Connect GitHub repo to Vercel
- [ ] Set `VITE_API_URL` environment variable
- [ ] Verify build passes
- [ ] Test all pages load
- [ ] Verify search functionality works
- [ ] Check Lighthouse score > 80

### Database
- [ ] PostgreSQL accessible from production backend
- [ ] Run migrations on production
- [ ] Seed demo data
- [ ] Verify queries execute < 500ms

### Pre-commit Hooks
```yaml
# .pre-commit-config.yaml
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
```

---

## 🧰 GitHub Student Pack Resources

| Resource | Use For | Benefit |
|----------|---------|---------|
| **GitHub Pro** | Private repos, branch protection | Free |
| **GitHub Actions** | CI/CD (3000 min/month) | Free |
| **GitHub Codespaces** | Cloud IDE (180h/month) | Free |
| **MongoDB Atlas** | Alternative DB credits | Free credits |
| **DigitalOcean** | Cloud hosting credits | $200 credits |
| **Azure** | Cloud services | $100 credits |
| **JetBrains IDEs** | IntelliJ, PyCharm, WebStorm | Free license |
| **Sentry** | Error tracking | Free tier |
| **New Relic** | APM monitoring | Free tier |

---

## 🔗 Cross-References
- **What to deploy (features):** → [03_FEATURE_TRIAGE.md](./03_FEATURE_TRIAGE.md)
- **Project structure for Docker:** → [07_PROJECT_STRUCTURE_AND_OWNERSHIP.md](./07_PROJECT_STRUCTURE_AND_OWNERSHIP.md)
- **When to deploy (Hour 46):** → [08_DEVELOPMENT_TIMELINE.md](./08_DEVELOPMENT_TIMELINE.md)

---

*Source: REFINED_CTO_BLUEPRINT_PROMPT.md (Section 14), ERROR_ANALYSIS (Errors #11, #20), QUICK_REFERENCE_INDEX, GitHub Student Pack doc*
