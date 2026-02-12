"""EBA (European Banking Authority) crawler — RSS + content_selectors."""
from __future__ import annotations

import asyncio
from typing import Any

import httpx

from src.sources.base import AbstractSource
from src.sources.fetch_helpers import (
    extract_with_selectors,
    fetch_html,
    parse_rss_entries,
    parse_iso_or_none,
    _headers,
)

try:
    from src.config import settings
except Exception:
    settings = None

MAX_ITEMS_PER_TARGET = 5
DELAY_MS = getattr(settings, "crawler_request_delay_ms", 2000) if settings else 2000


class EBASource(AbstractSource):
    """EBA crawler — RSS feed + article pages with content_selectors."""

    slug = "eba"
    name = "European Banking Authority"
    base_url = "https://www.eba.europa.eu"
    jurisdiction = ["EU"]

    async def fetch(self) -> list[dict[str, Any]]:
        """Fetch from RSS target and optionally enrich with article body via content_selectors."""
        results: list[dict[str, Any]] = []
        async with httpx.AsyncClient(headers=_headers(), timeout=30.0) as client:
            for target in self.crawl_targets:
                if target.get("type") != "rss":
                    continue
                url = self.full_url(target["url"])
                try:
                    resp = await client.get(url, follow_redirects=True)
                    resp.raise_for_status()
                    entries = parse_rss_entries(resp.text, self.base_url)
                except Exception:
                    continue
                for entry in entries[:MAX_ITEMS_PER_TARGET]:
                    item_url = entry["url"]
                    title = entry["title"]
                    published_at = entry.get("published_at")
                    raw_html = ""
                    extracted_text = ""
                    if self.content_selectors:
                        try:
                            await asyncio.sleep(DELAY_MS / 1000.0)
                            html = await fetch_html(client, item_url)
                            raw_html = html
                            parts = extract_with_selectors(html, self.content_selectors)
                            extracted_text = parts.get("body", "") or parts.get("title", "")
                            if parts.get("title"):
                                title = title or parts["title"]
                            if parts.get("date") and not published_at:
                                published_at = parse_iso_or_none(parts["date"])
                        except Exception:
                            pass
                    results.append({
                        "url": item_url,
                        "title": title or "EBA update",
                        "raw_html": raw_html or None,
                        "extracted_text": extracted_text or title,
                        "published_at": published_at,
                    })
                break
        return results
