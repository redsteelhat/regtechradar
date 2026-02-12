"""Scheduled crawl tasks — fetch from source and store in raw_contents (Bölüm 5.1)."""
import asyncio
from typing import Any

from src.db.connection import get_session
from src.db.repositories import ensure_source, get_source_id_by_slug, save_raw_contents, update_source_last_crawled
from src.sources import get_sources


def crawl_source(slug: str) -> list[str]:
    """
    Crawl a single source by slug: fetch items, write to raw_contents with content_hash dedup.
    Returns list of inserted raw_content ids (as hex strings) for logging.
    """
    sources = get_sources()
    source = next((s for s in sources if s.slug == slug), None)
    if not source:
        return []
    items: list[dict[str, Any]] = asyncio.run(source.fetch())
    if not items:
        return []
    session = get_session()
    try:
        source_id = get_source_id_by_slug(session, slug)
        if source_id is None:
            source_id = ensure_source(
                session,
                slug=slug,
                name=source.name,
                url=source.base_url,
                source_type="regulator",
                jurisdiction=source.jurisdiction,
            )
        inserted = save_raw_contents(session, source_id, items)
        if inserted:
            update_source_last_crawled(session, source_id)
        return [str(uid) for uid in inserted]
    finally:
        session.close()
