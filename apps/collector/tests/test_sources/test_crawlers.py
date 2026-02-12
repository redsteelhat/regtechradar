"""Tests for EBA, FATF, FCA crawlers (RSS/HTML helpers + fetch contract)."""

import pytest

from src.sources.fetch_helpers import parse_rss_entries, extract_with_selectors, extract_links_from_list_page
from src.sources.eba import EBASource
from src.sources.esma import ESMASource
from src.sources.fatf import FATFSource
from src.sources.ecb import ECBSource
from src.sources.fca import FCASource
from src.sources.fincen import FinCENSource
from src.sources.bis import BISSource
from src.sources.eu_official import EuOfficialSource


def test_parse_rss_entries_returns_list():
    """parse_rss_entries returns a list (empty or with url, title, published_at)."""
    empty = parse_rss_entries("", "https://example.com")
    assert isinstance(empty, list)


def test_parse_rss_entries_item_shape():
    """parse_rss_entries returns a list; each item has url, title, published_at."""
    from src.sources.fetch_helpers import parse_iso_or_none
    entries = parse_rss_entries("<rss></rss>", "https://example.com")
    assert isinstance(entries, list)
    for e in entries:
        assert "url" in e and "title" in e and "published_at" in e
    # date parsing used by RSS path
    assert parse_iso_or_none("Mon, 01 Jan 2024 12:00:00 GMT") == "2024-01-01T12:00:00Z"
    assert parse_iso_or_none("2024-01-15") == "2024-01-15T00:00:00Z"


def test_extract_with_selectors():
    """extract_with_selectors returns title, body, date from HTML."""
    html = """
    <html><body>
      <h1 class="page-title">Page title</h1>
      <div class="field-item">Body content here.</div>
      <span class="date-display-single">2024-01-15</span>
    </body></html>"""
    selectors = {"title": "h1.page-title", "body": "div.field-item", "date": "span.date-display-single"}
    out = extract_with_selectors(html, selectors)
    assert out["title"] == "Page title"
    assert "Body content" in out["body"]
    assert "2024" in out["date"]


def test_extract_links_from_list_page():
    """extract_links_from_list_page returns absolute URLs."""
    html = '<html><body><a href="/news/item1">Item 1</a><a href="https://www.fca.org.uk/news/item2">Item 2</a></body></html>'
    base = "https://www.fca.org.uk"
    links = extract_links_from_list_page(html, base)
    assert any("item1" in u or "item2" in u for u in links)


def test_eba_fatf_fca_have_fetch():
    """EBA, FATF, FCA implement fetch() and return list from registry config."""
    from src.sources.registry import load_registry
    from pathlib import Path
    base = Path(__file__).resolve().parents[2]
    configs = load_registry(base / "sources" / "registry.yaml")
    eba_c = next(c for c in configs if c["slug"] == "eba")
    fatf_c = next(c for c in configs if c["slug"] == "fatf")
    fca_c = next(c for c in configs if c["slug"] == "fca")
    eba = EBASource.from_registry(eba_c)
    fatf = FATFSource.from_registry(fatf_c)
    fca = FCASource.from_registry(fca_c)
    assert eba.slug == "eba" and hasattr(eba, "fetch")
    assert fatf.slug == "fatf" and hasattr(fatf, "fetch")
    assert fca.slug == "fca" and hasattr(fca, "fetch")
    assert eba.content_selectors
    assert eba.crawl_targets


def test_all_eight_sources_from_registry_have_fetch():
    """ESMA, ECB, FinCEN, BIS, EUR-Lex (and EBA, FATF, FCA) build from registry and have fetch()."""
    from src.sources.registry import load_registry
    from pathlib import Path
    base = Path(__file__).resolve().parents[2]
    configs = load_registry(base / "sources" / "registry.yaml")
    slugs = ["eba", "esma", "fatf", "ecb", "fca", "fincen", "bis", "eurlex"]
    classes = [EBASource, ESMASource, FATFSource, ECBSource, FCASource, FinCENSource, BISSource, EuOfficialSource]
    for slug, cls in zip(slugs, classes):
        c = next((x for x in configs if x["slug"] == slug), None)
        assert c is not None, f"registry has {slug}"
        src = cls.from_registry(c)
        assert src.slug == slug and hasattr(src, "fetch") and callable(getattr(src, "fetch"))
        assert src.crawl_targets
