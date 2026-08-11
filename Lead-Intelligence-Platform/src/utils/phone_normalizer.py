"""
Shared Phone Normalizer & Validation Utility.
Provides uniform regex matching, validation, and E.164 normalization across all platform modules.
"""

import re
from enum import Enum


class SharedPhoneCategory(str, Enum):
    """Phone number categories."""
    LANDLINE = "Landline"
    MOBILE = "Mobile"
    TOLL_FREE = "TollFree"
    INTERNATIONAL = "International"
    UNKNOWN = "Unknown"


# Strict Australian phone matching regex
AU_STRICT_PHONE_REGEX = re.compile(
    r'(?:\+?61\s*\(?0?\)?|\(?0[2378]\)?|\(?04\d{2}\)?)\s*\d{3,4}\s*\d{3,4}|1[38]00\s*\d{3}\s*\d{3}|13\s*\d{2}\s*\d{2}'
)

# Standard international E.164 format regex (e.g. +14155552671, +442079460958)
INTL_E164_REGEX = re.compile(
    r'\+(?:1|44|64|65|86|49|33|81|91|34|39|55|27|31|41|46|47)\d{7,12}'
)

# Valid country calling codes set
VALID_COUNTRY_CODES = {
    "1", "44", "61", "64", "65", "86", "49", "33", "81", "91", "34", "39", "55", "27", "31", "41", "46", "47"
}


class PhoneNormalizer:
    """Shared phone validation and E.164 normalization engine."""

    @classmethod
    def normalize(cls, raw_phone: str) -> tuple[str | None, str | None, SharedPhoneCategory]:
        """
        Normalizes raw phone string.
        
        Returns:
            tuple of (e164_number, formatted_number, category) or (None, None, UNKNOWN) if invalid.
        """
        if not raw_phone:
            return None, None, SharedPhoneCategory.UNKNOWN

        clean_digits = re.sub(r'[^\d+]', '', raw_phone.strip())
        digits_only = re.sub(r'\D', '', clean_digits)

        if len(digits_only) < 8 or len(digits_only) > 15:
            return None, None, SharedPhoneCategory.UNKNOWN

        # 1. Australian Number Processing
        if digits_only.startswith("0") and len(digits_only) == 10:
            digits_only = "61" + digits_only[1:]

        if digits_only.startswith("61") and len(digits_only) in (9, 10, 11):
            e164 = f"+{digits_only}"
            local_prefix = digits_only[2:4]
            category = SharedPhoneCategory.UNKNOWN

            if digits_only.startswith("614"):
                category = SharedPhoneCategory.MOBILE
                formatted = f"+61 {digits_only[2:5]} {digits_only[5:8]} {digits_only[8:]}"
            elif digits_only.startswith(("612", "613", "617", "618")):
                category = SharedPhoneCategory.LANDLINE
                formatted = f"+61 {digits_only[2]} {digits_only[3:7]} {digits_only[7:]}"
            elif digits_only.startswith(("611300", "611800")):
                category = SharedPhoneCategory.TOLL_FREE
                formatted = f"+61 {digits_only[2:6]} {digits_only[6:9]} {digits_only[9:]}"
            else:
                formatted = e164

            return e164, formatted, category

        # Local 1300 / 1800 Toll Free
        if digits_only.startswith(("1300", "1800")) and len(digits_only) == 10:
            formatted = f"{digits_only[:4]} {digits_only[4:7]} {digits_only[7:]}"
            return None, formatted, SharedPhoneCategory.TOLL_FREE

        if digits_only.startswith("13") and len(digits_only) == 6:
            formatted = f"{digits_only[:2]} {digits_only[2:4]} {digits_only[4:]}"
            return None, formatted, SharedPhoneCategory.TOLL_FREE

        # 2. International Number Processing with Country Code Check
        if clean_digits.startswith("+"):
            for cc in VALID_COUNTRY_CODES:
                if digits_only.startswith(cc) and (8 <= len(digits_only) <= 15):
                    e164 = f"+{digits_only}"
                    return e164, e164, SharedPhoneCategory.INTERNATIONAL

        return None, None, SharedPhoneCategory.UNKNOWN
