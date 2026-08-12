"""
Master Enrichment Pipeline Orchestrator for Phase 2 Deep Intelligence.
Coordinates Fetcher, Parser, Metadata, Contacts, Socials, CMS, Robots, Sitemap,
SEO, Structured Data, Expanded Tech, Performance, Accessibility, Link, and Security analyzers.
"""

import time
from src.database.repository import CompanyRepository
from src.discovery.models import Company, MetadataField, TargetStatus
from src.enrichment.accessibility_analyzer import AccessibilityAnalyzer
from src.enrichment.cms_detector import CMSDetector
from src.enrichment.contact_extractor import ContactExtractor
from src.enrichment.fetcher import HTTPFetcher
from src.enrichment.link_analyzer import LinkAnalyzer
from src.enrichment.metadata import MetadataExtractor
from src.enrichment.models import CompanyEnrichmentReport
from src.enrichment.parser import HTMLParserDocument
from src.enrichment.performance_analyzer import PerformanceAnalyzer
from src.enrichment.robots import RobotsTxtParser
from src.enrichment.security_analyzer import PassiveSecurityAnalyzer
from src.enrichment.seo_analyzer import SEOAnalyzer
from src.enrichment.sitemap import SitemapParser
from src.enrichment.social_extractor import SocialExtractor
from src.enrichment.structured_data_analyzer import StructuredDataAnalyzer
from src.enrichment.tech_detector import ExpandedTechDetector
from src.logging.logger import logger


from src.contact_discovery.discovery_engine import ContactDiscoveryEngine


class EnrichmentPipeline:
    """Orchestrates end-to-end website, technical, contact, and decision maker intelligence enrichment."""

    def __init__(self, repository: CompanyRepository | None = None, fetcher: HTTPFetcher | None = None):
        self.repository = repository
        self.fetcher = fetcher or HTTPFetcher()

        # Website Intelligence Analyzers
        self.metadata_extractor = MetadataExtractor()
        self.contact_extractor = ContactExtractor()
        self.social_extractor = SocialExtractor()
        self.cms_detector = CMSDetector()
        self.robots_parser = RobotsTxtParser(fetcher=self.fetcher)
        self.sitemap_parser = SitemapParser(fetcher=self.fetcher)

        # Phase 2 Technical Intelligence Analyzers
        self.seo_analyzer = SEOAnalyzer()
        self.structured_data_analyzer = StructuredDataAnalyzer()
        self.tech_detector = ExpandedTechDetector()
        self.performance_analyzer = PerformanceAnalyzer()
        self.accessibility_analyzer = AccessibilityAnalyzer()
        self.link_analyzer = LinkAnalyzer()
        self.security_analyzer = PassiveSecurityAnalyzer()

        # Phase 3 Contact Discovery Engine
        self.contact_discovery_engine = ContactDiscoveryEngine(fetcher=self.fetcher)

        # Phase 4 Decision Maker Discovery Engine
        from src.decision_maker.discovery import DecisionMakerDiscoveryEngine
        self.decision_maker_engine = DecisionMakerDiscoveryEngine(fetcher=self.fetcher)

    async def enrich_domain(self, domain: str) -> CompanyEnrichmentReport:
        """
        Enriches a single domain target through all website, technical, and contact discovery modules.
        """
        start_time = time.perf_counter()
        notes = []

        target_url = domain if domain.startswith(("http://", "https://")) else f"https://{domain}"

        # 1. Fetch HTML webpage
        logger.info(f"Enriching target domain: '{domain}'")
        fetch_result = await self.fetcher.fetch(target_url)

        if not fetch_result.is_success:
            notes.append(f"HTTP Fetch Failed: {fetch_result.error}")
            logger.warning(f"Fetch failed for '{domain}': {fetch_result.error}")

        # 2. Parse HTML Document (Reused across all DOM analyzers)
        doc = HTMLParserDocument(fetch_result.content, base_url=fetch_result.url)

        # 3. Metadata Extraction
        try:
            metadata = self.metadata_extractor.extract(doc, base_url=fetch_result.url)
        except Exception as err:
            logger.error(f"Metadata extraction error for '{domain}': {err}")
            notes.append(f"Metadata error: {err}")
            from src.enrichment.models import WebsiteMetadata
            metadata = WebsiteMetadata()

        # 4. Contact Extraction
        try:
            contacts = self.contact_extractor.extract(doc, base_url=fetch_result.url)
        except Exception as err:
            logger.error(f"Contact extraction error for '{domain}': {err}")
            notes.append(f"Contact extraction error: {err}")
            from src.enrichment.models import ContactIntelligence
            contacts = ContactIntelligence()

        # 5. Social Profile Extraction
        try:
            socials = self.social_extractor.extract(doc)
        except Exception as err:
            logger.error(f"Social extraction error for '{domain}': {err}")
            notes.append(f"Social extraction error: {err}")
            from src.enrichment.models import SocialProfiles
            socials = SocialProfiles()

        # 6. CMS Detection
        try:
            cms = self.cms_detector.detect(doc, headers=fetch_result.headers)
        except Exception as err:
            logger.error(f"CMS detection error for '{domain}': {err}")
            notes.append(f"CMS detection error: {err}")
            from src.enrichment.models import CMSDetectionResult
            cms = CMSDetectionResult()

        # 7. Robots.txt Analysis
        try:
            robots = await self.robots_parser.fetch_and_parse(domain)
        except Exception as err:
            logger.error(f"Robots.txt error for '{domain}': {err}")
            notes.append(f"Robots error: {err}")
            from src.enrichment.models import RobotsTxtData
            robots = RobotsTxtData()

        # 8. Sitemap.xml Analysis
        try:
            sitemap_override = robots.sitemap_urls[0] if robots.sitemap_urls else None
            sitemap = await self.sitemap_parser.fetch_and_parse(domain, sitemap_url_override=sitemap_override)
        except Exception as err:
            logger.error(f"Sitemap error for '{domain}': {err}")
            notes.append(f"Sitemap error: {err}")
            from src.enrichment.models import SitemapData
            sitemap = SitemapData()

        # --- Phase 2 Technical Intelligence Executions ---

        # 9. SEO Intelligence
        try:
            seo_result = self.seo_analyzer.analyze(doc, base_url=fetch_result.url)
        except Exception as err:
            logger.error(f"SEO analysis error for '{domain}': {err}")
            notes.append(f"SEO error: {err}")
            seo_result = None

        # 10. Structured Data Analysis
        try:
            structured_data_result = self.structured_data_analyzer.analyze(doc)
        except Exception as err:
            logger.error(f"Structured data analysis error for '{domain}': {err}")
            notes.append(f"Structured data error: {err}")
            structured_data_result = None

        # 11. Expanded Technology Intelligence
        try:
            tech_stack_result = self.tech_detector.analyze(doc, headers=fetch_result.headers)
        except Exception as err:
            logger.error(f"Tech stack analysis error for '{domain}': {err}")
            notes.append(f"Tech stack error: {err}")
            tech_stack_result = None

        # 12. Performance Intelligence
        try:
            performance_result = self.performance_analyzer.analyze(fetch_result, doc)
        except Exception as err:
            logger.error(f"Performance analysis error for '{domain}': {err}")
            notes.append(f"Performance error: {err}")
            performance_result = None

        # 13. Accessibility Intelligence
        try:
            accessibility_result = self.accessibility_analyzer.analyze(doc)
        except Exception as err:
            logger.error(f"Accessibility analysis error for '{domain}': {err}")
            notes.append(f"Accessibility error: {err}")
            accessibility_result = None

        # 14. Link Intelligence
        try:
            link_result = self.link_analyzer.analyze(doc, base_url=fetch_result.url)
        except Exception as err:
            logger.error(f"Link analysis error for '{domain}': {err}")
            notes.append(f"Link error: {err}")
            link_result = None

        # 15. Passive Security Header Analysis
        try:
            security_result = self.security_analyzer.analyze(fetch_result)
        except Exception as err:
            logger.error(f"Security analysis error for '{domain}': {err}")
            notes.append(f"Security error: {err}")
            security_result = None

        # --- Phase 3 Contact Discovery Engine Execution ---
        try:
            contact_discovery_result = await self.contact_discovery_engine.discover(
                domain=domain,
                doc=doc,
                source_url=fetch_result.url,
                socials=socials
            )
        except Exception as err:
            logger.error(f"Contact discovery error for '{domain}': {err}")
            notes.append(f"Contact discovery error: {err}")
            contact_discovery_result = None

        # --- Phase 4 Decision Maker Discovery Engine Execution ---
        try:
            c_emails = [e.address for e in contact_discovery_result.emails] if contact_discovery_result and hasattr(contact_discovery_result, "emails") else None
            c_phones = [p.formatted_number for p in contact_discovery_result.phones] if contact_discovery_result and hasattr(contact_discovery_result, "phones") else None
            sitemap_urls = sitemap.sitemap_urls if sitemap else None

            decision_maker_result = await self.decision_maker_engine.discover(
                domain=domain,
                doc=doc,
                source_url=fetch_result.url,
                sitemap_urls=sitemap_urls,
                contact_emails=c_emails,
                contact_phones=c_phones
            )
        except Exception as err:
            logger.error(f"Decision maker discovery error for '{domain}': {err}")
            notes.append(f"Decision maker discovery error: {err}")
            decision_maker_result = None

        # Phase 5 Business Intelligence Engine Execution ---
        try:
            from src.business_intelligence.engine import BusinessIntelligenceEngine
            bi_engine = BusinessIntelligenceEngine()
            addrs = contact_discovery_result.addresses if contact_discovery_result and hasattr(contact_discovery_result, "addresses") else None
            dms = decision_maker_result.decision_makers if decision_maker_result and hasattr(decision_maker_result, "decision_makers") else None

            bi_result = await bi_engine.analyze(
                domain=domain,
                doc=doc,
                metadata=metadata,
                addresses=addrs,
                decision_makers=dms,
                source_url=fetch_result.url
            )
        except Exception as err:
            logger.error(f"Business intelligence analysis error for '{domain}': {err}")
            notes.append(f"Business intelligence error: {err}")
            bi_result = None

        # Phase 6 Marketing Intelligence Engine Execution ---
        try:
            from src.marketing_intelligence.engine import MarketingIntelligenceEngine
            mkt_engine = MarketingIntelligenceEngine()

            mkt_result = await mkt_engine.analyze(
                domain=domain,
                doc=doc,
                metadata=metadata,
                socials=socials,
                seo_result=seo_result,
                structured_data=structured_data_result,
                tech_stack_result=tech_stack_result,
                robots=robots,
                sitemap=sitemap,
                source_url=fetch_result.url
            )
        except Exception as err:
            logger.error(f"Marketing intelligence analysis error for '{domain}': {err}")
            notes.append(f"Marketing intelligence error: {err}")
            mkt_result = None

        elapsed_sec = round(time.perf_counter() - start_time, 3)

        report = CompanyEnrichmentReport(
            domain=domain,
            fetch_result=fetch_result,
            metadata=metadata,
            contacts=contacts,
            socials=socials,
            cms=cms,
            robots=robots,
            sitemap=sitemap,
            seo=seo_result,
            structured_data=structured_data_result,
            tech_stack=tech_stack_result,
            performance=performance_result,
            accessibility=accessibility_result,
            links=link_result,
            security=security_result,
            contact_discovery=contact_discovery_result,
            decision_maker_discovery=decision_maker_result,
            business_intelligence=bi_result,
            marketing_intelligence=mkt_result,
            execution_time_seconds=elapsed_sec,
            is_successful=fetch_result.is_success,
            notes=notes
        )

        return report

    async def enrich_company(self, company: Company) -> CompanyEnrichmentReport:
        """
        Enriches a Company target entity and updates repository storage.
        """
        report = await self.enrich_domain(company.domain)

        # Update Company model attributes from enrichment results
        if report.metadata.title:
            company.name = MetadataField[str](
                value=report.metadata.title,
                confidence=0.8,
                source=report.fetch_result.url
            )

        if report.fetch_result.url:
            company.website_url = MetadataField[str](
                value=report.fetch_result.url,
                confidence=1.0,
                source="HTTPFetcher"
            )

        company.status = TargetStatus.ANALYZED if report.is_successful else TargetStatus.FAILED

        if self.repository:
            self.repository.update(company)

        return report

    async def enrich_batch(self, companies: list[Company]) -> list[CompanyEnrichmentReport]:
        """
        Processes a list of Company targets sequentially or concurrently.
        """
        reports = []
        for company in companies:
            try:
                report = await self.enrich_company(company)
                reports.append(report)
            except Exception as err:
                logger.error(f"Failed enrichment for target company '{company.domain}': {err}")
        return reports
