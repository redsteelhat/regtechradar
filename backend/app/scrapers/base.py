"""Base scraper with retry logic, RSS parsing, body fetching, and common utilities."""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime

import feedparser
import httpx
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/125.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

MAX_RETRIES = 3
TIMEOUT = 30.0


@dataclass
class RegulationItem:
    """A single scraped regulatory update."""
    title: str
    url: str
    source: str
    body_text: str = ""
    published_date: datetime | None = None
    category: str = "OTHER"
    tags: list[str] = field(default_factory=list)


class BaseScraper(ABC):
    """Abstract base class for all regulatory scrapers."""

    source_name: str = "UNKNOWN"

    def __init__(self):
        self._client: httpx.AsyncClient | None = None

    async def _get_client(self) -> httpx.AsyncClient:
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(
                headers=HEADERS,
                timeout=TIMEOUT,
                follow_redirects=True,
            )
        return self._client

    async def fetch(self, url: str) -> str | None:
        """Fetch a URL with retries. Returns HTML string or None."""
        client = await self._get_client()
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                resp = await client.get(url)
                resp.raise_for_status()
                return resp.text
            except httpx.HTTPError as exc:
                logger.warning(
                    "[%s] Attempt %d/%d failed for %s: %s",
                    self.source_name, attempt, MAX_RETRIES, url, exc,
                )
        logger.error("[%s] All retries exhausted for %s", self.source_name, url)
        return None

    async def fetch_rss(self, url: str) -> list[dict]:
        """Fetch and parse an RSS/Atom feed. Returns list of entry dicts."""
        raw = await self.fetch(url)
        if not raw:
            return []
        feed = feedparser.parse(raw)
        entries = []
        for entry in feed.entries:
            entries.append({
                "title": entry.get("title", "").strip(),
                "link": entry.get("link", ""),
                "published": entry.get("published", ""),
                "summary": entry.get("summary", ""),
                "updated": entry.get("updated", ""),
            })
        return entries

    async def fetch_body(self, url: str, selectors: list[str] | None = None) -> str:
        """Fetch a detail page and extract the main body text.

        Args:
            url: The detail page URL
            selectors: CSS selectors to try, in priority order.
                       Falls back to <article>, <main>, then <body>.
        """
        html = await self.fetch(url)
        if not html:
            return ""

        soup = BeautifulSoup(html, "lxml")

        # Remove scripts, styles, nav, footer
        for tag in soup.select("script, style, nav, footer, header, aside"):
            tag.decompose()

        # Try each selector in order
        candidates = selectors or []
        candidates += ["article", "main", "[role='main']", ".content", "#content"]

        for sel in candidates:
            el = soup.select_one(sel)
            if el:
                text = el.get_text(separator="\n", strip=True)
                if len(text) > 100:
                    return text[:5000]  # Cap at 5000 chars

        # Fallback: body
        body = soup.find("body")
        if body:
            text = body.get_text(separator="\n", strip=True)
            return text[:5000]

        return ""

    @abstractmethod
    async def scrape(self) -> list[RegulationItem]:
        """Scrape the regulator's website and return regulation items."""
        ...

    async def close(self):
        if self._client and not self._client.is_closed:
            await self._client.aclose()

    # ── Common utilities ────────────────────────────────────

    @staticmethod
    def parse_date(text: str) -> datetime | None:
        """Try multiple date formats."""
        for fmt in (
            "%d %B %Y", "%d/%m/%Y", "%Y-%m-%d", "%B %d, %Y",
            "%d %b %Y", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M:%SZ",
            "%a, %d %b %Y %H:%M:%S %z", "%a, %d %b %Y %H:%M:%S %Z",
        ):
            try:
                return datetime.strptime(text.strip(), fmt)
            except ValueError:
                continue
        return None

    @staticmethod
    def classify(title: str) -> str:
        """Common keyword-based category classification."""
        t = title.upper()
        if "DORA" in t or "DIGITAL OPERATIONAL RESILIENCE" in t:
            return "DORA"
        if "MICA" in t or "MARKETS IN CRYPTO" in t or "CRYPTO-ASSET" in t:
            return "MiCA"
        if "PSD" in t or "PAYMENT SERVICE" in t:
            return "PSD3"
        if "AMLA" in t or "ANTI-MONEY LAUNDERING AUTHORITY" in t:
            return "AMLA"
        if "AML" in t or "MONEY LAUNDERING" in t or "FINANCIAL CRIME" in t:
            return "AML"
        if "FATF" in t:
            return "FATF"
        return "OTHER"
