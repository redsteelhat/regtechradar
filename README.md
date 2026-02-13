# RegTech Radar 📡

> AI-powered regulatory intelligence for FinTech compliance teams

Track DORA, MiCA, PSD3, AMLA, and FATF regulatory changes automatically. AI summaries + personalized impact analysis by license type.

## Quick Start

### 1. Backend (Python)

```bash
cd backend
cp .env.example .env   # edit .env with your keys
pip install -e .
uvicorn app.main:app --reload
```

API runs at `http://localhost:8000` — docs at `/docs`.

### 2. Frontend (Next.js)

```bash
cd frontend
npm install
npm run dev
```

Dashboard runs at `http://localhost:3000`.

### 3. Seed Demo Data

Register an account, then click **"Seed Demo Data"** on the dashboard, or hit:

```bash
curl -X POST http://localhost:8000/api/admin/seed
```

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend API | Python, FastAPI, SQLAlchemy, aiosqlite |
| Scraping | httpx, BeautifulSoup, lxml |
| AI | OpenAI GPT-4o-mini |
| Email | Resend |
| Frontend | Next.js 14, TypeScript, App Router |
| Auth | JWT (python-jose + bcrypt) |
| Scheduler | APScheduler |

## Project Structure

```
RegTech/
├── backend/
│   ├── app/
│   │   ├── main.py          # FastAPI app
│   │   ├── config.py         # Pydantic settings
│   │   ├── database.py       # SQLAlchemy async
│   │   ├── models.py         # ORM models
│   │   ├── schemas.py        # Pydantic schemas
│   │   ├── deps.py           # Auth dependency
│   │   ├── scheduler.py      # Cron jobs
│   │   ├── routers/          # API endpoints
│   │   ├── scrapers/         # EBA, ESMA, FATF, FCA, FinCEN
│   │   └── services/         # AI, Auth, Email
│   └── pyproject.toml
├── frontend/
│   └── src/app/
│       ├── page.tsx           # Landing page
│       ├── login/             # Sign in
│       ├── register/          # Sign up
│       └── dashboard/         # Main app
│           ├── page.tsx       # Regulation feed
│           ├── [id]/          # Regulation detail
│           ├── alerts/        # Alert management
│           └── settings/      # Profile & subscription
└── README.md
```

## Environment Variables

See `backend/.env.example` for all required config.

## License

MIT
