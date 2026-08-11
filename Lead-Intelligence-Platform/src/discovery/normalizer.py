"""
Domain Normalization and Validation Module.
Ensures domain strings are clean, lowercase, and strictly formatted.
"""

import re
from urllib.parse import urlparse
from src.utils.exceptions import InvalidDomainError

# Standard domain regex matching hostnames and TLDs (e.g. example.com, roofing.com.au)
DOMAIN_REGEX = re.compile(
    r"^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$"
)


def normalize_domain(raw_input: str) -> str:
    """
    Cleans and normalizes a raw domain or URL string.
    
    Args:
        raw_input: Raw URL or domain string (e.g., 'https://WWW.RoofingPro.COM.AU/contact?id=1')
        
    Returns:
        Clean normalized domain string (e.g., 'roofingpro.com.au')
        
    Raises:
        InvalidDomainError: If domain is empty or malformed.
    """
    if not raw_input or not isinstance(raw_input, str):
        raise InvalidDomainError("Domain input must be a non-empty string.")

    cleaned = raw_input.strip().lower()

    # Prepend schema if missing to leverage urlparse
    if not cleaned.startswith(("http://", "https://")):
        cleaned = "https://" + cleaned

    try:
        parsed = urlparse(cleaned)
        netloc = parsed.netloc or parsed.path.split("/")[0]
        
        # Remove port numbers if present (e.g., domain.com:8080)
        domain = netloc.split(":")[0]
        
        # Strip leading www.
        if domain.startswith("www."):
            domain = domain[4:]

        domain = domain.strip()

        if not domain or not validate_domain(domain):
            raise InvalidDomainError(f"Invalid domain format: '{raw_input}'")

        return domain

    except Exception as err:
        if isinstance(err, InvalidDomainError):
            raise
        raise InvalidDomainError(f"Failed to parse domain '{raw_input}': {err}") from err


def validate_domain(domain: str) -> bool:
    """
    Validates syntax of a normalized domain string.
    
    Args:
        domain: Domain string to validate
        
    Returns:
        True if valid syntax, False otherwise.
    """
    if not domain or len(domain) > 253:
        return False
    return bool(DOMAIN_REGEX.match(domain))
