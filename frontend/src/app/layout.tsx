import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "RegTech Radar — Regulatory Intelligence, Delivered.",
  description:
    "Track DORA, MiCA, PSD3, AMLA, FATF regulatory changes automatically. AI-powered summaries and personalized impact analysis for FinTech compliance teams.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
