# RegTech Radar — Collector/API
FROM python:3.12-slim

WORKDIR /app

# Paket için gerekli dosyalar (editable install önce)
COPY pyproject.toml ./
COPY src/ src/
COPY sources/ sources/

RUN pip install --no-cache-dir uv \
    && uv pip install --system -e .

EXPOSE 8000
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
