"""Shared HTTP and HTML helpers for crawlers (httpx + BeautifulSoup)."""
from __future__ import annotations

import asyncio
from datetime import datetime
from typing import Any
from urllib.parse import urljoin, urlparse

import httpx
from bs4 import BeautifulSoup

try:
    from src.config import settings
except Exception:
    settings = None


def _headers() -> dict[str, str]:
    ua = getattr(settings, "crawler_user_agent", None) or "RegTechRadar/1.0 (+https://regtechradar.com/bot)"
    return {"User-Agent": ua, "Accept": "text/html,application/xml,application/rss+xml;q=0.9,*/*;q=0.8"}


async def fetch_html(client: httpx.AsyncClient, url: str) -> str:
    """Fetch URL and return response text."""
    resp = await client.get(url, follow_redirects=True, timeout=30.0)
    resp.raise_for_status()
    return resp.text


def extract_with_selectors(html: str, selectors: dict[str, str]) -> dict[str, str]:
    """
    Extract title, body, date from HTML using CSS selectors.

    Args:
        html: Raw HTML.
        selectors: e.g. {"title": "h1.page-title", "body": "div.field-item", "date": "span.date-display-single"}.

    Returns:
        Dict with keys title, body, date (values may be empty string).
    """
    soup = BeautifulSoup(html, "lxml")
    out: dict[str, str] = {"title": "", "body": "", "date": ""}
    for key, selector in selectors.items():
        if not selector:
            continue
        el = soup.select_one(selector)
        if el:
            text = el.get_text(separator=" ", strip=True)
            if key in out:
                out[key] = text
    return out


def extract_links_from_list_page(html: str, base_url: str, link_selector: str | None = None) -> list[str]:
    """
    Extract article/content links from a list page.

    Args:
        html: Raw HTML of list page.
        base_url: Base URL for resolving relative links.
        link_selector: Optional CSS selector for links (e.g. "a.news-item"). If None, uses common patterns.

    Returns:
        List of absolute URLs (deduplicated).
    """
    soup = BeautifulSoup(html, "lxml")
    seen: set[str] = set()
    urls: list[str] = []
    if link_selector:
        for a in soup.select(link_selector):
            href = a.get("href")
            if href and href.startswith(("/", "http")):
                full = urljoin(base_url, href)
                if full not in seen and base_url in full:
                    seen.add(full)
                    urls.append(full)
    else:
        for a in soup.select("a[href]"):
            href = a.get("href")
            if not href or href.startswith("#") or "javascript:" in href.lower():
                continue
            full = urljoin(base_url, href)
            if full in seen:
                continue
            parsed = urlparse(full)
            if parsed.path in ("/", ""):
                continue
            if base_url not in full:
                continue
            seen.add(full)
            urls.append(full)
    return urls


def parse_rss_entries(rss_text: str, base_url: str) -> list[dict[str, Any]]:
    """
    Parse RSS/Atom XML and return list of entries: url, title, published_at.

    Uses feedparser if available; otherwise minimal tag-based parse.
    """
    try:
        import feedparser
    except ImportError:
        return []
    feed = feedparser.parse(rss_text)
    entries: list[dict[str, Any]] = []
    for e in getattr(feed, "entries", [])[:20]:
        link = e.get("link") or (e.get("links", [{}])[0].get("href") if e.get("links") else None)
        if not link:
            continue
        if not link.startswith("http"):
            link = urljoin(base_url, link)
        title = e.get("title") or ""
        published = e.get("published") or e.get("updated")
        entries.append({
            "url": link,
            "title": title,
            "published_at": parse_iso_or_none(published),
        })
    return entries


def parse_iso_or_none(s: str | None) -> str | None:
    """Return ISO date string or None for storage."""
    if not s:
        return None
    s = s.strip()
    for fmt in ("%a, %d %b %Y %H:%M:%S %z", "%a, %d %b %Y %H:%M:%S %Z", "%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%d"):
        try:
            dt = datetime.strptime(s.replace(" GMT", " +0000").replace(" UTC", " +0000"), fmt)
            return dt.strftime("%Y-%m-%dT%H:%M:%SZ")
        except ValueError:
            continue
    return None
