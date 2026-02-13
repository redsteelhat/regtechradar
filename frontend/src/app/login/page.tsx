"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { login } from "@/lib/api";

/* Radar logo — small version */
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

export default function LoginPage() {
    const router = useRouter();
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError("");
        setLoading(true);
        try {
            await login(email, password);
            router.push("/dashboard");
        } catch (err: any) {
            setError(err.message || "Login failed");
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
            {/* Background glow */}
            <div
                style={{
                    position: "absolute", top: "50%", left: "50%",
                    transform: "translate(-50%, -50%)",
                    width: 600, height: 600,
                    background: "radial-gradient(circle, rgba(0,229,204,0.06) 0%, transparent 70%)",
                    pointerEvents: "none",
                }}
            />

            <div
                className="glass-card animate-in"
                style={{ width: "100%", maxWidth: 420, padding: 40, position: "relative" }}
            >
                {/* Logo */}
                <div style={{ textAlign: "center", marginBottom: 32 }}>
                    <div style={{ display: "inline-block", marginBottom: 16 }}>
                        <RadarIcon />
                    </div>
                    <h1
                        style={{
                            fontFamily: "var(--font-display)",
                            fontSize: 24, fontWeight: 800, letterSpacing: "-0.02em",
                        }}
                    >
                        Welcome back
                    </h1>
                    <p style={{ color: "#94A3B8", fontSize: 14, marginTop: 4 }}>
                        Sign in to your RegTech Radar account
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

                <form onSubmit={handleSubmit} style={{ display: "flex", flexDirection: "column", gap: 16 }}>
                    <div>
                        <label htmlFor="email">Email</label>
                        <input
                            id="email" type="email" className="input-field"
                            placeholder="you@company.com"
                            value={email} onChange={(e) => setEmail(e.target.value)} required
                        />
                    </div>
                    <div>
                        <label htmlFor="password">Password</label>
                        <input
                            id="password" type="password" className="input-field"
                            placeholder="••••••••"
                            value={password} onChange={(e) => setPassword(e.target.value)} required
                        />
                    </div>
                    <button
                        type="submit" className="btn btn-primary"
                        style={{ width: "100%", marginTop: 8, fontWeight: 700 }}
                        disabled={loading}
                    >
                        {loading ? "Signing in..." : "Sign In"}
                    </button>
                </form>

                <p
                    style={{
                        textAlign: "center", marginTop: 24,
                        fontSize: 13, color: "#475569",
                    }}
                >
                    Don&apos;t have an account?{" "}
                    <a href="/register" style={{ color: "#00E5CC", fontWeight: 600 }}>
                        Sign up free
                    </a>
                </p>
            </div>
        </div>
    );
}
