"""Regulations router — list, search, detail with impact scores."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.deps import get_current_user
from app.models import Regulation, ImpactScore, User
from app.schemas import (
    RegulationResponse,
    RegulationDetailResponse,
    RegulationCategoryEnum,
    RegulationSourceEnum,
)

router = APIRouter(prefix="/api/regulations", tags=["regulations"])


@router.get("", response_model=list[RegulationResponse])
async def list_regulations(
    search: str | None = Query(None, description="Search in title"),
    category: RegulationCategoryEnum | None = Query(None),
    source: RegulationSourceEnum | None = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(Regulation).order_by(desc(Regulation.created_at))

    if search:
        stmt = stmt.where(Regulation.title.ilike(f"%{search}%"))
    if category:
        stmt = stmt.where(Regulation.category == category.value)
    if source:
        stmt = stmt.where(Regulation.source == source.value)

    stmt = stmt.offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(stmt)
    return result.scalars().all()


@router.get("/stats")
async def regulation_stats(db: AsyncSession = Depends(get_db)):
    total = await db.scalar(select(func.count(Regulation.id)))

    from datetime import datetime, timedelta, timezone
    week_ago = datetime.now(timezone.utc) - timedelta(days=7)
    new_this_week = await db.scalar(
        select(func.count(Regulation.id)).where(Regulation.created_at >= week_ago)
    )

    sources_result = await db.execute(
        select(Regulation.source, func.count(Regulation.id)).group_by(Regulation.source)
    )
    categories_result = await db.execute(
        select(Regulation.category, func.count(Regulation.id)).group_by(Regulation.category)
    )

    return {
        "total_regulations": total or 0,
        "new_this_week": new_this_week or 0,
        "sources_active": len(sources_result.all()),
        "categories": {row[0]: row[1] for row in categories_result.all()},
    }


@router.get("/{regulation_id}", response_model=RegulationDetailResponse)
async def get_regulation(
    regulation_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(Regulation)
        .options(selectinload(Regulation.impact_scores))
        .where(Regulation.id == regulation_id)
    )
    reg = result.scalar_one_or_none()
    if not reg:
        raise HTTPException(status_code=404, detail="Regulation not found")
    return reg
