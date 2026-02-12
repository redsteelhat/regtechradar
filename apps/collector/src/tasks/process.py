"""AI processing pipeline task — parse → summarize → store (content_hash dedup: tekrar işleme yok)."""
from uuid import UUID

from src.db.connection import get_session
from src.db.repositories import raw_content_already_processed


def process_raw_content(raw_content_id: str | UUID) -> None:
    """
    Process a single raw content through AI pipeline.
    Skips if already processed (regulatory_update exists for this raw_content_id).
    """
    uid = UUID(str(raw_content_id)) if isinstance(raw_content_id, str) else raw_content_id
    session = get_session()
    try:
        if raw_content_already_processed(session, uid):
            return
        # TODO: parse → classify → summarize → embed → insert regulatory_update
    finally:
        session.close()
