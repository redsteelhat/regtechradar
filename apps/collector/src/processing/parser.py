"""HTML/PDF → clean text extraction (BeautifulSoup4, pdfplumber)."""
from __future__ import annotations

import io
import re

from bs4 import BeautifulSoup

try:
    import pdfplumber
except ImportError:
    pdfplumber = None


def extract_text_from_html(html: str) -> str:
    """
    Extract main text from HTML: strip script/style, prefer main/article/body, normalize whitespace.
    """
    if not (html or "").strip():
        return ""
    soup = BeautifulSoup(html, "lxml")
    for tag in soup.select("script, style, noscript, iframe"):
        tag.decompose()
    main = soup.select_one("main") or soup.select_one("article") or soup.select_one("[role='main']")
    root = main if main else soup.find("body") or soup
    text = root.get_text(separator=" ", strip=True) if root else ""
    return _normalize_whitespace(text)


def extract_text_from_pdf(path: str | None = None, content: bytes | None = None) -> str:
    """
    Extract text from PDF via pdfplumber.
    Provide either path (file path) or content (bytes); path takes precedence.
    """
    if pdfplumber is None:
        return ""
    if not path and not content:
        return ""
    try:
        if path:
            with pdfplumber.open(path) as pdf:
                return _pdf_pages_to_text(pdf)
        with pdfplumber.open(io.BytesIO(content)) as pdf:
            return _pdf_pages_to_text(pdf)
    except Exception:
        return ""


def _pdf_pages_to_text(pdf) -> str:
    """Extract text from all pages of an open pdfplumber PDF."""
    parts = []
    for page in pdf.pages:
        ptext = page.extract_text()
        if ptext:
            parts.append(ptext)
    return _normalize_whitespace("\n\n".join(parts))


def _normalize_whitespace(text: str) -> str:
    """Collapse runs of whitespace and strip."""
    if not text:
        return ""
    text = re.sub(r"\s+", " ", text)
    return text.strip()
