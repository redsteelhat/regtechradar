"""CompanyProfile Pydantic model."""
from pydantic import BaseModel


class CompanyProfile(BaseModel):
    """Company profile for impact scoring."""
    user_id: str
    company_name: str | None = None
    license_types: list[str]
    jurisdictions: list[str]
    domains: list[str]
    entity_size: str
    services: list[str]
