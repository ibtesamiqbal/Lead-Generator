"""
Social Profile Validator Module.
Validates syntax, query string redirects, and duplicate profile handles across social networks.
"""

from urllib.parse import urlparse
from src.contact_discovery.models import SocialProfileValidation
from src.enrichment.models import SocialProfiles
from src.logging.logger import logger


class SocialProfileValidator:
    """Validates previously discovered social media profiles."""

    def validate_profiles(self, socials: SocialProfiles) -> list[SocialProfileValidation]:
        """
        Runs validation rules against extracted social profile links.
        """
        validations = []
        seen_paths = set()

        profiles_dict = {
            "Facebook": socials.facebook,
            "Instagram": socials.instagram,
            "LinkedIn": socials.linkedin,
            "Twitter_X": socials.twitter_x,
            "YouTube": socials.youtube,
            "TikTok": socials.tiktok,
            "Pinterest": socials.pinterest
        }

        for platform, url in profiles_dict.items():
            if not url:
                continue

            parsed = urlparse(url)
            has_params = bool(parsed.query)
            clean_path = parsed.path.rstrip("/").lower()

            is_duplicate = clean_path in seen_paths and len(clean_path) > 1
            if clean_path and clean_path != "/":
                seen_paths.add(clean_path)

            is_valid_format = bool(parsed.scheme in ("http", "https") and parsed.netloc and clean_path)

            validations.append(
                SocialProfileValidation(
                    platform=platform,
                    url=url,
                    is_valid_format=is_valid_format,
                    is_duplicate=is_duplicate,
                    has_redirect_parameters=has_params
                )
            )

        return validations
