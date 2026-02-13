"""APScheduler-based task scheduler for scraping and digest delivery."""

from __future__ import annotations

import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler

logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler()


async def scrape_all_job():
    """Scheduled job: scrape all regulator sites."""
    from app.database import async_session
    from app.routers.admin import SCRAPERS, _store_regulation

    logger.info("Scheduled scrape starting...")
    async with async_session() as db:
        total = 0
        for ScraperClass in SCRAPERS:
            scraper = ScraperClass()
            try:
                items = await scraper.scrape()
                for item in items:
                    total += await _store_regulation(db, item)
            except Exception as exc:
                logger.error("Scheduled scraper %s failed: %s", ScraperClass.source_name, exc)
            finally:
                await scraper.close()
        await db.commit()
    logger.info("Scheduled scrape complete. %d new regulations.", total)


async def send_weekly_digest_job():
    """Scheduled job: send weekly digest emails to all active users."""
    from datetime import datetime, timedelta, timezone
    from sqlalchemy import select
    from app.database import async_session
    from app.models import Regulation, User
    from app.services import ai_service, email_service

    logger.info("Weekly digest job starting...")
    async with async_session() as db:
        week_ago = datetime.now(timezone.utc) - timedelta(days=7)
        result = await db.execute(
            select(Regulation).where(Regulation.created_at >= week_ago)
        )
        regulations = result.scalars().all()
        if not regulations:
            logger.info("No new regulations this week — skipping digest.")
            return

        reg_dicts = [
            {"title": r.title, "category": r.category.value if r.category else "OTHER",
             "ai_summary": r.ai_summary or "", "raw_content": r.raw_content}
            for r in regulations
        ]
        digest_body = await ai_service.generate_digest(reg_dicts)

        users_result = await db.execute(select(User).where(User.is_active == True))
        users = users_result.scalars().all()

        sent = 0
        for user in users:
            success = await email_service.send_weekly_digest(
                to_email=user.email,
                subject="📋 RegTech Radar — Weekly Regulatory Digest",
                html_body=f"<div style='font-family:Inter,sans-serif;max-width:600px;margin:0 auto;'>"
                          f"<h1 style='color:#06b6d4;'>RegTech Radar</h1>"
                          f"<div style='white-space:pre-wrap;'>{digest_body}</div>"
                          f"<hr><p style='color:#888;font-size:12px;'>You're receiving this because you subscribed to RegTech Radar.</p>"
                          f"</div>",
            )
            if success:
                sent += 1

    logger.info("Weekly digest sent to %d users.", sent)


def start_scheduler():
    """Register jobs and start the scheduler."""
    scheduler.add_job(scrape_all_job, "cron", hour=6, minute=0, id="daily_scrape", replace_existing=True)
    scheduler.add_job(send_weekly_digest_job, "cron", day_of_week="mon", hour=8, minute=0, id="weekly_digest", replace_existing=True)
    scheduler.start()
    logger.info("Scheduler started — daily scrape at 06:00 UTC, weekly digest Mondays 08:00 UTC.")


def stop_scheduler():
    if scheduler.running:
        scheduler.shutdown(wait=False)
        logger.info("Scheduler stopped.")
