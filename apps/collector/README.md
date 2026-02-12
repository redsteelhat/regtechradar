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

## Tests

```bash
pytest
```

## Registry

Source definitions: `sources/registry.yaml`
