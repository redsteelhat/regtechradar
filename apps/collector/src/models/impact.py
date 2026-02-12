"""Impact assessment Pydantic model — DB entity (impact_assessments table)."""
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class ImpactAssessment(BaseModel):
    """DB entity: impact_assessments table (update × company_profile impact score)."""
    id: UUID
    regulatory_update_id: UUID
    company_profile_id: UUID
    impact_score: int = Field(..., ge=0, le=100)
    impact_category: str  # direct | indirect | monitoring
    reasoning: str
    recommended_actions: list[str] | None = None
    created_at: datetime | None = None

    model_config = {"from_attributes": True}


class ImpactAssessmentCreate(BaseModel):
    """Payload for creating an impact assessment."""
    regulatory_update_id: UUID
    company_profile_id: UUID
    impact_score: int = Field(..., ge=0, le=100)
    impact_category: str
    reasoning: str
    recommended_actions: list[str] | None = None
