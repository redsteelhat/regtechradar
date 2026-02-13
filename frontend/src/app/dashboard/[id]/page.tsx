"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { getRegulation, RegulationDetail } from "@/lib/api";

function getImpactClass(score: number) {
    if (score >= 7) return "impact-high";
    if (score >= 4) return "impact-medium";
    return "impact-low";
}

function getImpactLabel(score: number) {
    if (score >= 7) return "KRİTİK";
    if (score >= 4) return "UYARI";
    return "BİLGİ";
}

function getImpactColor(score: number) {
    if (score >= 7) return "#EF4444";
    if (score >= 4) return "#F59E0B";
    return "#00E5CC";
}

function getCategoryClass(cat: string) {
    const map: Record<string, string> = {
        DORA: "cat-dora", MiCA: "cat-mica", PSD3: "cat-psd3",
        AMLA: "cat-amla", FATF: "cat-fatf", AML: "cat-aml", OTHER: "cat-other",
    };
    return map[cat] || "cat-other";
}

export default function RegulationDetailPage() {
    const params = useParams();
    const router = useRouter();
    const [reg, setReg] = useState<RegulationDetail | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {
        const id = Number(params.id);
        if (!id) return;
        getRegulation(id)
            .then(setReg)
            .catch((e) => setError(e.message))
            .finally(() => setLoading(false));
    }, [params.id]);

    if (loading) {
        return (
            <div style={{ padding: "28px 32px" }}>
                <div className="skeleton" style={{ height: 40, width: 300, marginBottom: 20 }} />
                <div className="skeleton" style={{ height: 200, marginBottom: 16 }} />
                <div className="skeleton" style={{ height: 300 }} />
            </div>
        );
    }

    if (error || !reg) {
        return (
            <div style={{ padding: "28px 32px", textAlign: "center" }}>
                <div style={{ fontSize: 48, marginBottom: 16 }}>❌</div>
                <h2 style={{ fontFamily: "var(--font-display)", marginBottom: 8 }}>
                    Regulation not found
                </h2>
                <p style={{ color: "#94A3B8", marginBottom: 20 }}>{error}</p>
                <button className="btn btn-secondary" onClick={() => router.back()}>← Go Back</button>
            </div>
        );
    }

    return (
        <div style={{ padding: "28px 32px", maxWidth: 960 }}>
            {/* Back */}
            <button
                className="btn btn-secondary btn-sm"
                onClick={() => router.back()}
                style={{ marginBottom: 20 }}
            >
                ← Back to Feed
            </button>

            {/* Header */}
            <div className="animate-in" style={{ marginBottom: 28 }}>
                <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 12 }}>
                    <span className={`category-chip ${getCategoryClass(reg.category)}`}>{reg.category}</span>
                    <span className="source-badge">{reg.source}</span>
                    <span
                        style={{
                            fontSize: 12, color: "#475569",
                            fontFamily: "var(--font-mono)",
                        }}
                    >
                        {reg.published_date
                            ? new Date(reg.published_date).toLocaleDateString("en-GB", {
                                day: "numeric", month: "long", year: "numeric",
                            })
                            : "Date unknown"}
                    </span>
                </div>
                <h1
                    style={{
                        fontFamily: "var(--font-display)",
                        fontSize: 24, fontWeight: 800,
                        letterSpacing: "-0.02em", lineHeight: 1.3, marginBottom: 12,
                    }}
                >
                    {reg.title}
                </h1>
                <a
                    href={reg.original_url} target="_blank" rel="noopener noreferrer"
                    style={{
                        fontSize: 13, display: "inline-flex",
                        alignItems: "center", gap: 4, color: "#00E5CC",
                    }}
                >
                    View original source ↗
                </a>
            </div>

            {/* AI Summary */}
            {reg.ai_summary && (
                <div
                    className="animate-in stagger-1"
                    style={{
                        padding: 24, marginBottom: 20,
                        background: "#162038",
                        border: "1px solid rgba(148,163,184,0.08)",
                        borderRadius: 14,
                    }}
                >
                    <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 14 }}>
                        <span style={{ fontSize: 18 }}>🤖</span>
                        <h2 style={{ fontFamily: "var(--font-display)", fontSize: 16, fontWeight: 700 }}>
                            AI Summary
                        </h2>
                    </div>
                    <div
                        style={{
                            fontSize: 14, lineHeight: 1.8, color: "#CBD5E1", whiteSpace: "pre-wrap",
                        }}
                    >
                        {reg.ai_summary}
                    </div>
                </div>
            )}

            {/* Impact Scores */}
            {reg.impact_scores && reg.impact_scores.length > 0 && (
                <div
                    className="animate-in stagger-2"
                    style={{
                        padding: 24, marginBottom: 20,
                        background: "#162038",
                        border: "1px solid rgba(148,163,184,0.08)",
                        borderRadius: 14,
                    }}
                >
                    <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 18 }}>
                        <span style={{ fontSize: 18 }}>📊</span>
                        <h2 style={{ fontFamily: "var(--font-display)", fontSize: 16, fontWeight: 700 }}>
                            Impact Analysis by License Type
                        </h2>
                    </div>
                    <div
                        style={{
                            display: "grid",
                            gridTemplateColumns: "repeat(auto-fill, minmax(280px, 1fr))",
                            gap: 12,
                        }}
                    >
                        {reg.impact_scores.map((is) => (
                            <div
                                key={is.id}
                                style={{
                                    padding: "16px 18px", borderRadius: 10,
                                    background: "rgba(0,0,0,0.2)",
                                    border: "1px solid rgba(148,163,184,0.06)",
                                }}
                            >
                                <div
                                    style={{
                                        display: "flex", justifyContent: "space-between",
                                        alignItems: "center", marginBottom: 8,
                                    }}
                                >
                                    <span
                                        style={{
                                            fontFamily: "var(--font-mono)",
                                            fontSize: 12, fontWeight: 600,
                                            textTransform: "uppercase", letterSpacing: "0.05em",
                                            color: "#F1F5F9",
                                        }}
                                    >
                                        {is.license_type}
                                    </span>
                                    <span
                                        className={`impact-badge ${getImpactClass(is.score)}`}
                                    >
                                        {getImpactLabel(is.score)} {is.score.toFixed(1)}
                                    </span>
                                </div>
                                {/* Score bar */}
                                <div
                                    style={{
                                        height: 6, borderRadius: 3,
                                        background: "rgba(148,163,184,0.1)",
                                        marginBottom: 10, overflow: "hidden",
                                    }}
                                >
                                    <div
                                        style={{
                                            height: "100%", width: `${is.score * 10}%`,
                                            borderRadius: 3,
                                            background: getImpactColor(is.score),
                                            transition: "width 0.5s ease",
                                        }}
                                    />
                                </div>
                                {is.explanation && (
                                    <p style={{ fontSize: 12, color: "#94A3B8", lineHeight: 1.5 }}>
                                        {is.explanation}
                                    </p>
                                )}
                            </div>
                        ))}
                    </div>
                </div>
            )}

            {/* Raw content */}
            <div
                className="animate-in stagger-3"
                style={{
                    padding: 24,
                    background: "#162038",
                    border: "1px solid rgba(148,163,184,0.08)",
                    borderRadius: 14,
                }}
            >
                <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 14 }}>
                    <span style={{ fontSize: 18 }}>📄</span>
                    <h2 style={{ fontFamily: "var(--font-display)", fontSize: 16, fontWeight: 700 }}>
                        Full Text
                    </h2>
                </div>
                <div
                    style={{
                        fontSize: 14, lineHeight: 1.8, color: "#94A3B8", whiteSpace: "pre-wrap",
                    }}
                >
                    {reg.raw_content || "Full text not yet available."}
                </div>
            </div>
        </div>
    );
}
