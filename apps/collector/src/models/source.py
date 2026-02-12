"""Source Pydantic models."""
from pydantic import BaseModel


class SourceConfig(BaseModel):
    """Source definition from registry."""
    slug: str
    name: str
    base_url: str
    jurisdiction: list[str]
    crawl_frequency: str = "6h"
    is_active: bool = True
