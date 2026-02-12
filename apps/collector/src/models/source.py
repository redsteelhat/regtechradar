"""Source Pydantic models (registry + DB)."""
from typing import Any

from pydantic import BaseModel, Field


class SourceConfig(BaseModel):
    """Source definition from registry (regtech.md §6)."""
    slug: str
    name: str
    base_url: str
    jurisdiction: list[str]
    crawl_frequency: str = "6h"
    priority: int = 1
    is_active: bool = True
    crawl_targets: list[dict[str, Any]] = Field(default_factory=list)
    content_selectors: dict[str, str] = Field(default_factory=dict)
