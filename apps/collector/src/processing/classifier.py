"""
Regulatory domain + update_type + severity classifier — Bölüm 5.2 taxonomy.
Rule-based keyword matching; can be replaced or augmented with AI later.
"""
import re

# Taxonomy (aligned with packages/shared constants/domains.ts — Bölüm 5.2)
REGULATORY_DOMAIN_KEYS = [
    "AML_KYC",
    "PAYMENTS",
    "OPEN_BANKING",
    "CRYPTO",
    "DORA_ICT",
    "DATA_PRIVACY",
    "CAPITAL_PRUDENTIAL",
    "CONSUMER",
    "SUSTAINABILITY",
    "MESSAGING",
]

UPDATE_TYPE_KEYS = [
    "new_regulation",
    "amendment",
    "rts_its",
    "guideline",
    "consultation",
    "enforcement",
    "opinion_statement",
    "deadline_reminder",
    "mutual_evaluation",
    "market_update",
]

SEVERITY_KEYS = ["critical", "high", "medium", "low", "info"]

# Keyword (lowercase) → domain. Order matters: first match wins per domain.
DOMAIN_KEYWORDS: list[tuple[list[str], str]] = [
    (["aml", "kyc", "sanctions", "beneficial ownership", "transaction monitoring", "fatf", "money laundering", "anti-money"], "AML_KYC"),
    (["payment", "sca", "instant payment", "fraud", "chargeback", "psp", "emi", "payment institution"], "PAYMENTS"),
    (["open banking", "psd2", "psd3", "data sharing", "consent", "aisp", "pisp", "api standard"], "OPEN_BANKING"),
    (["crypto", "mica", "stablecoin", "travel rule", "defi", "casp", "crypto-asset", "virtual asset"], "CRYPTO"),
    (["dora", "ict risk", "operational resilience", "third-party risk", "digital resilience", "ict third party"], "DORA_ICT"),
    (["gdpr", "data protection", "data transfer", "privacy", "cross-border data"], "DATA_PRIVACY"),
    (["capital requirement", "crd", "crr", "liquidity", "stress test", "prudential", "basael"], "CAPITAL_PRUDENTIAL"),
    (["consumer protection", "conduct", "complaint", "financial inclusion"], "CONSUMER"),
    (["esg", "taxonomy", "green finance", "sustainability", "climate"], "SUSTAINABILITY"),
    (["iso 20022", "swift", "messaging standard", "payment messaging"], "MESSAGING"),
]

# Keyword → update_type (consultation before guideline so "consultation on X" prefers consultation)
UPDATE_TYPE_KEYWORDS: list[tuple[list[str], str]] = [
    (["new regulation", "adopted", "entered into force", "law adopted", "regulation adopted"], "new_regulation"),
    (["amendment", "amending", "change to the"], "amendment"),
    (["rts", "its", "technical standard", "delegated regulation", "implementing regulation", "draft rts"], "rts_its"),
    (["consultation", "consult", "call for feedback", "call for comment", "public consultation"], "consultation"),
    (["guideline", "guidance", "recommendations", "eba guideline", "esma guideline"], "guideline"),
    (["enforcement", "penalty", "fine", "sanction", "breach", "supervisory measure"], "enforcement"),
    (["opinion", "statement", "q&a", "faq", "questions and answers"], "opinion_statement"),
    (["deadline", "compliance date", "by december", "by january", "effective from", "application date"], "deadline_reminder"),
    (["mutual evaluation", "fatf plenary", "greylist", "blacklist", "mutual evaluation report"], "mutual_evaluation"),
    (["market update", "statistic", "survey", "report on", "annual report"], "market_update"),
]

# Keyword → severity (high before critical so "30 days" => high, "urgent" => critical)
SEVERITY_KEYWORDS: list[tuple[list[str], str]] = [
    (["30 days", "within 30 days", "significant", "material impact", "high impact"], "high"),
    (["critical", "immediate", "urgent", "licence withdrawn", "withdrawal of authorisation"], "critical"),
    (["90 days", "moderate", "medium term"], "medium"),
    (["low impact", "informational", "minor"], "low"),
]


def _normalize(text: str) -> str:
    """Lowercase and collapse whitespace for matching."""
    if not text:
        return ""
    return re.sub(r"\s+", " ", text.lower().strip())


def classify_domains(text: str) -> list[str]:
    """
    Return domain taxonomy codes (Bölüm 5.2) from text.
    Uses keyword matching; at least one domain (default MESSAGING if no match).
    """
    normalized = _normalize(text)
    if not normalized:
        return ["MESSAGING"]
    found: set[str] = set()
    for keywords, domain in DOMAIN_KEYWORDS:
        for kw in keywords:
            if kw in normalized:
                found.add(domain)
                break
    if not found:
        return ["MESSAGING"]
    return sorted(found)


def classify_update_type(text: str) -> str:
    """Return update_type from taxonomy (Bölüm 5.2). Default: market_update."""
    normalized = _normalize(text)
    if not normalized:
        return "market_update"
    for keywords, update_type in UPDATE_TYPE_KEYWORDS:
        for kw in keywords:
            if kw in normalized:
                return update_type
    return "market_update"


def classify_severity(text: str) -> str:
    """Return severity level (Bölüm 5.2). Default: info."""
    normalized = _normalize(text)
    if not normalized:
        return "info"
    for keywords, severity in SEVERITY_KEYWORDS:
        for kw in keywords:
            if kw in normalized:
                return severity
    return "info"


def classify(text: str) -> dict[str, list[str] | str]:
    """
    One-shot classification: domains (list), update_type (str), severity (str).
    Convenience for pipeline.
    """
    return {
        "domains": classify_domains(text),
        "update_type": classify_update_type(text),
        "severity": classify_severity(text),
    }
