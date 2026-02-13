"""Base scraper with retry logic, logging, and common parsing utilities."""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime

import httpx

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

    @abstractmethod
    async def scrape(self) -> list[RegulationItem]:
        """Scrape the regulator's website and return regulation items."""
        ...

    async def close(self):
        if self._client and not self._client.is_closed:
            await self._client.aclose()
