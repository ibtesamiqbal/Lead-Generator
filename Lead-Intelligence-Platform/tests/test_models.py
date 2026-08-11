"""
Unit Tests for Discovery Data Schemas and MetadataField.
"""

from src.discovery.models import Company, MetadataField, TargetStatus


def test_metadata_field_confidence_bounds():
    """Verify MetadataField clamps confidence strictly to [0.0, 1.0]."""
    f1 = MetadataField[str](value="Test Business", confidence=1.5)
    assert f1.confidence == 1.0

    f2 = MetadataField[str](value="Low Confidence", confidence=-0.5)
    assert f2.confidence == 0.0

    f3 = MetadataField[str](value="Exact Match", confidence=0.85)
    assert f3.confidence == 0.85


def test_company_domain_auto_normalization():
    """Verify Company entity automatically normalizes raw domain inputs."""
    c = Company(domain="HTTPS://WWW.SydneyRoofers.com.au/about")
    assert c.domain == "sydneyroofers.com.au"
    assert c.status == TargetStatus.PENDING
    assert c.country.value == "Australia"
    assert c.industry.value == "Roofing"


def test_company_json_roundtrip():
    """Verify Company model serializes to and from JSON cleanly."""
    c1 = Company(
        domain="melbourneremovals.com.au",
        name=MetadataField[str](value="Melbourne Removals", confidence=0.9, source="https://melbourneremovals.com.au"),
        industry=MetadataField[str](value="Removal Companies", confidence=1.0)
    )

    json_str = c1.model_dump_json()
    assert "melbourneremovals.com.au" in json_str

    c2 = Company.model_validate_json(json_str)
    assert c2.domain == "melbourneremovals.com.au"
    assert c2.name.value == "Melbourne Removals"
    assert c2.name.confidence == 0.9
    assert c2.industry.value == "Removal Companies"
