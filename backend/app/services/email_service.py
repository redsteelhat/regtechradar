"""Email service using Resend for weekly digests and alerts."""

from __future__ import annotations

import logging

from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

_resend = None


def _get_resend():
    global _resend
    if _resend is None:
        try:
            import resend as _resend_mod
            _resend_mod.api_key = settings.RESEND_API_KEY
            _resend = _resend_mod
        except Exception as exc:
            logger.warning("Resend init failed: %s", exc)
    return _resend


async def send_weekly_digest(to_email: str, subject: str, html_body: str) -> bool:
    """Send a weekly digest email. Returns True on success."""
    resend = _get_resend()
    if not resend or not settings.RESEND_API_KEY:
        logger.info("Email skipped (no API key): %s → %s", subject, to_email)
        return False
    try:
        resend.Emails.send({
            "from": settings.EMAIL_FROM,
            "to": [to_email],
            "subject": subject,
            "html": html_body,
        })
        logger.info("Digest sent to %s", to_email)
        return True
    except Exception as exc:
        logger.error("Failed to send digest to %s: %s", to_email, exc)
        return False


async def send_alert(to_email: str, regulation_title: str, regulation_url: str) -> bool:
    """Send a single-regulation alert email."""
    resend = _get_resend()
    if not resend or not settings.RESEND_API_KEY:
        logger.info("Alert email skipped (no API key): %s", to_email)
        return False
    try:
        resend.Emails.send({
            "from": settings.EMAIL_FROM,
            "to": [to_email],
            "subject": f"🔔 RegTech Alert: {regulation_title}",
            "html": (
                f"<h2>New Regulatory Update</h2>"
                f"<p><strong>{regulation_title}</strong></p>"
                f'<p><a href="{regulation_url}">Read full regulation →</a></p>'
                f"<hr><p style='color:#888;font-size:12px;'>RegTech Radar — regulatory intelligence for FinTech</p>"
            ),
        })
        logger.info("Alert sent to %s for %s", to_email, regulation_title)
        return True
    except Exception as exc:
        logger.error("Failed to send alert to %s: %s", to_email, exc)
        return False
