"""ESMA (European Securities and Markets Authority) scraper."""

from __future__ import annotations

import logging
from datetime import datetime

from bs4 import BeautifulSoup

from app.scrapers.base import BaseScraper, RegulationItem

logger = logging.getLogger(__name__)

ESMA_BASE = "https://www.esma.europa.eu"
ESMA_NEWS_URL = f"{ESMA_BASE}/press-news/esma-news"


class ESMAScraper(BaseScraper):
    source_name = "ESMA"

    async def scrape(self) -> list[RegulationItem]:
        items: list[RegulationItem] = []

        html = await self.fetch(ESMA_NEWS_URL)
        if not html:
            return items

        soup = BeautifulSoup(html, "lxml")

        for row in soup.select(".view-content .views-row, article, .node--type-news")[:20]:
            link_el = row.select_one("a[href]")
            if not link_el:
                continue

            title = link_el.get_text(strip=True)
            href = link_el["href"]
            if not title or len(title) < 10:
                continue

            url = href if href.startswith("http") else f"{ESMA_BASE}{href}"

            date_el = row.select_one("time, .date-display-single, .field--name-created")
            pub_date = self._parse_date(date_el.get_text(strip=True)) if date_el else None

            items.append(RegulationItem(
                title=title,
                url=url,
                source="ESMA",
                published_date=pub_date,
                category=self._classify(title),
            ))

        logger.info("[ESMA] Scraped %d items", len(items))
        return items

    @staticmethod
    def _classify(title: str) -> str:
        t = title.upper()
        if "MICA" in t or "CRYPTO" in t or "DIGITAL ASSET" in t:
            return "MiCA"
        if "DORA" in t or "DIGITAL OPERATIONAL" in t:
            return "DORA"
        if "AML" in t or "MONEY LAUNDERING" in t:
            return "AMLA"
        return "OTHER"

    @staticmethod
    def _parse_date(text: str) -> datetime | None:
        for fmt in ("%d %B %Y", "%d/%m/%Y", "%Y-%m-%d", "%B %d, %Y"):
            try:
                return datetime.strptime(text.strip(), fmt)
            except ValueError:
                continue
        return None
