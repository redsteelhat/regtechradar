"""Tests for dedup module (content_hash, raw_content_hash for Bölüm 5.1)."""
from src.processing.dedup import content_hash, raw_content_hash


def test_content_hash():
    """Hash is deterministic and differs for different content."""
    a = content_hash("hello")
    b = content_hash("hello")
    c = content_hash("world")
    assert a == b
    assert a != c
    assert len(a) == 64  # SHA-256 hex


def test_raw_content_hash_dedup():
    """Same URL + same body => same hash (dedup); different body => different hash."""
    url = "https://example.eu/news/1"
    body = "Same text"
    h1 = raw_content_hash(url=url, extracted_text=body)
    h2 = raw_content_hash(url=url, extracted_text=body)
    assert h1 == h2
    assert len(h1) == 64
    h3 = raw_content_hash(url=url, extracted_text="Other text")
    assert h1 != h3
    h4 = raw_content_hash(url=url, raw_html=body)
    assert h1 == h4
