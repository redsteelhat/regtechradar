"""Company profile (user context) Pydantic model — DB entity (company_profiles table)."""
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class CompanyProfile(BaseModel):
    """DB entity: company_profiles table — user's company context for impact scoring."""
    id: UUID
    user_id: UUID
    company_name: str | None = None
    license_types: list[str] | None = None
    jurisdictions: list[str] | None = None
    domains: list[str] | None = None
    entity_size: str | None = None
    services: list[str] | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    model_config = {"from_attributes": True}


class CompanyProfileCreate(BaseModel):
    """Payload for creating a company profile."""
    user_id: UUID
    company_name: str | None = None
    license_types: list[str] | None = None
    jurisdictions: list[str] | None = None
    domains: list[str] | None = None
    entity_size: str | None = None
    services: list[str] | None = None
