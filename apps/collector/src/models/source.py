"""Source Pydantic models — registry config and DB entity (sources table)."""
from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field


class SourceConfig(BaseModel):
    """Source definition from registry (regtech.md §6) — used by crawlers."""
    slug: str
    name: str
    base_url: str
    jurisdiction: list[str]
    crawl_frequency: str = "6h"
    priority: int = 1
    is_active: bool = True
    crawl_targets: list[dict[str, Any]] = Field(default_factory=list)
    content_selectors: dict[str, str] = Field(default_factory=dict)


class Source(BaseModel):
    """DB entity: sources table (Alembic 001)."""
    id: UUID
    slug: str
    name: str
    url: str
    source_type: str
    jurisdiction: list[str] = Field(default_factory=list)
    crawl_frequency: str = "6h"
    is_active: bool = True
    last_crawled_at: datetime | None = None
    config_json: dict[str, Any] | None = None
    created_at: datetime | None = None

    model_config = {"from_attributes": True}
