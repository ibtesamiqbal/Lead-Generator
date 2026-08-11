"""
Unit Tests for Domain Normalizer and Validator.
"""

import pytest
from src.discovery.normalizer import normalize_domain, validate_domain
from src.utils.exceptions import InvalidDomainError


def test_normalize_domain_valid_urls():
    """Test normalization of various valid URL and domain formats."""
    assert normalize_domain("https://www.RoofingPro.com.au/contact?id=12") == "roofingpro.com.au"
    assert normalize_domain("http://subdomain.example.org/") == "subdomain.example.org"
    assert normalize_domain("  WWW.ACME.COM  ") == "acme.com"
    assert normalize_domain("removalists-sydney.com.au") == "removalists-sydney.com.au"


def test_normalize_domain_invalid_inputs():
    """Test that invalid domains raise InvalidDomainError."""
    with pytest.raises(InvalidDomainError):
        normalize_domain("")

    with pytest.raises(InvalidDomainError):
        normalize_domain("   ")

    with pytest.raises(InvalidDomainError):
        normalize_domain("invalid_domain_without_tld")

    with pytest.raises(InvalidDomainError):
        normalize_domain("http://.com")


def test_validate_domain_syntax():
    """Test syntax regex validator."""
    assert validate_domain("roofing.com.au") is True
    assert validate_domain("acme.org") is True
    assert validate_domain("not a domain") is False
    assert validate_domain("-invalid.com") is False
