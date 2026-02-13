"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { register } from "@/lib/api";

function RadarIcon() {
    return (
        <svg width="44" height="44" viewBox="0 0 40 40" fill="none">
            <circle cx="20" cy="20" r="18" stroke="#0A7E72" strokeWidth="1.5" strokeDasharray="3 3" opacity="0.5" />
            <circle cx="20" cy="20" r="12" stroke="#00E5CC" strokeWidth="1.5" strokeDasharray="2 2" opacity="0.7" />
            <circle cx="20" cy="20" r="6" fill="#00E5CC" opacity="0.15" />
            <circle cx="20" cy="20" r="3" fill="#00E5CC" />
            <path d="M20 20 L20 2" stroke="#00E5CC" strokeWidth="2" strokeLinecap="round" opacity="0.9">
                <animateTransform attributeName="transform" type="rotate" from="0 20 20" to="360 20 20" dur="4s" repeatCount="indefinite" />
            </path>
            <circle cx="28" cy="10" r="2" fill="#F59E0B" opacity="0.9">
                <animate attributeName="opacity" values="0.9;0.3;0.9" dur="2s" repeatCount="indefinite" />
            </circle>
        </svg>
    );
}

const LICENSE_TYPES = [
    { value: "EMI", label: "Electronic Money Institution (EMI)" },
    { value: "PI", label: "Payment Institution (PI)" },
    { value: "VASP", label: "Virtual Asset Service Provider (VASP)" },
    { value: "BANK", label: "Bank / Credit Institution" },
    { value: "INV_FIRM", label: "Investment Firm" },
    { value: "INSURANCE", label: "Insurance" },
    { value: "OTHER", label: "Other" },
];

export default function RegisterPage() {
    const router = useRouter();
    const [form, setForm] = useState({
        email: "", password: "", full_name: "", company_name: "", license_type: "OTHER",
    });
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);

    const update = (key: string, value: string) =>
        setForm((prev) => ({ ...prev, [key]: value }));

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError("");
        setLoading(true);
        try {
            await register(form);
            router.push("/dashboard");
        } catch (err: any) {
            setError(err.message || "Registration failed");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div
            style={{
                minHeight: "100vh",
                display: "flex", alignItems: "center", justifyContent: "center",
                padding: 24, position: "relative", overflow: "hidden",
            }}
        >
            <div
                style={{
                    position: "absolute", top: "50%", left: "50%",
                    transform: "translate(-50%, -50%)",
                    width: 700, height: 700,
                    background: "radial-gradient(circle, rgba(0,229,204,0.06) 0%, transparent 70%)",
                    pointerEvents: "none",
                }}
            />

            <div
                className="glass-card animate-in"
                style={{ width: "100%", maxWidth: 480, padding: 40, position: "relative" }}
            >
                <div style={{ textAlign: "center", marginBottom: 28 }}>
                    <div style={{ display: "inline-block", marginBottom: 16 }}>
                        <RadarIcon />
                    </div>
                    <h1
                        style={{
                            fontFamily: "var(--font-display)",
                            fontSize: 24, fontWeight: 800, letterSpacing: "-0.02em",
                        }}
                    >
                        Create your account
                    </h1>
                    <p style={{ color: "#94A3B8", fontSize: 14, marginTop: 4 }}>
                        Start tracking regulatory changes in minutes
                    </p>
                </div>

                {error && (
                    <div
                        style={{
                            padding: "10px 14px", borderRadius: 8,
                            background: "rgba(239,68,68,0.1)",
                            border: "1px solid rgba(239,68,68,0.25)",
                            color: "#EF4444", fontSize: 13, marginBottom: 20,
                        }}
                    >
                        {error}
                    </div>
                )}

                <form onSubmit={handleSubmit} style={{ display: "flex", flexDirection: "column", gap: 14 }}>
                    <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 14 }}>
                        <div>
                            <label htmlFor="full_name">Full Name</label>
                            <input
                                id="full_name" className="input-field" placeholder="Jane Doe"
                                value={form.full_name} onChange={(e) => update("full_name", e.target.value)}
                            />
                        </div>
                        <div>
                            <label htmlFor="company_name">Company</label>
                            <input
                                id="company_name" className="input-field" placeholder="Acme FinTech"
                                value={form.company_name} onChange={(e) => update("company_name", e.target.value)}
                            />
                        </div>
                    </div>
                    <div>
                        <label htmlFor="reg-email">Email</label>
                        <input
                            id="reg-email" type="email" className="input-field" placeholder="you@company.com"
                            value={form.email} onChange={(e) => update("email", e.target.value)} required
                        />
                    </div>
                    <div>
                        <label htmlFor="reg-password">Password</label>
                        <input
                            id="reg-password" type="password" className="input-field" placeholder="Min 8 characters"
                            value={form.password} onChange={(e) => update("password", e.target.value)}
                            required minLength={8}
                        />
                    </div>
                    <div>
                        <label htmlFor="license_type">License Type</label>
                        <select
                            id="license_type" className="input-field"
                            value={form.license_type} onChange={(e) => update("license_type", e.target.value)}
                        >
                            {LICENSE_TYPES.map((lt) => (
                                <option key={lt.value} value={lt.value}>{lt.label}</option>
                            ))}
                        </select>
                    </div>
                    <button
                        type="submit" className="btn btn-primary"
                        style={{ width: "100%", marginTop: 8, fontWeight: 700 }}
                        disabled={loading}
                    >
                        {loading ? "Creating account..." : "Create Account"}
                    </button>
                </form>

                <p
                    style={{
                        textAlign: "center", marginTop: 20,
                        fontSize: 13, color: "#475569",
                    }}
                >
                    Already have an account?{" "}
                    <a href="/login" style={{ color: "#00E5CC", fontWeight: 600 }}>Sign in</a>
                </p>
            </div>
        </div>
    );
}
