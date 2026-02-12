"""Tests for classifier (Bölüm 5.2 taxonomy: domains, update_type, severity)."""
from src.processing.classifier import (
    REGULATORY_DOMAIN_KEYS,
    UPDATE_TYPE_KEYS,
    SEVERITY_KEYS,
    classify_domains,
    classify_update_type,
    classify_severity,
    classify,
)


def test_taxonomy_constants():
    assert "AML_KYC" in REGULATORY_DOMAIN_KEYS
    assert "CRYPTO" in REGULATORY_DOMAIN_KEYS
    assert "DORA_ICT" in REGULATORY_DOMAIN_KEYS
    assert len(REGULATORY_DOMAIN_KEYS) == 10
    assert "new_regulation" in UPDATE_TYPE_KEYS
    assert "consultation" in UPDATE_TYPE_KEYS
    assert "critical" in SEVERITY_KEYS
    assert "info" in SEVERITY_KEYS


def test_classify_domains_empty():
    assert classify_domains("") == ["MESSAGING"]
    assert classify_domains("   ") == ["MESSAGING"]


def test_classify_domains_keywords():
    assert "AML_KYC" in classify_domains("AML and KYC requirements and FATF recommendations")
    assert "CRYPTO" in classify_domains("MiCA regulation on crypto-assets and stablecoins")
    assert "DORA_ICT" in classify_domains("DORA digital operational resilience and ICT risk")
    assert "PAYMENTS" in classify_domains("Payment services and SCA")


def test_classify_domains_multiple():
    text = "EBA guideline on AML and payment institution reporting"
    domains = classify_domains(text)
    assert "AML_KYC" in domains
    assert "PAYMENTS" in domains
    assert all(d in REGULATORY_DOMAIN_KEYS for d in domains)


def test_classify_update_type():
    assert classify_update_type("") == "market_update"
    assert classify_update_type("Call for feedback and public consultation") == "consultation"
    assert classify_update_type("EBA publishes new guideline on fraud") == "guideline"
    assert classify_update_type("Commission adopts implementing regulation") == "rts_its"
    assert classify_update_type("Draft RTS on reporting") == "rts_its"
    assert classify_update_type("Enforcement action and penalty") == "enforcement"
    assert classify_update_type("Market statistics report") == "market_update"


def test_classify_severity():
    assert classify_severity("") == "info"
    assert classify_severity("Compliance within 30 days required") == "high"
    assert classify_severity("Critical deadline and immediate action") == "critical"
    assert classify_severity("Informational update only") == "low"
    assert classify_severity("Random text with no severity hint") == "info"


def test_classify_returns_all_keys():
    result = classify("EBA consultation on AML and DORA ICT risk")
    assert "domains" in result
    assert "update_type" in result
    assert "severity" in result
    assert isinstance(result["domains"], list)
    assert result["update_type"] == "consultation"
    assert "AML_KYC" in result["domains"] or "DORA_ICT" in result["domains"]
