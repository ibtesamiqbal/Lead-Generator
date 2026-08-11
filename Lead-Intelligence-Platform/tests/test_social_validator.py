"""
Unit Tests for SocialProfileValidator.
"""

from src.contact_discovery.social_validator import SocialProfileValidator
from src.enrichment.models import SocialProfiles


def test_social_profile_validator():
    """Verify social profile format validation and redirect parameter detection."""
    socials = SocialProfiles(
        facebook="https://facebook.com/roofingpro?utm_source=header",
        linkedin="https://linkedin.com/company/roofingpro"
    )
    validator = SocialProfileValidator()
    validations = validator.validate_profiles(socials)

    assert len(validations) == 2
    fb_val = next(v for v in validations if v.platform == "Facebook")
    assert fb_val.has_redirect_parameters is True
    assert fb_val.is_valid_format is True
