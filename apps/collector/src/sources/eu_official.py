"""EUR-Lex / Official Journal (EU) crawler — direct-access / page_list style."""
from __future__ import annotations

import asyncio
from typing import Any

import httpx
from bs4 import BeautifulSoup

from src.sources.base import AbstractSource
from src.sources.fetch_helpers import (
    fetch_html,
    extract_links_from_list_page,
    _headers,
)

try:
    from src.config import settings
except Exception:
    settings = None

MAX_ITEMS_PER_TARGET = 5
DELAY_MS = getattr(settings, "crawler_request_delay_ms", 2000) if settings else 2000


class EuOfficialSource(AbstractSource):
    """EUR-Lex crawler — /oj/direct-access.html and eur-lex content pages."""

    slug = "eurlex"
    name = "EUR-Lex (Official Journal)"
    base_url = "https://eur-lex.europa.eu"
    jurisdiction = ["EU"]

    async def fetch(self) -> list[dict[str, Any]]:
        """Fetch from list/custom target: extract links from direct-access or similar page."""
        results: list[dict[str, Any]] = []
        list_url = None
        for target in self.crawl_targets:
            url_path = target.get("url", "")
            list_url = self.full_url(url_path)
            # Support both page_list and custom; we treat custom as a single list page
            if target.get("type") in ("page_list", "custom") or not target.get("type"):
                break
        if not list_url:
            return results
        async with httpx.AsyncClient(headers=_headers(), timeout=30.0) as client:
            try:
                html = await fetch_html(client, list_url)
            except Exception:
                return results
            links = extract_links_from_list_page(html, self.base_url)
            for item_url in links[:MAX_ITEMS_PER_TARGET]:
                if "eur-lex.europa.eu" not in item_url:
                    continue
                if item_url == list_url or item_url.rstrip("/") == list_url.rstrip("/"):
                    continue
                # Prefer OJ or legal content paths
                if "/oj/" not in item_url and "/legal-content/" not in item_url and "/EN/" not in item_url:
                    continue
                try:
                    await asyncio.sleep(DELAY_MS / 1000.0)
                    page_html = await fetch_html(client, item_url)
                except Exception:
                    continue
                soup = BeautifulSoup(page_html, "lxml")
                title_el = soup.select_one("h1") or soup.select_one("title")
                title = title_el.get_text(strip=True) if title_el else "EUR-Lex update"
                body_el = soup.select_one("main") or soup.select_one("article") or soup.select_one(".content") or soup.select_one("[role='main']")
                body = body_el.get_text(separator=" ", strip=True)[:5000] if body_el else ""
                results.append({
                    "url": item_url,
                    "title": title,
                    "raw_html": page_html,
                    "extracted_text": body or title,
                    "published_at": None,
                })
        return results
