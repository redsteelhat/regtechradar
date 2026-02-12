# Migrations — Prisma (web) + Alembic (collector)

Aynı PostgreSQL veritabanı kullanılır. **Sıra önemli:** Önce Prisma (auth tabloları), sonra Alembic (collector tabloları). Prisma boş/yalnızca extension içeren bir şemada çalışmalıdır; Alembic sonra kendi tablolarını ekler.

## Sıra

1. **Prisma** — NextAuth tabloları: `User`, `Account`, `Session`, `VerificationToken`.
2. **Alembic** — Collector tabloları: `sources`, `raw_contents`, `regulatory_updates`, `company_profiles`, `impact_assessments`, `alert_rules`, `digests` (Bölüm 5.1).

## Ön koşul

- Docker: `docker compose up -d` (Postgres + Redis).
- Kök dizinde `.env` ve `DATABASE_URL=postgresql://regtech:regtech@localhost:5432/regtechradar`.

## Komutlar (proje kökünden)

```bash
# Her iki migration (önerilen) — önce Prisma, sonra Alembic
npm run migrate

# Sadece web (Prisma) — auth tabloları
npm run migrate:web

# Sadece collector (Alembic) — collector tabloları
npm run migrate:collector
```

## Tek tek çalıştırma

### Alembic (apps/collector)

```bash
cd apps/collector
alembic upgrade head
```

- Config, `.env` veya `../.env` / `../../.env` dosyasından `DATABASE_URL` okur.
- Mevcut revizyon: `001` (initial schema).
- Geri alma: `alembic downgrade -1`.

### Prisma (apps/web)

```bash
cd apps/web
npx prisma migrate deploy
npx prisma generate
```

- `DATABASE_URL` ortam değişkeninden veya `apps/web/.env` dosyasından okunur.
- Kökten `npm run migrate:web` ile çalıştırırsan kök `.env` kullanılır (dotenv-cli).
- Prisma önce çalıştırılmalıdır (veritabanı boş veya sadece extension’lar olmalı); sonra Alembic çalıştırılır.

## Yeni migration ekleme

### Alembic

```bash
cd apps/collector
alembic revision -m "açıklama"
# versions/ içinde yeni dosyayı düzenle, sonra:
alembic upgrade head
```

### Prisma

```bash
cd apps/web
npx prisma migrate dev --name migration_adi
# migration.sql otomatik üretilir
```

## P3005: "The database schema is not empty"

Bu hata, Prisma’dan önce Alembic çalıştığında (veritabanında zaten tablolar varken `migrate:web` çalıştırıldığında) oluşur.

**Çözüm 1 (tercih):** Veritabanını sıfırlayıp migration’ları yeni sırayla uygula:

```bash
docker compose down -v
docker compose up -d
# Postgres hazır olana kadar birkaç saniye bekle
npm run migrate
```

**Çözüm 2 (mevcut DB’yi korumak):** Prisma migration’ı elle uygulayıp “uygulandı” olarak işaretle:

```bash
cd apps/web
npx prisma db execute --file prisma/migrations/20260212000000_init_auth/migration.sql
npx prisma migrate resolve --applied 20260212000000_init_auth
npx prisma generate
```

---

## Dosya konumları

| Ne            | Nerede |
|---------------|--------|
| Alembic config | `apps/collector/alembic.ini` |
| Alembic env   | `apps/collector/alembic/env.py` |
| Alembic migrations | `apps/collector/alembic/versions/*.py` |
| Prisma schema | `apps/web/prisma/schema.prisma` |
| Prisma migrations | `apps/web/prisma/migrations/*/migration.sql` |
