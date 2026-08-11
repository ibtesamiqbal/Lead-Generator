"""
Social Media Profile Extractor Module.
Detects and normalizes social profile links (Facebook, Instagram, LinkedIn, X, YouTube, TikTok, Pinterest).
"""

from urllib.parse import urlparse, urlunparse
from src.enrichment.models import SocialProfiles
from src.enrichment.parser import HTMLParserDocument

# Domain signature mapping for targeted social networks
SOCIAL_DOMAINS = {
    "facebook": ["facebook.com", "fb.com", "fb.me"],
    "instagram": ["instagram.com", "instagr.am"],
    "linkedin": ["linkedin.com"],
    "twitter_x": ["twitter.com", "x.com"],
    "youtube": ["youtube.com", "youtu.be"],
    "tiktok": ["tiktok.com"],
    "pinterest": ["pinterest.com", "pin.it"],
}


class SocialExtractor:
    """Extracts and normalizes public social media profile URLs from HTML DOM."""

    def extract(self, doc: HTMLParserDocument) -> SocialProfiles:
        """
        Extracts social profile links found in document href attributes.
        """
        detected: dict[str, str] = {}

        for link in doc.get_all_links():
            href = link["href"].strip()
            if not href.startswith(("http://", "https://", "//")):
                continue

            network, normalized = self._identify_social_network(href)
            if network and network not in detected:
                detected[network] = normalized

        return SocialProfiles(
            facebook=detected.get("facebook"),
            instagram=detected.get("instagram"),
            linkedin=detected.get("linkedin"),
            twitter_x=detected.get("twitter_x"),
            youtube=detected.get("youtube"),
            tiktok=detected.get("tiktok"),
            pinterest=detected.get("pinterest"),
        )

    def _identify_social_network(self, raw_url: str) -> tuple[str | None, str | None]:
        if raw_url.startswith("//"):
            url = "https:" + raw_url
        else:
            url = raw_url

        try:
            parsed = urlparse(url)
            netloc = parsed.netloc.lower().split(":")[0]
            if netloc.startswith("www."):
                netloc = netloc[4:]

            for network, domains in SOCIAL_DOMAINS.items():
                if any(netloc == d or netloc.endswith("." + d) for d in domains):
                    # Filter out share intents or non-profile links
                    path = parsed.path.lower()
                    if any(p in path for p in ["/sharer", "/share", "/intent", "/embed", "/dialog"]):
                        continue

                    # Clean query strings and trailing slashes
                    clean_path = parsed.path.rstrip("/")
                    clean_url = urlunparse((parsed.scheme or "https", netloc, clean_path, "", "", "")).lower()
                    return network, clean_url

        except Exception:
            pass

        return None, None
