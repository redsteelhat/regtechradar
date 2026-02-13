"""FCA (Financial Conduct Authority, UK) scraper — RSS + HTML hybrid."""

from __future__ import annotations

import logging

from bs4 import BeautifulSoup

from app.scrapers.base import BaseScraper, RegulationItem

logger = logging.getLogger(__name__)

FCA_BASE = "https://www.fca.org.uk"
FCA_RSS_URL = f"{FCA_BASE}/news/rss.xml"
FCA_NEWS_URL = f"{FCA_BASE}/news/news-stories"


class FCAScraper(BaseScraper):
    source_name = "FCA"

    async def scrape(self) -> list[RegulationItem]:
        items: list[RegulationItem] = []

        # ── Strategy 1: RSS feed ──────────────────────────
        entries = await self.fetch_rss(FCA_RSS_URL)
        for entry in entries[:25]:
            title = entry["title"]
            link = entry["link"]
            if not title or len(title) < 10 or not link:
                continue

            pub_date = self.parse_date(entry["published"]) if entry["published"] else None

            items.append(RegulationItem(
                title=title,
                url=link,
                source="FCA",
                body_text=entry.get("summary", "")[:2000],
                published_date=pub_date,
                category=self.classify(title),
            ))

        # ── Strategy 2: HTML fallback ─────────────────────
        if len(items) < 3:
            html = await self.fetch(FCA_NEWS_URL)
            if html:
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
                    if any(i.url == url for i in items):
                        continue

                    date_el = row.select_one(".date, time, .search-item__date")
                    pub_date = self.parse_date(date_el.get_text(strip=True)) if date_el else None

                    items.append(RegulationItem(
                        title=title,
                        url=url,
                        source="FCA",
                        published_date=pub_date,
                        category=self.classify(title),
                    ))

        # ── Fetch body for top items ──────────────────────
        for item in items[:5]:
            if not item.body_text:
                item.body_text = await self.fetch_body(
                    item.url,
                    selectors=[".article-body", ".main-content", "article"],
                )

        logger.info("[FCA] Scraped %d items", len(items))
        return items
