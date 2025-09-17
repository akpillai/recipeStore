# Recipes Backend (FastAPI)

## Local setup

```bash
cd backend
python -m venv .venv && source .venv/bin/activate  # on Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env  # fill values (for local SQLite you can skip DATABASE_URL)
uvicorn app.main:app --reload
```

- Default DB is SQLite (`dev.db`) for local dev (if `DATABASE_URL` isn't set).
- On Render, `DATABASE_URL` is injected from the managed Postgres.

## Endpoints
- `POST /recipes` create recipe
- `GET /recipes?q=...` search recipes
- `GET /recipes/{id}` get one
- `POST /ai/ask` ask AI by `recipe_name` or free-form `question`

## Security
- Put secrets in environment variables only. `.env` is ignored by Git.
