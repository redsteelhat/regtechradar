const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// ── Types ──────────────────────────────────────────────────────────────────

export interface Regulation {
    id: number;
    source: string;
    category: string;
    title: string;
    original_url: string;
    published_date: string | null;
    ai_summary: string | null;
    impact_tags: string | null;
    status: string;
    created_at: string;
}

export interface RegulationDetail extends Regulation {
    raw_content: string;
    impact_scores: ImpactScore[];
}

export interface ImpactScore {
    id: number;
    license_type: string;
    score: number;
    explanation: string | null;
    created_at: string;
}

export interface User {
    id: number;
    email: string;
    full_name: string | null;
    company_name: string | null;
    license_type: string;
    plan: string;
    created_at: string;
}

export interface Alert {
    id: number;
    keyword: string | null;
    category: string | null;
    enabled: boolean;
    created_at: string;
}

export interface DashboardStats {
    total_regulations: number;
    new_this_week: number;
    sources_active: number;
    categories: Record<string, number>;
}

// ── Token management ───────────────────────────────────────────────────────

function getToken(): string | null {
    if (typeof window === 'undefined') return null;
    return localStorage.getItem('regtech_token');
}

export function setToken(token: string) {
    localStorage.setItem('regtech_token', token);
}

export function clearToken() {
    localStorage.removeItem('regtech_token');
}

// ── Fetch helper ───────────────────────────────────────────────────────────

async function apiFetch<T>(path: string, options: RequestInit = {}): Promise<T> {
    const token = getToken();
    const headers: Record<string, string> = {
        'Content-Type': 'application/json',
        ...(options.headers as Record<string, string> || {}),
    };
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }

    const res = await fetch(`${API_BASE}${path}`, {
        ...options,
        headers,
    });

    if (!res.ok) {
        const err = await res.json().catch(() => ({ detail: res.statusText }));
        throw new Error(err.detail || `API Error: ${res.status}`);
    }

    if (res.status === 204) return {} as T;
    return res.json();
}

// ── Auth API ───────────────────────────────────────────────────────────────

export async function register(data: {
    email: string;
    password: string;
    full_name?: string;
    company_name?: string;
    license_type?: string;
}): Promise<{ access_token: string }> {
    const result = await apiFetch<{ access_token: string }>('/api/auth/register', {
        method: 'POST',
        body: JSON.stringify(data),
    });
    setToken(result.access_token);
    return result;
}

export async function login(email: string, password: string): Promise<{ access_token: string }> {
    const result = await apiFetch<{ access_token: string }>('/api/auth/login', {
        method: 'POST',
        body: JSON.stringify({ email, password }),
    });
    setToken(result.access_token);
    return result;
}

export async function getMe(): Promise<User> {
    return apiFetch<User>('/api/auth/me');
}

// ── Regulations API ────────────────────────────────────────────────────────

export async function getRegulations(params?: {
    search?: string;
    category?: string;
    source?: string;
    page?: number;
}): Promise<Regulation[]> {
    const qs = new URLSearchParams();
    if (params?.search) qs.set('search', params.search);
    if (params?.category) qs.set('category', params.category);
    if (params?.source) qs.set('source', params.source);
    if (params?.page) qs.set('page', String(params.page));
    return apiFetch<Regulation[]>(`/api/regulations?${qs.toString()}`);
}

export async function getRegulation(id: number): Promise<RegulationDetail> {
    return apiFetch<RegulationDetail>(`/api/regulations/${id}`);
}

export async function getStats(): Promise<DashboardStats> {
    return apiFetch<DashboardStats>('/api/regulations/stats');
}

// ── Alerts API ─────────────────────────────────────────────────────────────

export async function getAlerts(): Promise<Alert[]> {
    return apiFetch<Alert[]>('/api/alerts');
}

export async function createAlert(data: { keyword?: string; category?: string }): Promise<Alert> {
    return apiFetch<Alert>('/api/alerts', {
        method: 'POST',
        body: JSON.stringify(data),
    });
}

export async function deleteAlert(id: number): Promise<void> {
    await apiFetch<void>(`/api/alerts/${id}`, { method: 'DELETE' });
}

// ── Admin API ──────────────────────────────────────────────────────────────

export async function triggerScrape(): Promise<{ message: string }> {
    return apiFetch<{ message: string }>('/api/admin/scrape', { method: 'POST' });
}

export async function seedDemoData(): Promise<{ message: string }> {
    return apiFetch<{ message: string }>('/api/admin/seed', { method: 'POST' });
}
