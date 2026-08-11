"""
Email Intelligence Finder Module.
Extracts public business emails, classifies email purpose, validates syntax, filters spam traps, and rates confidence.
"""

import re
from urllib.parse import urlparse
from src.contact_discovery.models import ConfidenceLevel, ContactEmail, EmailCategory
from src.enrichment.parser import HTMLParserDocument
from src.logging.logger import logger


class EmailFinder:
    """Discovers, validates syntax, classifies, and filters public email addresses."""

    EMAIL_REGEX = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')

    SPAM_TRAP_DOMAINS = {
        "example.com", "domain.com", "email.com", "sentry.io",
        "schema.org", "wixpress.com", "wordpress.org", "gravatar.com",
        "format.com", "elementor.com", "bootstrap.com"
    }

    SPAM_TRAP_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"}

    CLASSIFICATION_MAP = {
        "info": EmailCategory.GENERAL,
        "contact": EmailCategory.GENERAL,
        "hello": EmailCategory.GENERAL,
        "enquiries": EmailCategory.GENERAL,
        "enquiry": EmailCategory.GENERAL,
        "admin": EmailCategory.GENERAL,
        "sales": EmailCategory.SALES,
        "quotes": EmailCategory.SALES,
        "quote": EmailCategory.SALES,
        "support": EmailCategory.SUPPORT,
        "help": EmailCategory.SUPPORT,
        "service": EmailCategory.SUPPORT,
        "careers": EmailCategory.CAREERS,
        "jobs": EmailCategory.CAREERS,
        "hr": EmailCategory.CAREERS,
        "marketing": EmailCategory.MARKETING,
        "media": EmailCategory.MARKETING,
        "accounts": EmailCategory.ACCOUNTS,
        "billing": EmailCategory.ACCOUNTS,
        "invoices": EmailCategory.ACCOUNTS
    }

    def find_emails(self, doc: HTMLParserDocument, source_url: str = "") -> list[ContactEmail]:
        """
        Extracts and classifies all valid public email addresses from document.
        """
        raw_text = doc.soup.get_text()
        mailto_links = [
            a.get("href").replace("mailto:", "").split("?")[0].strip()
            for a in doc.soup.find_all("a", href=True)
            if str(a.get("href")).startswith("mailto:")
        ]

        # Combine text regex matches with mailto links
        found_matches = set(self.EMAIL_REGEX.findall(raw_text))
        found_matches.update(mailto_links)

        results = []
        seen_addresses = set()

        for raw_email in found_matches:
            clean_email = raw_email.strip().lower()
            if not clean_email or clean_email in seen_addresses:
                continue

            # 1. Spam Trap / Placeholder Filtering
            if not self._is_valid_business_email(clean_email):
                continue

            seen_addresses.add(clean_email)

            # 2. Category Classification
            prefix = clean_email.split("@")[0]
            category = self.CLASSIFICATION_MAP.get(prefix, EmailCategory.UNKNOWN)
            if category == EmailCategory.UNKNOWN and "." in prefix:
                # Potential owner direct email e.g. john.smith@domain.com
                category = EmailCategory.OWNER

            # 3. Confidence Level Assignment
            is_mailto = clean_email in mailto_links
            is_contact_page = "contact" in source_url.lower()
            confidence = ConfidenceLevel.HIGH if (is_mailto or is_contact_page) else ConfidenceLevel.MEDIUM

            results.append(
                ContactEmail(
                    address=clean_email,
                    category=category,
                    source_url=source_url,
                    discovery_method="HTML DOM & Mailto Parsing",
                    confidence=confidence,
                    is_valid_syntax=True
                )
            )

        return results

    def _is_valid_business_email(self, email: str) -> bool:
        """Syntax validation and spam trap / dummy asset filter."""
        if "@" not in email:
            return False
        user, domain = email.rsplit("@", 1)

        # Ignore domain spam traps
        if domain in self.SPAM_TRAP_DOMAINS:
            return False

        # Ignore image extension spam traps (e.g. logo@2x.png)
        for ext in self.SPAM_TRAP_EXTENSIONS:
            if domain.endswith(ext) or user.endswith(ext):
                return False

        # Ensure valid TLD length
        if "." not in domain or len(domain.split(".")[-1]) < 2:
            return False

        return True
