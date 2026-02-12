# @regtech-radar/shared

Paylaşılan TypeScript tipleri ve sabitler — **regtech.md Bölüm 5.2** taxonomy ile uyumlu.

## İçerik

- **types/** — API ve veri modelleri
  - `regulatory-update` — RegulatoryUpdate, RegulatoryDomain, UpdateType, Severity
  - `impact` — ImpactAssessment, CompanyProfile, ImpactCategory
  - `api` — FeedQueryParams, FeedResponse, SearchResponse, vb.
- **constants/** — Taxonomy ve etiketler
  - `domains` — REGULATORY_DOMAINS, UPDATE_TYPES, SEVERITY_LEVELS + `*_KEYS` dizileri (filtre/dropdown)
  - `jurisdictions` — JURISDICTIONS, JURISDICTION_LABELS

## Kullanım

```ts
import {
  type RegulatoryUpdate,
  type RegulatoryDomain,
  REGULATORY_DOMAINS,
  REGULATORY_DOMAIN_KEYS,
  JURISDICTIONS,
  JURISDICTION_LABELS,
} from '@regtech-radar/shared';
```

## Build

```bash
npm run build
```

`apps/web` bu paketi workspace bağımlılığı ile kullanır; kökten `npm run build` shared’ı önce derler.
