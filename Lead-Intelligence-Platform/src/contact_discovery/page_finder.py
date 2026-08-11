"""
Secondary Contact Page Finder Module.
Discovers and classifies secondary contact, about, team, support, careers, and quote request page URLs.
"""

from urllib.parse import urljoin, urlparse
from src.contact_discovery.models import ContactPage, ContactPageCategory
from src.enrichment.parser import HTMLParserDocument
from src.logging.logger import logger


class ContactPageFinder:
    """Discovers secondary contact-related URLs on the target site."""

    PATH_PATTERNS = {
        ContactPageCategory.CONTACT: ["contact", "contact-us", "contactus", "get-in-touch"],
        ContactPageCategory.ABOUT: ["about", "about-us", "aboutus", "our-company", "our-story"],
        ContactPageCategory.TEAM: ["team", "our-team", "staff", "management", "people"],
        ContactPageCategory.SUPPORT: ["support", "help", "faq", "customer-service"],
        ContactPageCategory.CAREERS: ["careers", "jobs", "join-our-team", "work-with-us"],
        ContactPageCategory.QUOTE: ["quote", "get-a-quote", "estimate", "request-quote"]
    }

    def find_contact_pages(self, doc: HTMLParserDocument, base_url: str = "") -> list[ContactPage]:
        """
        Scans all document links for secondary contact page matches.
        """
        all_links = doc.get_all_links()
        results = []
        seen_urls = set()

        base_domain = urlparse(base_url).netloc.lower() if base_url else ""

        for link in all_links:
            href = link["href"].strip()
            text = link["text"].strip()

            abs_url = urljoin(base_url, href) if base_url else href

            if abs_url in seen_urls:
                continue

            # Ensure internal domain link
            if base_domain and base_domain not in urlparse(abs_url).netloc.lower():
                continue

            category = self._classify_url(abs_url, text)
            if category:
                seen_urls.add(abs_url)
                results.append(
                    ContactPage(
                        url=abs_url,
                        category=category,
                        title=text or None
                    )
                )

        return results

    def _classify_url(self, url: str, text: str) -> ContactPageCategory | None:
        """Classifies link URL path and anchor text."""
        path = urlparse(url).path.lower()
        clean_text = text.lower()

        # 1. Match URL Path first
        for cat, keywords in self.PATH_PATTERNS.items():
            for kw in keywords:
                if kw in path:
                    return cat

        # 2. Fallback to anchor text
        for cat, keywords in self.PATH_PATTERNS.items():
            for kw in keywords:
                if kw in clean_text:
                    return cat

        return None
