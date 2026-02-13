"use client";

import { useEffect, useState } from "react";
import { useRouter, usePathname } from "next/navigation";
import { getMe, clearToken, User } from "@/lib/api";

/* Sidebar Radar Logo */
function SidebarLogo({ size = 0.8 }: { size?: number }) {
    const s = size;
    return (
        <svg width={40 * s} height={40 * s} viewBox="0 0 40 40" fill="none" style={{ flexShrink: 0 }}>
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
            <circle cx="11" cy="14" r="1.5" fill="#00E5CC" opacity="0.7">
                <animate attributeName="opacity" values="0.7;0.2;0.7" dur="3s" repeatCount="indefinite" />
            </circle>
        </svg>
    );
}

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
    const router = useRouter();
    const pathname = usePathname();
    const [user, setUser] = useState<User | null>(null);
    const [sidebarOpen, setSidebarOpen] = useState(true);

    useEffect(() => {
        getMe().then(setUser).catch(() => router.push("/login"));
    }, [router]);

    const navItems = [
        { href: "/dashboard", label: "Regulations", icon: "📋" },
        { href: "/dashboard/alerts", label: "Alerts", icon: "🔔" },
        { href: "/dashboard/settings", label: "Settings", icon: "⚙️" },
    ];

    const handleLogout = () => {
        clearToken();
        router.push("/login");
    };

    return (
        <div style={{ display: "flex", minHeight: "100vh" }}>
            {/* ── Sidebar ─────────────────────────────────── */}
            <aside
                style={{
                    width: sidebarOpen ? 260 : 72,
                    background: "#162038",
                    borderRight: "1px solid rgba(0,229,204,0.08)",
                    display: "flex", flexDirection: "column",
                    transition: "width var(--transition-smooth)",
                    overflow: "hidden", flexShrink: 0,
                }}
            >
                {/* Logo */}
                <div
                    style={{
                        padding: "18px 16px",
                        display: "flex", alignItems: "center", gap: 10,
                        borderBottom: "1px solid rgba(148,163,184,0.08)",
                        cursor: "pointer",
                    }}
                    onClick={() => setSidebarOpen(!sidebarOpen)}
                >
                    <SidebarLogo />
                    {sidebarOpen && (
                        <span
                            style={{
                                fontFamily: "var(--font-display)",
                                fontSize: 17, fontWeight: 800,
                                letterSpacing: -0.5, whiteSpace: "nowrap",
                                color: "#F1F5F9",
                            }}
                        >
                            Reg<span style={{ color: "#00E5CC" }}>Tech</span> Radar
                        </span>
                    )}
                </div>

                {/* Nav */}
                <nav style={{ flex: 1, padding: "12px 8px" }}>
                    {navItems.map((item) => {
                        const active = pathname === item.href;
                        return (
                            <a
                                key={item.href}
                                href={item.href}
                                style={{
                                    display: "flex", alignItems: "center", gap: 12,
                                    padding: "10px 12px", borderRadius: 8, marginBottom: 4,
                                    background: active ? "rgba(0,229,204,0.08)" : "transparent",
                                    color: active ? "#00E5CC" : "#94A3B8",
                                    fontSize: 14,
                                    fontWeight: active ? 600 : 400,
                                    fontFamily: "var(--font-body)",
                                    textDecoration: "none",
                                    transition: "all var(--transition-fast)",
                                    whiteSpace: "nowrap",
                                }}
                            >
                                <span style={{ fontSize: 18, minWidth: 24, textAlign: "center" }}>
                                    {item.icon}
                                </span>
                                {sidebarOpen && item.label}
                            </a>
                        );
                    })}
                </nav>

                {/* User info */}
                {user && (
                    <div style={{ padding: 16, borderTop: "1px solid rgba(148,163,184,0.08)" }}>
                        <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
                            <div
                                style={{
                                    width: 32, height: 32, minWidth: 32,
                                    borderRadius: "50%", background: "#0A7E72",
                                    display: "flex", alignItems: "center", justifyContent: "center",
                                    fontSize: 14, fontWeight: 700, color: "#F1F5F9",
                                    fontFamily: "var(--font-display)",
                                }}
                            >
                                {(user.full_name || user.email)[0].toUpperCase()}
                            </div>
                            {sidebarOpen && (
                                <div style={{ overflow: "hidden" }}>
                                    <div
                                        style={{
                                            fontSize: 13, fontWeight: 600,
                                            whiteSpace: "nowrap", overflow: "hidden",
                                            textOverflow: "ellipsis",
                                        }}
                                    >
                                        {user.full_name || user.email}
                                    </div>
                                    <div
                                        style={{
                                            fontSize: 11, color: "#475569",
                                            display: "flex", alignItems: "center", gap: 6,
                                        }}
                                    >
                                        <span
                                            className={`category-chip cat-${user.license_type.toLowerCase()}`}
                                            style={{ padding: "1px 6px", fontSize: 9 }}
                                        >
                                            {user.license_type}
                                        </span>
                                        <span style={{ textTransform: "capitalize" }}>{user.plan}</span>
                                    </div>
                                </div>
                            )}
                        </div>
                        {sidebarOpen && (
                            <button
                                className="btn btn-secondary btn-sm"
                                style={{ width: "100%", marginTop: 12, fontSize: 12 }}
                                onClick={handleLogout}
                            >
                                Sign Out
                            </button>
                        )}
                    </div>
                )}
            </aside>

            {/* ── Main Content ────────────────────────────── */}
            <main style={{ flex: 1, overflow: "auto", background: "#0B1628" }}>
                {children}
            </main>
        </div>
    );
}
