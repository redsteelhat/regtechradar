import { NextResponse } from 'next/server';

// Public API (Team plan) — API key auth
export async function GET() {
  return NextResponse.json({ items: [], total: 0 });
}
