"""Tests for dedup module."""
from src.processing.dedup import content_hash


def test_content_hash():
    """Hash is deterministic and differs for different content."""
    a = content_hash("hello")
    b = content_hash("hello")
    c = content_hash("world")
    assert a == b
    assert a != c
    assert len(a) == 64  # SHA-256 hex
