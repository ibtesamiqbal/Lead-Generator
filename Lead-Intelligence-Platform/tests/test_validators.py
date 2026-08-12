"""
Unit tests for Decision Maker Candidate Validators.
"""

from src.decision_maker.validators import DecisionMakerValidator


def test_name_validation():
    assert DecisionMakerValidator.is_valid_name("John Smith") is True
    assert DecisionMakerValidator.is_valid_name("Dr. Sarah Connor") is True

    # Invalid names
    assert DecisionMakerValidator.is_valid_name("About Us") is False
    assert DecisionMakerValidator.is_valid_name("Our Leadership Team") is False
    assert DecisionMakerValidator.is_valid_name("Read Bio") is False
    assert DecisionMakerValidator.is_valid_name("Contact Us") is False
    assert DecisionMakerValidator.is_valid_name("http://example.com") is False
    assert DecisionMakerValidator.is_valid_name("12345") is False


def test_linkedin_url_validation():
    assert DecisionMakerValidator.is_valid_linkedin_url("https://www.linkedin.com/in/john-doe-1234") is True
    assert DecisionMakerValidator.is_valid_linkedin_url("https://linkedin.com/pub/sarah-smith/5/6/7") is True

    assert DecisionMakerValidator.is_valid_linkedin_url("https://facebook.com/johndoe") is False
    assert DecisionMakerValidator.is_valid_linkedin_url("https://linkedin.com/company/acme-corp") is False


def test_split_full_name():
    first, last = DecisionMakerValidator.split_full_name("John Smith")
    assert first == "John"
    assert last == "Smith"

    first_dr, last_dr = DecisionMakerValidator.split_full_name("Dr. Sarah Connor")
    assert first_dr == "Sarah"
    assert last_dr == "Connor"
