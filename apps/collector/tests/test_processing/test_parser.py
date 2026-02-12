"""Tests for HTML/PDF parser (extract_text_from_html, extract_text_from_pdf)."""
from src.processing.parser import extract_text_from_html, extract_text_from_pdf, _normalize_whitespace


def test_extract_text_from_html_empty():
    assert extract_text_from_html("") == ""
    assert extract_text_from_html("   ") == ""


def test_extract_text_from_html_strips_script_style():
    html = """
    <html><head><script>alert(1);</script><style>.x{}</style></head>
    <body><p>Hello world.</p></body></html>
    """
    out = extract_text_from_html(html)
    assert "Hello world" in out
    assert "alert" not in out
    assert ".x" not in out


def test_extract_text_from_html_prefers_main_article():
    html = """
    <html><body>
    <nav>Nav here</nav>
    <main><article><p>Main content here.</p></article></main>
    </body></html>
    """
    out = extract_text_from_html(html)
    assert "Main content" in out


def test_extract_text_from_html_normalizes_whitespace():
    html = "<html><body><p>  One   two\n\nthree  </p></body></html>"
    out = extract_text_from_html(html)
    assert "One two three" in out


def test_normalize_whitespace():
    assert _normalize_whitespace("  a  b  c  ") == "a b c"
    assert _normalize_whitespace("") == ""


def test_extract_text_from_pdf_no_input():
    assert extract_text_from_pdf() == ""
    assert extract_text_from_pdf(path="", content=None) == ""


def test_extract_text_from_pdf_invalid_path_returns_empty():
    out = extract_text_from_pdf(path="/nonexistent/file.pdf")
    assert out == ""
