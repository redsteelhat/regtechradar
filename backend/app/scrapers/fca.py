"""FCA (Financial Conduct Authority, UK) scraper."""

from __future__ import annotations

import logging
from datetime import datetime

from bs4 import BeautifulSoup

from app.scrapers.base import BaseScraper, RegulationItem

logger = logging.getLogger(__name__)

FCA_BASE = "https://www.fca.org.uk"
FCA_NEWS_URL = f"{FCA_BASE}/news/news-stories"


class FCAScraper(BaseScraper):
    source_name = "FCA"

    async def scrape(self) -> list[RegulationItem]:
        items: list[RegulationItem] = []

        html = await self.fetch(FCA_NEWS_URL)
        if not html:
            return items

        soup = BeautifulSoup(html, "lxml")

        for row in soup.select(".search-item, article, .listing-item, .views-row")[:20]:
            link_el = row.select_one("a[href]")
            if not link_el:
                continue

            title = link_el.get_text(strip=True)
            href = link_el["href"]
            if not title or len(title) < 10:
                continue

            url = href if href.startswith("http") else f"{FCA_BASE}{href}"

            date_el = row.select_one(".date, time, .search-item__date")
            pub_date = self._parse_date(date_el.get_text(strip=True)) if date_el else None

            items.append(RegulationItem(
                title=title,
                url=url,
                source="FCA",
                published_date=pub_date,
                category=self._classify(title),
            ))

        logger.info("[FCA] Scraped %d items", len(items))
        return items

    @staticmethod
    def _classify(title: str) -> str:
        t = title.upper()
        if "AML" in t or "MONEY LAUNDERING" in t or "FINANCIAL CRIME" in t:
            return "AML"
        if "CRYPTO" in t or "DIGITAL ASSET" in t:
            return "MiCA"
        if "PAYMENT" in t or "PSD" in t:
            return "PSD3"
        if "OPERATIONAL RESILIENCE" in t:
            return "DORA"
        return "OTHER"

    @staticmethod
    def _parse_date(text: str) -> datetime | None:
        for fmt in ("%d %B %Y", "%d/%m/%Y", "%Y-%m-%d", "%B %d, %Y"):
            try:
                return datetime.strptime(text.strip(), fmt)
            except ValueError:
                continue
        return None
