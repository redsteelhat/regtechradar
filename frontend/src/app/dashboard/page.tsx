"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import {
    getRegulations, getStats, seedDemoData,
    Regulation, DashboardStats,
} from "@/lib/api";

const CATEGORIES = ["", "DORA", "MiCA", "PSD3", "AMLA", "FATF", "AML", "OTHER"];
const SOURCES = ["", "EBA", "ESMA", "FATF", "FCA", "FinCEN"];

function getCategoryClass(cat: string) {
    const map: Record<string, string> = {
        DORA: "cat-dora", MiCA: "cat-mica", PSD3: "cat-psd3",
        AMLA: "cat-amla", FATF: "cat-fatf", AML: "cat-aml", OTHER: "cat-other",
    };
    return map[cat] || "cat-other";
}

function formatDate(d: string | null) {
    if (!d) return "—";
    return new Date(d).toLocaleDateString("en-GB", {
        day: "numeric", month: "short", year: "numeric",
    });
}

export default function DashboardPage() {
    const router = useRouter();
    const [regulations, setRegulations] = useState<Regulation[]>([]);
    const [stats, setStats] = useState<DashboardStats | null>(null);
    const [search, setSearch] = useState("");
    const [category, setCategory] = useState("");
    const [source, setSource] = useState("");
    const [loading, setLoading] = useState(true);
    const [seeding, setSeeding] = useState(false);

    const load = async () => {
        setLoading(true);
        try {
            const [regs, st] = await Promise.all([
                getRegulations({
                    search: search || undefined,
                    category: category || undefined,
                    source: source || undefined,
                }),
                getStats(),
            ]);
            setRegulations(regs);
            setStats(st);
        } catch (err) { console.error(err); }
        finally { setLoading(false); }
    };

    useEffect(() => { load(); }, [category, source]);

    const handleSearch = (e: React.FormEvent) => { e.preventDefault(); load(); };

    const handleSeed = async () => {
        setSeeding(true);
        try { await seedDemoData(); await load(); }
        catch (err) { console.error(err); }
        finally { setSeeding(false); }
    };

    return (
        <div style={{ padding: "28px 32px" }}>
            {/* ── Header ──────────────────────────────────── */}
            <div
                style={{
                    display: "flex", justifyContent: "space-between",
                    alignItems: "flex-start", marginBottom: 28,
                    flexWrap: "wrap", gap: 16,
                }}
            >
                <div>
                    <h1
                        style={{
                            fontFamily: "var(--font-display)",
                            fontSize: 26, fontWeight: 800,
                            letterSpacing: "-0.02em", marginBottom: 4,
                        }}
                    >
                        Regulatory Feed
                    </h1>
                    <p style={{ color: "#94A3B8", fontSize: 14 }}>
                        Track the latest regulatory changes across key jurisdictions
                    </p>
                </div>
                <button className="btn btn-secondary" onClick={handleSeed} disabled={seeding}>
                    {seeding ? "Seeding..." : "🌱 Seed Demo Data"}
                </button>
            </div>

            {/* ── Stats Cards ─────────────────────────────── */}
            {stats && (
                <div
                    className="animate-in"
                    style={{
                        display: "grid",
                        gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))",
                        gap: 14, marginBottom: 28,
                    }}
                >
                    {[
                        { label: "Total Regulations", value: stats.total_regulations, icon: "📊", color: "#00E5CC" },
                        { label: "New This Week", value: stats.new_this_week, icon: "🆕", color: "#10B981" },
                        { label: "Sources Active", value: stats.sources_active, icon: "🌐", color: "#818CF8" },
                        { label: "Categories", value: Object.keys(stats.categories).length, icon: "🏷️", color: "#F59E0B" },
                    ].map((card) => (
                        <div
                            key={card.label}
                            style={{
                                padding: "20px 24px",
                                display: "flex", alignItems: "center", gap: 16,
                                background: "#162038",
                                border: "1px solid rgba(148,163,184,0.08)",
                                borderRadius: 14,
                            }}
                        >
                            <div
                                style={{
                                    width: 44, height: 44, borderRadius: 10,
                                    background: `${card.color}12`,
                                    display: "flex", alignItems: "center", justifyContent: "center",
                                    fontSize: 20,
                                }}
                            >
                                {card.icon}
                            </div>
                            <div>
                                <div
                                    style={{
                                        fontFamily: "var(--font-display)",
                                        fontSize: 24, fontWeight: 800, color: card.color,
                                    }}
                                >
                                    {card.value}
                                </div>
                                <div style={{ fontSize: 12, color: "#475569", fontWeight: 500 }}>
                                    {card.label}
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            )}

            {/* ── Search & Filters ────────────────────────── */}
            <div
                style={{
                    padding: "16px 20px", marginBottom: 20,
                    display: "flex", gap: 12, flexWrap: "wrap", alignItems: "center",
                    background: "#162038",
                    border: "1px solid rgba(148,163,184,0.08)",
                    borderRadius: 14,
                }}
            >
                <form
                    onSubmit={handleSearch}
                    style={{ flex: 1, minWidth: 200, display: "flex", gap: 8 }}
                >
                    <input
                        className="input-field" placeholder="Search regulations..."
                        value={search} onChange={(e) => setSearch(e.target.value)}
                        style={{ flex: 1 }}
                    />
                    <button type="submit" className="btn btn-primary btn-sm">Search</button>
                </form>
                <select
                    className="input-field" style={{ width: 160 }}
                    value={category} onChange={(e) => setCategory(e.target.value)}
                >
                    <option value="">All Categories</option>
                    {CATEGORIES.filter(Boolean).map((c) => (
                        <option key={c} value={c}>{c}</option>
                    ))}
                </select>
                <select
                    className="input-field" style={{ width: 140 }}
                    value={source} onChange={(e) => setSource(e.target.value)}
                >
                    <option value="">All Sources</option>
                    {SOURCES.filter(Boolean).map((s) => (
                        <option key={s} value={s}>{s}</option>
                    ))}
                </select>
            </div>

            {/* ── Regulations List ────────────────────────── */}
            {loading ? (
                <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
                    {[1, 2, 3, 4].map((i) => (
                        <div key={i} className="skeleton" style={{ height: 96, borderRadius: 14 }} />
                    ))}
                </div>
            ) : regulations.length === 0 ? (
                <div
                    style={{
                        padding: 60, textAlign: "center",
                        background: "#162038",
                        border: "1px solid rgba(148,163,184,0.08)",
                        borderRadius: 14,
                    }}
                >
                    <div style={{ fontSize: 48, marginBottom: 16 }}>📭</div>
                    <h3
                        style={{
                            fontFamily: "var(--font-display)",
                            fontSize: 18, fontWeight: 700, marginBottom: 8,
                        }}
                    >
                        No regulations found
                    </h3>
                    <p style={{ color: "#94A3B8", fontSize: 14, marginBottom: 20 }}>
                        Click &quot;Seed Demo Data&quot; above to populate with sample regulations,
                        or try different search criteria.
                    </p>
                    <button className="btn btn-primary" onClick={handleSeed} disabled={seeding}>
                        {seeding ? "Seeding..." : "🌱 Seed Demo Data"}
                    </button>
                </div>
            ) : (
                <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
                    {regulations.map((reg, i) => (
                        <div
                            key={reg.id}
                            className={`animate-in stagger-${Math.min(i + 1, 4)}`}
                            style={{
                                padding: "20px 24px", cursor: "pointer",
                                background: "#162038",
                                border: "1px solid rgba(148,163,184,0.08)",
                                borderRadius: 14,
                                transition: "all var(--transition-smooth)",
                            }}
                            onClick={() => router.push(`/dashboard/${reg.id}`)}
                            onMouseEnter={(e) => {
                                (e.currentTarget as HTMLElement).style.borderColor = "rgba(0,229,204,0.2)";
                                (e.currentTarget as HTMLElement).style.transform = "translateY(-2px)";
                            }}
                            onMouseLeave={(e) => {
                                (e.currentTarget as HTMLElement).style.borderColor = "rgba(148,163,184,0.08)";
                                (e.currentTarget as HTMLElement).style.transform = "translateY(0)";
                            }}
                        >
                            <div
                                style={{
                                    display: "flex", alignItems: "flex-start",
                                    justifyContent: "space-between", gap: 16,
                                }}
                            >
                                <div style={{ flex: 1 }}>
                                    <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 8 }}>
                                        <span className={`category-chip ${getCategoryClass(reg.category)}`}>
                                            {reg.category}
                                        </span>
                                        <span className="source-badge">{reg.source}</span>
                                    </div>
                                    <h3
                                        style={{
                                            fontFamily: "var(--font-display)",
                                            fontSize: 15, fontWeight: 700,
                                            marginBottom: 6, lineHeight: 1.4,
                                        }}
                                    >
                                        {reg.title}
                                    </h3>
                                    {reg.ai_summary && (
                                        <p
                                            style={{
                                                fontSize: 13, color: "#94A3B8",
                                                lineHeight: 1.5,
                                                display: "-webkit-box",
                                                WebkitLineClamp: 2,
                                                WebkitBoxOrient: "vertical",
                                                overflow: "hidden",
                                            }}
                                        >
                                            {reg.ai_summary}
                                        </p>
                                    )}
                                </div>
                                <div style={{ textAlign: "right", flexShrink: 0 }}>
                                    <div
                                        style={{
                                            fontSize: 12, color: "#475569", marginBottom: 6,
                                            fontFamily: "var(--font-mono)",
                                        }}
                                    >
                                        {formatDate(reg.published_date)}
                                    </div>
                                    <div
                                        style={{ fontSize: 11, color: "#475569", textTransform: "capitalize" }}
                                    >
                                        {reg.status}
                                    </div>
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}
