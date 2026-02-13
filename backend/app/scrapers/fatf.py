"""FATF (Financial Action Task Force) scraper."""

from __future__ import annotations

import logging
from datetime import datetime

from bs4 import BeautifulSoup

from app.scrapers.base import BaseScraper, RegulationItem

logger = logging.getLogger(__name__)

FATF_BASE = "https://www.fatf-gafi.org"
FATF_NEWS_URL = f"{FATF_BASE}/publications/"


class FATFScraper(BaseScraper):
    source_name = "FATF"

    async def scrape(self) -> list[RegulationItem]:
        items: list[RegulationItem] = []

        html = await self.fetch(FATF_NEWS_URL)
        if not html:
            return items

        soup = BeautifulSoup(html, "lxml")

        for row in soup.select(".publications-list .item, article, .content-item, .views-row")[:20]:
            link_el = row.select_one("a[href]")
            if not link_el:
                continue

            title = link_el.get_text(strip=True)
            href = link_el["href"]
            if not title or len(title) < 10:
                continue

            url = href if href.startswith("http") else f"{FATF_BASE}{href}"

            date_el = row.select_one(".date, time, .meta-date")
            pub_date = self._parse_date(date_el.get_text(strip=True)) if date_el else None

            items.append(RegulationItem(
                title=title,
                url=url,
                source="FATF",
                published_date=pub_date,
                category="FATF",
            ))

        logger.info("[FATF] Scraped %d items", len(items))
        return items

    @staticmethod
    def _parse_date(text: str) -> datetime | None:
        for fmt in ("%d %B %Y", "%B %Y", "%d/%m/%Y", "%Y-%m-%d"):
            try:
                return datetime.strptime(text.strip(), fmt)
            except ValueError:
                continue
        return None
