import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'RegTech Radar',
  description: 'Regulatory Intelligence Platform for FinTech',
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
