"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { getMe, clearToken, User } from "@/lib/api";

export default function SettingsPage() {
    const router = useRouter();
    const [user, setUser] = useState<User | null>(null);

    useEffect(() => {
        getMe().then(setUser).catch(() => router.push("/login"));
    }, [router]);

    if (!user) {
        return (
            <div style={{ padding: "28px 32px" }}>
                <div className="skeleton" style={{ height: 200, borderRadius: 14 }} />
            </div>
        );
    }

    return (
        <div style={{ padding: "28px 32px", maxWidth: 700 }}>
            <div style={{ marginBottom: 28 }}>
                <h1
                    style={{
                        fontFamily: "var(--font-display)",
                        fontSize: 26, fontWeight: 800,
                        letterSpacing: "-0.02em", marginBottom: 4,
                    }}
                >
                    ⚙️ Settings
                </h1>
                <p style={{ color: "#94A3B8", fontSize: 14 }}>
                    Manage your profile and subscription
                </p>
            </div>

            {/* Profile Card */}
            <div
                className="animate-in"
                style={{
                    padding: 28, marginBottom: 16,
                    background: "#162038",
                    border: "1px solid rgba(148,163,184,0.08)",
                    borderRadius: 14,
                }}
            >
                <h2 style={{ fontFamily: "var(--font-display)", fontSize: 16, fontWeight: 700, marginBottom: 20 }}>
                    Profile
                </h2>
                <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16 }}>
                    {[
                        { label: "Email", value: user.email },
                        { label: "Full Name", value: user.full_name || "—" },
                        { label: "Company", value: user.company_name || "—" },
                        { label: "License Type", value: user.license_type },
                    ].map((item) => (
                        <div key={item.label}>
                            <label>{item.label}</label>
                            <div
                                style={{
                                    padding: "10px 14px",
                                    background: "rgba(0,0,0,0.2)",
                                    borderRadius: 8, fontSize: 14,
                                    color: "#F1F5F9",
                                    fontFamily: item.label === "License Type" ? "var(--font-mono)" : "inherit",
                                }}
                            >
                                {item.value}
                            </div>
                        </div>
                    ))}
                </div>
            </div>

            {/* Subscription Card */}
            <div
                className="animate-in stagger-1"
                style={{
                    padding: 28, marginBottom: 16,
                    background: "#162038",
                    border: "1px solid rgba(148,163,184,0.08)",
                    borderRadius: 14,
                }}
            >
                <h2 style={{ fontFamily: "var(--font-display)", fontSize: 16, fontWeight: 700, marginBottom: 16 }}>
                    Subscription
                </h2>
                <div
                    style={{
                        display: "flex", alignItems: "center", justifyContent: "space-between",
                        padding: "16px 20px", borderRadius: 10,
                        background: "rgba(0,0,0,0.2)",
                        border: "1px solid rgba(148,163,184,0.06)",
                    }}
                >
                    <div>
                        <div
                            style={{
                                fontFamily: "var(--font-display)",
                                fontSize: 18, fontWeight: 800,
                                textTransform: "capitalize", marginBottom: 4,
                                color: "#00E5CC",
                            }}
                        >
                            {user.plan} Plan
                        </div>
                        <div style={{ fontSize: 12, color: "#475569" }}>
                            {user.plan === "free"
                                ? "Upgrade for AI analysis, unlimited views, and alerts"
                                : "Full access to all RegTech Radar features"}
                        </div>
                    </div>
                    {user.plan === "free" && (
                        <button className="btn btn-primary btn-sm" style={{ fontWeight: 700 }}>
                            Upgrade →
                        </button>
                    )}
                </div>
            </div>

            {/* Danger Zone */}
            <div
                className="animate-in stagger-2"
                style={{
                    padding: 28,
                    background: "rgba(239,68,68,0.03)",
                    border: "1px solid rgba(239,68,68,0.12)",
                    borderRadius: 14,
                }}
            >
                <h2
                    style={{
                        fontFamily: "var(--font-display)",
                        fontSize: 16, fontWeight: 700, marginBottom: 16,
                        color: "#EF4444",
                    }}
                >
                    Danger Zone
                </h2>
                <div
                    style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}
                >
                    <div>
                        <div style={{ fontSize: 14, fontWeight: 600, marginBottom: 2 }}>
                            Sign out of all devices
                        </div>
                        <div style={{ fontSize: 12, color: "#475569" }}>
                            This will invalidate your current session
                        </div>
                    </div>
                    <button
                        className="btn btn-danger btn-sm"
                        onClick={() => { clearToken(); router.push("/login"); }}
                    >
                        Sign Out
                    </button>
                </div>
            </div>
        </div>
    );
}
