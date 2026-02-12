-- RegTech Radar — Postgres init (pgvector + pg_trgm)
-- Tablolar Alembic migration ile oluşturulur; bu dosya sadece extension'ları açar.
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS pg_trgm;
