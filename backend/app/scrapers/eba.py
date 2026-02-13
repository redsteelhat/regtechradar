"""EBA (European Banking Authority) scraper."""

from __future__ import annotations

import logging
from datetime import datetime

from bs4 import BeautifulSoup

from app.scrapers.base import BaseScraper, RegulationItem

logger = logging.getLogger(__name__)

EBA_BASE = "https://www.eba.europa.eu"
EBA_NEWS_URL = f"{EBA_BASE}/regulation-and-policy/single-rulebook/interactive-single-rulebook"


class EBAScraper(BaseScraper):
    source_name = "EBA"

    async def scrape(self) -> list[RegulationItem]:
        items: list[RegulationItem] = []

        # Primary: EBA press releases / regulatory news
        html = await self.fetch(f"{EBA_BASE}/newsroom/press-releases")
        if not html:
            return items

        soup = BeautifulSoup(html, "lxml")

        for article in soup.select("article, .view-content .views-row, .item-list li")[:20]:
            link_el = article.select_one("a[href]")
            if not link_el:
                continue

            title = link_el.get_text(strip=True)
            href = link_el["href"]
            if not title or len(title) < 10:
                continue

            url = href if href.startswith("http") else f"{EBA_BASE}{href}"

            date_el = article.select_one("time, .date, .field--name-created")
            pub_date = self._parse_date(date_el.get_text(strip=True)) if date_el else None

            items.append(RegulationItem(
                title=title,
                url=url,
                source="EBA",
                published_date=pub_date,
                category=self._classify(title),
            ))

        logger.info("[EBA] Scraped %d items", len(items))
        return items

    @staticmethod
    def _classify(title: str) -> str:
        t = title.upper()
        if "DORA" in t or "DIGITAL OPERATIONAL RESILIENCE" in t:
            return "DORA"
        if "MICA" in t or "MARKETS IN CRYPTO" in t:
            return "MiCA"
        if "PSD" in t or "PAYMENT SERVICE" in t:
            return "PSD3"
        if "AML" in t or "ANTI-MONEY" in t or "AMLA" in t:
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
