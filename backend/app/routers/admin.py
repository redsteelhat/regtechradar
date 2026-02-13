"""Admin router — manual scrape trigger, data seeding, stats."""

from __future__ import annotations

import logging

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Regulation, RegulationSource, RegulationCategory, RegulationStatus, ImpactScore, LicenseType
from app.scrapers.base import RegulationItem
from app.scrapers.eba import EBAScraper
from app.scrapers.esma import ESMAScraper
from app.scrapers.fatf import FATFScraper
from app.scrapers.fca import FCAScraper
from app.scrapers.fincen import FinCENScraper
from app.services import ai_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/admin", tags=["admin"])

SCRAPERS = [EBAScraper, ESMAScraper, FATFScraper, FCAScraper, FinCENScraper]

LICENSE_TYPES = [lt.value for lt in LicenseType if lt != LicenseType.OTHER]


@router.post("/scrape")
async def trigger_scrape(db: AsyncSession = Depends(get_db)):
    """Run all scrapers, store new regulations, and generate AI analysis."""
    total_new = 0

    for ScraperClass in SCRAPERS:
        scraper = ScraperClass()
        try:
            items = await scraper.scrape()
            for item in items:
                total_new += await _store_regulation(db, item)
        except Exception as exc:
            logger.error("Scraper %s failed: %s", ScraperClass.source_name, exc)
        finally:
            await scraper.close()

    await db.commit()
    return {"message": f"Scrape complete. {total_new} new regulations added."}


@router.post("/seed")
async def seed_demo_data(db: AsyncSession = Depends(get_db)):
    """Seed the database with demo regulation data for development."""
    demo_items = _get_demo_data()
    count = 0
    for item in demo_items:
        existing = await db.execute(
            select(Regulation).where(Regulation.original_url == item.url)
        )
        if existing.scalar_one_or_none():
            continue

        source_val = _map_source(item.source)
        category_val = _map_category(item.category)

        reg = Regulation(
            source=source_val,
            category=category_val,
            title=item.title,
            original_url=item.url,
            published_date=item.published_date,
            raw_content=item.body_text,
            ai_summary=await ai_service.summarize(item.body_text) if item.body_text else None,
            status=RegulationStatus.ANALYZED,
        )
        db.add(reg)
        await db.flush()

        # Generate impact scores for each license type
        for lt in LICENSE_TYPES:
            impact = await ai_service.analyze_impact(item.body_text or item.title, lt)
            score = ImpactScore(
                regulation_id=reg.id,
                license_type=LicenseType(lt),
                score=impact["score"],
                explanation=impact["explanation"],
            )
            db.add(score)

        count += 1

    await db.commit()
    return {"message": f"Seeded {count} demo regulations."}


async def _store_regulation(db: AsyncSession, item: RegulationItem) -> int:
    """Store a single scraped regulation if it doesn't already exist. Returns 1 if new, 0 if duplicate."""
    existing = await db.execute(
        select(Regulation).where(Regulation.original_url == item.url)
    )
    if existing.scalar_one_or_none():
        return 0

    source_val = _map_source(item.source)
    category_val = _map_category(item.category)

    reg = Regulation(
        source=source_val,
        category=category_val,
        title=item.title,
        original_url=item.url,
        published_date=item.published_date,
        raw_content=item.body_text,
        status=RegulationStatus.NEW,
    )
    db.add(reg)
    await db.flush()

    # Generate AI summary
    if item.body_text:
        reg.ai_summary = await ai_service.summarize(item.body_text)
        reg.status = RegulationStatus.ANALYZED

    # Generate impact scores
    for lt in LICENSE_TYPES:
        impact = await ai_service.analyze_impact(item.body_text or item.title, lt)
        score = ImpactScore(
            regulation_id=reg.id,
            license_type=LicenseType(lt),
            score=impact["score"],
            explanation=impact["explanation"],
        )
        db.add(score)

    return 1


def _map_source(source: str) -> RegulationSource:
    mapping = {"EBA": RegulationSource.EBA, "ESMA": RegulationSource.ESMA, "FATF": RegulationSource.FATF, "FCA": RegulationSource.FCA, "FinCEN": RegulationSource.FINCEN}
    return mapping.get(source, RegulationSource.EBA)


def _map_category(cat: str) -> RegulationCategory:
    mapping = {"DORA": RegulationCategory.DORA, "MiCA": RegulationCategory.MICA, "PSD3": RegulationCategory.PSD3, "AMLA": RegulationCategory.AMLA, "FATF": RegulationCategory.FATF, "AML": RegulationCategory.AML}
    return mapping.get(cat, RegulationCategory.OTHER)


def _get_demo_data() -> list[RegulationItem]:
    """Return hardcoded demo regulations for seeding."""
    from datetime import datetime
    return [
        RegulationItem(
            title="DORA — Final RTS on ICT Risk Management Framework Published",
            url="https://www.eba.europa.eu/dora-rts-ict-risk-2025",
            source="EBA",
            category="DORA",
            published_date=datetime(2025, 1, 17),
            body_text=(
                "The European Banking Authority has published the final Regulatory Technical Standards (RTS) "
                "on ICT risk management frameworks under the Digital Operational Resilience Act (DORA). "
                "Financial entities must implement comprehensive ICT risk management practices including "
                "identification, protection, detection, response, and recovery capabilities. "
                "The RTS specifies requirements for ICT third-party risk management, incident reporting, "
                "and digital operational resilience testing. Compliance deadline: January 17, 2025."
            ),
        ),
        RegulationItem(
            title="MiCA — Crypto-Asset Service Providers Authorization Requirements",
            url="https://www.esma.europa.eu/mica-casp-authorization-2025",
            source="ESMA",
            category="MiCA",
            published_date=datetime(2025, 6, 30),
            body_text=(
                "ESMA has released final guidelines on the authorization process for Crypto-Asset "
                "Service Providers (CASPs) under the Markets in Crypto-Assets Regulation (MiCA). "
                "CASPs must apply for authorization by June 30, 2025, demonstrating adequate capital, "
                "governance arrangements, and operational resilience. The guidelines cover AML/CFT "
                "compliance requirements, custody of crypto-assets, and consumer protection measures."
            ),
        ),
        RegulationItem(
            title="PSD3 — Enhanced Strong Customer Authentication Standards",
            url="https://www.eba.europa.eu/psd3-sca-standards-2025",
            source="EBA",
            category="PSD3",
            published_date=datetime(2025, 3, 15),
            body_text=(
                "The EBA has issued updated technical standards for Strong Customer Authentication (SCA) "
                "under PSD3. Key changes include stricter requirements for transaction risk analysis, "
                "new exemption thresholds, and enhanced fraud monitoring obligations. Payment service "
                "providers must update their authentication mechanisms and reporting frameworks."
            ),
        ),
        RegulationItem(
            title="AMLA — New EU Anti-Money Laundering Authority Operational Framework",
            url="https://www.eba.europa.eu/amla-operational-framework-2025",
            source="EBA",
            category="AMLA",
            published_date=datetime(2025, 7, 1),
            body_text=(
                "The new EU Anti-Money Laundering Authority (AMLA) headquartered in Frankfurt has issued "
                "its initial operational framework. AMLA will directly supervise the highest-risk financial "
                "entities and coordinate national Financial Intelligence Units. Key requirements include "
                "enhanced beneficial ownership transparency, virtual asset provider supervision, and "
                "a €10,000 cash payment limit across the EU."
            ),
        ),
        RegulationItem(
            title="FATF — Updated Guidance on Virtual Assets and VASPs",
            url="https://www.fatf-gafi.org/vasp-guidance-update-2025",
            source="FATF",
            category="FATF",
            published_date=datetime(2025, 2, 28),
            body_text=(
                "FATF has released an updated Guidance for a Risk-Based Approach to Virtual Assets and "
                "Virtual Asset Service Providers. The guidance strengthens the travel rule implementation, "
                "introduces DeFi protocol obligations, and provides clarified peer-to-peer transaction "
                "monitoring requirements. Member jurisdictions are expected to implement these standards "
                "within 12 months."
            ),
        ),
        RegulationItem(
            title="FCA — Consumer Duty Implementation Review Findings",
            url="https://www.fca.org.uk/consumer-duty-review-2025",
            source="FCA",
            category="OTHER",
            published_date=datetime(2025, 4, 10),
            body_text=(
                "The FCA has published its first comprehensive review of Consumer Duty implementation. "
                "The review identifies areas where firms need improvement including price and value "
                "assessments, product governance, and customer support standards. Firms failing to "
                "meet expectations face enhanced supervisory action and potential enforcement proceedings."
            ),
        ),
        RegulationItem(
            title="FinCEN — Beneficial Ownership Reporting Rule Updates",
            url="https://www.fincen.gov/boi-reporting-update-2025",
            source="FinCEN",
            category="AML",
            published_date=datetime(2025, 1, 1),
            body_text=(
                "FinCEN has issued updates to the Beneficial Ownership Information (BOI) reporting requirements "
                "under the Corporate Transparency Act. Companies formed before 2024 must file initial reports "
                "by January 1, 2025. The rule requires disclosure of individuals who own or control 25% or more "
                "of a company. Non-compliance carries civil penalties of $500 per day and criminal penalties "
                "up to $10,000 and 2 years imprisonment."
            ),
        ),
        RegulationItem(
            title="ESMA — Guidelines on Crypto-Asset Transfer Monitoring",
            url="https://www.esma.europa.eu/crypto-transfer-monitoring-2025",
            source="ESMA",
            category="MiCA",
            published_date=datetime(2025, 5, 20),
            body_text=(
                "ESMA has published guidelines on monitoring and reporting crypto-asset transfers as part "
                "of the MiCA implementation. CASPs must implement real-time transaction monitoring systems, "
                "maintain records of all transfer data for at least 5 years, and report suspicious transactions "
                "to national competent authorities within 24 hours. Travel rule compliance is mandatory "
                "for all transfers above €1,000."
            ),
        ),
    ]
