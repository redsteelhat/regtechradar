"""Data access layer — sources, raw_contents (Bölüm 5.1 raw storage + dedup)."""
from datetime import datetime, timezone
from typing import Any
from uuid import UUID

from sqlalchemy import text
from sqlalchemy.orm import Session

from src.processing.dedup import raw_content_hash


def get_source_id_by_slug(session: Session, slug: str) -> UUID | None:
    """Return source id for slug, or None if not found."""
    row = session.execute(text("SELECT id FROM sources WHERE slug = :slug"), {"slug": slug}).fetchone()
    return row[0] if row else None


def ensure_source(
    session: Session,
    slug: str,
    name: str,
    url: str,
    source_type: str = "regulator",
    jurisdiction: list[str] | None = None,
) -> UUID:
    """Get or create source by slug; return id."""
    j = jurisdiction or []
    existing = session.execute(text("SELECT id FROM sources WHERE slug = :slug"), {"slug": slug}).fetchone()
    if existing:
        return existing[0]
    session.execute(
        text("""
            INSERT INTO sources (slug, name, url, source_type, jurisdiction, crawl_frequency, is_active)
            VALUES (:slug, :name, :url, :source_type, :jurisdiction, '6h', true)
        """),
        {"slug": slug, "name": name, "url": url, "source_type": source_type, "jurisdiction": j},
    )
    session.commit()
    row = session.execute(text("SELECT id FROM sources WHERE slug = :slug"), {"slug": slug}).fetchone()
    assert row
    return row[0]


def save_raw_contents(
    session: Session,
    source_id: UUID,
    items: list[dict[str, Any]],
) -> list[UUID]:
    """
    Insert crawl items into raw_contents; skip duplicates by content_hash (Bölüm 5.1).
    Each item: url, title, raw_html, extracted_text, published_at (optional).
    Returns list of inserted row ids (new only).
    """
    inserted: list[UUID] = []
    now = datetime.now(timezone.utc)
    for item in items:
        url = item.get("url") or ""
        title = item.get("title")
        raw_html = item.get("raw_html")
        extracted_text = item.get("extracted_text")
        published_at = item.get("published_at")
        if not url:
            continue
        ch = raw_content_hash(url=url, extracted_text=extracted_text, raw_html=raw_html, title=title)
        # ON CONFLICT (content_hash) DO NOTHING RETURNING id — only returns rows that were inserted
        result = session.execute(
            text("""
                INSERT INTO raw_contents (source_id, url, title, raw_html, extracted_text, content_hash, published_at, crawled_at)
                VALUES (:source_id, :url, :title, :raw_html, :extracted_text, :content_hash, :published_at, :crawled_at)
                ON CONFLICT (content_hash) DO NOTHING
                RETURNING id
            """),
            {
                "source_id": source_id,
                "url": url,
                "title": title,
                "raw_html": raw_html,
                "extracted_text": extracted_text,
                "content_hash": ch,
                "published_at": published_at,
                "crawled_at": now,
            },
        )
        row = result.fetchone()
        if row:
            inserted.append(row[0])
    session.commit()
    return inserted


def update_source_last_crawled(session: Session, source_id: UUID) -> None:
    """Set last_crawled_at = now() for source."""
    session.execute(
        text("UPDATE sources SET last_crawled_at = :now WHERE id = :id"),
        {"now": datetime.now(timezone.utc), "id": source_id},
    )
    session.commit()
