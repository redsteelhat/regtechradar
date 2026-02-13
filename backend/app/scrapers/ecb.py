"""ECB (European Central Bank) scraper — RSS + HTML hybrid."""

from __future__ import annotations

import logging

from app.scrapers.base import BaseScraper, RegulationItem

logger = logging.getLogger(__name__)

ECB_BASE = "https://www.ecb.europa.eu"
ECB_RSS_URL = f"{ECB_BASE}/rss/press.html"
ECB_SUPERVISION_URL = "https://www.bankingsupervision.europa.eu/press/pr/html/index.en.html"

# ECB press release RSS – XML feed URL
ECB_RSS_FEED = f"{ECB_BASE}/rss/press.xml"


class ECBScraper(BaseScraper):
    source_name = "ECB"

    async def scrape(self) -> list[RegulationItem]:
        items: list[RegulationItem] = []

        # ── Strategy 1: RSS feed ──────────────────────────
        entries = await self.fetch_rss(ECB_RSS_FEED)
        for entry in entries[:25]:
            title = entry["title"]
            link = entry["link"]
            if not title or len(title) < 10 or not link:
                continue

            pub_date = self.parse_date(entry["published"]) if entry["published"] else None

            items.append(RegulationItem(
                title=title,
                url=link,
                source="ECB",
                body_text=entry.get("summary", "")[:2000],
                published_date=pub_date,
                category=self.classify(title),
            ))

        # ── Strategy 2: HTML fallback (banking supervision) ──
        if len(items) < 5:
            html = await self.fetch(ECB_SUPERVISION_URL)
            if html:
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(html, "lxml")
                for row in soup.select("article, .item, .content-box, dt, .title")[:20]:
                    link_el = row.select_one("a[href]") or (row if row.name == "a" else None)
                    if not link_el or not link_el.get("href"):
                        continue

                    title = link_el.get_text(strip=True)
                    href = link_el["href"]
                    if not title or len(title) < 10:
                        continue

                    url = href if href.startswith("http") else f"https://www.bankingsupervision.europa.eu{href}"

                    # Avoid duplicates within this scrape
                    if any(i.url == url for i in items):
                        continue

                    items.append(RegulationItem(
                        title=title,
                        url=url,
                        source="ECB",
                        published_date=None,
                        category=self.classify(title),
                    ))

        # ── Fetch body text for new items (top 5 only to limit requests) ──
        for item in items[:5]:
            if not item.body_text:
                item.body_text = await self.fetch_body(
                    item.url,
                    selectors=[".section", ".content-box", "article", ".ecb-pressRelease"],
                )

        logger.info("[ECB] Scraped %d items", len(items))
        return items
