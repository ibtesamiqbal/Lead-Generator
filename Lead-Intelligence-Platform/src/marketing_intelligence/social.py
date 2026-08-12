"""
Social Presence Analyzer (Phase 06).
Analyzes social media footprint reusing Phase 02/03 SocialProfiles.
"""

from src.enrichment.models import SocialProfiles
from src.marketing_intelligence.models import SocialPresence


class SocialPresenceAnalyzer:
    """Evaluates social media channel presence and calculates social completeness score."""

    def analyze_social(self, socials: SocialProfiles | None = None) -> SocialPresence:
        """
        Returns populated SocialPresence model.
        """
        presence = SocialPresence()
        if not socials:
            return presence

        active_channels = 0

        if socials.facebook:
            presence.has_facebook = True
            presence.facebook_url = socials.facebook
            active_channels += 1

        if socials.linkedin:
            presence.has_linkedin = True
            presence.linkedin_url = socials.linkedin
            active_channels += 1

        if socials.instagram:
            presence.has_instagram = True
            presence.instagram_url = socials.instagram
            active_channels += 1

        tw_link = getattr(socials, "twitter_x", None) or getattr(socials, "twitter", None)
        if tw_link:
            presence.has_twitter = True
            presence.twitter_url = tw_link
            active_channels += 1

        if socials.youtube:
            presence.has_youtube = True
            presence.youtube_url = socials.youtube
            active_channels += 1

        if getattr(socials, "tiktok", None):
            presence.has_tiktok = True
            active_channels += 1

        presence.social_completeness_score = round(min(100.0, (active_channels / 4.0) * 100.0), 1)
        return presence
