# RegTech Radar

Regulatory Intelligence Platform for FinTech — B2B SaaS to track regulatory changes (DORA, MiCA, PSD3, AMLA, FATF, etc.), AI summaries, impact analysis, and weekly digest.

## Monorepo structure (Turborepo)

- **apps/web** — Next.js 14 (App Router), dashboard, auth, feed, search, settings
- **apps/collector** — Python FastAPI backend: crawlers, AI pipeline, Celery tasks
- **packages/shared** — Shared TypeScript types and constants

## Prerequisites

- Node.js 18+
- npm 10+ (or pnpm/yarn)
- Python 3.12+
- PostgreSQL 16, Redis 7 (for full stack)

## Quick start

### Root (install and build shared + web)

```bash
npm install
npm run build
```

### Web app

```bash
cd apps/web && npm run dev
```

Open [http://localhost:3000](http://localhost:3000).

### Collector (API + crawlers)

```bash
cd apps/collector
python -m venv .venv
.venv\Scripts\activate   # Windows
pip install -e ".[dev]"
uvicorn src.main:app --reload --port 8000
```

API docs: [http://localhost:8000/docs](http://localhost:8000/docs).

## Create GitHub repo

1. Create a new repository on GitHub (e.g. `regtech-radar`).
2. From this folder:

```bash
git init
git add .
git commit -m "chore: monorepo scaffold (Turborepo, apps/web, apps/collector, packages/shared)"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/regtech-radar.git
git push -u origin main
```

## Docs

- [regtech.md](./regtech.md) — Product and architecture (single source of truth)
- [regtechradartodolist.md](./regtechradartodolist.md) — Todo list

## License

Proprietary.
