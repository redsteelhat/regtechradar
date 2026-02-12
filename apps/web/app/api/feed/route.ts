import { NextResponse } from 'next/server';

export async function GET() {
  // BFF → Python backend /internal or /updates
  return NextResponse.json({ items: [], total: 0, page: 1, per_page: 20 });
}
