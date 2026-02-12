"""Tests for registry loader."""
from pathlib import Path

import pytest

from src.sources.registry import load_registry


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
