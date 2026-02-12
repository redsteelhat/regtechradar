"""Content deduplication by content_hash (SHA-256) — Bölüm 5.1."""
import hashlib


def content_hash(text: str) -> str:
    """Compute SHA-256 hash of normalized content."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def raw_content_hash(url: str, extracted_text: str | None = None, raw_html: str | None = None, title: str | None = None) -> str:
    """
    Compute content_hash for raw_contents dedup.
    Same URL + same body => same hash (duplicate skipped).
    """
    body = (extracted_text or "").strip() or (raw_html or "").strip() or (title or "").strip()
    canonical = f"{url.strip()}\n{body}"
    return content_hash(canonical)
