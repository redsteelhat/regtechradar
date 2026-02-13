"""FATF (Financial Action Task Force) scraper — HTML scraping + body fetch."""

from __future__ import annotations

import logging

from bs4 import BeautifulSoup

from app.scrapers.base import BaseScraper, RegulationItem

logger = logging.getLogger(__name__)

FATF_BASE = "https://www.fatf-gafi.org"
FATF_NEWS_URL = f"{FATF_BASE}/publications/"


class FATFScraper(BaseScraper):
    source_name = "FATF"

    async def scrape(self) -> list[RegulationItem]:
        items: list[RegulationItem] = []

        # FATF has no RSS feed — HTML scraping only
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
            pub_date = self.parse_date(date_el.get_text(strip=True)) if date_el else None

            # FATF content can be AML-specific or general FATF
            category = self.classify(title)
            if category == "OTHER":
                category = "FATF"

            items.append(RegulationItem(
                title=title,
                url=url,
                source="FATF",
                published_date=pub_date,
                category=category,
            ))

        # Fetch body for top items
        for item in items[:5]:
            if not item.body_text:
                item.body_text = await self.fetch_body(
                    item.url,
                    selectors=[".content-main", "article", ".field-items"],
                )

        logger.info("[FATF] Scraped %d items", len(items))
        return items
