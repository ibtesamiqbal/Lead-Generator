"""
Unit Tests for Shared Phone Normalizer Utility.
"""

from src.utils.phone_normalizer import PhoneNormalizer, SharedPhoneCategory


def test_phone_normalizer_australian_numbers():
    """Verify Australian landline, mobile, and toll free phone normalization."""
    # Landline
    e164, formatted, cat = PhoneNormalizer.normalize("(02) 9876 5432")
    assert e164 == "+61298765432"
    assert cat == SharedPhoneCategory.LANDLINE

    # Mobile
    e164, formatted, cat = PhoneNormalizer.normalize("0412 345 678")
    assert e164 == "+61412345678"
    assert cat == SharedPhoneCategory.MOBILE

    # Toll Free
    e164, formatted, cat = PhoneNormalizer.normalize("1300 123 456")
    assert formatted == "1300 123 456"
    assert cat == SharedPhoneCategory.TOLL_FREE


def test_phone_normalizer_rejects_malformed():
    """Verify random numeric strings or invalid country codes are rejected."""
    e164, formatted, cat = PhoneNormalizer.normalize("46550741244379")
    assert e164 is None
    assert cat == SharedPhoneCategory.UNKNOWN
