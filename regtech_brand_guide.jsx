import { useState } from "react";

const BRAND = {
    colors: {
        primary: { name: "Radar Navy", hex: "#0B1628", rgb: "11, 22, 40", usage: "Ana arka plan, header, footer, metin ağırlığı" },
        primaryLight: { name: "Deep Slate", hex: "#162038", rgb: "22, 32, 56", usage: "Kartlar, paneller, ikincil yüzeyler" },
        accent: { name: "Signal Cyan", hex: "#00E5CC", rgb: "0, 229, 204", usage: "CTA butonlar, aktif durumlar, vurgular, logo aksan" },
        accentMuted: { name: "Muted Teal", hex: "#0A7E72", rgb: "10, 126, 114", usage: "Hover durumları, ikincil aksanlar, linkler" },
        alert: { name: "Regulatory Amber", hex: "#F59E0B", rgb: "245, 158, 11", usage: "Uyarılar, deadline bildirimleri, acil güncellemeler" },
        alertSoft: { name: "Warm Gold", hex: "#FCD34D", rgb: "252, 211, 77", usage: "Hafif vurgular, badge arka planları" },
        danger: { name: "Compliance Red", hex: "#EF4444", rgb: "239, 68, 68", usage: "Kritik uyarılar, son tarih geçişleri, hata durumları" },
        success: { name: "Cleared Green", hex: "#10B981", rgb: "16, 185, 129", usage: "Onay durumları, uyumlu göstergeleri, başarı mesajları" },
        text: { name: "Cloud White", hex: "#F1F5F9", rgb: "241, 245, 249", usage: "Başlıklar, birincil metin (koyu arka plan üzerinde)" },
        textSecondary: { name: "Slate Gray", hex: "#94A3B8", rgb: "148, 163, 184", usage: "İkincil metin, açıklamalar, placeholder" },
        textTertiary: { name: "Dim Slate", hex: "#475569", rgb: "71, 85, 105", usage: "Devre dışı durumlar, footnote, çizgi renkleri" },
        surface: { name: "Panel Dark", hex: "#1E293B", rgb: "30, 41, 59", usage: "Input alanları, dropdown menüler, modal arka plan" },
        white: { name: "Pure White", hex: "#FFFFFF", rgb: "255, 255, 255", usage: "Açık tema metin, beyaz logo versiyonu" },
    },
    fonts: {
        display: { name: "DM Sans", weight: "700, 800", usage: "Logo tipi, büyük başlıklar (H1, H2), hero text" },
        body: { name: "IBM Plex Sans", weight: "400, 500, 600", usage: "Gövde metin, paragraflar, UI elementleri" },
        mono: { name: "JetBrains Mono", weight: "400, 500", usage: "Kod blokları, regülasyon numaraları, teknik referanslar" },
    }
};

const Logo = ({ size = 1, theme = "dark", showText = true, showTagline = false }) => {
    const s = size;
    const isDark = theme === "dark";
    const bg = isDark ? "transparent" : "transparent";
    const textColor = isDark ? "#F1F5F9" : "#0B1628";
    const subtextColor = isDark ? "#94A3B8" : "#475569";

    return (
        <div style={{ display: "inline-flex", alignItems: "center", gap: 10 * s, background: bg }}>
            <svg width={40 * s} height={40 * s} viewBox="0 0 40 40" fill="none">
                {/* Outer radar ring */}
                <circle cx="20" cy="20" r="18" stroke="#0A7E72" strokeWidth="1.5" strokeDasharray="3 3" opacity="0.5" />
                {/* Middle radar ring */}
                <circle cx="20" cy="20" r="12" stroke="#00E5CC" strokeWidth="1.5" strokeDasharray="2 2" opacity="0.7" />
                {/* Inner solid circle */}
                <circle cx="20" cy="20" r="6" fill="#00E5CC" opacity="0.15" />
                <circle cx="20" cy="20" r="3" fill="#00E5CC" />
                {/* Radar sweep */}
                <path d="M20 20 L20 2" stroke="#00E5CC" strokeWidth="2" strokeLinecap="round" opacity="0.9">
                    <animateTransform attributeName="transform" type="rotate" from="0 20 20" to="360 20 20" dur="4s" repeatCount="indefinite" />
                </path>
                {/* Sweep glow */}
                <path d="M20 20 L20 2 A18 18 0 0 1 35 10 Z" fill="url(#sweepGrad)" opacity="0.15">
                    <animateTransform attributeName="transform" type="rotate" from="0 20 20" to="360 20 20" dur="4s" repeatCount="indefinite" />
                </path>
                {/* Detection blips */}
                <circle cx="28" cy="10" r="2" fill="#F59E0B" opacity="0.9">
                    <animate attributeName="opacity" values="0.9;0.3;0.9" dur="2s" repeatCount="indefinite" />
                </circle>
                <circle cx="11" cy="14" r="1.5" fill="#00E5CC" opacity="0.7">
                    <animate attributeName="opacity" values="0.7;0.2;0.7" dur="3s" repeatCount="indefinite" />
                </circle>
                <circle cx="30" cy="26" r="1.5" fill="#EF4444" opacity="0.8">
                    <animate attributeName="opacity" values="0.8;0.3;0.8" dur="2.5s" repeatCount="indefinite" />
                </circle>
                <defs>
                    <linearGradient id="sweepGrad" x1="20" y1="2" x2="35" y2="10">
                        <stop offset="0%" stopColor="#00E5CC" stopOpacity="1" />
                        <stop offset="100%" stopColor="#00E5CC" stopOpacity="0" />
                    </linearGradient>
                </defs>
            </svg>
            {showText && (
                <div style={{ display: "flex", flexDirection: "column" }}>
                    <span style={{
                        fontFamily: "'DM Sans', sans-serif",
                        fontSize: 20 * s, fontWeight: 800,
                        color: textColor, letterSpacing: -0.5 * s, lineHeight: 1.1
                    }}>
                        Reg<span style={{ color: "#00E5CC" }}>Tech</span> Radar
                    </span>
                    {showTagline && (
                        <span style={{
                            fontFamily: "'IBM Plex Sans', sans-serif",
                            fontSize: 9.5 * s, fontWeight: 500, color: subtextColor,
                            letterSpacing: 2 * s, textTransform: "uppercase", marginTop: 2 * s
                        }}>
                            Regulatory Intelligence
                        </span>
                    )}
                </div>
            )}
        </div>
    );
};

const ColorSwatch = ({ color, large }) => (
    <div style={{
        display: "flex", flexDirection: "column", gap: 6,
        minWidth: large ? 140 : 100
    }}>
        <div style={{
            width: "100%", height: large ? 72 : 52, borderRadius: 10,
            background: color.hex,
            border: color.hex === "#FFFFFF" ? "1px solid #334155" : color.hex === "#0B1628" ? "1px solid #1E293B" : "none",
            boxShadow: "0 2px 8px rgba(0,0,0,0.3)"
        }} />
        <div>
            <div style={{ fontSize: 12, fontWeight: 700, color: "#F1F5F9", fontFamily: "'DM Sans', sans-serif" }}>{color.name}</div>
            <div style={{ fontSize: 11, color: "#94A3B8", fontFamily: "'JetBrains Mono', monospace" }}>{color.hex}</div>
            {large && <div style={{ fontSize: 10, color: "#475569", marginTop: 2, lineHeight: 1.4, fontFamily: "'IBM Plex Sans', sans-serif" }}>{color.usage}</div>}
        </div>
    </div>
);

const sections = [
    { id: "logo", label: "Logo" },
    { id: "colors", label: "Renkler" },
    { id: "typo", label: "Tipografi" },
    { id: "usage", label: "Kullanım Kuralları" },
    { id: "icons", label: "İkonografi" },
    { id: "voice", label: "Marka Sesi" },
];

export default function BrandGuide() {
    const [activeSection, setActiveSection] = useState("logo");

    return (
        <div style={{
            minHeight: "100vh",
            background: "#0B1628",
            fontFamily: "'IBM Plex Sans', sans-serif",
            color: "#F1F5F9"
        }}>
            <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=IBM+Plex+Sans:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet" />

            {/* Top Bar */}
            <div style={{
                padding: "20px 28px",
                borderBottom: "1px solid rgba(0,229,204,0.1)",
                display: "flex", alignItems: "center", justifyContent: "space-between",
                background: "linear-gradient(180deg, rgba(0,229,204,0.04) 0%, transparent 100%)"
            }}>
                <Logo size={0.85} theme="dark" showTagline={false} />
                <span style={{
                    fontSize: 11, fontWeight: 600, color: "#0A7E72",
                    letterSpacing: 2, textTransform: "uppercase",
                    padding: "5px 12px", borderRadius: 6,
                    border: "1px solid rgba(0,229,204,0.2)",
                    background: "rgba(0,229,204,0.05)"
                }}>Brand Identity Guide</span>
            </div>

            {/* Navigation */}
            <div style={{
                display: "flex", gap: 4, padding: "12px 28px",
                borderBottom: "1px solid rgba(148,163,184,0.08)",
                overflowX: "auto"
            }}>
                {sections.map(s => (
                    <button key={s.id} onClick={() => setActiveSection(s.id)} style={{
                        padding: "7px 16px", borderRadius: 8, border: "none",
                        background: activeSection === s.id ? "rgba(0,229,204,0.12)" : "transparent",
                        color: activeSection === s.id ? "#00E5CC" : "#94A3B8",
                        fontSize: 13, fontWeight: 600, cursor: "pointer",
                        transition: "all 0.2s", whiteSpace: "nowrap",
                        fontFamily: "'IBM Plex Sans', sans-serif"
                    }}>{s.label}</button>
                ))}
            </div>

            {/* Content */}
            <div style={{ padding: "28px", maxWidth: 920, margin: "0 auto" }}>

                {/* ===== LOGO ===== */}
                {activeSection === "logo" && (
                    <div>
                        <h2 style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 26, fontWeight: 800, margin: "0 0 6px" }}>
                            Logo Sistemi
                        </h2>
                        <p style={{ color: "#94A3B8", fontSize: 14, margin: "0 0 28px", lineHeight: 1.6 }}>
                            Logo, düzenleyici değişiklikleri sürekli tarayan bir radar konseptini yansıtır. Dönen tarama çizgisi aktif izlemeyi, renkli noktalar (blip) farklı öncelik seviyelerindeki güncellemeleri temsil eder.
                        </p>

                        {/* Primary Logo - Dark */}
                        <div style={{
                            padding: "40px", borderRadius: 16, marginBottom: 16,
                            background: "#0B1628", border: "1px solid rgba(0,229,204,0.12)",
                            textAlign: "center"
                        }}>
                            <span style={{ fontSize: 10, color: "#475569", letterSpacing: 2, textTransform: "uppercase", fontWeight: 600 }}>Birincil Logo — Koyu Arka Plan</span>
                            <div style={{ marginTop: 20, display: "flex", justifyContent: "center" }}>
                                <Logo size={1.8} theme="dark" showTagline={true} />
                            </div>
                        </div>

                        {/* Primary Logo - Light */}
                        <div style={{
                            padding: "40px", borderRadius: 16, marginBottom: 16,
                            background: "#F8FAFC", border: "1px solid #E2E8F0",
                            textAlign: "center"
                        }}>
                            <span style={{ fontSize: 10, color: "#94A3B8", letterSpacing: 2, textTransform: "uppercase", fontWeight: 600 }}>Birincil Logo — Açık Arka Plan</span>
                            <div style={{ marginTop: 20, display: "flex", justifyContent: "center" }}>
                                <Logo size={1.8} theme="light" showTagline={true} />
                            </div>
                        </div>

                        {/* Variations */}
                        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: 12, marginTop: 16 }}>
                            {/* Icon only */}
                            <div style={{
                                padding: "28px", borderRadius: 14, textAlign: "center",
                                background: "#162038", border: "1px solid rgba(148,163,184,0.08)"
                            }}>
                                <span style={{ fontSize: 10, color: "#475569", letterSpacing: 1.5, textTransform: "uppercase", fontWeight: 600 }}>Sadece İkon</span>
                                <div style={{ marginTop: 16, display: "flex", justifyContent: "center" }}>
                                    <Logo size={1.5} theme="dark" showText={false} />
                                </div>
                                <p style={{ fontSize: 10, color: "#64748b", marginTop: 12 }}>Favicon, app icon, sosyal medya profil</p>
                            </div>
                            {/* Wordmark only */}
                            <div style={{
                                padding: "28px", borderRadius: 14, textAlign: "center",
                                background: "#162038", border: "1px solid rgba(148,163,184,0.08)"
                            }}>
                                <span style={{ fontSize: 10, color: "#475569", letterSpacing: 1.5, textTransform: "uppercase", fontWeight: 600 }}>Sadece Yazı</span>
                                <div style={{ marginTop: 20, display: "flex", justifyContent: "center" }}>
                                    <span style={{
                                        fontFamily: "'DM Sans', sans-serif",
                                        fontSize: 26, fontWeight: 800, color: "#F1F5F9", letterSpacing: -0.5
                                    }}>Reg<span style={{ color: "#00E5CC" }}>Tech</span> Radar</span>
                                </div>
                                <p style={{ fontSize: 10, color: "#64748b", marginTop: 12 }}>Email header, footer, küçük alanlar</p>
                            </div>
                            {/* Monochrome */}
                            <div style={{
                                padding: "28px", borderRadius: 14, textAlign: "center",
                                background: "#162038", border: "1px solid rgba(148,163,184,0.08)"
                            }}>
                                <span style={{ fontSize: 10, color: "#475569", letterSpacing: 1.5, textTransform: "uppercase", fontWeight: 600 }}>Monokrom</span>
                                <div style={{ marginTop: 20, display: "flex", justifyContent: "center" }}>
                                    <span style={{
                                        fontFamily: "'DM Sans', sans-serif",
                                        fontSize: 26, fontWeight: 800, color: "#F1F5F9", letterSpacing: -0.5
                                    }}>RegTech Radar</span>
                                </div>
                                <p style={{ fontSize: 10, color: "#64748b", marginTop: 12 }}>Baskı, tek renk kullanım</p>
                            </div>
                        </div>

                        {/* Logo Construction */}
                        <div style={{
                            marginTop: 24, padding: "24px", borderRadius: 14,
                            background: "rgba(0,229,204,0.04)", border: "1px solid rgba(0,229,204,0.1)"
                        }}>
                            <h4 style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 14, fontWeight: 700, color: "#00E5CC", margin: "0 0 12px" }}>Logo Anatomisi</h4>
                            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16, fontSize: 13, color: "#94A3B8", lineHeight: 1.7 }}>
                                <div>
                                    <p style={{ margin: "0 0 8px" }}><span style={{ color: "#00E5CC", fontWeight: 600 }}>Radar İkonu:</span> Üç eş merkezli halka (dış: kesikli/pasif izleme, orta: aktif tarama, iç: odak noktası). Dönen tarama çizgisi canlılık ve sürekli izlemeyi ifade eder.</p>
                                    <p style={{ margin: 0 }}><span style={{ color: "#F59E0B", fontWeight: 600 }}>Blip Noktaları:</span> Cyan = bilgi, Amber = uyarı, Red = kritik. Regülasyon güncellemelerinin öncelik seviyelerini temsil eder.</p>
                                </div>
                                <div>
                                    <p style={{ margin: "0 0 8px" }}><span style={{ color: "#F1F5F9", fontWeight: 600 }}>Tipografi:</span> "Reg" beyaz, "Tech" Signal Cyan, "Radar" beyaz. Cyan vurgusu teknoloji ve inovasyon odağını belirtir.</p>
                                    <p style={{ margin: 0 }}><span style={{ color: "#F1F5F9", fontWeight: 600 }}>Tagline:</span> "REGULATORY INTELLIGENCE" — spaced uppercase, IBM Plex Sans Medium. Sadece yeterli alan olduğunda kullanılır.</p>
                                </div>
                            </div>
                        </div>
                    </div>
                )}

                {/* ===== COLORS ===== */}
                {activeSection === "colors" && (
                    <div>
                        <h2 style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 26, fontWeight: 800, margin: "0 0 6px" }}>
                            Renk Paleti
                        </h2>
                        <p style={{ color: "#94A3B8", fontSize: 14, margin: "0 0 28px", lineHeight: 1.6 }}>
                            Koyu, otoriter bir zemin üzerine yüksek kontrastlı sinyal renkleri. Finansal güvenilirlik + teknolojik kesinlik izlenimi yaratır.
                        </p>

                        {/* Primary */}
                        <h4 style={{ fontSize: 12, fontWeight: 700, color: "#475569", letterSpacing: 2, margin: "0 0 12px", textTransform: "uppercase" }}>Birincil Renkler</h4>
                        <div style={{ display: "flex", gap: 16, flexWrap: "wrap", marginBottom: 28 }}>
                            <ColorSwatch color={BRAND.colors.primary} large />
                            <ColorSwatch color={BRAND.colors.primaryLight} large />
                            <ColorSwatch color={BRAND.colors.accent} large />
                            <ColorSwatch color={BRAND.colors.accentMuted} large />
                        </div>

                        {/* Signal Colors */}
                        <h4 style={{ fontSize: 12, fontWeight: 700, color: "#475569", letterSpacing: 2, margin: "0 0 12px", textTransform: "uppercase" }}>Sinyal Renkleri (Durum & Uyarı)</h4>
                        <div style={{ display: "flex", gap: 16, flexWrap: "wrap", marginBottom: 28 }}>
                            <ColorSwatch color={BRAND.colors.alert} large />
                            <ColorSwatch color={BRAND.colors.alertSoft} large />
                            <ColorSwatch color={BRAND.colors.danger} large />
                            <ColorSwatch color={BRAND.colors.success} large />
                        </div>

                        {/* Neutrals */}
                        <h4 style={{ fontSize: 12, fontWeight: 700, color: "#475569", letterSpacing: 2, margin: "0 0 12px", textTransform: "uppercase" }}>Nötr Tonlar & Metin</h4>
                        <div style={{ display: "flex", gap: 16, flexWrap: "wrap", marginBottom: 28 }}>
                            <ColorSwatch color={BRAND.colors.text} large />
                            <ColorSwatch color={BRAND.colors.textSecondary} large />
                            <ColorSwatch color={BRAND.colors.textTertiary} large />
                            <ColorSwatch color={BRAND.colors.surface} large />
                            <ColorSwatch color={BRAND.colors.white} large />
                        </div>

                        {/* Ratio Guide */}
                        <div style={{
                            padding: "20px 24px", borderRadius: 14,
                            background: "#162038", border: "1px solid rgba(148,163,184,0.08)"
                        }}>
                            <h4 style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 14, fontWeight: 700, margin: "0 0 14px", color: "#F1F5F9" }}>Renk Kullanım Oranları</h4>
                            <div style={{ display: "flex", height: 32, borderRadius: 8, overflow: "hidden", marginBottom: 12 }}>
                                <div style={{ width: "45%", background: "#0B1628", display: "flex", alignItems: "center", justifyContent: "center", fontSize: 10, fontWeight: 600, color: "#94A3B8" }}>%45</div>
                                <div style={{ width: "25%", background: "#162038", display: "flex", alignItems: "center", justifyContent: "center", fontSize: 10, fontWeight: 600, color: "#94A3B8" }}>%25</div>
                                <div style={{ width: "15%", background: "#1E293B", display: "flex", alignItems: "center", justifyContent: "center", fontSize: 10, fontWeight: 600, color: "#94A3B8" }}>%15</div>
                                <div style={{ width: "10%", background: "#00E5CC", display: "flex", alignItems: "center", justifyContent: "center", fontSize: 10, fontWeight: 700, color: "#0B1628" }}>%10</div>
                                <div style={{ width: "5%", background: "#F59E0B", display: "flex", alignItems: "center", justifyContent: "center", fontSize: 9, fontWeight: 700, color: "#0B1628" }}>%5</div>
                            </div>
                            <div style={{ display: "flex", gap: 16, fontSize: 11, color: "#94A3B8", flexWrap: "wrap" }}>
                                <span><span style={{ color: "#F1F5F9", fontWeight: 600 }}>Radar Navy:</span> Dominant zemin</span>
                                <span><span style={{ color: "#F1F5F9", fontWeight: 600 }}>Deep Slate:</span> Kartlar & paneller</span>
                                <span><span style={{ color: "#F1F5F9", fontWeight: 600 }}>Panel Dark:</span> İnput & yüzeyler</span>
                                <span><span style={{ color: "#00E5CC", fontWeight: 600 }}>Signal Cyan:</span> Aksiyonlar & vurgular</span>
                                <span><span style={{ color: "#F59E0B", fontWeight: 600 }}>Amber/Red:</span> Uyarılar</span>
                            </div>
                        </div>
                    </div>
                )}

                {/* ===== TYPOGRAPHY ===== */}
                {activeSection === "typo" && (
                    <div>
                        <h2 style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 26, fontWeight: 800, margin: "0 0 6px" }}>
                            Tipografi
                        </h2>
                        <p style={{ color: "#94A3B8", fontSize: 14, margin: "0 0 28px", lineHeight: 1.6 }}>
                            Üç fontluk bir sistem: otoriter başlıklar, okunabilir gövde, ve teknik referanslar için monospace.
                        </p>

                        {/* DM Sans */}
                        <div style={{
                            padding: "28px", borderRadius: 14, marginBottom: 16,
                            background: "#162038", border: "1px solid rgba(148,163,184,0.08)"
                        }}>
                            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 16, flexWrap: "wrap", gap: 8 }}>
                                <div>
                                    <span style={{ fontSize: 11, color: "#00E5CC", fontWeight: 600, letterSpacing: 2, textTransform: "uppercase" }}>Display Font</span>
                                    <h3 style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 32, fontWeight: 800, margin: "4px 0 0" }}>DM Sans</h3>
                                </div>
                                <div style={{ textAlign: "right" }}>
                                    <div style={{ fontSize: 11, color: "#475569" }}>Ağırlıklar: 700, 800</div>
                                    <div style={{ fontSize: 11, color: "#475569" }}>Google Fonts — Ücretsiz</div>
                                </div>
                            </div>
                            <div style={{ fontFamily: "'DM Sans', sans-serif" }}>
                                <div style={{ fontSize: 36, fontWeight: 800, color: "#F1F5F9", marginBottom: 6 }}>H1 — Regulation Update</div>
                                <div style={{ fontSize: 24, fontWeight: 800, color: "#F1F5F9", marginBottom: 6 }}>H2 — DORA Compliance Deadline</div>
                                <div style={{ fontSize: 18, fontWeight: 700, color: "#F1F5F9", marginBottom: 6 }}>H3 — MiCA Level 2 Measures</div>
                                <div style={{ fontSize: 14, fontWeight: 700, color: "#F1F5F9" }}>H4 — Impact Assessment Score</div>
                            </div>
                            <p style={{ fontSize: 11, color: "#475569", marginTop: 14, marginBottom: 0 }}>Kullanım: Logo tipi, sayfa başlıkları, hero alanları, bülten konuları, dashboard widget başlıkları</p>
                        </div>

                        {/* IBM Plex Sans */}
                        <div style={{
                            padding: "28px", borderRadius: 14, marginBottom: 16,
                            background: "#162038", border: "1px solid rgba(148,163,184,0.08)"
                        }}>
                            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 16, flexWrap: "wrap", gap: 8 }}>
                                <div>
                                    <span style={{ fontSize: 11, color: "#F59E0B", fontWeight: 600, letterSpacing: 2, textTransform: "uppercase" }}>Body Font</span>
                                    <h3 style={{ fontFamily: "'IBM Plex Sans', sans-serif", fontSize: 32, fontWeight: 600, margin: "4px 0 0" }}>IBM Plex Sans</h3>
                                </div>
                                <div style={{ textAlign: "right" }}>
                                    <div style={{ fontSize: 11, color: "#475569" }}>Ağırlıklar: 400, 500, 600</div>
                                    <div style={{ fontSize: 11, color: "#475569" }}>Google Fonts — Ücretsiz</div>
                                </div>
                            </div>
                            <div style={{ fontFamily: "'IBM Plex Sans', sans-serif" }}>
                                <p style={{ fontSize: 16, fontWeight: 400, color: "#CBD5E1", lineHeight: 1.7, margin: "0 0 10px" }}>
                                    Regular 400 — Avrupa Bankacılık Otoritesi (EBA), DORA kapsamında ICT risk yönetimi çerçevesini güncelleyerek üçüncü taraf hizmet sağlayıcı denetim gereksinimlerini genişletti.
                                </p>
                                <p style={{ fontSize: 14, fontWeight: 500, color: "#94A3B8", lineHeight: 1.6, margin: "0 0 10px" }}>
                                    Medium 500 — Bu güncelleme, finansal kuruluşların mevcut vendor sözleşmelerini Nisan 2026'ya kadar yeniden gözden geçirmesini zorunlu kılıyor.
                                </p>
                                <p style={{ fontSize: 13, fontWeight: 600, color: "#F1F5F9", margin: 0 }}>
                                    SemiBold 600 — UI butonları, etiketler, navigasyon öğeleri ve vurgulanan paragraflar.
                                </p>
                            </div>
                        </div>

                        {/* JetBrains Mono */}
                        <div style={{
                            padding: "28px", borderRadius: 14,
                            background: "#162038", border: "1px solid rgba(148,163,184,0.08)"
                        }}>
                            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 16, flexWrap: "wrap", gap: 8 }}>
                                <div>
                                    <span style={{ fontSize: 11, color: "#10B981", fontWeight: 600, letterSpacing: 2, textTransform: "uppercase" }}>Monospace Font</span>
                                    <h3 style={{ fontFamily: "'JetBrains Mono', monospace", fontSize: 28, fontWeight: 500, margin: "4px 0 0" }}>JetBrains Mono</h3>
                                </div>
                                <div style={{ textAlign: "right" }}>
                                    <div style={{ fontSize: 11, color: "#475569" }}>Ağırlıklar: 400, 500</div>
                                    <div style={{ fontSize: 11, color: "#475569" }}>Google Fonts — Ücretsiz</div>
                                </div>
                            </div>
                            <div style={{ fontFamily: "'JetBrains Mono', monospace", fontSize: 13, color: "#94A3B8", lineHeight: 1.8 }}>
                                <div>EU 2022/2554  —  DORA Regulation</div>
                                <div>EU 2024/1624  —  AML Regulation</div>
                                <div>Art. 15(3)    —  ICT Third-Party Risk</div>
                                <div style={{ color: "#00E5CC" }}>deadline: 2026-04-17T23:59:00Z</div>
                            </div>
                            <p style={{ fontSize: 11, color: "#475569", marginTop: 14, marginBottom: 0, fontFamily: "'IBM Plex Sans', sans-serif" }}>Kullanım: Regülasyon numaraları, tarihler, API referansları, kod blokları, teknik tanımlayıcılar</p>
                        </div>

                        {/* Scale */}
                        <div style={{
                            marginTop: 16, padding: "20px 24px", borderRadius: 14,
                            background: "rgba(0,229,204,0.04)", border: "1px solid rgba(0,229,204,0.1)"
                        }}>
                            <h4 style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 14, fontWeight: 700, margin: "0 0 12px", color: "#00E5CC" }}>Boyut Skalası</h4>
                            <div style={{ display: "grid", gridTemplateColumns: "auto 1fr auto", gap: "6px 20px", fontSize: 12, alignItems: "baseline" }}>
                                {[
                                    ["H1", "36px / 800", "DM Sans"],
                                    ["H2", "24px / 800", "DM Sans"],
                                    ["H3", "18px / 700", "DM Sans"],
                                    ["H4", "14px / 700", "DM Sans"],
                                    ["Body L", "16px / 400", "IBM Plex Sans"],
                                    ["Body M", "14px / 400-500", "IBM Plex Sans"],
                                    ["Body S", "13px / 500", "IBM Plex Sans"],
                                    ["Caption", "11px / 500", "IBM Plex Sans"],
                                    ["Code", "13px / 400", "JetBrains Mono"],
                                ].map(([label, size, font], i) => (
                                    <>
                                        <span key={`l${i}`} style={{ color: "#00E5CC", fontWeight: 600, fontFamily: "'JetBrains Mono', monospace", fontSize: 11 }}>{label}</span>
                                        <span key={`s${i}`} style={{ color: "#94A3B8", fontFamily: "'JetBrains Mono', monospace", fontSize: 11 }}>{size}</span>
                                        <span key={`f${i}`} style={{ color: "#475569", fontSize: 11 }}>{font}</span>
                                    </>
                                ))}
                            </div>
                        </div>
                    </div>
                )}

                {/* ===== USAGE RULES ===== */}
                {activeSection === "usage" && (
                    <div>
                        <h2 style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 26, fontWeight: 800, margin: "0 0 6px" }}>
                            Kullanım Kuralları
                        </h2>
                        <p style={{ color: "#94A3B8", fontSize: 14, margin: "0 0 28px", lineHeight: 1.6 }}>
                            Marka tutarlılığını korumak için uyulması gereken temel kurallar.
                        </p>

                        {/* Do's */}
                        <div style={{
                            padding: "24px", borderRadius: 14, marginBottom: 16,
                            background: "rgba(16,185,129,0.04)", border: "1px solid rgba(16,185,129,0.15)"
                        }}>
                            <h4 style={{ fontSize: 14, fontWeight: 700, color: "#10B981", margin: "0 0 16px", fontFamily: "'DM Sans', sans-serif" }}>✓ Doğru Kullanım</h4>
                            {[
                                "Logo etrafında minimum ikon yüksekliği kadar (40px) boşluk bırakın",
                                "Koyu arka plan (#0B1628 veya #162038) üzerinde tam renkli logo kullanın",
                                "Açık arka planlarda dark theme logosunu kullanın (Tech kısmı cyan kalır)",
                                "Signal Cyan (#00E5CC) sadece interaktif elementler ve birincil aksiyonlar için kullanın",
                                "Regülasyon referanslarında her zaman JetBrains Mono kullanın",
                                "Amber rengi sadece deadline ve uyarı bağlamında kullanın",
                                "Beyaz alan bırakın — yoğun veri gösterimlerinde bile nefes alanı koruyun"
                            ].map((rule, i) => (
                                <div key={i} style={{ display: "flex", gap: 10, marginBottom: 8, alignItems: "flex-start" }}>
                                    <span style={{ color: "#10B981", fontSize: 14, marginTop: 1 }}>●</span>
                                    <span style={{ fontSize: 13, color: "#CBD5E1", lineHeight: 1.5 }}>{rule}</span>
                                </div>
                            ))}
                        </div>

                        {/* Don'ts */}
                        <div style={{
                            padding: "24px", borderRadius: 14, marginBottom: 16,
                            background: "rgba(239,68,68,0.04)", border: "1px solid rgba(239,68,68,0.15)"
                        }}>
                            <h4 style={{ fontSize: 14, fontWeight: 700, color: "#EF4444", margin: "0 0 16px", fontFamily: "'DM Sans', sans-serif" }}>✗ Yanlış Kullanım</h4>
                            {[
                                "Logoyu döndürmeyin, eğmeyin veya oranlarını değiştirmeyin",
                                "Logo renklerini değiştirmeyin (monokrom dışında)",
                                "Signal Cyan'ı büyük arka plan alanlarında kullanmayın — gözü yorar",
                                "Amber ve Red'i dekoratif amaçla kullanmayın — sadece durum bildirimi için",
                                "Body text'te DM Sans kullanmayın — sadece başlıklar için",
                                "Logoyu karmaşık fotoğraf veya desen üzerine yerleştirmeyin",
                                "Tagline'ı logosuz bağımsız kullanmayın"
                            ].map((rule, i) => (
                                <div key={i} style={{ display: "flex", gap: 10, marginBottom: 8, alignItems: "flex-start" }}>
                                    <span style={{ color: "#EF4444", fontSize: 14, marginTop: 1 }}>●</span>
                                    <span style={{ fontSize: 13, color: "#CBD5E1", lineHeight: 1.5 }}>{rule}</span>
                                </div>
                            ))}
                        </div>

                        {/* Minimum Sizes */}
                        <div style={{
                            padding: "24px", borderRadius: 14,
                            background: "#162038", border: "1px solid rgba(148,163,184,0.08)"
                        }}>
                            <h4 style={{ fontSize: 14, fontWeight: 700, color: "#F1F5F9", margin: "0 0 16px", fontFamily: "'DM Sans', sans-serif" }}>Minimum Boyutlar</h4>
                            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: 16 }}>
                                {[
                                    { label: "Tam Logo (ikon + yazı)", min: "Genişlik: 140px", rec: "Önerilen: 180px+" },
                                    { label: "Sadece İkon", min: "32×32px", rec: "Önerilen: 40×40px+" },
                                    { label: "Favicon", min: "16×16px", rec: "32×32px (retina)" }
                                ].map((s, i) => (
                                    <div key={i} style={{ padding: "14px", borderRadius: 10, background: "rgba(0,0,0,0.2)" }}>
                                        <div style={{ fontSize: 12, fontWeight: 600, color: "#F1F5F9", marginBottom: 6 }}>{s.label}</div>
                                        <div style={{ fontSize: 11, color: "#94A3B8" }}>Min: {s.min}</div>
                                        <div style={{ fontSize: 11, color: "#00E5CC" }}>{s.rec}</div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    </div>
                )}

                {/* ===== ICONS ===== */}
                {activeSection === "icons" && (
                    <div>
                        <h2 style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 26, fontWeight: 800, margin: "0 0 6px" }}>
                            İkonografi & UI Elementleri
                        </h2>
                        <p style={{ color: "#94A3B8", fontSize: 14, margin: "0 0 28px", lineHeight: 1.6 }}>
                            Ürün içinde kullanılacak ikonlar, badge'ler ve durum göstergeleri.
                        </p>

                        {/* Priority Badges */}
                        <h4 style={{ fontSize: 12, fontWeight: 700, color: "#475569", letterSpacing: 2, margin: "0 0 14px", textTransform: "uppercase" }}>Öncelik Badge Sistemi</h4>
                        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr 1fr", gap: 12, marginBottom: 28 }}>
                            {[
                                { label: "KRİTİK", color: "#EF4444", bg: "rgba(239,68,68,0.12)", desc: "Son tarih <7 gün, ceza riski" },
                                { label: "UYARI", color: "#F59E0B", bg: "rgba(245,158,11,0.12)", desc: "Son tarih <30 gün, aksiyon gerekli" },
                                { label: "BİLGİ", color: "#00E5CC", bg: "rgba(0,229,204,0.12)", desc: "Yeni güncelleme, takip önerisi" },
                                { label: "DÜŞÜK", color: "#94A3B8", bg: "rgba(148,163,184,0.08)", desc: "Uzun vadeli, izleme yeterli" }
                            ].map((b, i) => (
                                <div key={i} style={{
                                    padding: "16px", borderRadius: 12, textAlign: "center",
                                    background: "#162038", border: "1px solid rgba(148,163,184,0.08)"
                                }}>
                                    <span style={{
                                        display: "inline-block", padding: "4px 14px", borderRadius: 6,
                                        background: b.bg, color: b.color,
                                        fontSize: 11, fontWeight: 700, letterSpacing: 1,
                                        fontFamily: "'IBM Plex Sans', sans-serif"
                                    }}>{b.label}</span>
                                    <p style={{ fontSize: 11, color: "#64748b", marginTop: 10, marginBottom: 0, lineHeight: 1.4 }}>{b.desc}</p>
                                </div>
                            ))}
                        </div>

                        {/* Regulator Tags */}
                        <h4 style={{ fontSize: 12, fontWeight: 700, color: "#475569", letterSpacing: 2, margin: "0 0 14px", textTransform: "uppercase" }}>Regülatör Etiketleri</h4>
                        <div style={{ display: "flex", gap: 8, flexWrap: "wrap", marginBottom: 28 }}>
                            {["EBA", "ESMA", "ECB", "FATF", "FCA", "SEC", "FinCEN", "BaFin", "ACPR", "CSSF"].map(tag => (
                                <span key={tag} style={{
                                    padding: "5px 12px", borderRadius: 6,
                                    background: "#1E293B", border: "1px solid #334155",
                                    color: "#CBD5E1", fontSize: 12, fontWeight: 600,
                                    fontFamily: "'JetBrains Mono', monospace"
                                }}>{tag}</span>
                            ))}
                        </div>

                        {/* Topic Tags */}
                        <h4 style={{ fontSize: 12, fontWeight: 700, color: "#475569", letterSpacing: 2, margin: "0 0 14px", textTransform: "uppercase" }}>Konu Etiketleri</h4>
                        <div style={{ display: "flex", gap: 8, flexWrap: "wrap", marginBottom: 28 }}>
                            {[
                                { label: "DORA", color: "#818CF8" }, { label: "MiCA", color: "#F472B6" },
                                { label: "AML/KYC", color: "#34D399" }, { label: "PSD3", color: "#60A5FA" },
                                { label: "ISO 20022", color: "#FBBF24" }, { label: "GDPR", color: "#A78BFA" },
                                { label: "AMLA", color: "#FB923C" }, { label: "Travel Rule", color: "#2DD4BF" }
                            ].map(tag => (
                                <span key={tag.label} style={{
                                    padding: "5px 12px", borderRadius: 6,
                                    background: `${tag.color}15`, border: `1px solid ${tag.color}30`,
                                    color: tag.color, fontSize: 12, fontWeight: 600,
                                    fontFamily: "'IBM Plex Sans', sans-serif"
                                }}>{tag.label}</span>
                            ))}
                        </div>

                        {/* Sample Card */}
                        <h4 style={{ fontSize: 12, fontWeight: 700, color: "#475569", letterSpacing: 2, margin: "0 0 14px", textTransform: "uppercase" }}>Örnek Güncelleme Kartı</h4>
                        <div style={{
                            padding: "20px", borderRadius: 14,
                            background: "#162038", border: "1px solid rgba(148,163,184,0.08)",
                            borderLeft: "4px solid #F59E0B"
                        }}>
                            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 10 }}>
                                <div style={{ display: "flex", gap: 8, alignItems: "center" }}>
                                    <span style={{ padding: "3px 10px", borderRadius: 5, background: "rgba(245,158,11,0.12)", color: "#F59E0B", fontSize: 10, fontWeight: 700, letterSpacing: 1 }}>UYARI</span>
                                    <span style={{ padding: "3px 10px", borderRadius: 5, background: "rgba(129,140,248,0.1)", border: "1px solid rgba(129,140,248,0.2)", color: "#818CF8", fontSize: 10, fontWeight: 600 }}>DORA</span>
                                    <span style={{ padding: "3px 10px", borderRadius: 5, background: "#1E293B", border: "1px solid #334155", color: "#CBD5E1", fontSize: 10, fontWeight: 600, fontFamily: "'JetBrains Mono', monospace" }}>EBA</span>
                                </div>
                                <span style={{ fontSize: 11, color: "#475569", fontFamily: "'JetBrains Mono', monospace" }}>2026-02-10</span>
                            </div>
                            <h3 style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 16, fontWeight: 800, margin: "0 0 8px", color: "#F1F5F9" }}>
                                EBA, DORA Register of Information Şablonlarını Güncelledi
                            </h3>
                            <p style={{ fontSize: 13, color: "#94A3B8", margin: "0 0 12px", lineHeight: 1.6 }}>
                                Üçüncü taraf ICT hizmet sağlayıcıları için raporlama şablonları revize edildi. Yeni alanlar eklendi ve mevcut veri formatları değiştirildi...
                            </p>
                            <div style={{ display: "flex", gap: 12, alignItems: "center" }}>
                                <span style={{ fontSize: 11, color: "#F59E0B", fontWeight: 600 }}>Deadline: 2026-04-17</span>
                                <span style={{ fontSize: 11, color: "#475569" }}>•</span>
                                <span style={{ fontSize: 11, color: "#00E5CC", fontWeight: 600 }}>Etki Skoru: 8.2/10</span>
                            </div>
                        </div>
                    </div>
                )}

                {/* ===== BRAND VOICE ===== */}
                {activeSection === "voice" && (
                    <div>
                        <h2 style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 26, fontWeight: 800, margin: "0 0 6px" }}>
                            Marka Sesi & Tonu
                        </h2>
                        <p style={{ color: "#94A3B8", fontSize: 14, margin: "0 0 28px", lineHeight: 1.6 }}>
                            RegTech Radar'ın tüm iletişim kanallarında tutarlı bir kişiliği vardır.
                        </p>

                        {/* Voice Pillars */}
                        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 14, marginBottom: 24 }}>
                            {[
                                { title: "Otoriter ama Erişilebilir", icon: "🎯", desc: "Regülasyon karmaşıklığını herkesin anlayabileceği dile çeviriyoruz. Jargon kullanırken mutlaka açıklama ekliyoruz. Bilgiç değil, rehber edici konuşuyoruz." },
                                { title: "Acil ama Panik Yapmayan", icon: "⚡", desc: "Deadline'ları net bildiriyoruz ama korku dilinden kaçınıyoruz. 'Ceza alabilirsiniz!' yerine 'Bu tarihe kadar şu aksiyonu almanız gerekiyor' diyoruz." },
                                { title: "Kesin ama Kapsayıcı", icon: "📐", desc: "Belirsizlikten kaçınıyoruz. Tarihler, madde numaraları ve kaynak referansları her zaman var. Ama yorumu her zaman bağlamla birlikte sunuyoruz." },
                                { title: "Teknolojik ama İnsani", icon: "🤝", desc: "AI-powered analizden bahsederken soğuk olmuyoruz. Compliance officer'ların gerçek stresini anlıyoruz ve empatik bir dil kullanıyoruz." }
                            ].map((p, i) => (
                                <div key={i} style={{
                                    padding: "20px", borderRadius: 14,
                                    background: "#162038", border: "1px solid rgba(148,163,184,0.08)"
                                }}>
                                    <div style={{ fontSize: 24, marginBottom: 8 }}>{p.icon}</div>
                                    <h4 style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 15, fontWeight: 700, margin: "0 0 8px", color: "#F1F5F9" }}>{p.title}</h4>
                                    <p style={{ fontSize: 13, color: "#94A3B8", margin: 0, lineHeight: 1.6 }}>{p.desc}</p>
                                </div>
                            ))}
                        </div>

                        {/* Tone Examples */}
                        <div style={{
                            padding: "24px", borderRadius: 14,
                            background: "rgba(0,229,204,0.04)", border: "1px solid rgba(0,229,204,0.1)"
                        }}>
                            <h4 style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 14, fontWeight: 700, margin: "0 0 16px", color: "#00E5CC" }}>Ton Örnekleri</h4>
                            {[
                                { bad: "DORA yürürlüğe girdi, uyumsanız ceza alırsınız!!!", good: "DORA 17 Ocak 2025'ten itibaren uygulanıyor. Aşağıda kurumunuz için kontrol edilmesi gereken 5 kritik maddeyi özetledik." },
                                { bad: "Bu çok teknik bir konu, uzmanınıza danışın.", good: "Art. 15(3) kapsamında ICT vendor sözleşmelerinizde bulunması gereken minimum klozları aşağıda sade bir dille özetledik." },
                                { bad: "Yeni bir güncelleme var.", good: "EBA, DORA Register of Information şablonlarını güncelledi → 3 yeni zorunlu alan eklendi. Mevcut raporlarınızı Nisan 2026'ya kadar uyumlamanız gerekiyor." }
                            ].map((ex, i) => (
                                <div key={i} style={{ marginBottom: i < 2 ? 16 : 0 }}>
                                    <div style={{ display: "flex", gap: 12 }}>
                                        <div style={{ flex: 1, padding: "12px", borderRadius: 8, background: "rgba(239,68,68,0.06)", border: "1px solid rgba(239,68,68,0.1)" }}>
                                            <span style={{ fontSize: 10, color: "#EF4444", fontWeight: 700, letterSpacing: 1 }}>✗ YAPMAYIN</span>
                                            <p style={{ fontSize: 12, color: "#94A3B8", margin: "6px 0 0", lineHeight: 1.5 }}>{ex.bad}</p>
                                        </div>
                                        <div style={{ flex: 1, padding: "12px", borderRadius: 8, background: "rgba(16,185,129,0.06)", border: "1px solid rgba(16,185,129,0.1)" }}>
                                            <span style={{ fontSize: 10, color: "#10B981", fontWeight: 700, letterSpacing: 1 }}>✓ YAPIN</span>
                                            <p style={{ fontSize: 12, color: "#CBD5E1", margin: "6px 0 0", lineHeight: 1.5 }}>{ex.good}</p>
                                        </div>
                                    </div>
                                </div>
                            ))}
                        </div>

                        {/* Slogan Options */}
                        <div style={{
                            marginTop: 16, padding: "24px", borderRadius: 14,
                            background: "#162038", border: "1px solid rgba(148,163,184,0.08)"
                        }}>
                            <h4 style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 14, fontWeight: 700, margin: "0 0 16px", color: "#F1F5F9" }}>Slogan Seçenekleri</h4>
                            {[
                                { slogan: "Regulatory Intelligence, Delivered.", usage: "Ana slogan — web sitesi hero, email footer" },
                                { slogan: "Her regülasyon değişikliği, senin dilinle.", usage: "Türkçe pazarlama — landing page, sosyal medya" },
                                { slogan: "Stay Compliant. Stay Ahead.", usage: "Kısa format — sosyal medya bio, badge" },
                                { slogan: "Your compliance radar, always scanning.", usage: "Bülten header — email digest açılış" }
                            ].map((s, i) => (
                                <div key={i} style={{ display: "flex", justifyContent: "space-between", alignItems: "center", padding: "10px 0", borderBottom: i < 3 ? "1px solid rgba(148,163,184,0.06)" : "none" }}>
                                    <span style={{ fontFamily: "'DM Sans', sans-serif", fontSize: 15, fontWeight: 700, color: "#F1F5F9" }}>"{s.slogan}"</span>
                                    <span style={{ fontSize: 11, color: "#475569", textAlign: "right" }}>{s.usage}</span>
                                </div>
                            ))}
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}