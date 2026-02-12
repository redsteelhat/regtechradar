# CLAUDE.md — RegTech Radar

> **Proje**: RegTech Radar — Regulatory Intelligence Platform  
> **Versiyon**: 0.1.0 (MVP)  
> **Son Güncelleme**: 2026-02-12  
> **Durum**: Pre-development / Architecture Phase

---

## 1. Proje Kimliği

**RegTech Radar**, FinTech şirketlerinin takip etmesi gereken regülasyon değişikliklerini (DORA, MiCA, PSD3/PSR, AMLA, FATF, IPR, TFR vb.) otomatik olarak toplayan, AI ile özetleyen, şirket profiline göre etki analizi yapan ve haftalık bülten + searchable dashboard olarak sunan bir B2B SaaS ürünüdür.

### Hedef Kullanıcılar (Persona)

| Persona | Rol | Acı Noktası |
|---------|-----|-------------|
| **Compliance Officer** | Orta ölçekli CASP / PSP / Neobank | Haftada 8-12 saat regülatör sitelerini tarayarak değişiklik arıyor; çoğu zaman geç fark ediyor |
| **Head of Legal** | FinTech startup (Series A-B) | Birden fazla jurisdiksiyonda (EU + UK + TR) düzenleme takibi yapamıyor; dış danışmana bağımlı |
| **GRC Manager** | Banka / Sigorta (DORA kapsamı) | DORA + NIS2 + GDPR + sektörel düzenlemelerin kesişimini mapping'leyemiyor |
| **FinTech Founder / CPO** | Erken aşama girişim | Hangi düzenlemenin ürününü nasıl etkileyeceğini anlayamıyor; reaktif kalıyor |

### Değer Önerisi (Value Proposition)

```
"Regülatör sitelerini sen tarama — RegTech Radar her hafta sana özetlenmiş,
 kişiselleştirilmiş ve eyleme dönüştürülebilir regulatory intelligence sunsun."
```

---

## 2. Mimari Genel Bakış

```
┌─────────────────────────────────────────────────────────────────┐
│                        RegTech Radar                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────┐    ┌──────────────┐    ┌───────────────────────┐  │
│  │ COLLECTOR │───▶│  PROCESSOR   │───▶│     DELIVERY LAYER    │  │
│  │  (Crawl)  │    │ (AI Pipeline)│    │                       │  │
│  └──────────┘    └──────────────┘    │  ┌─────────────────┐  │  │
│       │                │              │  │  Next.js Web App │  │  │
│       ▼                ▼              │  │  (Dashboard)     │  │  │
│  ┌──────────┐    ┌──────────────┐    │  └─────────────────┘  │  │
│  │  SOURCE   │    │  PostgreSQL  │    │  ┌─────────────────┐  │  │
│  │ REGISTRY  │    │   + pgvector │    │  │  Email Digest   │  │  │
│  │ (YAML)    │    │              │    │  │  (Resend)       │  │  │
│  └──────────┘    └──────────────┘    │  └─────────────────┘  │  │
│                        │              │  ┌─────────────────┐  │  │
│                        ▼              │  │  REST API        │  │  │
│                  ┌──────────────┐    │  │  (Public)        │  │  │
│                  │  Vector DB   │    │  └─────────────────┘  │  │
│                  │  (Semantic   │    └───────────────────────┘  │
│                  │   Search)    │                                │
│                  └──────────────┘                                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Katman Açıklamaları

| Katman | Sorumluluk | Teknoloji |
|--------|-----------|-----------|
| **Collector** | Regülatör kaynaklarını periyodik olarak tarar; yeni içerikleri tespit eder | Python + Playwright/httpx + Celery Beat |
| **Processor** | Ham içeriği parse eder, AI ile özetler, etki skoru atar, embedding üretir | Python + Claude API (Sonnet) + tiktoken |
| **Storage** | Yapılandırılmış veri + vector embedding'ler | PostgreSQL 16 + pgvector extension |
| **Delivery — Web** | Dashboard, arama, filtre, kullanıcı profili, alert yönetimi | Next.js 14 (App Router) + Tailwind CSS + shadcn/ui |
| **Delivery — Email** | Haftalık/günlük digest, breaking alert | Resend (React Email templates) |
| **Delivery — API** | Programatik erişim (Team/Enterprise plan) | Next.js API Routes + API key auth |

---

## 3. Teknoloji Yığını (Tech Stack)

### 3.1 Backend (Python)

```
Runtime:          Python 3.12+
Framework:        FastAPI (collector/processor microservices)
Task Queue:       Celery + Redis (scheduled crawling, AI pipeline)
Scheduler:        Celery Beat (cron-based crawl schedules)
HTTP Client:      httpx (async) + Playwright (JS-rendered pages)
HTML Parsing:     BeautifulSoup4 + lxml
PDF Extraction:   pdfplumber (regülatör PDF'leri için)
AI/LLM:          Anthropic Claude API (claude-sonnet-4-5-20250929)
Embeddings:       Anthropic Voyage veya OpenAI text-embedding-3-small
Validation:       Pydantic v2 (tüm data modelleri)
Testing:          pytest + pytest-asyncio + factory-boy
```

### 3.2 Frontend (TypeScript)

```
Framework:        Next.js 14 (App Router, RSC)
Language:         TypeScript 5.x (strict mode)
Styling:          Tailwind CSS 3.4 + shadcn/ui component library
State:            Zustand (client state) + React Query/TanStack Query (server state)
Auth:             NextAuth.js v5 (Email magic link + Google OAuth)
Email:            Resend SDK + React Email (template rendering)
Charts:           Recharts (regulatory timeline, trend visualization)
Search:           Client-side instant search + server-side semantic search
Deployment:       Vercel (frontend) + Railway/Fly.io (backend)
```

### 3.3 Database

```
Primary DB:       PostgreSQL 16
  - pgvector:     Semantic search (embedding similarity)
  - pg_trgm:      Fuzzy text search (regülasyon adı, anahtar kelime)
Cache:            Redis 7 (Celery broker + session cache + rate limiting)
```

### 3.4 Altyapı & DevOps

```
Monorepo:         Turborepo (apps/web, apps/api, packages/shared)
Containerization: Docker + Docker Compose (local dev)
CI/CD:            GitHub Actions
Monitoring:       Sentry (error tracking) + Axiom (logs)
Secrets:          doppler veya .env.vault
```

---

## 4. Dizin Yapısı

```
regtech-radar/
├── apps/
│   ├── web/                          # Next.js frontend
│   │   ├── app/
│   │   │   ├── (auth)/
│   │   │   │   ├── login/
│   │   │   │   └── signup/
│   │   │   ├── (dashboard)/
│   │   │   │   ├── feed/             # Ana regulatory feed
│   │   │   │   ├── search/           # Semantic + keyword search
│   │   │   │   ├── alerts/           # Custom alert yönetimi
│   │   │   │   ├── impact/           # Kişiselleştirilmiş etki analizi
│   │   │   │   ├── timeline/         # Regulatory calendar/timeline
│   │   │   │   └── settings/
│   │   │   │       ├── profile/      # Şirket profili & lisans türü
│   │   │   │       ├── billing/
│   │   │   │       └── team/
│   │   │   ├── api/                  # Next.js API routes (BFF)
│   │   │   │   ├── auth/
│   │   │   │   ├── feed/
│   │   │   │   ├── search/
│   │   │   │   ├── webhooks/
│   │   │   │   │   └── stripe/
│   │   │   │   └── v1/              # Public API (Team plan)
│   │   │   │       ├── updates/
│   │   │   │       └── search/
│   │   │   ├── layout.tsx
│   │   │   └── page.tsx             # Landing page (marketing)
│   │   ├── components/
│   │   │   ├── ui/                  # shadcn/ui components
│   │   │   ├── feed/
│   │   │   │   ├── UpdateCard.tsx
│   │   │   │   ├── ImpactBadge.tsx
│   │   │   │   ├── SourceTag.tsx
│   │   │   │   └── FilterBar.tsx
│   │   │   ├── search/
│   │   │   │   ├── SearchBar.tsx
│   │   │   │   └── ResultsList.tsx
│   │   │   ├── timeline/
│   │   │   │   └── RegulatoryTimeline.tsx
│   │   │   ├── alerts/
│   │   │   │   ├── AlertRuleBuilder.tsx
│   │   │   │   └── AlertList.tsx
│   │   │   ├── email/
│   │   │   │   ├── WeeklyDigest.tsx  # React Email template
│   │   │   │   └── BreakingAlert.tsx
│   │   │   └── shared/
│   │   │       ├── Navbar.tsx
│   │   │       ├── Sidebar.tsx
│   │   │       └── Footer.tsx
│   │   ├── lib/
│   │   │   ├── db.ts                # Prisma client
│   │   │   ├── auth.ts              # NextAuth config
│   │   │   ├── stripe.ts            # Stripe SDK wrapper
│   │   │   ├── resend.ts            # Email client
│   │   │   └── api-client.ts        # Backend API client
│   │   ├── prisma/
│   │   │   ├── schema.prisma
│   │   │   └── migrations/
│   │   ├── public/
│   │   ├── tailwind.config.ts
│   │   ├── next.config.js
│   │   └── package.json
│   │
│   └── collector/                    # Python backend
│       ├── src/
│       │   ├── __init__.py
│       │   ├── main.py              # FastAPI app entry
│       │   ├── config.py            # Settings (pydantic-settings)
│       │   ├── sources/
│       │   │   ├── registry.py      # Source registry loader
│       │   │   ├── base.py          # AbstractSource class
│       │   │   ├── eba.py           # EBA crawler
│       │   │   ├── esma.py          # ESMA crawler
│       │   │   ├── fatf.py          # FATF crawler
│       │   │   ├── ecb.py           # ECB crawler
│       │   │   ├── fca.py           # FCA (UK) crawler
│       │   │   ├── fincen.py        # FinCEN (US) crawler
│       │   │   ├── bis.py           # BIS/BCBS crawler
│       │   │   ├── eu_official.py   # EUR-Lex / Official Journal
│       │   │   └── rss_generic.py   # Generic RSS/Atom feed parser
│       │   ├── processing/
│       │   │   ├── parser.py        # HTML/PDF → clean text
│       │   │   ├── dedup.py         # Content deduplication
│       │   │   ├── classifier.py    # Regulatory domain classifier
│       │   │   ├── summarizer.py    # Claude API summarization
│       │   │   ├── impact.py        # Impact scoring engine
│       │   │   └── embedder.py      # Vector embedding generation
│       │   ├── delivery/
│       │   │   ├── digest.py        # Weekly digest builder
│       │   │   └── webhook.py       # Alert webhook dispatcher
│       │   ├── tasks/
│       │   │   ├── celery_app.py    # Celery configuration
│       │   │   ├── crawl.py         # Scheduled crawl tasks
│       │   │   ├── process.py       # AI processing pipeline
│       │   │   └── notify.py        # Notification tasks
│       │   ├── models/
│       │   │   ├── source.py        # Source Pydantic models
│       │   │   ├── update.py        # RegulatoryUpdate model
│       │   │   ├── impact.py        # ImpactAssessment model
│       │   │   └── user.py          # CompanyProfile model
│       │   ├── db/
│       │   │   ├── connection.py    # SQLAlchemy async engine
│       │   │   ├── repositories.py  # Data access layer
│       │   │   └── migrations/      # Alembic migrations
│       │   └── api/
│       │       ├── routes/
│       │       │   ├── health.py
│       │       │   ├── updates.py
│       │       │   ├── search.py
│       │       │   └── admin.py
│       │       └── middleware.py
│       ├── sources/
│       │   └── registry.yaml        # Source definitions
│       ├── tests/
│       │   ├── test_sources/
│       │   ├── test_processing/
│       │   └── fixtures/
│       ├── pyproject.toml
│       ├── Dockerfile
│       └── celerybeat-schedule.py
│
├── packages/
│   └── shared/
│       ├── types/                    # Shared TypeScript types
│       │   ├── regulatory-update.ts
│       │   ├── impact.ts
│       │   └── api.ts
│       └── constants/
│           ├── domains.ts            # Regulatory domain taxonomy
│           └── jurisdictions.ts
│
├── docker-compose.yml
├── turbo.json
├── package.json
├── .github/
│   └── workflows/
│       ├── ci.yml
│       ├── deploy-web.yml
│       └── deploy-collector.yml
├── .env.example
├── CLAUDE.md                         # ← Bu dosya
└── README.md
```

---

## 5. Veri Modeli

### 5.1 Temel Entity'ler

```sql
-- Regülatör kaynak tanımları
CREATE TABLE sources (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    slug            TEXT UNIQUE NOT NULL,          -- 'eba', 'fatf', 'esma'
    name            TEXT NOT NULL,                 -- 'European Banking Authority'
    url             TEXT NOT NULL,                 -- Base URL
    source_type     TEXT NOT NULL,                 -- 'regulator', 'standard_body', 'advisory'
    jurisdiction    TEXT[] NOT NULL,               -- ['EU'], ['UK'], ['US', 'GLOBAL']
    crawl_frequency TEXT NOT NULL DEFAULT '6h',    -- '1h', '6h', '12h', '24h'
    is_active       BOOLEAN DEFAULT true,
    last_crawled_at TIMESTAMPTZ,
    config_json     JSONB,                        -- Crawler-specific config
    created_at      TIMESTAMPTZ DEFAULT now()
);

-- Ham crawl sonuçları
CREATE TABLE raw_contents (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_id       UUID REFERENCES sources(id),
    url             TEXT NOT NULL,
    title           TEXT,
    raw_html        TEXT,
    extracted_text  TEXT,
    content_hash    TEXT NOT NULL,                 -- SHA-256 for dedup
    published_at    TIMESTAMPTZ,
    crawled_at      TIMESTAMPTZ DEFAULT now(),
    UNIQUE(content_hash)
);

-- İşlenmiş regülasyon güncellemeleri (ana entity)
CREATE TABLE regulatory_updates (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    raw_content_id  UUID REFERENCES raw_contents(id),
    source_id       UUID REFERENCES sources(id),
    
    -- İçerik
    title           TEXT NOT NULL,
    summary_short   TEXT NOT NULL,                 -- 2-3 cümle (feed kartı için)
    summary_long    TEXT NOT NULL,                 -- Detaylı AI özeti
    original_url    TEXT NOT NULL,
    original_lang   TEXT DEFAULT 'en',
    
    -- Sınıflandırma
    domains         TEXT[] NOT NULL,               -- ['AML_KYC', 'PAYMENTS', 'CRYPTO']
    regulations     TEXT[],                        -- ['MiCA', 'DORA', 'PSD3']
    jurisdictions   TEXT[] NOT NULL,               -- ['EU', 'UK']
    update_type     TEXT NOT NULL,                 -- Aşağıda taxonomy var
    severity        TEXT NOT NULL,                 -- 'critical', 'high', 'medium', 'low', 'info'
    
    -- Tarih bilgisi
    published_at    TIMESTAMPTZ NOT NULL,
    effective_date  TIMESTAMPTZ,                   -- Yürürlük tarihi (varsa)
    deadline_date   TIMESTAMPTZ,                   -- Uyum son tarihi (varsa)
    
    -- AI-generated
    key_takeaways   TEXT[],                        -- 3-5 madde
    action_items    TEXT[],                        -- "Bunu yapmanız gerekebilir" listesi
    affected_entities TEXT[],                      -- ['CASP', 'PSP', 'Bank', 'InsuranceCo']
    
    -- Embedding (semantic search için)
    embedding       vector(1536),                  -- pgvector
    
    -- Meta
    is_published    BOOLEAN DEFAULT false,
    published_in_digest UUID,                      -- Hangi digest'te yayınlandı
    created_at      TIMESTAMPTZ DEFAULT now(),
    updated_at      TIMESTAMPTZ DEFAULT now()
);

-- Şirket profilleri (kişiselleştirme için)
CREATE TABLE company_profiles (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         UUID NOT NULL,                 -- NextAuth user id
    company_name    TEXT,
    
    -- Profil bilgileri (etki skoru hesabı için)
    license_types   TEXT[],                        -- ['EMI', 'PI', 'CASP', 'AISP']
    jurisdictions   TEXT[],                        -- Aktif olduğu pazarlar
    domains         TEXT[],                        -- İlgi alanları
    entity_size     TEXT,                          -- 'startup', 'scaleup', 'enterprise'
    services        TEXT[],                        -- ['custody', 'exchange', 'lending']
    
    created_at      TIMESTAMPTZ DEFAULT now(),
    updated_at      TIMESTAMPTZ DEFAULT now()
);

-- Kişiselleştirilmiş etki skorları
CREATE TABLE impact_assessments (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    regulatory_update_id UUID REFERENCES regulatory_updates(id),
    company_profile_id   UUID REFERENCES company_profiles(id),
    
    impact_score        INTEGER NOT NULL CHECK (impact_score BETWEEN 0 AND 100),
    impact_category     TEXT NOT NULL,             -- 'direct', 'indirect', 'monitoring'
    reasoning           TEXT NOT NULL,              -- AI açıklaması
    recommended_actions TEXT[],
    
    created_at          TIMESTAMPTZ DEFAULT now(),
    UNIQUE(regulatory_update_id, company_profile_id)
);

-- Custom alert kuralları
CREATE TABLE alert_rules (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         UUID NOT NULL,
    name            TEXT NOT NULL,
    
    -- Filtre koşulları (JSON Logic veya basit AND/OR)
    conditions      JSONB NOT NULL,
    -- Örnek: {"domains": ["AML_KYC"], "severity": ["critical","high"], "jurisdictions": ["EU"]}
    
    -- Bildirim kanalı
    channel         TEXT NOT NULL DEFAULT 'email', -- 'email', 'webhook', 'slack'
    channel_config  JSONB,                        -- Webhook URL, Slack channel vb.
    
    is_active       BOOLEAN DEFAULT true,
    last_triggered  TIMESTAMPTZ,
    created_at      TIMESTAMPTZ DEFAULT now()
);

-- Haftalık digest kayıtları
CREATE TABLE digests (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    week_start      DATE NOT NULL,
    week_end        DATE NOT NULL,
    
    -- İçerik
    intro_text      TEXT,                          -- AI-generated haftalık giriş
    highlight_ids   UUID[],                        -- Öne çıkan güncellemeler
    stats_json      JSONB,                        -- Haftalık istatistikler
    
    sent_at         TIMESTAMPTZ,
    recipient_count INTEGER,
    open_rate       DECIMAL(5,4),
    click_rate      DECIMAL(5,4),
    
    created_at      TIMESTAMPTZ DEFAULT now()
);

-- Index'ler
CREATE INDEX idx_updates_domains ON regulatory_updates USING GIN (domains);
CREATE INDEX idx_updates_jurisdictions ON regulatory_updates USING GIN (jurisdictions);
CREATE INDEX idx_updates_regulations ON regulatory_updates USING GIN (regulations);
CREATE INDEX idx_updates_published ON regulatory_updates (published_at DESC);
CREATE INDEX idx_updates_severity ON regulatory_updates (severity);
CREATE INDEX idx_updates_embedding ON regulatory_updates USING ivfflat (embedding vector_cosine_ops);
CREATE INDEX idx_raw_hash ON raw_contents (content_hash);
```

### 5.2 Regülasyon Domain Taxonomy

```python
REGULATORY_DOMAINS = {
    "AML_KYC":       "AML/KYC, Sanctions, Beneficial Ownership, Transaction Monitoring",
    "PAYMENTS":      "Payment Services, SCA, Instant Payments, Fraud, Chargeback",
    "OPEN_BANKING":  "Open Banking, PSD2/PSD3, Data Sharing, Consent, API Standards",
    "CRYPTO":        "Crypto-Assets, Stablecoins, MiCA, Travel Rule, DeFi",
    "DORA_ICT":      "Digital Operational Resilience, ICT Risk, Third-Party Risk",
    "DATA_PRIVACY":  "GDPR, Data Protection, Cross-Border Data Transfer",
    "CAPITAL_PRUDENTIAL": "Capital Requirements, CRD/CRR, Liquidity, Stress Testing",
    "CONSUMER":      "Consumer Protection, Conduct, Complaints, Financial Inclusion",
    "SUSTAINABILITY": "ESG Disclosure, Taxonomy, Green Finance",
    "MESSAGING":     "ISO 20022, SWIFT, Payment Messaging Standards",
}

UPDATE_TYPES = {
    "new_regulation":       "Yeni düzenleme/kanun yayınlandı",
    "amendment":            "Mevcut düzenlemeye değişiklik",
    "rts_its":              "Teknik standart (RTS/ITS) taslağı veya finali",
    "guideline":            "Kılavuz/rehber yayını",
    "consultation":         "Kamuoyu görüşüne açılma (consultation paper)",
    "enforcement":          "Yaptırım, ceza, enforcement action",
    "opinion_statement":    "Resmi görüş/açıklama (opinion, statement, Q&A)",
    "deadline_reminder":    "Uyum tarih hatırlatıcısı",
    "mutual_evaluation":    "FATF karşılıklı değerlendirme sonucu",
    "market_update":        "Pazar verisi, istatistik raporu",
}

SEVERITY_LEVELS = {
    "critical": "Acil aksiyon gerektirir; doğrudan ceza/lisans riski",
    "high":     "30 gün içinde değerlendirilmeli; önemli operasyonel etki",
    "medium":   "90 gün içinde planlanmalı; orta vadeli etki",
    "low":      "Bilgilendirme; dolaylı veya uzun vadeli etki",
    "info":     "Genel bilgi; doğrudan aksiyon gerektirmez",
}
```

---

## 6. Kaynak Registry (Source Configuration)

```yaml
# sources/registry.yaml
sources:
  # ── Tier A: Regülatörler & Standart Kurumları ──
  - slug: eba
    name: European Banking Authority
    base_url: https://www.eba.europa.eu
    jurisdiction: [EU]
    crawl_targets:
      - url: /regulation-and-policy/single-rulebook/interactive-single-rulebook
        type: page_list
      - url: /rss/news
        type: rss
      - url: /regulation-and-policy
        type: page_crawl
        depth: 2
    content_selectors:
      title: "h1.page-title"
      body: "div.field-item"
      date: "span.date-display-single"
    crawl_frequency: 6h
    priority: 1

  - slug: esma
    name: European Securities and Markets Authority
    base_url: https://www.esma.europa.eu
    jurisdiction: [EU]
    crawl_targets:
      - url: /press-news/esma-news
        type: page_list
      - url: /document-library
        type: page_list
    crawl_frequency: 6h
    priority: 1

  - slug: fatf
    name: Financial Action Task Force
    base_url: https://www.fatf-gafi.org
    jurisdiction: [GLOBAL]
    crawl_targets:
      - url: /en/publications
        type: page_list
      - url: /en/topics/fatf-recommendations
        type: page_crawl
    crawl_frequency: 12h
    priority: 1

  - slug: ecb
    name: European Central Bank
    base_url: https://www.ecb.europa.eu
    jurisdiction: [EU]
    crawl_targets:
      - url: /press/pr
        type: page_list
      - url: /pub/pub/topic/supervision
        type: page_list
    crawl_frequency: 6h
    priority: 1

  - slug: fca
    name: Financial Conduct Authority
    base_url: https://www.fca.org.uk
    jurisdiction: [UK]
    crawl_targets:
      - url: /news
        type: page_list
      - url: /publications
        type: page_list
    crawl_frequency: 6h
    priority: 1

  - slug: fincen
    name: Financial Crimes Enforcement Network
    base_url: https://www.fincen.gov
    jurisdiction: [US]
    crawl_targets:
      - url: /news-room
        type: page_list
    crawl_frequency: 12h
    priority: 1

  - slug: bis
    name: Bank for International Settlements
    base_url: https://www.bis.org
    jurisdiction: [GLOBAL]
    crawl_targets:
      - url: /bcbs/publications
        type: page_list
      - url: /cpmi/publications
        type: page_list
    crawl_frequency: 24h
    priority: 1

  - slug: eurlex
    name: EUR-Lex (Official Journal)
    base_url: https://eur-lex.europa.eu
    jurisdiction: [EU]
    crawl_targets:
      - url: /oj/direct-access.html
        type: custom  # Needs dedicated parser
    crawl_frequency: 24h
    priority: 1

  # ── Tier B: Ek Kaynaklar (Faz 2'de) ──
  # - slug: eiopa
  # - slug: fsb
  # - slug: iosco
  # - slug: amla (aktif olunca)
  # - slug: spk (Türkiye)
  # - slug: bddk (Türkiye)
```

---

## 7. AI Pipeline Detayları

### 7.1 Özetleme Prompt Şablonu

```python
SUMMARIZE_SYSTEM_PROMPT = """
Sen bir kıdemli RegTech analistsin. Görevin regülatör yayınlarını FinTech compliance
profesyonelleri için özetlemek.

Kurallar:
1. Kısa özet (summary_short): Tam 2-3 cümle. Neyin değiştiğini ve kimi etkilediğini söyle.
2. Detaylı özet (summary_long): 150-300 kelime. Bağlam, teknik detay ve zaman çizelgesi ver.
3. key_takeaways: 3-5 madde, her biri 1 cümle.
4. action_items: Compliance officer'ın yapması gereken somut adımlar.
5. affected_entities: Etkilenen kurum türleri listesi.
6. domains: Uygun domain taxonomy kodları.
7. severity: Aciliyet seviyesi ve gerekçesi.
8. update_type: İçerik türü sınıflandırması.

Yanıtını kesinlikle JSON formatında ver. Markdown veya başka format kullanma.
Spekülatif yorum yapma; sadece kaynaktaki gerçekleri raporla.
Tarihler varsa ISO 8601 formatında yaz.
"""

SUMMARIZE_USER_TEMPLATE = """
Kaynak: {source_name} ({source_slug})
Jurisdiksiyon: {jurisdiction}
Yayın tarihi: {published_at}
Başlık: {title}
URL: {url}

--- İçerik Başlangıç ---
{extracted_text}
--- İçerik Sonu ---

Yukarıdaki regülatör yayınını analiz et ve JSON olarak yanıtla.
"""
```

### 7.2 Etki Skoru Hesaplama

```python
IMPACT_SYSTEM_PROMPT = """
Sen bir compliance impact analistsin. Bir regülasyon güncellemesinin belirli bir
şirket profili üzerindeki etkisini değerlendiriyorsun.

Değerlendirme kriterleri:
- Doğrudan uygulanabilirlik (lisans türü eşleşmesi)
- Jurisdiksiyon örtüşmesi
- Zaman baskısı (deadline yakınlığı)
- Ceza/yaptırım riski
- Operasyonel etki büyüklüğü

Çıktı (JSON):
- impact_score: 0-100 arası tam sayı
- impact_category: 'direct' | 'indirect' | 'monitoring'
- reasoning: 2-3 cümle Türkçe açıklama
- recommended_actions: Somut adımlar listesi (varsa)
"""
```

### 7.3 AI Kullanım Kısıtları

```
- Model: claude-sonnet-4-5-20250929 (maliyet/performans dengesi)
- Max input: 8,000 token per document (truncate with smart extraction)
- Rate limit: Max 50 req/min (Anthropic tier'a göre ayarla)
- Fallback: Eğer API down ise, raw content'i publish et, AI özeti "pending" olarak işaretle
- Cost tracking: Her API çağrısının token kullanımını logla (maliyet kontrolü)
- Caching: Aynı content_hash için tekrar AI çağrısı yapma
```

---

## 8. Özellik Matrisi (MVP vs. V2)

### MVP (Faz 1 — 6 hafta)

| Özellik | Durum | Detay |
|---------|-------|-------|
| 8 regülatör kaynağı crawling | 🔴 TODO | EBA, ESMA, FATF, ECB, FCA, FinCEN, BIS, EUR-Lex |
| AI özetleme (short + long) | 🔴 TODO | Claude Sonnet ile |
| Domain sınıflandırma | 🔴 TODO | 10 domain taxonomy |
| Severity derecelendirme | 🔴 TODO | 5 seviyeli |
| Web dashboard (feed view) | 🔴 TODO | Filtrelenebilir, sıralanabilir liste |
| Keyword search | 🔴 TODO | PostgreSQL full-text search |
| Şirket profili oluşturma | 🔴 TODO | Lisans türü, jurisdiksiyon, ilgi alanları |
| Temel etki skoru | 🔴 TODO | Profil-güncelleme eşleşme skoru |
| Haftalık email digest | 🔴 TODO | Resend + React Email |
| Ücretsiz plan + Stripe entegrasyonu | 🔴 TODO | Free (5 özet/hafta) + Premium ($29/ay) |
| Auth (magic link + Google) | 🔴 TODO | NextAuth v5 |
| Landing page | 🔴 TODO | Conversion-optimized |

### V2 (Faz 2 — +4 hafta)

| Özellik | Detay |
|---------|-------|
| Semantic search | pgvector ile benzer içerik bulma |
| Custom alert rules | Domain + severity + keyword kombinasyonlu alert builder |
| Regulatory timeline/calendar | Yaklaşan deadline'ların görsel takvimi |
| Team plan | Çoklu kullanıcı, shared workspace, API erişim |
| Webhook notifications | Slack, Teams, custom webhook |
| PDF rapor export | Aylık compliance summary raporu |
| Bookmark & notes | Güncelleme üzerine not ekleme |
| Türkçe arayüz | i18n desteği (TR + EN) |

### V3 (Faz 3 — gelecek)

| Özellik | Detay |
|---------|-------|
| Regulatory mapping | Düzenleme → mevcut policy/prosedür eşleştirme |
| Gap analysis | "Şu düzenlemeye uyumlu musun?" self-assessment |
| Compliance score | Genel uyum skoru dashboard'u |
| Enterprise SSO | SAML/OIDC |
| On-prem deployment | Self-hosted option |

---

## 9. API Tasarımı

### 9.1 Public API (Team Plan)

```
Base URL: https://api.regtechradar.com/v1
Auth:     Bearer token (API key, Settings'ten oluşturulur)
Format:   JSON
Rate:     100 req/saat (Team), 1000 req/saat (Enterprise)

GET  /v1/updates
     ?domains=AML_KYC,PAYMENTS
     &jurisdictions=EU,UK
     &severity=critical,high
     &from=2026-01-01
     &to=2026-02-12
     &page=1&per_page=20

GET  /v1/updates/:id
     Detaylı güncelleme (summary, takeaways, impact)

GET  /v1/updates/:id/impact
     ?profile_id=xxx
     Kişiselleştirilmiş etki analizi

GET  /v1/search
     ?q=DORA+subcontracting
     &type=semantic|keyword
     &limit=10

GET  /v1/timeline
     ?from=2026-01-01&to=2026-12-31
     Yaklaşan deadline'lar ve regulatory calendar

GET  /v1/domains
     Domain taxonomy listesi

GET  /v1/sources
     Aktif kaynak listesi ve son crawl zamanları
```

### 9.2 Internal API (BFF — Next.js → Python Backend)

```
POST /internal/crawl/trigger          # Manuel crawl tetikle
GET  /internal/crawl/status           # Crawl durumu
POST /internal/process/:raw_id        # Tek içeriği işle
GET  /internal/stats                  # Admin dashboard istatistikleri
POST /internal/digest/preview         # Digest önizleme oluştur
POST /internal/digest/send            # Digest gönder
```

---

## 10. Email Digest Yapısı

```
📬 RegTech Radar — Haftalık Özet
   Hafta: 3-9 Şubat 2026

   🔴 KRİTİK (2)
   ├── AMLA ilk denetim raporunu yayınladı — doğrudan etkilenen kurumlar listesi
   └── FATF Recommendation 16 güncellemesi — Travel Rule kapsamı genişledi

   🟠 YÜKSEK ÖNEMLİ (5)
   ├── EBA: DORA RTS subcontracting final taslağı
   ├── ESMA: MiCA Level 2 measures Q&A güncellemesi
   ├── FCA: Crypto asset promotions enforcement action
   ├── ECB: Instant payments fraud monitoring guidance
   └── EUR-Lex: PSR trialogue anlaşma metni yayınlandı

   🟡 ORTA (8)
   └── [Liste...]

   📊 Bu Hafta Sayılarla
   ├── 15 yeni güncelleme tespit edildi
   ├── 3 tanesi profilinizi doğrudan etkiliyor
   └── 2 yaklaşan deadline: 28 Şubat (DORA RoI), 1 Mart (MiCA Q1 rapor)

   [Dashboard'da Tümünü Gör →]

   ── Kişiselleştirilmiş Etki ──
   Profiliniz: EMI Lisansı | EU + UK | Payments + Crypto

   ⚡ Sizin için en önemli 3 güncelleme:
   1. PSR trialogue → VoP zorunluluğu genişliyor (Etki: 85/100)
   2. MiCA Level 2 → Custody raporlama detayları (Etki: 72/100)
   3. DORA RTS → Subcontracting kuralları netleşti (Etki: 68/100)
```

---

## 11. Fiyatlandırma & Billing

```
┌─────────────────┬──────────────┬───────────────┬──────────────────┐
│                 │   FREE       │   PRO         │   TEAM           │
├─────────────────┼──────────────┼───────────────┼──────────────────┤
│ Fiyat           │ $0           │ $29/ay        │ $99/ay           │
│ Kullanıcı       │ 1            │ 1             │ 5 (ek $15/kişi)  │
│ Feed erişimi    │ Son 7 gün    │ Tam arşiv     │ Tam arşiv        │
│ AI özet         │ 5/hafta      │ Unlimited     │ Unlimited        │
│ Etki analizi    │ ✗            │ ✓             │ ✓                │
│ Custom alerts   │ 1            │ 10            │ Unlimited        │
│ Email digest    │ Haftalık     │ Günlük option │ Günlük + instant │
│ Search          │ Keyword      │ + Semantic    │ + Semantic       │
│ API erişim      │ ✗            │ ✗             │ ✓ (100 req/saat) │
│ Webhook         │ ✗            │ ✗             │ ✓                │
│ Export (PDF)    │ ✗            │ ✓             │ ✓                │
│ Stripe Price ID │ (free tier)  │ price_xxx     │ price_yyy        │
└─────────────────┴──────────────┴───────────────┴──────────────────┘

Billing: Stripe Checkout + Customer Portal
Trial:   14 gün Pro trial (kredi kartı gerekmez)
```

---

## 12. Geliştirme Kuralları

### 12.1 Kod Stili

```
Python:
  - Formatter: ruff format
  - Linter: ruff check (select = ["E", "F", "I", "N", "W", "UP", "B", "SIM"])
  - Type hints: Her fonksiyonda zorunlu
  - Docstrings: Google style
  - Async: I/O-bound işlemler için async/await tercih et

TypeScript:
  - Strict mode: Evet
  - Formatter: Prettier (printWidth: 100)
  - Linter: ESLint + @typescript-eslint
  - Components: Functional + hooks only (no class components)
  - Naming: PascalCase components, camelCase functions, SCREAMING_SNAKE constants
```

### 12.2 Git Conventions

```
Branch naming:  feat/xxx, fix/xxx, chore/xxx
Commit format:  conventional commits (feat:, fix:, docs:, chore:, refactor:)
PR rules:       - Squash merge only
                - Require 1 approval (solo founder → self-review checklist)
                - All CI checks must pass
                - No direct push to main
```

### 12.3 Güvenlik Kuralları

```
- API anahtarları ve secrets ASLA koda yazılmaz; .env veya secret manager kullan
- Kullanıcı inputu her zaman sanitize et (XSS, SQL injection)
- Rate limiting: Tüm public endpoint'lerde zorunlu
- Crawler: robots.txt'e saygı göster; aggressive crawling yapma
- GDPR: Kullanıcı verisi minimum tut; silme hakkı destekle
- Content: Regülatör içeriğini OLDUĞU GİBİ kaydet; modifiye etme
- AI output: "Bu AI tarafından üretilmiştir" uyarısı ekle
```

### 12.4 Test Stratejisi

```
Unit tests:        Tüm processing fonksiyonları (parser, classifier, dedup)
Integration tests: Source crawlers (fixtures ile, gerçek HTTP çağrısı yok)
E2E tests:         Kritik kullanıcı akışları (signup → profile → feed → digest)
AI tests:          Golden set ile regression test (10 bilinen güncelleme → beklenen çıktı)
Coverage hedefi:   Backend %80+, Frontend %60+
```

---

## 13. Ortam Değişkenleri

```bash
# .env.example

# ── Database ──
DATABASE_URL=postgresql://user:pass@localhost:5432/regtechradar
REDIS_URL=redis://localhost:6379/0

# ── Auth ──
NEXTAUTH_URL=http://localhost:3000
NEXTAUTH_SECRET=generate-with-openssl-rand-base64-32
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=

# ── AI ──
ANTHROPIC_API_KEY=sk-ant-xxx
EMBEDDING_PROVIDER=voyage  # veya 'openai'
VOYAGE_API_KEY=             # veya OPENAI_API_KEY

# ── Email ──
RESEND_API_KEY=re_xxx
FROM_EMAIL=radar@regtechradar.com

# ── Billing ──
STRIPE_SECRET_KEY=sk_test_xxx
STRIPE_WEBHOOK_SECRET=whsec_xxx
STRIPE_PRO_PRICE_ID=price_xxx
STRIPE_TEAM_PRICE_ID=price_yyy

# ── Crawler ──
CRAWLER_USER_AGENT="RegTechRadar/1.0 (+https://regtechradar.com/bot)"
CRAWLER_RESPECT_ROBOTS_TXT=true
CRAWLER_MAX_CONCURRENT=3
CRAWLER_REQUEST_DELAY_MS=2000

# ── Monitoring ──
SENTRY_DSN=
AXIOM_TOKEN=

# ── Feature Flags ──
ENABLE_SEMANTIC_SEARCH=false  # V2'de true yap
ENABLE_WEBHOOKS=false         # V2'de true yap
```

---

## 14. Lansman Kontrol Listesi (MVP)

```
Geliştirme Öncesi:
  [ ] Domain satın al (regtechradar.com / regtechradar.io)
  [ ] Stripe hesabı kur ve ürünleri/fiyatları oluştur
  [ ] Resend domain doğrulamasını yap
  [ ] Vercel + Railway/Fly.io hesapları aç
  [ ] GitHub repo oluştur (monorepo scaffold)

Backend:
  [ ] Source registry YAML'ı tamamla (8 kaynak)
  [ ] İlk 3 crawler'ı yaz ve test et (EBA, FATF, FCA)
  [ ] AI pipeline (summarize + classify) çalışır durumda
  [ ] Celery Beat schedule'ı kur
  [ ] Database migration'ları hazırla
  [ ] Internal API endpoint'leri çalışır durumda
  [ ] Kalan 5 crawler'ı tamamla

Frontend:
  [ ] Auth flow (signup, login, magic link)
  [ ] Company profile setup wizard
  [ ] Feed page (filtreleme, sıralama, pagination)
  [ ] Update detail page
  [ ] Search page
  [ ] Settings + billing (Stripe Customer Portal)
  [ ] Landing page (conversion-optimized)
  [ ] Weekly digest email template

Lansman:
  [ ] 50+ güncelleme seed data ile doldur (geçmiş 2 hafta)
  [ ] İlk haftalık digest'i gönder (beta kullanıcılara)
  [ ] Product Hunt launch hazırlığı
  [ ] LinkedIn announcement yazısı
  [ ] 3 beta müşteri onayı al (testimonial için)
  [ ] Monitoring + alerting kur (Sentry, uptime)
  [ ] GDPR privacy policy + terms of service
```

---

## 15. Başarı Metrikleri (KPI)

```
Lansman sonrası 30 gün:
  - 200+ email subscriber (free tier)
  - 20+ Pro trial başlatma
  - 5+ paying customer ($145+ MRR)
  - Digest open rate > %40
  - Digest click rate > %15

Lansman sonrası 90 gün:
  - 1,000+ subscriber
  - 50+ paying ($1,450+ MRR)
  - 3+ Team plan ($297+ MRR)
  - NPS > 40
  - Churn rate < %8/ay

Ürün sağlığı:
  - Crawl success rate > %95
  - AI summarization quality score > 4/5 (user feedback)
  - Feed freshness: Ortalama güncelleme gecikmesi < 4 saat
  - Uptime > %99.5
```

---

*Bu doküman projenin tek gerçek kaynağıdır (single source of truth). Tüm mimari kararlar, teknoloji seçimleri ve geliştirme standartları burada tanımlanır. Güncellemeler PR ile yapılır.*