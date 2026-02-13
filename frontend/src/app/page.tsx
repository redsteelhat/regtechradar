"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";

/* ── Inline Radar Logo SVG ─────────────────────────────────── */
function RadarLogo({ size = 1 }: { size?: number }) {
  const s = size;
  return (
    <svg width={40 * s} height={40 * s} viewBox="0 0 40 40" fill="none">
      <circle cx="20" cy="20" r="18" stroke="#0A7E72" strokeWidth="1.5" strokeDasharray="3 3" opacity="0.5" />
      <circle cx="20" cy="20" r="12" stroke="#00E5CC" strokeWidth="1.5" strokeDasharray="2 2" opacity="0.7" />
      <circle cx="20" cy="20" r="6" fill="#00E5CC" opacity="0.15" />
      <circle cx="20" cy="20" r="3" fill="#00E5CC" />
      <path d="M20 20 L20 2" stroke="#00E5CC" strokeWidth="2" strokeLinecap="round" opacity="0.9">
        <animateTransform attributeName="transform" type="rotate" from="0 20 20" to="360 20 20" dur="4s" repeatCount="indefinite" />
      </path>
      <path d="M20 20 L20 2 A18 18 0 0 1 35 10 Z" fill="url(#sweepGradLanding)" opacity="0.15">
        <animateTransform attributeName="transform" type="rotate" from="0 20 20" to="360 20 20" dur="4s" repeatCount="indefinite" />
      </path>
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
        <linearGradient id="sweepGradLanding" x1="20" y1="2" x2="35" y2="10">
          <stop offset="0%" stopColor="#00E5CC" stopOpacity="1" />
          <stop offset="100%" stopColor="#00E5CC" stopOpacity="0" />
        </linearGradient>
      </defs>
    </svg>
  );
}

export default function LandingPage() {
  const router = useRouter();
  const [email, setEmail] = useState("");

  const features = [
    { icon: "🔍", title: "Auto-Scraping", desc: "EBA, ESMA, FATF, FCA, FinCEN — monitored daily" },
    { icon: "🤖", title: "AI Summarization", desc: "Key changes distilled into actionable bullet points" },
    { icon: "📊", title: "Impact Scoring", desc: "Personalized 1-10 score by your license type" },
    { icon: "📧", title: "Weekly Digest", desc: "Everything you need, straight to your inbox every Monday" },
    { icon: "🔔", title: "Custom Alerts", desc: "Set keyword & category alerts — never miss what matters" },
    { icon: "🔐", title: "Team Access", desc: "Share dashboards, API access, and manage your compliance team" },
  ];

  const categories = [
    { name: "DORA", color: "#818CF8", desc: "Digital Operational Resilience" },
    { name: "MiCA", color: "#F472B6", desc: "Markets in Crypto-Assets" },
    { name: "PSD3", color: "#60A5FA", desc: "Payment Services Directive" },
    { name: "AMLA", color: "#FB923C", desc: "Anti-Money Laundering Authority" },
    { name: "FATF", color: "#FBBF24", desc: "Financial Action Task Force" },
  ];

  const pricing = [
    {
      name: "Free", price: "$0", period: "/forever",
      desc: "Weekly regulatory summary",
      features: ["Weekly email digest", "Basic regulation feed", "5 regulation views/day"],
      cta: "Get Started", highlight: false,
    },
    {
      name: "Premium", price: "$29", period: "/month",
      desc: "Full regulatory intelligence",
      features: ["Everything in Free", "AI impact analysis", "Unlimited regulation views", "Custom alerts", "Detailed summaries", "Search & filters"],
      cta: "Start Free Trial", highlight: true,
    },
    {
      name: "Team", price: "$99", period: "/month",
      desc: "For compliance teams",
      features: ["Everything in Premium", "5 team members", "API access", "Custom integrations", "Priority support", "Export & reporting"],
      cta: "Contact Sales", highlight: false,
    },
  ];

  return (
    <div style={{ minHeight: "100vh" }}>
      {/* ── Navigation ─────────────────────────────────── */}
      <nav
        style={{
          position: "fixed", top: 0, left: 0, right: 0, zIndex: 100,
          padding: "16px 40px",
          display: "flex", alignItems: "center", justifyContent: "space-between",
          background: "rgba(11, 22, 40, 0.88)",
          backdropFilter: "blur(20px)",
          borderBottom: "1px solid rgba(0, 229, 204, 0.1)",
        }}
      >
        <div style={{ display: "flex", alignItems: "center", gap: 10, cursor: "pointer" }}>
          <RadarLogo size={0.85} />
          <span
            style={{
              fontFamily: "var(--font-display)",
              fontSize: 20, fontWeight: 800,
              letterSpacing: -0.5, color: "#F1F5F9",
            }}
          >
            Reg<span style={{ color: "#00E5CC" }}>Tech</span> Radar
          </span>
        </div>
        <div style={{ display: "flex", gap: 12 }}>
          <button className="btn btn-secondary" onClick={() => router.push("/login")}>
            Sign In
          </button>
          <button className="btn btn-primary" onClick={() => router.push("/register")}>
            Get Started
          </button>
        </div>
      </nav>

      {/* ── Hero ───────────────────────────────────────── */}
      <section
        style={{
          paddingTop: 160, paddingBottom: 100,
          textAlign: "center", position: "relative", overflow: "hidden",
        }}
      >
        {/* Gradient orbs */}
        <div
          style={{
            position: "absolute", top: -200, left: "50%", transform: "translateX(-50%)",
            width: 800, height: 600,
            background: "radial-gradient(ellipse, rgba(0,229,204,0.1) 0%, transparent 70%)",
            pointerEvents: "none",
          }}
        />
        <div
          style={{
            position: "absolute", top: 100, right: -100,
            width: 400, height: 400,
            background: "radial-gradient(circle, rgba(10,126,114,0.08) 0%, transparent 70%)",
            pointerEvents: "none",
          }}
        />

        <div
          className="animate-in"
          style={{ maxWidth: 800, margin: "0 auto", padding: "0 24px", position: "relative" }}
        >
          {/* Hero badge */}
          <div
            style={{
              display: "inline-flex", alignItems: "center",
              padding: "6px 16px", borderRadius: 6,
              background: "rgba(0,229,204,0.08)",
              border: "1px solid rgba(0,229,204,0.2)",
              fontSize: 13, fontWeight: 600,
              color: "#00E5CC", marginBottom: 24,
              fontFamily: "var(--font-body)",
            }}
          >
            🚀 2025: DORA + MiCA + AMLA all in effect
          </div>

          <h1
            style={{
              fontFamily: "var(--font-display)",
              fontSize: "clamp(36px, 5vw, 60px)",
              fontWeight: 800, lineHeight: 1.1,
              marginBottom: 20, letterSpacing: "-0.02em",
              color: "#F1F5F9",
            }}
          >
            Regulatory Intelligence
            <br />
            <span style={{ color: "#00E5CC" }}>Delivered.</span>
          </h1>

          <p
            style={{
              fontFamily: "var(--font-body)",
              fontSize: 17, color: "#94A3B8",
              maxWidth: 600, margin: "0 auto 32px", lineHeight: 1.7,
            }}
          >
            Stop drowning in regulatory PDFs. RegTech Radar scrapes 5 major
            regulators, summarizes changes with AI, and scores how each one
            impacts <em>your</em> specific license.
          </p>

          <div style={{ display: "flex", gap: 12, justifyContent: "center", flexWrap: "wrap" }}>
            <button
              className="btn btn-primary"
              style={{ padding: "14px 32px", fontSize: 16, fontWeight: 700 }}
              onClick={() => router.push("/register")}
            >
              Start Free →
            </button>
            <button
              className="btn btn-secondary"
              style={{ padding: "14px 32px", fontSize: 16 }}
              onClick={() => router.push("/dashboard")}
            >
              View Dashboard
            </button>
          </div>

          {/* Category pills */}
          <div
            style={{
              display: "flex", gap: 10, justifyContent: "center",
              flexWrap: "wrap", marginTop: 48,
            }}
          >
            {categories.map((cat) => (
              <div
                key={cat.name}
                style={{
                  padding: "6px 16px", borderRadius: 6,
                  background: `${cat.color}15`,
                  border: `1px solid ${cat.color}30`,
                  color: cat.color,
                  fontSize: 13, fontWeight: 600,
                  fontFamily: "var(--font-body)",
                }}
              >
                {cat.name}
                <span style={{ fontSize: 11, opacity: 0.7, marginLeft: 6, fontWeight: 400 }}>
                  {cat.desc}
                </span>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── Features Grid ──────────────────────────────── */}
      <section style={{ padding: "60px 40px 100px", maxWidth: 1200, margin: "0 auto" }}>
        <h2
          style={{
            fontFamily: "var(--font-display)",
            textAlign: "center", fontSize: 32, fontWeight: 800,
            marginBottom: 48, letterSpacing: "-0.02em",
          }}
        >
          Everything your compliance team needs
        </h2>
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit, minmax(320px, 1fr))",
            gap: 16,
          }}
        >
          {features.map((f, i) => (
            <div
              key={f.title}
              className={`glass-card animate-in stagger-${Math.min(i + 1, 4)}`}
              style={{ padding: 28 }}
            >
              <div
                style={{
                  fontSize: 28, marginBottom: 12,
                  width: 52, height: 52, borderRadius: 10,
                  background: "rgba(0,229,204,0.06)",
                  display: "flex", alignItems: "center", justifyContent: "center",
                }}
              >
                {f.icon}
              </div>
              <h3
                style={{
                  fontFamily: "var(--font-display)",
                  fontSize: 17, fontWeight: 700, marginBottom: 8,
                }}
              >
                {f.title}
              </h3>
              <p style={{ color: "#94A3B8", fontSize: 14, lineHeight: 1.6 }}>{f.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* ── Pricing ────────────────────────────────────── */}
      <section style={{ padding: "80px 40px", maxWidth: 1100, margin: "0 auto" }}>
        <h2
          style={{
            fontFamily: "var(--font-display)",
            textAlign: "center", fontSize: 32, fontWeight: 800,
            marginBottom: 12, letterSpacing: "-0.02em",
          }}
        >
          Simple, transparent pricing
        </h2>
        <p
          style={{
            textAlign: "center", color: "#94A3B8",
            marginBottom: 48, fontSize: 16,
          }}
        >
          Start free. Upgrade when you need deeper insights.
        </p>
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit, minmax(280px, 1fr))",
            gap: 16, alignItems: "stretch",
          }}
        >
          {pricing.map((plan) => (
            <div
              key={plan.name}
              className="glass-card"
              style={{
                padding: 32,
                border: plan.highlight ? "1px solid rgba(0,229,204,0.4)" : undefined,
                position: "relative", overflow: "hidden",
              }}
            >
              {plan.highlight && (
                <div
                  style={{
                    position: "absolute", top: 0, left: 0, right: 0, height: 3,
                    background: "#00E5CC",
                  }}
                />
              )}
              <h3
                style={{
                  fontFamily: "var(--font-display)",
                  fontSize: 20, fontWeight: 700, marginBottom: 4,
                }}
              >
                {plan.name}
              </h3>
              <p style={{ fontSize: 13, color: "#475569", marginBottom: 16 }}>{plan.desc}</p>
              <div style={{ marginBottom: 24 }}>
                <span
                  style={{
                    fontFamily: "var(--font-display)",
                    fontSize: 40, fontWeight: 800,
                  }}
                >
                  {plan.price}
                </span>
                <span style={{ color: "#475569", fontSize: 14 }}>{plan.period}</span>
              </div>
              <ul
                style={{
                  listStyle: "none", display: "flex",
                  flexDirection: "column", gap: 10, marginBottom: 24,
                }}
              >
                {plan.features.map((feat) => (
                  <li
                    key={feat}
                    style={{
                      fontSize: 14, color: "#94A3B8",
                      display: "flex", alignItems: "center", gap: 8,
                    }}
                  >
                    <span style={{ color: "#10B981" }}>✓</span>
                    {feat}
                  </li>
                ))}
              </ul>
              <button
                className={`btn ${plan.highlight ? "btn-primary" : "btn-secondary"}`}
                style={{ width: "100%" }}
                onClick={() => router.push("/register")}
              >
                {plan.cta}
              </button>
            </div>
          ))}
        </div>
      </section>

      {/* ── Footer ─────────────────────────────────────── */}
      <footer
        style={{
          padding: "40px",
          borderTop: "1px solid rgba(0,229,204,0.08)",
          textAlign: "center", color: "#475569", fontSize: 13,
          fontFamily: "var(--font-body)",
        }}
      >
        © 2025 RegTech Radar. Regulatory Intelligence, Delivered.
      </footer>
    </div>
  );
}
