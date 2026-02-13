"""FinCEN (Financial Crimes Enforcement Network, US) scraper."""

from __future__ import annotations

import logging
from datetime import datetime

from bs4 import BeautifulSoup

from app.scrapers.base import BaseScraper, RegulationItem

logger = logging.getLogger(__name__)

FINCEN_BASE = "https://www.fincen.gov"
FINCEN_NEWS_URL = f"{FINCEN_BASE}/news-room"


class FinCENScraper(BaseScraper):
    source_name = "FinCEN"

    async def scrape(self) -> list[RegulationItem]:
        items: list[RegulationItem] = []

        html = await self.fetch(FINCEN_NEWS_URL)
        if not html:
            return items

        soup = BeautifulSoup(html, "lxml")

        for row in soup.select(".view-content .views-row, article, .news-item, .item-list li")[:20]:
            link_el = row.select_one("a[href]")
            if not link_el:
                continue

            title = link_el.get_text(strip=True)
            href = link_el["href"]
            if not title or len(title) < 10:
                continue

            url = href if href.startswith("http") else f"{FINCEN_BASE}{href}"

            date_el = row.select_one(".date, time, .field--name-created, .datetime")
            pub_date = self._parse_date(date_el.get_text(strip=True)) if date_el else None

            items.append(RegulationItem(
                title=title,
                url=url,
                source="FinCEN",
                published_date=pub_date,
                category="AML",  # FinCEN is primarily AML-focused
            ))

        logger.info("[FinCEN] Scraped %d items", len(items))
        return items

    @staticmethod
    def _parse_date(text: str) -> datetime | None:
        for fmt in ("%B %d, %Y", "%m/%d/%Y", "%Y-%m-%d", "%d %B %Y"):
            try:
                return datetime.strptime(text.strip(), fmt)
            except ValueError:
                continue
        return None
