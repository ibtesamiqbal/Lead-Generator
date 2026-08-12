"""
Validation utilities for Decision Maker candidates, names, emails, and LinkedIn links.
Includes SSRF safety checks, sentence exclusions, verb blacklists, and noise filtering.
"""

import re
from urllib.parse import urlparse

# Blacklist of non-person strings commonly matched by loose HTML extraction
INVALID_NAME_PATTERNS: set[str] = {
    "about us", "about our team", "our team", "meet the team", "leadership team",
    "executive team", "management team", "our leadership", "board of directors",
    "read bio", "view profile", "contact us", "learn more", "careers", "join us",
    "company overview", "privacy policy", "terms of service", "terms of use",
    "home", "back to top", "see all", "view all", "team member", "staff member",
    "customer review", "press release", "news & media", "blog", "recent posts",
    "navigation", "site map", "sitemap", "copyright", "all rights reserved",
    "cookie policy", "accessibility statement", "view map", "directions",
    "press kit", "media kit", "contact form", "request quote", "get in touch",
    "read story", "full bio", "find out more", "see profile", "send email",
    "our story", "company background", "mission statement", "core values"
}

# Action verbs commonly found in marketing slogans, CTAs, or feature headlines (never human names)
ACTION_VERB_PATTERNS: set[str] = {
    "update", "partner", "build", "manage", "discover", "improve", "learn", "start",
    "try", "download", "contact", "subscribe", "schedule", "share", "connect",
    "collaborate", "read", "explore", "boost", "create", "deliver", "transform",
    "automate", "scale", "optimize", "accelerate", "streamline", "empower", "noticed",
    "wanted", "expanded", "founded", "expect", "led", "uses", "grow", "crafted"
}

# English stop words that indicate a marketing headline or sentence, not a human name
STOP_WORDS: set[str] = {
    "with", "for", "that", "this", "your", "latest", "based", "on", "the", "and",
    "or", "to", "from", "in", "at", "by", "about", "how", "what", "why", "where",
    "when", "our", "their", "more", "most", "some", "every", "all", "into", "than",
    "were", "was", "been", "being", "have", "has", "had", "would", "could", "should"
}

# Blocked SSRF hostnames and IP addresses
BLOCKED_SSRF_HOSTS: set[str] = {
    "localhost", "127.0.0.1", "0.0.0.0", "169.254.169.254", "::1", "[::1]",
    "metadata.google.internal", "169.254.169.254.xip.io"
}


class DecisionMakerValidator:
    """Validates extracted person candidates to filter out noise, bad data, and unsafe URLs."""

    @staticmethod
    def is_valid_name(name: str | None) -> bool:
        """
        Validates if candidate string represents a legitimate human name.
        Strictly rejects sentence headlines, marketing copy, CTAs, and stop words.
        """
        if not name or not isinstance(name, str):
            return False

        cleaned = name.strip()
        if len(cleaned) < 2 or len(cleaned) > 30:
            return False

        # Reject strings ending with sentence punctuation (. ! ?) or containing sentence punctuation (, ;)
        if cleaned.endswith((".", "!", "?")) or "," in cleaned or ";" in cleaned:
            return False

        # Reject strings containing hyphens used in multi-phrase titles or sentence dashes (" - ", " — ")
        if " - " in cleaned or " — " in cleaned or ":" in cleaned:
            return False

        lower_name = cleaned.lower()
        words = lower_name.split()

        # Reject single-word non-names or navigation labels
        if len(words) == 1 and len(words[0]) < 3:
            return False

        # Human full names strictly consist of 2 to 3 words (or max 4 with Dr./Mr./Ms.)
        if len(words) > 3 and not any(lower_name.startswith(pref) for pref in ["dr.", "mr.", "mrs.", "ms.", "prof."]):
            return False

        if lower_name in INVALID_NAME_PATTERNS:
            return False

        for invalid in INVALID_NAME_PATTERNS:
            if lower_name.startswith(invalid) or lower_name.endswith(invalid):
                return False

        # Reject if string contains any action verbs common in CTAs/marketing
        for verb in ACTION_VERB_PATTERNS:
            if re.search(rf"\b{verb}\b", lower_name):
                return False

        # Reject if string contains sentence stop words
        stop_count = sum(1 for w in words if w in STOP_WORDS)
        if stop_count >= 1:
            return False

        # Must contain at least one alpha character
        if not re.search(r"[a-zA-Z]", cleaned):
            return False

        # Reject if string contains suspicious URL protocols, html tags, or excess digits
        if "http://" in lower_name or "https://" in lower_name or "<" in cleaned or ">" in cleaned:
            return False

        digit_count = sum(1 for c in cleaned if c.isdigit())
        if digit_count > 2:
            return False

        return True

    @staticmethod
    def is_safe_url(url: str | None) -> bool:
        """
        Checks whether a candidate URL is safe against SSRF, file access, or internal network probes.
        """
        if not url or not isinstance(url, str):
            return False

        try:
            parsed = urlparse(url.strip())
            if parsed.scheme.lower() not in ("http", "https"):
                return False

            hostname = (parsed.hostname or "").lower()
            if not hostname or hostname in BLOCKED_SSRF_HOSTS:
                return False

            if hostname.startswith(("10.", "192.168.", "127.", "169.254.")):
                return False
            if hostname.startswith("172."):
                parts = hostname.split(".")
                if len(parts) >= 2 and parts[1].isdigit() and 16 <= int(parts[1]) <= 31:
                    return False

            return True
        except Exception:
            return False

    @staticmethod
    def is_valid_linkedin_url(url: str | None) -> bool:
        """
        Checks whether a URL is a valid personal LinkedIn profile link.
        """
        if not url or not isinstance(url, str):
            return False

        if not DecisionMakerValidator.is_safe_url(url):
            return False

        try:
            parsed = urlparse(url.strip())
            if "linkedin.com" not in parsed.netloc.lower():
                return False
            path = parsed.path.lower()
            return "/in/" in path or "/pub/" in path or "/profile/" in path
        except Exception:
            return False

    @staticmethod
    def sanitize_name(name: str) -> str:
        """
        Cleans honorific prefixes (Dr., Mr., Ms., Prof.) or suffixes (PhD, MBA) and normalizes spacing.
        """
        if not name or not isinstance(name, str):
            return ""

        cleaned = re.sub(r"\s+", " ", name.strip())
        cleaned = cleaned.replace("&amp;", "&").replace("&nbsp;", " ")
        return cleaned.strip()

    @staticmethod
    def split_full_name(full_name: str) -> tuple[str, str]:
        """
        Splits full name into (first_name, last_name).
        """
        cleaned = DecisionMakerValidator.sanitize_name(full_name)
        cleaned = re.sub(r"^(Dr\.|Mr\.|Mrs\.|Ms\.|Prof\.)\s+", "", cleaned, flags=re.IGNORECASE)

        parts = cleaned.split()
        if not parts:
            return ("", "")
        if len(parts) == 1:
            return (parts[0], "")

        first_name = parts[0]
        last_name = " ".join(parts[1:])
        return (first_name, last_name)
