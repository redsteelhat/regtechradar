"""AI summarization and impact analysis using OpenAI."""

from __future__ import annotations

import json
import logging

from openai import AsyncOpenAI

from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY) if settings.OPENAI_API_KEY else None


# ── Prompts ─────────────────────────────────────────────────────────────────

SUMMARY_SYSTEM = (
    "You are a regulatory analyst specializing in financial services regulation. "
    "Summarize the following regulatory text in 3-5 concise bullet points. "
    "Focus on: what changed, who is affected, key deadlines, and required actions. "
    "Write in clear, professional English."
)

IMPACT_SYSTEM = (
    "You are a compliance advisor. Given a regulatory text and a financial license type, "
    "evaluate how this regulation impacts the holder of that specific license. "
    "Return valid JSON with exactly two keys:\n"
    '  "score": a number from 1 (minimal impact) to 10 (critical, immediate action needed),\n'
    '  "explanation": a 2-3 sentence explanation of why this score was assigned.\n'
    "Be precise and actionable."
)

DIGEST_SYSTEM = (
    "You are the editor of a weekly regulatory bulletin for FinTech compliance teams. "
    "Given a list of regulatory updates, produce a concise newsletter-style summary. "
    "Group by category (DORA, MiCA, PSD3, AMLA, FATF, Other). "
    "For each item include the title, a one-line summary, and an impact indicator (🔴 High / 🟡 Medium / 🟢 Low). "
    "End with a 'Key Dates' section listing upcoming deadlines."
)


# ── Public API ──────────────────────────────────────────────────────────────

async def summarize(text: str) -> str:
    """Return an AI-generated summary of regulatory text."""
    if not client:
        return _fallback_summary(text)
    try:
        resp = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SUMMARY_SYSTEM},
                {"role": "user", "content": text[:12_000]},
            ],
            temperature=0.3,
            max_tokens=600,
        )
        return resp.choices[0].message.content.strip()
    except Exception as exc:
        logger.warning("AI summarization failed: %s", exc)
        return _fallback_summary(text)


async def analyze_impact(text: str, license_type: str) -> dict:
    """Return {"score": float, "explanation": str} for a given license type."""
    if not client:
        return {"score": 5.0, "explanation": "AI service not configured — default medium impact."}
    try:
        resp = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": IMPACT_SYSTEM},
                {"role": "user", "content": f"License type: {license_type}\n\nRegulatory text:\n{text[:12_000]}"},
            ],
            temperature=0.2,
            max_tokens=300,
            response_format={"type": "json_object"},
        )
        data = json.loads(resp.choices[0].message.content)
        return {
            "score": float(data.get("score", 5)),
            "explanation": data.get("explanation", ""),
        }
    except Exception as exc:
        logger.warning("AI impact analysis failed: %s", exc)
        return {"score": 5.0, "explanation": f"Analysis unavailable: {exc}"}


async def generate_digest(regulations: list[dict]) -> str:
    """Generate a weekly digest newsletter body from a list of regulation dicts."""
    if not client:
        return _fallback_digest(regulations)
    items_text = "\n\n".join(
        f"[{r.get('category', 'OTHER')}] {r.get('title', 'Untitled')}\n{r.get('ai_summary', r.get('raw_content', '')[:500])}"
        for r in regulations
    )
    try:
        resp = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": DIGEST_SYSTEM},
                {"role": "user", "content": items_text[:15_000]},
            ],
            temperature=0.4,
            max_tokens=1500,
        )
        return resp.choices[0].message.content.strip()
    except Exception as exc:
        logger.warning("AI digest generation failed: %s", exc)
        return _fallback_digest(regulations)


# ── Fallbacks (when no API key) ─────────────────────────────────────────────

def _fallback_summary(text: str) -> str:
    sentences = text.replace("\n", " ").split(". ")
    return ". ".join(sentences[:3]) + ("." if sentences else "")


def _fallback_digest(regulations: list[dict]) -> str:
    lines = [f"• {r.get('title', 'Untitled')} ({r.get('category', 'OTHER')})" for r in regulations]
    return "This week's regulatory updates:\n\n" + "\n".join(lines)
