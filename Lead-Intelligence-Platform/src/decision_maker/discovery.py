"""
Master Decision Maker Discovery Engine Orchestrator (Phase 04).
Coordinates LeadershipPageScanner, PeopleExtractor, TitleNormalizer, and DecisionMakerRanker.
Enforces strict confidence thresholding (min 0.70).
"""

import time
from src.decision_maker.models import DecisionMaker, DecisionMakerDiscoveryReport
from src.decision_maker.people_extractor import PeopleExtractor
from src.decision_maker.ranking import DecisionMakerRanker
from src.decision_maker.website_scanner import LeadershipPageScanner
from src.enrichment.fetcher import HTTPFetcher
from src.enrichment.parser import HTMLParserDocument
from src.logging.logger import logger


class DecisionMakerDiscoveryEngine:
    """Orchestrates end-to-end Decision Maker Discovery (Phase 04)."""

    MIN_CONFIDENCE_THRESHOLD = 0.70  # Only return verified candidates meeting or exceeding 70% confidence

    def __init__(self, fetcher: HTTPFetcher | None = None):
        self.fetcher = fetcher or HTTPFetcher()
        self.scanner = LeadershipPageScanner()
        self.extractor = PeopleExtractor()

    async def discover(
        self,
        domain: str,
        doc: HTMLParserDocument,
        source_url: str = "",
        sitemap_urls: list[str] | None = None,
        contact_emails: list[str] | None = None,
        contact_phones: list[str] | None = None
    ) -> DecisionMakerDiscoveryReport:
        """
        Executes Decision Maker discovery across primary DOM and discovered leadership pages.
        """
        start_time = time.perf_counter()
        notes = []
        all_decision_makers: list[DecisionMaker] = []

        if not domain:
            return DecisionMakerDiscoveryReport(
                domain="unknown",
                is_successful=False,
                notes=["Empty domain provided"]
            )

        # 1. Discover candidate leadership / team pages
        try:
            leadership_pages = self.scanner.find_leadership_pages(
                doc=doc,
                base_url=source_url,
                sitemap_urls=sitemap_urls
            )
            logger.info(f"Discovered {len(leadership_pages)} leadership candidate pages for domain '{domain}'")
        except Exception as err:
            logger.error(f"Error scanning leadership pages for '{domain}': {err}")
            notes.append(f"Scanner error: {err}")
            leadership_pages = []

        # 2. Extract decision makers from primary webpage DOM (homepage / landing)
        try:
            primary_people = self.extractor.extract_people(doc, source_url=source_url, is_leadership_page=False)
            all_decision_makers.extend(primary_people)
        except Exception as err:
            logger.error(f"Error extracting primary page decision makers for '{domain}': {err}")
            notes.append(f"Primary page extraction error: {err}")

        # 3. Crawl top candidate leadership pages (limit to max 3 unique secondary pages)
        crawled_urls = {source_url.rstrip("/")}
        crawled_count = 0

        for page in leadership_pages:
            if crawled_count >= 3:
                break

            normalized_page_url = page.url.rstrip("/")
            if normalized_page_url in crawled_urls:
                continue

            crawled_urls.add(normalized_page_url)

            try:
                logger.info(f"Fetching leadership page for '{domain}': {page.url}")
                fetch_res = await self.fetcher.fetch(page.url)

                if fetch_res.is_success and fetch_res.content:
                    crawled_count += 1
                    page_doc = HTMLParserDocument(fetch_res.content, base_url=fetch_res.url)
                    page_people = self.extractor.extract_people(page_doc, source_url=fetch_res.url, is_leadership_page=True)
                    all_decision_makers.extend(page_people)
                    notes.append(f"Crawled leadership page: {page.url} (Found {len(page_people)} people)")
                else:
                    notes.append(f"Failed fetching leadership page {page.url}: {fetch_res.error or 'HTTP status ' + str(fetch_res.status_code)}")

            except Exception as err:
                logger.warning(f"Error crawling leadership page {page.url}: {err}")
                notes.append(f"Leadership page crawl error ({page.url}): {err}")

        # 4. Deduplicate all extracted decision makers across pages
        try:
            deduped = self.extractor._deduplicate_people(all_decision_makers)
        except Exception as err:
            logger.error(f"Deduplication error for '{domain}': {err}")
            deduped = all_decision_makers

        # 5. Enrich contact emails/phones if available from Phase 03 and missing
        if contact_emails or contact_phones:
            for dm in deduped:
                if not dm.email and contact_emails:
                    if dm.first_name and dm.last_name:
                        first_lower = dm.first_name.lower()
                        last_lower = dm.last_name.lower()
                        for email_addr in contact_emails:
                            local_part = email_addr.split("@")[0].lower()
                            if first_lower in local_part or last_lower in local_part:
                                dm.email = email_addr
                                break

        # 6. Priority ranking and confidence sorting
        try:
            ranked_decision_makers = DecisionMakerRanker.rank_decision_makers(deduped)
        except Exception as err:
            logger.error(f"Ranking error for '{domain}': {err}")
            notes.append(f"Ranking error: {err}")
            ranked_decision_makers = deduped

        # 7. Strict confidence thresholding: discard unverified low-confidence guesses (< 0.70)
        verified_decision_makers = [dm for dm in ranked_decision_makers if dm.confidence >= self.MIN_CONFIDENCE_THRESHOLD]

        elapsed = round(time.perf_counter() - start_time, 4)

        report = DecisionMakerDiscoveryReport(
            domain=domain,
            leadership_pages=leadership_pages,
            decision_makers=verified_decision_makers,
            total_people_found=len(verified_decision_makers),
            execution_time_seconds=elapsed,
            is_successful=True,
            notes=notes
        )

        logger.info(f"Completed Decision Maker discovery for '{domain}': {len(verified_decision_makers)} verified decision makers ranked in {elapsed}s")
        return report
