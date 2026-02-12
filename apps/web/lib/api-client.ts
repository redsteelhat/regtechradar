// Backend (collector) API client — base URL from env
const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000';

export async function fetchFeed(params: Record<string, string>) {
  const search = new URLSearchParams(params).toString();
  const res = await fetch(`${API_BASE}/updates?${search}`);
  if (!res.ok) throw new Error('Feed fetch failed');
  return res.json();
}

export async function fetchSearch(q: string) {
  const res = await fetch(`${API_BASE}/search?q=${encodeURIComponent(q)}`);
  if (!res.ok) throw new Error('Search failed');
  return res.json();
}
