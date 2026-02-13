"""Pydantic schemas for request/response validation."""

from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, EmailStr, Field


# ── Enums (mirror SQLAlchemy enums for API) ──────────────────────────────

class RegulationCategoryEnum(str, Enum):
    DORA = "DORA"
    MICA = "MiCA"
    PSD3 = "PSD3"
    AMLA = "AMLA"
    FATF = "FATF"
    AML = "AML"
    OTHER = "OTHER"


class RegulationSourceEnum(str, Enum):
    EBA = "EBA"
    ESMA = "ESMA"
    FATF = "FATF"
    FCA = "FCA"
    FINCEN = "FinCEN"


class LicenseTypeEnum(str, Enum):
    EMI = "EMI"
    PI = "PI"
    VASP = "VASP"
    BANK = "BANK"
    INV_FIRM = "INV_FIRM"
    INSURANCE = "INSURANCE"
    OTHER = "OTHER"


class PlanTierEnum(str, Enum):
    FREE = "free"
    PREMIUM = "premium"
    TEAM = "team"


# ── Auth ─────────────────────────────────────────────────────────────────

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    full_name: str | None = None
    company_name: str | None = None
    license_type: LicenseTypeEnum = LicenseTypeEnum.OTHER


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str | None
    company_name: str | None
    license_type: LicenseTypeEnum
    plan: PlanTierEnum
    created_at: datetime

    model_config = {"from_attributes": True}


# ── Regulations ──────────────────────────────────────────────────────────

class RegulationResponse(BaseModel):
    id: int
    source: RegulationSourceEnum
    category: RegulationCategoryEnum
    title: str
    original_url: str
    published_date: datetime | None
    ai_summary: str | None
    impact_tags: str | None
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}


class RegulationDetailResponse(RegulationResponse):
    raw_content: str
    impact_scores: list[ImpactScoreResponse] = []


class ImpactScoreResponse(BaseModel):
    id: int
    license_type: LicenseTypeEnum
    score: float
    explanation: str | None
    created_at: datetime

    model_config = {"from_attributes": True}


# Forward ref resolution
RegulationDetailResponse.model_rebuild()


# ── Alerts ───────────────────────────────────────────────────────────────

class AlertCreateRequest(BaseModel):
    keyword: str | None = None
    category: RegulationCategoryEnum | None = None


class AlertResponse(BaseModel):
    id: int
    keyword: str | None
    category: RegulationCategoryEnum | None
    enabled: bool
    created_at: datetime

    model_config = {"from_attributes": True}


# ── Dashboard Stats ─────────────────────────────────────────────────────

class DashboardStats(BaseModel):
    total_regulations: int
    new_this_week: int
    sources_active: int
    categories: dict[str, int]
