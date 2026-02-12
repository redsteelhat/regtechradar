# Geliştirme Kılavuzu

Bu doküman [regtech.md](../regtech.md) Bölüm 12 (Geliştirme Kuralları) ile uyumludur.

---

## Kod stili

### Python (apps/collector)

- **Formatter:** `ruff format`
- **Linter:** `ruff check` (select = E, F, I, N, W, UP, B, SIM)
- **Type hints:** Her fonksiyonda zorunlu
- **Docstrings:** Google style
- **Async:** I/O-bound işlemler için `async`/`await` tercih et

```bash
cd apps/collector
ruff format src
ruff check src
```

### TypeScript (apps/web, packages/shared)

- **Strict mode:** Açık
- **Formatter:** Prettier (printWidth: 100)
- **Linter:** ESLint + @typescript-eslint
- **Components:** Sadece functional + hooks (class component yok)
- **İsimlendirme:** PascalCase (component), camelCase (fonksiyon), SCREAMING_SNAKE (sabit)

```bash
npm run format
npm run lint
```

---

## Git kuralları

- **Branch:** `feat/xxx`, `fix/xxx`, `chore/xxx`
- **Commit:** Conventional commits — `feat:`, `fix:`, `docs:`, `chore:`, `refactor:`
- **PR:** Squash merge; CI geçmeli; doğrudan `main` push yok

Örnek commit mesajları:

```
feat(web): add UpdateCard component
fix(collector): dedup content_hash encoding
docs: update README quick start
chore: add .env.example
```

---

## Güvenlik

- API anahtarları ve secrets koda yazılmaz; `.env` veya secret manager kullan.
- Kullanıcı girdisi her zaman sanitize edilir (XSS, SQL injection).
- Tüm public endpoint’lerde rate limiting zorunlu.
- Crawler: `robots.txt`’e uy; agresif crawl yapma.
- GDPR: Veriyi minimum tut; silme hakkı destekle.
- Regülatör içeriği olduğu gibi kaydedilir; değiştirme.
- AI çıktıları için “Bu AI tarafından üretilmiştir” uyarısı ekle.

---

## Test stratejisi

| Tür | Kapsam |
|-----|--------|
| **Unit** | Tüm processing fonksiyonları (parser, classifier, dedup) |
| **Integration** | Source crawlers (fixtures ile; gerçek HTTP yok) |
| **E2E** | Kritik akışlar: signup → profile → feed → digest |
| **AI** | Golden set ile regression (bilinen güncellemeler → beklenen çıktı) |

Hedef: Backend %80+, Frontend %60+ coverage.

---

## Yerel geliştirme

1. `.env` dosyasını `.env.example`’dan oluştur ve doldur.
2. Web: `npm run dev` (kök dizinde).
3. Collector: Ayrı terminalde `apps/collector` içinde venv kurup `uvicorn src.main:app --reload --port 8000`.
4. Mimari ve veri modeli için [regtech.md](../regtech.md) tek referans dokümandır.
