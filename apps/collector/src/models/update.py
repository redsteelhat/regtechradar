"""Regulatory update Pydantic models — RawContent (raw_contents) and RegulatoryUpdate (regulatory_updates)."""
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class RawContent(BaseModel):
    """DB entity: raw_contents table (crawler output before processing)."""
    id: UUID
    source_id: UUID | None = None
    url: str
    title: str | None = None
    raw_html: str | None = None
    extracted_text: str | None = None
    content_hash: str
    published_at: datetime | None = None
    crawled_at: datetime | None = None

    model_config = {"from_attributes": True}


class RegulatoryUpdate(BaseModel):
    """DB entity: regulatory_updates table (processed update with summaries, domains, embedding)."""
    id: UUID
    raw_content_id: UUID | None = None
    source_id: UUID | None = None
    title: str
    summary_short: str
    summary_long: str
    original_url: str
    original_lang: str = "en"
    domains: list[str] = Field(default_factory=list)
    regulations: list[str] | None = None
    jurisdictions: list[str] = Field(default_factory=list)
    update_type: str
    severity: str
    published_at: datetime
    effective_date: datetime | None = None
    deadline_date: datetime | None = None
    key_takeaways: list[str] | None = None
    action_items: list[str] | None = None
    affected_entities: list[str] | None = None
    is_published: bool = False
    published_in_digest: UUID | None = None
    embedding: list[float] | None = None  # vector(1536) for semantic search
    created_at: datetime | None = None
    updated_at: datetime | None = None

    model_config = {"from_attributes": True}


class RegulatoryUpdateCreate(BaseModel):
    """Payload for creating a regulatory update (from processing pipeline)."""
    raw_content_id: UUID | None = None
    source_id: UUID | None = None
    title: str
    summary_short: str
    summary_long: str
    original_url: str
    original_lang: str = "en"
    domains: list[str] = Field(default_factory=list)
    regulations: list[str] | None = None
    jurisdictions: list[str] = Field(default_factory=list)
    update_type: str
    severity: str
    published_at: datetime
    effective_date: datetime | None = None
    deadline_date: datetime | None = None
    key_takeaways: list[str] | None = None
    action_items: list[str] | None = None
    affected_entities: list[str] | None = None
    embedding: list[float] | None = None
