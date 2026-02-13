"use client";

import { useEffect, useState } from "react";
import { getAlerts, createAlert, deleteAlert, Alert } from "@/lib/api";

const CATEGORIES = ["DORA", "MiCA", "PSD3", "AMLA", "FATF", "AML", "OTHER"];

function getCategoryClass(cat: string) {
    const map: Record<string, string> = {
        DORA: "cat-dora", MiCA: "cat-mica", PSD3: "cat-psd3",
        AMLA: "cat-amla", FATF: "cat-fatf", AML: "cat-aml", OTHER: "cat-other",
    };
    return map[cat] || "cat-other";
}

export default function AlertsPage() {
    const [alerts, setAlerts] = useState<Alert[]>([]);
    const [keyword, setKeyword] = useState("");
    const [category, setCategory] = useState("");
    const [loading, setLoading] = useState(true);
    const [creating, setCreating] = useState(false);

    const load = async () => {
        try { const data = await getAlerts(); setAlerts(data); }
        catch (err) { console.error(err); }
        finally { setLoading(false); }
    };

    useEffect(() => { load(); }, []);

    const handleCreate = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!keyword && !category) return;
        setCreating(true);
        try {
            await createAlert({ keyword: keyword || undefined, category: category || undefined });
            setKeyword(""); setCategory(""); await load();
        } catch (err) { console.error(err); }
        finally { setCreating(false); }
    };

    const handleDelete = async (id: number) => {
        try { await deleteAlert(id); setAlerts((prev) => prev.filter((a) => a.id !== id)); }
        catch (err) { console.error(err); }
    };

    return (
        <div style={{ padding: "28px 32px", maxWidth: 800 }}>
            <div style={{ marginBottom: 28 }}>
                <h1
                    style={{
                        fontFamily: "var(--font-display)",
                        fontSize: 26, fontWeight: 800,
                        letterSpacing: "-0.02em", marginBottom: 4,
                    }}
                >
                    🔔 Custom Alerts
                </h1>
                <p style={{ color: "#94A3B8", fontSize: 14 }}>
                    Get notified when regulations matching your criteria are published
                </p>
            </div>

            {/* Create Alert Form */}
            <div
                className="animate-in"
                style={{
                    padding: 24, marginBottom: 28,
                    background: "#162038",
                    border: "1px solid rgba(148,163,184,0.08)",
                    borderRadius: 14,
                }}
            >
                <h2 style={{ fontFamily: "var(--font-display)", fontSize: 16, fontWeight: 700, marginBottom: 16 }}>
                    Create New Alert
                </h2>
                <form
                    onSubmit={handleCreate}
                    style={{ display: "flex", gap: 12, flexWrap: "wrap", alignItems: "flex-end" }}
                >
                    <div style={{ flex: 1, minWidth: 200 }}>
                        <label htmlFor="alert-keyword">Keyword</label>
                        <input
                            id="alert-keyword" className="input-field"
                            placeholder="e.g. crypto, operational resilience..."
                            value={keyword} onChange={(e) => setKeyword(e.target.value)}
                        />
                    </div>
                    <div style={{ width: 180 }}>
                        <label htmlFor="alert-category">Category</label>
                        <select
                            id="alert-category" className="input-field"
                            value={category} onChange={(e) => setCategory(e.target.value)}
                        >
                            <option value="">Any Category</option>
                            {CATEGORIES.map((c) => <option key={c} value={c}>{c}</option>)}
                        </select>
                    </div>
                    <button
                        type="submit" className="btn btn-primary"
                        disabled={creating || (!keyword && !category)}
                    >
                        {creating ? "Creating..." : "+ Add Alert"}
                    </button>
                </form>
            </div>

            {/* Alerts List */}
            {loading ? (
                <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
                    {[1, 2, 3].map((i) => (
                        <div key={i} className="skeleton" style={{ height: 64, borderRadius: 14 }} />
                    ))}
                </div>
            ) : alerts.length === 0 ? (
                <div
                    style={{
                        padding: 48, textAlign: "center",
                        background: "#162038",
                        border: "1px solid rgba(148,163,184,0.08)",
                        borderRadius: 14,
                    }}
                >
                    <div style={{ fontSize: 48, marginBottom: 16 }}>🔕</div>
                    <h3 style={{ fontFamily: "var(--font-display)", fontSize: 16, fontWeight: 700, marginBottom: 8 }}>
                        No alerts configured
                    </h3>
                    <p style={{ color: "#94A3B8", fontSize: 13 }}>
                        Create your first alert above to start receiving notifications
                    </p>
                </div>
            ) : (
                <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
                    {alerts.map((alert, i) => (
                        <div
                            key={alert.id}
                            className={`animate-in stagger-${Math.min(i + 1, 4)}`}
                            style={{
                                padding: "16px 20px",
                                display: "flex", alignItems: "center", justifyContent: "space-between",
                                background: "#162038",
                                border: "1px solid rgba(148,163,184,0.08)",
                                borderRadius: 14,
                            }}
                        >
                            <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
                                <span style={{ fontSize: 20 }}>{alert.enabled ? "🔔" : "🔕"}</span>
                                <div>
                                    <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
                                        {alert.keyword && (
                                            <span style={{ fontSize: 14, fontWeight: 600 }}>
                                                &quot;{alert.keyword}&quot;
                                            </span>
                                        )}
                                        {alert.category && (
                                            <span className={`category-chip ${getCategoryClass(alert.category)}`}>
                                                {alert.category}
                                            </span>
                                        )}
                                    </div>
                                    <div
                                        style={{
                                            fontSize: 11, color: "#475569", marginTop: 4,
                                            fontFamily: "var(--font-mono)",
                                        }}
                                    >
                                        Created{" "}
                                        {new Date(alert.created_at).toLocaleDateString("en-GB", {
                                            day: "numeric", month: "short", year: "numeric",
                                        })}
                                    </div>
                                </div>
                            </div>
                            <button className="btn btn-danger btn-sm" onClick={() => handleDelete(alert.id)}>
                                Delete
                            </button>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}
