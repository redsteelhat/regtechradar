"""SQLAlchemy ORM models for RegTech Radar."""

import enum
from datetime import datetime, timezone

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from app.database import Base


# ── Enums ───────────────────────────────────────────────────────────────────

class RegulationCategory(str, enum.Enum):
    DORA = "DORA"
    MICA = "MiCA"
    PSD3 = "PSD3"
    AMLA = "AMLA"
    FATF = "FATF"
    AML = "AML"
    OTHER = "OTHER"


class RegulationSource(str, enum.Enum):
    EBA = "EBA"
    ESMA = "ESMA"
    FATF = "FATF"
    FCA = "FCA"
    FINCEN = "FinCEN"


class LicenseType(str, enum.Enum):
    EMI = "EMI"           # Electronic Money Institution
    PI = "PI"             # Payment Institution
    VASP = "VASP"         # Virtual Asset Service Provider
    BANK = "BANK"         # Bank / Credit Institution
    INV_FIRM = "INV_FIRM" # Investment Firm
    INSURANCE = "INSURANCE"
    OTHER = "OTHER"


class PlanTier(str, enum.Enum):
    FREE = "free"
    PREMIUM = "premium"
    TEAM = "team"


class RegulationStatus(str, enum.Enum):
    NEW = "new"
    ANALYZED = "analyzed"
    PUBLISHED = "published"


# ── Models ──────────────────────────────────────────────────────────────────

def _utcnow():
    return datetime.now(timezone.utc)


class Regulation(Base):
    __tablename__ = "regulations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    source = Column(Enum(RegulationSource), nullable=False, index=True)
    category = Column(Enum(RegulationCategory), default=RegulationCategory.OTHER, index=True)
    title = Column(String(512), nullable=False)
    original_url = Column(String(1024), nullable=False, unique=True)
    published_date = Column(DateTime, nullable=True)
    raw_content = Column(Text, nullable=False, default="")
    ai_summary = Column(Text, nullable=True)
    impact_tags = Column(String(512), nullable=True)  # comma-separated tags
    status = Column(Enum(RegulationStatus), default=RegulationStatus.NEW, index=True)
    created_at = Column(DateTime, default=_utcnow)
    updated_at = Column(DateTime, default=_utcnow, onupdate=_utcnow)

    impact_scores = relationship("ImpactScore", back_populates="regulation", cascade="all, delete-orphan")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(320), nullable=False, unique=True, index=True)
    hashed_password = Column(String(128), nullable=False)
    full_name = Column(String(256), nullable=True)
    company_name = Column(String(256), nullable=True)
    license_type = Column(Enum(LicenseType), default=LicenseType.OTHER)
    plan = Column(Enum(PlanTier), default=PlanTier.FREE)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=_utcnow)

    alerts = relationship("Alert", back_populates="user", cascade="all, delete-orphan")
    subscription = relationship("Subscription", back_populates="user", uselist=False, cascade="all, delete-orphan")


class ImpactScore(Base):
    __tablename__ = "impact_scores"

    id = Column(Integer, primary_key=True, autoincrement=True)
    regulation_id = Column(Integer, ForeignKey("regulations.id", ondelete="CASCADE"), nullable=False, index=True)
    license_type = Column(Enum(LicenseType), nullable=False, index=True)
    score = Column(Float, nullable=False)  # 1-10
    explanation = Column(Text, nullable=True)
    created_at = Column(DateTime, default=_utcnow)

    regulation = relationship("Regulation", back_populates="impact_scores")


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    keyword = Column(String(256), nullable=True)
    category = Column(Enum(RegulationCategory), nullable=True)
    enabled = Column(Boolean, default=True)
    created_at = Column(DateTime, default=_utcnow)

    user = relationship("User", back_populates="alerts")


class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True)
    plan = Column(Enum(PlanTier), default=PlanTier.FREE)
    stripe_customer_id = Column(String(256), nullable=True)
    active_until = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=_utcnow)

    user = relationship("User", back_populates="subscription")
