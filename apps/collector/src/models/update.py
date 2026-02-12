"""RegulatoryUpdate Pydantic model — matches DB."""
from datetime import datetime
from pydantic import BaseModel


class RegulatoryUpdate(BaseModel):
    """Processed regulatory update."""
    title: str
    summary_short: str
    summary_long: str
    original_url: str
    original_lang: str = "en"
    domains: list[str]
    regulations: list[str]
    jurisdictions: list[str]
    update_type: str
    severity: str
    published_at: datetime
    effective_date: datetime | None = None
    deadline_date: datetime | None = None
    key_takeaways: list[str]
    action_items: list[str]
    affected_entities: list[str]
