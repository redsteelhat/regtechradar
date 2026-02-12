"""ImpactAssessment Pydantic model."""
from pydantic import BaseModel


class ImpactAssessment(BaseModel):
    """Company profile impact for one update."""
    regulatory_update_id: str
    company_profile_id: str
    impact_score: int  # 0-100
    impact_category: str  # direct | indirect | monitoring
    reasoning: str
    recommended_actions: list[str]
