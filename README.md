# RegTech Radar

**Regulatory Intelligence Platform** — FinTech şirketlerinin takip etmesi gereken regülasyon değişikliklerini (DORA, MiCA, PSD3, AMLA, FATF vb.) otomatik toplayan, AI ile özetleyen, şirket profiline göre etki analizi yapan ve haftalık bülten + dashboard olarak sunan B2B SaaS.

- **Versiyon:** 0.1.0 (MVP)  
- **Tek kaynak:** [regtech.md](./regtech.md) — ürün, mimari, veri modeli, tech stack

---

## Monorepo yapısı (Turborepo)

| Paket | Açıklama |
|-------|----------|
| **apps/web** | Next.js 14 (App Router), dashboard, auth, feed, search, settings |
| **apps/collector** | Python FastAPI: crawlers, AI pipeline, Celery |
| **packages/shared** | Paylaşılan TypeScript tipleri ve sabitler (domains, jurisdictions) |

```
regtech-radar/
├── apps/web/          # Next.js frontend
├── apps/collector/   # Python backend (sources, processing, api)
├── packages/shared/   # @regtech-radar/shared
├── turbo.json
├── package.json
└── .env.example
```

---

## Gereksinimler

- **Node.js** 18+
- **npm** 10+ (veya pnpm/yarn)
- **Python** 3.12+
- **PostgreSQL** 16, **Redis** 7 (tam stack için)

---

## Ortam (.env)

```bash
cp .env.example .env
```

`.env` içindeki değerleri doldur. Tüm değişkenler [regtech.md Bölüm 13](./regtech.md) ile uyumludur.

### Veritabanı (Docker)

```bash
docker compose up -d
```

PostgreSQL 16 (pgvector, pg_trgm) ve Redis 7 ayağa kalkar. Varsayılan: `DATABASE_URL=postgresql://regtech:regtech@localhost:5432/regtechradar`, `REDIS_URL=redis://localhost:6379/0`.

**Collector migration (Alembic):**

```bash
cd apps/collector
pip install -e ".[dev]"
alembic upgrade head
```

**Web migration (Prisma):**

```bash
cd apps/web
npx prisma migrate deploy
# veya geliştirme: npx prisma migrate dev
npx prisma generate
```

---

## Hızlı başlangıç

### Kök: kurulum ve build

```bash
npm install
npm run build
```

### Web uygulaması

```bash
npm run dev
```

Sadece **web** ve **shared** çalışır; [http://localhost:3000](http://localhost:3000) açılır.

### Collector API (ayrı terminal)

```bash
cd apps/collector
python -m venv .venv
.venv\Scripts\activate   # Windows
pip install -e ".[dev]"
uvicorn src.main:app --reload --port 8000
```

API dokümantasyonu: [http://localhost:8000/docs](http://localhost:8000/docs).

---

## Scripts

| Komut | Açıklama |
|-------|----------|
| `npm run build` | Tüm paketleri build eder (shared → web) |
| `npm run dev` | Web + shared watch (collector dahil değil) |
| `npm run migrate` | Prisma + Alembic migration (önce web/auth, sonra collector) |
| `npm run migrate:collector` | Sadece Alembic (collector tabloları) |
| `npm run migrate:web` | Sadece Prisma (NextAuth tabloları; kök .env kullanır) |
| `npm run lint` | Lint (turbo) |
| `npm run format` | Prettier ile format |
| `npm run clean` | Build çıktılarını temizler |

---

## Dokümantasyon

| Dosya | İçerik |
|-------|--------|
| [regtech.md](./regtech.md) | Ürün kimliği, mimari, veri modeli, API, fiyatlandırma, geliştirme kuralları |
| [regtechradartodolist.md](./regtechradartodolist.md) | Faz bazlı todo listesi (Faz 0–11 + V2) |
| [docs/CONTRIBUTING.md](./docs/CONTRIBUTING.md) | Kod stili, Git kuralları, geliştirme notları |
| [docs/infra/MIGRATIONS.md](./docs/infra/MIGRATIONS.md) | Alembic + Prisma migration sırası ve komutları |

---

## GitHub’a gönderme

1. GitHub’da yeni repo oluştur (örn. `regtech-radar`).
2. Proje kökünde:

```bash
git remote add origin https://github.com/KULLANICI_ADI/regtech-radar.git
git branch -M main
git push -u origin main
```

---

## Lisans

Proprietary.
