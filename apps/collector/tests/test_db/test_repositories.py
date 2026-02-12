"""Tests for raw storage and dedup: save_raw_contents, content_hash, tekrar işlemeyi engelleme (Bölüm 5.1)."""
import os
from datetime import datetime, timezone
import uuid

import pytest
from sqlalchemy import text
from sqlalchemy.orm import Session

from src.db.connection import get_session
from src.db.repositories import (
    ensure_source,
    get_source_id_by_slug,
    save_raw_contents,
    raw_content_already_processed,
    get_raw_content_ids_pending_processing,
)


def _has_postgres() -> bool:
    try:
        from src.config import settings
        url = settings.database_url
    except Exception:
        url = os.environ.get("DATABASE_URL", "")
    return "postgresql" in url


@pytest.mark.skipif(not _has_postgres(), reason="DATABASE_URL not set or not Postgres")
def test_ensure_source_and_save_raw_contents_dedup():
    """Ensure source exists, save two items (same content_hash second time), expect one insert on second call."""
    session = get_session()
    slug = f"test-{uuid.uuid4().hex[:8]}"
    try:
        source_id = ensure_source(
            session,
            slug=slug,
            name="Test Source",
            url="https://test.example.eu",
            source_type="regulator",
            jurisdiction=["EU"],
        )
        assert source_id is not None
        assert get_source_id_by_slug(session, slug) == source_id

        items = [
            {
                "url": "https://test.example.eu/doc/1",
                "title": "Doc 1",
                "extracted_text": "Body one",
                "raw_html": None,
                "published_at": None,
            },
        ]
        inserted = save_raw_contents(session, source_id, items)
        assert len(inserted) == 1
        first_id = inserted[0]

        # Same content => same content_hash => duplicate, no new row
        inserted2 = save_raw_contents(session, source_id, items)
        assert len(inserted2) == 0

        # Different URL + same body => new row
        items2 = [{**items[0], "url": "https://test.example.eu/doc/2"}]
        inserted3 = save_raw_contents(session, source_id, items2)
        assert len(inserted3) == 1
        assert inserted3[0] != first_id
    finally:
        session.execute(text("DELETE FROM raw_contents WHERE source_id = (SELECT id FROM sources WHERE slug = :s)"), {"s": slug})
        session.execute(text("DELETE FROM sources WHERE slug = :s"), {"s": slug})
        session.commit()
        session.close()


@pytest.mark.skipif(not _has_postgres(), reason="DATABASE_URL not set or not Postgres")
def test_raw_content_already_processed_and_pending():
    """raw_content_already_processed and get_raw_content_ids_pending_processing (tekrar işlemeyi engelleme)."""
    session = get_session()
    slug = f"test-{uuid.uuid4().hex[:8]}"
    now = datetime.now(timezone.utc)
    try:
        source_id = ensure_source(
            session, slug=slug, name="Test Source", url="https://test.example.eu",
            source_type="regulator", jurisdiction=["EU"],
        )
        items = [{"url": "https://test.example.eu/doc/dedup", "title": "Dedup", "extracted_text": "Body", "published_at": None}]
        inserted = save_raw_contents(session, source_id, items)
        assert len(inserted) == 1
        raw_id = inserted[0]

        assert raw_content_already_processed(session, raw_id) is False
        pending = get_raw_content_ids_pending_processing(session, limit=10)
        assert raw_id in pending

        session.execute(
            text("""
                INSERT INTO regulatory_updates
                (raw_content_id, source_id, title, summary_short, summary_long, original_url,
                 domains, jurisdictions, update_type, severity, published_at)
                VALUES (:raw_id, :source_id, 'T', 'S', 'L', 'https://test.example.eu/doc/dedup',
                 ARRAY['DORA_ICT'], ARRAY['EU'], 'guideline', 'medium', :now)
            """),
            {"raw_id": raw_id, "source_id": source_id, "now": now},
        )
        session.commit()

        assert raw_content_already_processed(session, raw_id) is True
        pending2 = get_raw_content_ids_pending_processing(session, limit=10)
        assert raw_id not in pending2
    finally:
        session.execute(text("DELETE FROM regulatory_updates WHERE raw_content_id IN (SELECT id FROM raw_contents WHERE source_id = (SELECT id FROM sources WHERE slug = :s))"), {"s": slug})
        session.execute(text("DELETE FROM raw_contents WHERE source_id = (SELECT id FROM sources WHERE slug = :s)"), {"s": slug})
        session.execute(text("DELETE FROM sources WHERE slug = :s"), {"s": slug})
        session.commit()
        session.close()
