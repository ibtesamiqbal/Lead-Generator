"""
Master Contact Discovery Engine Orchestrator (Phase 03).
Coordinates EmailFinder, PhoneFinder, ContactPageFinder, AddressFinder, HoursFinder, and SocialValidator.
"""

import time
from src.contact_discovery.address_finder import AddressFinder
from src.contact_discovery.email_finder import EmailFinder
from src.contact_discovery.hours_finder import BusinessHoursFinder
from src.contact_discovery.models import ContactDiscoveryReport
from src.contact_discovery.page_finder import ContactPageFinder
from src.contact_discovery.phone_finder import PhoneFinder
from src.contact_discovery.social_validator import SocialProfileValidator
from src.enrichment.fetcher import HTTPFetcher
from src.enrichment.models import SocialProfiles
from src.enrichment.parser import HTMLParserDocument
from src.logging.logger import logger


class ContactDiscoveryEngine:
    """Orchestrates end-to-end contact intelligence discovery."""

    def __init__(self, fetcher: HTTPFetcher | None = None):
        self.fetcher = fetcher or HTTPFetcher()
        self.email_finder = EmailFinder()
        self.phone_finder = PhoneFinder()
        self.page_finder = ContactPageFinder()
        self.address_finder = AddressFinder()
        self.hours_finder = BusinessHoursFinder()
        self.social_validator = SocialProfileValidator()

    async def discover(self, domain: str, doc: HTMLParserDocument, source_url: str = "", socials: SocialProfiles | None = None) -> ContactDiscoveryReport:
        """
        Executes contact discovery pipeline across DOM document and discovered secondary pages.
        """
        start_time = time.perf_counter()
        notes = []

        # 1. Primary Page Discoveries
        emails = self.email_finder.find_emails(doc, source_url=source_url)
        phones = self.phone_finder.find_phones(doc, source_url=source_url)
        pages = self.page_finder.find_contact_pages(doc, base_url=source_url)
        addresses = self.address_finder.find_addresses(doc, source_url=source_url)
        hours = self.hours_finder.find_hours(doc, source_url=source_url)
        social_validations = self.social_validator.validate_profiles(socials or SocialProfiles())

        # 2. Optionally fetch secondary contact page if discovered to extract extra contacts
        if pages and self.fetcher:
            try:
                top_contact_page = pages[0].url
                fetch_res = await self.fetcher.fetch(top_contact_page)
                if fetch_res.is_success and fetch_res.content:
                    sec_doc = HTMLParserDocument(fetch_res.content, base_url=fetch_res.url)

                    sec_emails = self.email_finder.find_emails(sec_doc, source_url=top_contact_page)
                    sec_phones = self.phone_finder.find_phones(sec_doc, source_url=top_contact_page)
                    sec_addresses = self.address_finder.find_addresses(sec_doc, source_url=top_contact_page)

                    # Deduplicate with primary page results
                    existing_email_addrs = {e.address for e in emails}
                    for e in sec_emails:
                        if e.address not in existing_email_addrs:
                            emails.append(e)
                            existing_email_addrs.add(e.address)

                    existing_phone_keys = {p.e164_number or p.formatted_number for p in phones}
                    for p in sec_phones:
                        key = p.e164_number or p.formatted_number
                        if key not in existing_phone_keys:
                            phones.append(p)
                            existing_phone_keys.add(key)

                    if sec_addresses and not addresses:
                        addresses.extend(sec_addresses)
            except Exception as err:
                logger.warning(f"Failed secondary contact page crawl for '{domain}': {err}")
                notes.append(f"Secondary page crawl error: {err}")

        elapsed = round(time.perf_counter() - start_time, 4)

        report = ContactDiscoveryReport(
            domain=domain,
            emails=emails,
            phones=phones,
            addresses=addresses,
            operating_hours=hours,
            contact_pages=pages,
            social_validations=social_validations,
            total_emails_found=len(emails),
            total_phones_found=len(phones),
            execution_time_seconds=elapsed,
            is_successful=True,
            notes=notes
        )

        return report
