"""ESMA (European Securities and Markets Authority) scraper — RSS + HTML hybrid."""

from __future__ import annotations

import logging

from bs4 import BeautifulSoup

from app.scrapers.base import BaseScraper, RegulationItem

logger = logging.getLogger(__name__)

ESMA_BASE = "https://www.esma.europa.eu"
ESMA_NEWS_URL = f"{ESMA_BASE}/press-news/esma-news"


class ESMAScraper(BaseScraper):
    source_name = "ESMA"

    async def scrape(self) -> list[RegulationItem]:
        items: list[RegulationItem] = []

        # ── Strategy 1: Try to discover RSS from the page ──
        html = await self.fetch(ESMA_NEWS_URL)
        if html:
            soup = BeautifulSoup(html, "lxml")

            # Check for RSS link in head
            rss_link = soup.select_one('link[type="application/rss+xml"]')
            if rss_link and rss_link.get("href"):
                rss_url = rss_link["href"]
                if not rss_url.startswith("http"):
                    rss_url = f"{ESMA_BASE}{rss_url}"
                entries = await self.fetch_rss(rss_url)
                for entry in entries[:25]:
                    title = entry["title"]
                    link = entry["link"]
                    if not title or len(title) < 10 or not link:
                        continue
                    pub_date = self.parse_date(entry["published"]) if entry["published"] else None
                    items.append(RegulationItem(
                        title=title,
                        url=link,
                        source="ESMA",
                        body_text=entry.get("summary", "")[:2000],
                        published_date=pub_date,
                        category=self.classify(title),
                    ))

            # ── Strategy 2: HTML scraping ─────────────────
            if len(items) < 3:
                for row in soup.select(".view-content .views-row, article, .node--type-news")[:20]:
                    link_el = row.select_one("a[href]")
                    if not link_el:
                        continue

                    title = link_el.get_text(strip=True)
                    href = link_el["href"]
                    if not title or len(title) < 10:
                        continue

                    url = href if href.startswith("http") else f"{ESMA_BASE}{href}"
                    if any(i.url == url for i in items):
                        continue

                    date_el = row.select_one("time, .date-display-single, .field--name-created")
                    pub_date = self.parse_date(date_el.get_text(strip=True)) if date_el else None

                    items.append(RegulationItem(
                        title=title,
                        url=url,
                        source="ESMA",
                        published_date=pub_date,
                        category=self.classify(title),
                    ))

        # ── Fetch body for top items ──────────────────────
        for item in items[:5]:
            if not item.body_text:
                item.body_text = await self.fetch_body(
                    item.url,
                    selectors=[".field--name-body", "article", ".node__content"],
                )

        logger.info("[ESMA] Scraped %d items", len(items))
        return items
