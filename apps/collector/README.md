# RegTech Radar — Collector

Python backend: FastAPI API, source crawlers, AI processing pipeline, Celery tasks.

## Setup

```bash
cd apps/collector
python -m venv .venv
.venv\Scripts\activate   # Windows
pip install -e ".[dev]"
```

## Run API

```bash
uvicorn src.main:app --reload --port 8000
```

## Migrations (Alembic)

Veritabanı tabloları (sources, raw_contents, regulatory_updates, vb.) Alembic ile yönetilir.

```bash
# Proje kökünden
npm run migrate:collector

# veya bu dizinden
alembic upgrade head
```

Config `DATABASE_URL` için `.env`, `../.env`, `../../.env` dosyalarına bakar. Yeni migration: `alembic revision -m "açıklama"`.

## Tests

```bash
pytest
```

## Registry

Source definitions: `sources/registry.yaml`
