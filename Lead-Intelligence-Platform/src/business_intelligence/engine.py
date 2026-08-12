"""
Master Business Intelligence Engine Orchestrator (Phase 05).
Synthesizes industry classification, service detection, geographic footprint,
company size estimation, years in business, business model, trust signals, and hiring signals.
"""

import time
from src.business_intelligence.business_model import BusinessModelClassifier
from src.business_intelligence.classifier import IndustryClassifier
from src.business_intelligence.company_size import CompanySizeEstimator
from src.business_intelligence.geography import GeographicDetector
from src.business_intelligence.hiring import HiringSignalDetector
from src.business_intelligence.models import BusinessIntelligenceReport
from src.business_intelligence.service_detector import ServiceDetector
from src.business_intelligence.trust_signals import TrustSignalDetector
from src.business_intelligence.years_in_business import YearsInBusinessDetector
from src.contact_discovery.models import BusinessAddress
from src.decision_maker.models import DecisionMaker
from src.enrichment.models import WebsiteMetadata
from src.enrichment.parser import HTMLParserDocument
from src.logging.logger import logger


class BusinessIntelligenceEngine:
    """Orchestrates end-to-end Business Intelligence analysis for Phase 05."""

    def __init__(self):
        self.classifier = IndustryClassifier()
        self.service_detector = ServiceDetector()
        self.geography_detector = GeographicDetector()
        self.size_estimator = CompanySizeEstimator()
        self.years_detector = YearsInBusinessDetector()
        self.model_classifier = BusinessModelClassifier()
        self.trust_detector = TrustSignalDetector()
        self.hiring_detector = HiringSignalDetector()

    async def analyze(
        self,
        domain: str,
        doc: HTMLParserDocument | None,
        metadata: WebsiteMetadata | None = None,
        addresses: list[BusinessAddress] | None = None,
        decision_makers: list[DecisionMaker] | None = None,
        source_url: str = ""
    ) -> BusinessIntelligenceReport:
        """
        Synthesizes structured Business Intelligence profile from website DOM and collected phase data.
        """
        start_time = time.perf_counter()
        notes = []

        title = metadata.title if metadata else None
        meta_desc = metadata.meta_description if metadata else None

        # 1. Industry Classification
        industry, ind_confidence = self.classifier.classify_industry(doc, title=title, meta_desc=meta_desc)

        # 2. Service Detection
        primary_svcs, secondary_svcs = self.service_detector.detect_services(doc, industry=industry)

        # 3. Geographic Footprint
        geography = self.geography_detector.detect_geography(doc, addresses=addresses)

        # 4. Hiring Signals
        hiring = self.hiring_detector.detect_hiring(doc, base_url=source_url)

        # 5. Company Size Estimation
        size_tier, emp_range, size_conf = self.size_estimator.estimate_size(
            doc,
            decision_makers=decision_makers,
            office_count=geography.office_locations_count,
            has_careers_page=hiring.has_careers_page
        )

        # 6. Years in Business
        founded_yr, years_in_biz = self.years_detector.detect_years(doc)

        # 7. Business Model
        biz_model = self.model_classifier.classify_model(doc, industry=industry)

        # 8. Trust Signals
        trust = self.trust_detector.detect_trust_signals(doc)

        report = BusinessIntelligenceReport(
            domain=domain,
            industry=industry,
            industry_confidence=ind_confidence,
            business_model=biz_model,
            company_size_tier=size_tier,
            estimated_employee_range=emp_range,
            company_size_confidence=size_conf,
            founded_year=founded_yr,
            years_in_business=years_in_biz,
            primary_services=primary_svcs,
            secondary_services=secondary_svcs,
            geography=geography,
            trust_signals=trust,
            hiring=hiring,
            is_successful=True,
            notes=notes
        )

        elapsed = round(time.perf_counter() - start_time, 4)
        logger.info(f"Completed Business Intelligence analysis for '{domain}': Industry={industry.value}, Size={emp_range} in {elapsed}s")
        return report
