"""Tests for registry loader and source base."""
from pathlib import Path

import pytest

from src.sources.registry import load_registry
from src.sources import get_sources, AbstractSource


def test_load_registry_returns_eight_sources():
    """Registry should load 8 sources (EBA, ESMA, FATF, ECB, FCA, FinCEN, BIS, EUR-Lex)."""
    base = Path(__file__).resolve().parents[2]  # apps/collector
    path = base / "sources" / "registry.yaml"
    sources = load_registry(path)
    assert len(sources) == 8
    slugs = [s["slug"] for s in sources]
    assert slugs == [
        "eba",
        "esma",
        "fatf",
        "ecb",
        "fca",
        "fincen",
        "bis",
        "eurlex",
    ]


def test_load_registry_source_has_required_keys():
    """Each source must have slug, name, base_url, jurisdiction."""
    base = Path(__file__).resolve().parents[2]
    path = base / "sources" / "registry.yaml"
    sources = load_registry(path)
    for s in sources:
        assert "slug" in s
        assert "name" in s
        assert "base_url" in s
        assert "jurisdiction" in s
        assert isinstance(s["jurisdiction"], list)


def test_get_sources_returns_eight_abstract_sources():
    """get_sources() should return 8 AbstractSource instances from registry."""
    base = Path(__file__).resolve().parents[2]
    configs = load_registry(base / "sources" / "registry.yaml")
    sources = get_sources(configs)
    assert len(sources) == 8
    for s in sources:
        assert isinstance(s, AbstractSource)
        assert s.slug
        assert s.base_url.startswith("https://")


def test_from_registry_sets_crawl_targets_and_full_url():
    """from_registry populates crawl_targets; full_url builds correct URL."""
    configs = load_registry(Path(__file__).resolve().parents[2] / "sources" / "registry.yaml")
    eba_config = next(c for c in configs if c["slug"] == "eba")
    from src.sources.eba import EBASource
    eba = EBASource.from_registry(eba_config)
    assert eba.slug == "eba"
    assert len(eba.crawl_targets) >= 2
    assert eba.full_url("/rss/news") == "https://www.eba.europa.eu/rss/news"
