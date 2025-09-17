# Recipes Frontend (Next.js)

## Local dev
```bash
cd frontend
npm install
cp .env.local.example .env.local  # point to your backend
npm run dev
```

- `NEXT_PUBLIC_API_BASE_URL` must point to your FastAPI backend.
