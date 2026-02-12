"""Content deduplication by content_hash (SHA-256)."""
import hashlib


def content_hash(text: str) -> str:
    """Compute SHA-256 hash of normalized content."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()
