"""
Unit tests for Phase 05 Business Intelligence sub-analyzers:
IndustryClassifier, ServiceDetector, GeographicDetector, CompanySizeEstimator, YearsInBusinessDetector, BusinessModelClassifier, TrustSignalDetector, HiringSignalDetector.
"""

from src.business_intelligence import (
    BusinessModelClassifier,
    BusinessModelType,
    CompanySizeEstimator,
    CompanySizeTier,
    GeographicDetector,
    HiringSignalDetector,
    IndustryCategory,
    IndustryClassifier,
    ServiceDetector,
    TrustSignalDetector,
    YearsInBusinessDetector,
)
from src.contact_discovery.models import BusinessAddress
from src.decision_maker.models import DecisionMaker, Department, Seniority
from src.enrichment.parser import HTMLParserDocument


def test_industry_classifier():
    classifier = IndustryClassifier()
    doc = HTMLParserDocument("<html><body><h1>Commercial Roofing Specialists</h1><p>Roof repair and metal roofing replacement.</p></body></html>")
    industry, conf = classifier.classify_industry(doc, title="Roofing Specialists")

    assert industry == IndustryCategory.ROOFING
    assert conf >= 0.70


def test_service_detector():
    detector = ServiceDetector()
    doc = HTMLParserDocument("<html><body><p>We provide roof repair, commercial roofing, and gutter installation services.</p></body></html>")
    primary, secondary = detector.detect_services(doc, industry=IndustryCategory.ROOFING)

    assert "Roof Repair" in primary or "Commercial Roofing" in primary


def test_geographic_detector():
    detector = GeographicDetector()
    doc = HTMLParserDocument("<html><body><p>Serving Dallas, Fort Worth, and Arlington</p></body></html>")
    addrs = [BusinessAddress(raw_address="123 Main St, Dallas, TX", city="Dallas", state="TX", country="USA", source_url="http://ex.com")]
    geo = detector.detect_geography(doc, addresses=addrs)

    assert geo.primary_headquarters == "Dallas, TX, USA"
    assert "Dallas" in geo.service_areas or "Fort Worth" in geo.service_areas


def test_company_size_estimator():
    estimator = CompanySizeEstimator()
    dms = [
        DecisionMaker(full_name=f"Person {i}", title="Manager", normalized_title="Manager", priority=50, confidence=0.8, source_url="http://ex.com")
        for i in range(16)
    ]
    tier, emp_range, conf = estimator.estimate_size(doc=None, decision_makers=dms)

    assert tier == CompanySizeTier.MID_MARKET
    assert emp_range == "51-250"


def test_years_in_business_detector():
    detector = YearsInBusinessDetector()
    doc = HTMLParserDocument("<html><body><footer>Founded in 2006. Celebrating 20 years.</footer></body></html>")
    founded, years = detector.detect_years(doc)

    assert founded == 2006
    assert years == 20


def test_business_model_classifier():
    classifier = BusinessModelClassifier()
    doc = HTMLParserDocument("<html><body><p>Commercial and residential roofing services for homeowners and business contractors.</p></body></html>")
    model = classifier.classify_model(doc, industry=IndustryCategory.ROOFING)

    assert model == BusinessModelType.BOTH


def test_trust_signals_detector():
    detector = TrustSignalDetector()
    doc = HTMLParserDocument("<html><body><p>Read customer testimonials and view our project portfolio. GAF Certified contractor.</p></body></html>")
    signals = detector.detect_trust_signals(doc)

    assert signals.has_testimonials is True
    assert signals.has_portfolio is True
    assert "GAF Certified" in signals.certifications


def test_hiring_signal_detector():
    detector = HiringSignalDetector()
    doc = HTMLParserDocument("<html><body><a href='/careers'>We're Hiring! Join our team</a></body></html>")
    signals = detector.detect_hiring(doc, base_url="https://company.com")

    assert signals.currently_hiring is True
    assert signals.has_careers_page is True
    assert signals.careers_page_url == "https://company.com/careers"
