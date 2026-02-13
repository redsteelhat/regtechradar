"""FinCEN (Financial Crimes Enforcement Network, US) scraper — HTML + body fetch."""

from __future__ import annotations

import logging

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
            pub_date = self.parse_date(date_el.get_text(strip=True)) if date_el else None

            items.append(RegulationItem(
                title=title,
                url=url,
                source="FinCEN",
                published_date=pub_date,
                category="AML",  # FinCEN is primarily AML-focused
            ))

        # Fetch body for top items
        for item in items[:5]:
            if not item.body_text:
                item.body_text = await self.fetch_body(
                    item.url,
                    selectors=[".field--name-body", "article", ".node__content"],
                )

        logger.info("[FinCEN] Scraped %d items", len(items))
        return items
