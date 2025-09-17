# RecipeHub Monorepo (Backend + Frontend)

## What’s inside
- `backend/` FastAPI + Postgres (Render)
- `frontend/` Next.js (Vercel)

## Sensitive data
- Secrets live in environment variables only.
- `.env` files are **gitignored**. Use the `*.example` files for placeholders.

## Local quickstart
```bash
# Backend
cd backend
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Optionally set DATABASE_URL, else SQLite dev.db is used
uvicorn app.main:app --reload

# Frontend (in separate terminal)
cd frontend
npm install
cp .env.local.example .env.local
npm run dev
```

## Deploy: Render (backend) + Postgres
1) Push this repo to GitHub (see commands below).
2) In Render, click **New +** → **Blueprint** and point to your repo.
3) Render will detect `render.yaml`. It will create:
   - A **Web Service** at `backend/` with `uvicorn` start command
   - A **PostgreSQL** instance and inject `DATABASE_URL`
4) In the Web Service → **Environment** tab, add:
   - `OPENAI_API_KEY` (Secret)
   - `AI_MODEL` (optional, defaults to `gpt-4o-mini`)
   - `CORS_ALLOW_ORIGINS` (e.g., your Vercel URL)
5) Deploy.

## Deploy: Vercel (frontend)
1) Import the same GitHub repo in Vercel.
2) Set **Root Directory** to `frontend/` in Vercel project settings.
3) Add an Environment Variable:
   - `NEXT_PUBLIC_API_BASE_URL=https://<your-render-service>.onrender.com`
4) Deploy.

## GitHub (first push)
```bash
cd /path/to/recipehub-monorepo
git init
git add .
git commit -m "feat: initial recipes app (FastAPI + Next.js)"
git branch -M main
git remote add origin https://github.com/<your-username>/recipehub-monorepo.git
git push -u origin main
```
