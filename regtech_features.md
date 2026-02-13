# RegTech Radar — Tam Özellik Listesi

> **95 özellik · 11 kategori · 4 geliştirme fazı**
>
> Her özellik şu bilgileri içerir:
> - **Faz:** 🟢 MVP (3-4 hafta) · 🟡 v1.0 (Ay 2-3) · 🟣 v2.0 (Ay 4-6) · 🔴 v3.0 (Ay 7-12)
> - **Öncelik:** 🔴 Must Have · 🟡 Should Have · ⚪ Nice to Have

---

## 1. 📡 Veri Toplama & Kaynak İzleme

| # | Özellik | Faz | Öncelik | Açıklama |
|---|---------|-----|---------|----------|
| 1.1 | Regülatör Sitesi Scraping (EBA, ESMA, FATF, FCA, ECB) | 🟢 MVP | 🔴 Must | Avrupa ve global regülatörlerin resmi duyuru sayfalarını otomatik tarama. RSS, HTML scraping ve sitemap monitoring ile yeni yayınları tespit etme. |
| 1.2 | Official Gazette / Resmi Gazete İzleme | 🟢 MVP | 🔴 Must | AB Official Journal ve ulusal Resmi Gazeteler'den yeni mevzuat yayınlarını otomatik çekme. |
| 1.3 | Konsültasyon & Draft İzleme | 🟡 v1.0 | 🟡 Should | Henüz yürürlüğe girmemiş taslak regülasyonları ve konsültasyon kağıtlarını takip etme. Erken uyarı avantajı sağlar. |
| 1.4 | Ulusal Regülatör Genişleme (BaFin, ACPR, CSSF, CNMV, DNB) | 🟡 v1.0 | 🟡 Should | AB üye ülkelerin ulusal otoritelerinin duyurularını ekleme — MiCA ve DORA'nın ulusal uygulamalarını takip için kritik. |
| 1.5 | US Regülatörler (SEC, FinCEN, OCC, CFPB, Fed) | 🟣 v2.0 | ⚪ Nice | ABD piyasa regülatörlerini ekleme. Global FinTech'ler için AB+US kapsamı. |
| 1.6 | APAC Regülatörler (MAS, HKMA, JFSA, RBA) | 🔴 v3.0 | ⚪ Nice | Asya-Pasifik regülatörlerini ekleme — tam global kapsam. |
| 1.7 | Hukuk Firması & Advisory Yayın Takibi | 🟡 v1.0 | 🟡 Should | EY, Deloitte, DLA Piper, Hogan Lovells gibi Tier-B kaynakların regülasyon yorumlarını takip. |
| 1.8 | Parlamento & Komite Takvimi | 🟣 v2.0 | ⚪ Nice | AB Parlamentosu, ECON komitesi ve ulusal parlamento finansal düzenleme oturumlarını takvime entegre etme. |
| 1.9 | Custom Kaynak Ekleme (URL/RSS) | 🟣 v2.0 | 🟡 Should | Kullanıcıların kendi takip etmek istediği kaynakları (özel blog, sektör derneği vb.) sisteme ekleyebilmesi. |

---

## 2. 🧠 AI İşleme & Analiz Motoru

| # | Özellik | Faz | Öncelik | Açıklama |
|---|---------|-----|---------|----------|
| 2.1 | Otomatik Özetleme (Türkçe & İngilizce) | 🟢 MVP | 🔴 Must | Her yeni regülasyon güncellemesini 2-3 cümlelik yönetici özeti + detaylı analize dönüştürme. Çift dilli destek. |
| 2.2 | Konu Sınıflandırma (DORA, MiCA, AML, PSD3...) | 🟢 MVP | 🔴 Must | Gelen her güncellemeyi otomatik olarak ilgili regülasyon alanına (DORA, MiCA, AML/KYC, PSD3, GDPR, ISO 20022 vb.) kategorize etme. |
| 2.3 | Öncelik Skorlama (1-10) | 🟢 MVP | 🔴 Must | Her güncellemenin aciliyetini 1-10 arası skorlama: deadline yakınlığı, ceza potansiyeli, etkilenen kurum sayısı ve aksiyon gerektirip gerektirmediğine göre. |
| 2.4 | "Bu Seni Nasıl Etkiler" Etki Analizi | 🟡 v1.0 | 🔴 Must | Kullanıcının kurum profiline göre kişiselleştirilmiş etki değerlendirmesi: "Bu güncelleme sizin lisans türünüz için şu maddeleri etkiler." |
| 2.5 | Madde Bazlı Değişiklik Karşılaştırma (Diff) | 🟡 v1.0 | 🟡 Should | Bir regülasyonun önceki ve güncel versiyonları arasındaki değişiklikleri madde bazında highlight etme — ne eklendi, ne çıktı, ne değişti. |
| 2.6 | Cross-Reference Mapping | 🟣 v2.0 | 🟡 Should | Regülasyonlar arası çapraz referans: "DORA Art. 15 → MiCA Art. 45 ile ilişkili", "PSD3 bu DORA maddesiyle çelişebilir" gibi bağlantıları gösterme. |
| 2.7 | Sentiment & Direction Analizi | 🟣 v2.0 | ⚪ Nice | Regülatörün konsültasyon dökümanlarından ve konuşmalarından gelecek düzenleme yönünü tahmin etme — sıkılaştırma mı gevşeme mi bekleniyor. |
| 2.8 | Aksiyon Öğesi Çıkarma (Action Items) | 🟡 v1.0 | 🔴 Must | Her güncellemeden somut aksiyon öğeleri çıkarma: "Vendor sözleşmelerini gözden geçirin", "RoI şablonunu güncelleyin", "Board'a rapor sunun" gibi. |
| 2.9 | Çoklu Dil Desteği (EN, TR, DE, FR, ES) | 🔴 v3.0 | ⚪ Nice | AI özetleme ve analizlerin 5+ dilde sunulması — her kullanıcı kendi dilinde okur. |
| 2.10 | Doğal Dil Soru-Cevap (Chat) | 🟣 v2.0 | 🟡 Should | "DORA kapsamında vendor sözleşmelerinde bulunması gereken minimum klozlar neler?" gibi doğal dilde soru sorabilme. |

---

## 3. 📬 İçerik Dağıtım & Bildirimler

| # | Özellik | Faz | Öncelik | Açıklama |
|---|---------|-----|---------|----------|
| 3.1 | Haftalık Email Digest | 🟢 MVP | 🔴 Must | Her Pazartesi sabahı, geçen haftanın tüm güncellemelerinin öncelik sırasına göre özetlendiği profesyonel email bülteni. |
| 3.2 | Gerçek Zamanlı Email Alert (Kritik) | 🟢 MVP | 🔴 Must | Öncelik skoru 8+ olan güncellemeler için anında email bildirimi — büyük regülasyon değişiklikleri ve yaklaşan deadline'lar için. |
| 3.3 | Web Dashboard | 🟢 MVP | 🔴 Must | Tüm güncellemelerin listelendiği, filtrelenebildiği ve aranabildiği web tabanlı kontrol paneli. |
| 3.4 | Push Notification (Mobil) | 🟡 v1.0 | 🟡 Should | Kritik güncellemeler için mobil push bildirimi — iOS ve Android. |
| 3.5 | Slack / Teams Entegrasyonu | 🟡 v1.0 | 🔴 Must | Güncellemeleri doğrudan Slack kanalına veya MS Teams'e gönderme. Compliance takımının mevcut workflow'una entegre olma. |
| 3.6 | RSS Feed Çıkışı | 🟡 v1.0 | 🟡 Should | Kullanıcıların kendi RSS okuyucularında veya otomasyon araçlarında (Zapier vb.) kullanabileceği feed. |
| 3.7 | Aylık Executive Summary Raporu (PDF) | 🟣 v2.0 | 🟡 Should | Board'a veya C-level'a sunulmaya hazır, önceki ayın regülasyon manzarasını özetleyen profesyonel PDF rapor. |
| 3.8 | WhatsApp Business / Telegram Bot | 🟣 v2.0 | ⚪ Nice | Mesajlaşma uygulamaları üzerinden günlük/haftalık özet gönderme — özellikle MENA ve Türkiye pazarı için. |
| 3.9 | Webhook API | 🟣 v2.0 | 🟡 Should | Kullanıcıların kendi sistemlerine (GRC tool, JIRA, internal portal) güncellemeleri webhook ile aktarabilmesi. |
| 3.10 | Podcast / Audio Digest | 🔴 v3.0 | ⚪ Nice | Haftalık bültenin AI-generated sesli versiyonu — yolda veya egzersiz sırasında dinlenebilir format. |

---

## 4. 🎯 Kişiselleştirme & Profil

| # | Özellik | Faz | Öncelik | Açıklama |
|---|---------|-----|---------|----------|
| 4.1 | Kurum Profili Tanımlama | 🟢 MVP | 🔴 Must | Kullanıcının kurum türünü (banka, EMI, PI, kripto, sigorta, yatırım, FinTech) ve lisans bilgilerini girmesi. Tüm içerik buna göre filtrelenir. |
| 4.2 | Konu Filtresi (Watchlist) | 🟢 MVP | 🔴 Must | Kullanıcının sadece ilgilendiği konuları seçmesi: DORA, MiCA, AML, PSD3, ISO 20022 vb. Gereksiz gürültüyü filtreler. |
| 4.3 | Coğrafya Filtresi | 🟡 v1.0 | 🔴 Must | Operasyon yapılan ülkeleri seçme — sadece ilgili ulusal regülatör güncellemelerini gösterme. |
| 4.4 | Birden Fazla Kurum Profili | 🟣 v2.0 | 🟡 Should | Danışmanlık firmaları ve hukuk büroları için birden fazla müşteri profili oluşturma — her biri farklı filtre seti. |
| 4.5 | Kişisel Bildirim Kuralları | 🟡 v1.0 | 🟡 Should | "DORA ile ilgili öncelik 7+ güncellemeleri anında bildir, MiCA haftalık yeterli" gibi kişisel kural tanımlama. |
| 4.6 | Okuma Geçmişi & İşaretleme | 🟡 v1.0 | 🟡 Should | Okundu/okunmadı durumu, yer imi, not ekleme — kişisel regülasyon takip defteri. |
| 4.7 | İlgi Alanı Öğrenme (AI) | 🟣 v2.0 | ⚪ Nice | Kullanıcının okuma ve etkileşim pattern'lerinden ilgi alanlarını öğrenip öncelik skorlarını kişiselleştirme. |
| 4.8 | Rol Bazlı Görünüm | 🟣 v2.0 | 🟡 Should | CCO (Chief Compliance Officer), CTO, Legal Counsel, Board Member rolleri için farklı detay seviyesinde görünüm. |

---

## 5. 📊 Dashboard & Görselleştirme

| # | Özellik | Faz | Öncelik | Açıklama |
|---|---------|-----|---------|----------|
| 5.1 | Regülasyon Feed (Sonsuz Scroll) | 🟢 MVP | 🔴 Must | Tüm güncellemelerin kronolojik sırada, kart formatında listelendiği ana feed. Filtreler, arama ve sıralama ile. |
| 5.2 | Öncelik Matrisi Görünümü | 🟢 MVP | 🟡 Should | Güncellemeleri Aciliyet × Etki matrisinde 2D grid olarak gösteren görsel — bir bakışta en kritik öğeyi görme. |
| 5.3 | Regülasyon Takvimi (Calendar View) | 🟡 v1.0 | 🔴 Must | Tüm bilinen deadline'ları, yürürlük tarihlerini ve konsültasyon bitiş tarihlerini takvim formatında görme. |
| 5.4 | Compliance Status Board (Kanban) | 🟡 v1.0 | 🟡 Should | "İzleniyor → Değerlendiriliyor → Aksiyon Alınıyor → Tamamlandı" sütunlarıyla Kanban tarzı takip panosu. |
| 5.5 | Regülatör Bazlı Gruplandırma | 🟡 v1.0 | 🟡 Should | Güncellemeleri regülatör bazında gruplandırma — EBA haftada kaç güncelleme yayınlıyor, FATF ne kadar aktif. |
| 5.6 | Trend Analizi Grafikler | 🟣 v2.0 | 🟡 Should | Regülasyon aktivitesi trendleri: hangi alan hızlanıyor (AI regulation artışı gibi), aylık güncelleme hacmi, regülatör bazlı aktivite. |
| 5.7 | Regülasyon İlişki Haritası (Graph) | 🟣 v2.0 | ⚪ Nice | DORA, MiCA, PSD3, AMLA, GDPR arası bağlantıları interaktif graf/ağ diyagramı olarak gösterme. |
| 5.8 | Ceza & Enforcement Tracker | 🟣 v2.0 | 🟡 Should | Verilen cezaları, enforcement action'ları ve emsal kararları takip etme — "Bu maddeyi ihlal eden X kuruma Y ceza verildi." |
| 5.9 | Karşılaştırma Dashboard (Benchmark) | 🔴 v3.0 | ⚪ Nice | Sektördeki diğer kurumlarla anonim uyumluluk seviyesi karşılaştırması — "Sektörün %68'i bu maddeye uyumlu." |
| 5.10 | Executive KPI Widget'ları | 🟣 v2.0 | 🟡 Should | Board-ready KPI'lar: açık aksiyon sayısı, yaklaşan deadline sayısı, ortalama uyumluluk skoru, risk exposure. |

---

## 6. ✅ Uyumluluk Yönetimi & İş Akışları

| # | Özellik | Faz | Öncelik | Açıklama |
|---|---------|-----|---------|----------|
| 6.1 | Aksiyon Öğesi Atama (Task Assignment) | 🟡 v1.0 | 🔴 Must | Her güncellemeden çıkan aksiyon öğelerini takım üyelerine atama, deadline belirleme ve ilerleme takibi. |
| 6.2 | Compliance Checklist Şablonları | 🟡 v1.0 | 🔴 Must | DORA, MiCA, AMLA gibi büyük regülasyonlar için önceden hazırlanmış uyumluluk kontrol listeleri. Madde madde ilerleme takibi. |
| 6.3 | Doküman Yükleme & Eşleştirme | 🟣 v2.0 | 🟡 Should | Politika dokümanlarını yükleyip ilgili regülasyon maddelerine eşleştirme — "Bu politika DORA Art. 5-15'i kapsıyor." |
| 6.4 | Audit Trail & Kanıt Toplama | 🟣 v2.0 | 🔴 Must | Her uyumluluk aksiyonunun tarih, sorumlu ve kanıtıyla birlikte kaydedilmesi — denetçi/regülatör taleplerine hazırlık. |
| 6.5 | Gap Analizi Otomasyonu | 🟣 v2.0 | 🟡 Should | Mevcut uyumluluk durumu ile yeni gereksinim arasındaki farkı otomatik tespit — "Bu yeni madde için 3 ek kontrol gerekiyor." |
| 6.6 | JIRA / Asana / Monday Entegrasyonu | 🟣 v2.0 | 🟡 Should | Aksiyon öğelerini mevcut proje yönetim araçlarına otomatik senkronize etme. |
| 6.7 | Otomatik Hatırlatıcı Zinciri | 🟡 v1.0 | 🟡 Should | Deadline'a 90, 60, 30, 14, 7 ve 1 gün kala otomatik escalation bildirimleri — sorumlu + yönetici + CCO. |
| 6.8 | Board Raporu Generator | 🟣 v2.0 | 🟡 Should | Aylık/çeyreklik compliance board raporunu otomatik oluşturma — açık konular, tamamlananlar, risk exposure, öneriler. |

---

## 7. 👥 Takım & İşbirliği

| # | Özellik | Faz | Öncelik | Açıklama |
|---|---------|-----|---------|----------|
| 7.1 | Takım Üyeleri & Roller | 🟡 v1.0 | 🔴 Must | Admin, Editor, Viewer rolleri ile takım yönetimi. Kim neyi görebilir, kime atama yapabilir. |
| 7.2 | Güncelleme Üzerine Yorum / Tartışma | 🟡 v1.0 | 🟡 Should | Her regülasyon güncellemesi altında takım içi yorum ve tartışma thread'i — "Bu madde bizi nasıl etkiler?" tartışması. |
| 7.3 | İç Bilgi Notu Paylaşımı | 🟡 v1.0 | 🟡 Should | Bir güncelleme hakkında iç analiz notu yazıp takımla paylaşma — kurum içi bilgi bankası oluşturma. |
| 7.4 | Mention & Tagging (@kullanıcı) | 🟣 v2.0 | ⚪ Nice | Yorumlarda ve notlarda takım üyelerini etiketleme — bildirimle dikkat çekme. |
| 7.5 | Paylaşılabilir Bülten (External Share) | 🟣 v2.0 | 🟡 Should | Seçili güncellemeleri kurum dışı paydaşlarla (denetçi, hukuk danışmanı, board) tek tıkla paylaşma — branded PDF veya link. |
| 7.6 | Multi-Tenant (Danışmanlık Modu) | 🔴 v3.0 | 🟡 Should | Hukuk ve danışmanlık firmaları için çoklu müşteri yönetimi — her müşteri ayrı profil, ayrı watchlist, tek panel. |

---

## 8. 🔌 API & Entegrasyonlar

| # | Özellik | Faz | Öncelik | Açıklama |
|---|---------|-----|---------|----------|
| 8.1 | RESTful API (Read) | 🟡 v1.0 | 🔴 Must | Güncellemeleri, kategorileri ve öncelik skorlarını programatik olarak çekebilen API — kullanıcıların kendi dashboard'larına entegre etmesi için. |
| 8.2 | Webhook Endpoints | 🟣 v2.0 | 🟡 Should | Yeni güncelleme, deadline yaklaştığında veya kural tetiklendiğinde dış sistemlere webhook gönderme. |
| 8.3 | Slack App (Native) | 🟡 v1.0 | 🔴 Must | Slack workspace'e kurulabilen native app: kanal seçimi, öncelik filtresi, slash komutları (/regtech-latest). |
| 8.4 | MS Teams App | 🟣 v2.0 | 🟡 Should | Microsoft Teams için native uygulama — kurumsal ortamlarda Slack alternatifi. |
| 8.5 | Zapier / Make Connector | 🟣 v2.0 | 🟡 Should | No-code otomasyon platformlarıyla entegrasyon — "Yeni DORA güncellemesi → Google Sheet'e ekle → Slack'te bildir" gibi akışlar. |
| 8.6 | GRC Platform Entegrasyonları | 🔴 v3.0 | ⚪ Nice | ServiceNow GRC, MetricStream, Archer gibi kurumsal GRC platformlarına veri aktarımı. |
| 8.7 | SSO / SAML Entegrasyonu | 🟣 v2.0 | 🔴 Must | Kurumsal Single Sign-On desteği — Okta, Azure AD, Google Workspace ile giriş. |
| 8.8 | Bulk Export (CSV, JSON, PDF) | 🟡 v1.0 | 🟡 Should | Filtrelenmiş güncellemeleri toplu dışa aktarma — raporlama ve arşivleme için. |

---

## 9. 🔍 Arama & Keşif

| # | Özellik | Faz | Öncelik | Açıklama |
|---|---------|-----|---------|----------|
| 9.1 | Full-Text Arama | 🟢 MVP | 🔴 Must | Tüm güncelleme başlıkları, özetleri ve orijinal metinlerinde hızlı tam metin arama. |
| 9.2 | Gelişmiş Filtreler | 🟢 MVP | 🔴 Must | Regülatör, konu, öncelik, tarih aralığı, durum ve coğrafyaya göre çoklu filtreleme. |
| 9.3 | Kayıtlı Arama & Filtre Setleri | 🟡 v1.0 | 🟡 Should | Sık kullanılan filtre kombinasyonlarını kaydetme — "DORA + EBA + Öncelik 7+ + Son 30 gün" gibi. |
| 9.4 | Semantik Arama (AI) | 🟣 v2.0 | 🟡 Should | Anahtar kelime yerine anlam bazlı arama: "cloud outsourcing riskleri" araması DORA ICT third-party maddelerini bulur. |
| 9.5 | İlgili Güncelleme Önerileri | 🟡 v1.0 | 🟡 Should | Bir güncellemeyi okurken "Bununla İlgili" bölümünde ilişkili önceki güncellemeleri gösterme. |
| 9.6 | Regülasyon Kütüphanesi (Tam Metin) | 🟣 v2.0 | ⚪ Nice | DORA, MiCA, PSD2/3, AMLA gibi temel regülasyonların tam metinlerini aranabilir kütüphane olarak sunma. |

---

## 10. 💰 Monetizasyon & Büyüme

| # | Özellik | Faz | Öncelik | Açıklama |
|---|---------|-----|---------|----------|
| 10.1 | Free Tier (Haftalık Digest) | 🟢 MVP | 🔴 Must | Ücretsiz haftalık email bülteni — top 10 güncelleme özeti. Lead generation ve organik büyüme motoru. |
| 10.2 | Pro Plan ($29/ay) | 🟢 MVP | 🔴 Must | Tam dashboard erişimi, gerçek zamanlı alertler, tüm regülatörler, öncelik skorlama, konu filtreleri. |
| 10.3 | Team Plan ($99/ay, 5 kullanıcı) | 🟡 v1.0 | 🔴 Must | Pro + takım yönetimi, yorum/tartışma, aksiyon atama, Slack entegrasyonu, paylaşılabilir raporlar. |
| 10.4 | Enterprise Plan (Custom) | 🟣 v2.0 | 🟡 Should | Team + SSO, API erişim, custom entegrasyonlar, dedicated account manager, SLA, çoklu profil. |
| 10.5 | Consultant Plan ($199/ay) | 🟣 v2.0 | 🟡 Should | Multi-tenant danışmanlık modu — 10 müşteri profili, white-label raporlar, bulk export. |
| 10.6 | API Access (Usage-Based) | 🟣 v2.0 | 🟡 Should | API çağrı başına fiyatlandırma — diğer platformların RegTech Radar verisini embed etmesi için. |
| 10.7 | Sponsored Content / Partner Listings | 🟡 v1.0 | ⚪ Nice | RegTech vendor'ların çözümlerini ilgili güncelleme bağlamında sponsorlu olarak gösterme (etiketli, etik sınırlar dahilinde). |
| 10.8 | Referral Programı | 🟡 v1.0 | 🟡 Should | Mevcut kullanıcıların yeni kullanıcı getirmesine 1 ay ücretsiz Pro erişim ödülü. |
| 10.9 | Annual Discount (%20) | 🟡 v1.0 | 🔴 Must | Yıllık ödeme seçeneğinde %20 indirim — churn azaltma ve cash flow iyileştirme. |

---

## 11. 🛡️ Altyapı & Güvenlik

| # | Özellik | Faz | Öncelik | Açıklama |
|---|---------|-----|---------|----------|
| 11.1 | HTTPS / TLS 1.3 Encryption | 🟢 MVP | 🔴 Must | Tüm veri iletişiminde end-to-end şifreleme. |
| 11.2 | GDPR Uyumluluk | 🟢 MVP | 🔴 Must | Kullanıcı verisi işleme, consent yönetimi, data export/delete hakları — bir RegTech ürünü olarak GDPR uyumlu olmak zorunlu. |
| 11.3 | Rate Limiting & DDoS Koruması | 🟢 MVP | 🔴 Must | API ve web dashboard için rate limiting, Cloudflare veya benzeri DDoS koruması. |
| 11.4 | Uptime SLA (%99.5+) | 🟡 v1.0 | 🔴 Must | Monitoring, alerting ve automated failover ile minimum %99.5 uptime garantisi. |
| 11.5 | SOC 2 Type II Hazırlık | 🟣 v2.0 | 🟡 Should | Enterprise müşteriler için SOC 2 uyumluluk sürecini başlatma — trust center oluşturma. |
| 11.6 | Data Residency Seçenekleri (EU/US) | 🔴 v3.0 | ⚪ Nice | Veri lokasyonu seçimi — AB müşterileri için EU-only hosting garantisi. |
| 11.7 | 2FA / MFA Desteği | 🟡 v1.0 | 🔴 Must | İki faktörlü kimlik doğrulama — TOTP ve SMS. |
| 11.8 | Audit Log (Admin) | 🟣 v2.0 | 🟡 Should | Tüm kullanıcı aksiyonlarının loglanması — kim ne zaman ne yaptı. |

---

## Faz Bazlı Özet

| Faz | Özellik Sayısı | Zaman Dilimi | Odak |
|-----|---------------|--------------|------|
| 🟢 MVP | 17 | 3-4 hafta | Scraping + AI özetleme + email digest + web dashboard + Free/Pro plan |
| 🟡 v1.0 | 30 | Ay 2-3 | Etki analizi + aksiyon yönetimi + Slack + takım + takvim + Team plan |
| 🟣 v2.0 | 33 | Ay 4-6 | Semantik arama + audit trail + SSO + board raporu + Enterprise plan |
| 🔴 v3.0 | 15 | Ay 7-12 | Global kapsam + çoklu dil + GRC entegrasyon + danışmanlık modu |

---

## Öncelik Bazlı Özet

| Öncelik | Sayı | Açıklama |
|---------|------|----------|
| 🔴 Must Have | 35 | Ürünün çalışması ve gelir üretmesi için şart olan özellikler |
| 🟡 Should Have | 42 | Rekabet avantajı ve müşteri tutma için önemli özellikler |
| ⚪ Nice to Have | 18 | Fark yaratan ama ertelenebilir özellikler |

---

## Strateji Notu

> **MVP'de 17 özellikle lansman yap**, haftalık email digest ile ücretsiz kullanıcı topla. **v1.0'da 30 özellikle ücretli plana geç** (Pro $29/ay + Team $99/ay). **v2.0'da 33 özellikle enterprise'a genişle.** v3.0'daki 15 özellik global platform vizyonu için — ilk gelirler geldikten sonra.