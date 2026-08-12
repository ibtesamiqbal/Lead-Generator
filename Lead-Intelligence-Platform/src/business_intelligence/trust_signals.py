"""
Trust Signal Detector (Phase 05).
Detects testimonials, reviews, case studies, portfolios, certifications, awards, warranties, and financing.
"""

import re
from src.business_intelligence.models import TrustSignals
from src.enrichment.parser import HTMLParserDocument


class TrustSignalDetector:
    """Detects credibility and trust signals across DOM content."""

    KNOWN_CERTIFICATIONS = [
        "GAF Certified", "ISO 9001", "ISO 27001", "Master Plumber", "NATE Certified",
        "EPA Certified", "BBB Accredited", "SOC 2", "HIPAA Compliant", "OSHA"
    ]

    def detect_trust_signals(self, doc: HTMLParserDocument | None) -> TrustSignals:
        """
        Returns populated TrustSignals model.
        """
        signals = TrustSignals()
        if not doc or not doc.soup:
            return signals

        text = doc.soup.get_text(separator=" ").lower()
        html_str = str(doc.soup).lower()

        # 1. Testimonials
        if any(kw in text for kw in ["testimonial", "what our clients say", "customer story", "reviews", "client reviews"]):
            signals.has_testimonials = True
            signals.has_reviews = True

        # 2. Case Studies & Portfolio
        if any(kw in text for kw in ["case study", "case studies", "client stories", "customer results"]):
            signals.has_case_studies = True
        if any(kw in text for kw in ["portfolio", "our work", "gallery", "recent projects"]):
            signals.has_portfolio = True

        # 3. Financing & Warranty
        if any(kw in text for kw in ["financing", "financing available", "financing options", "0% apr", "payment plans", "finance options", "monthly payments"]):
            signals.has_financing = True
        if any(kw in text for kw in ["warranty", "guarantee", "lifetime warranty", "100% satisfaction guarantee"]):
            signals.has_warranty = True

        # 4. Certifications
        certs = []
        for cert in self.KNOWN_CERTIFICATIONS:
            if re.search(rf"\b{re.escape(cert.lower())}\b", text):
                certs.append(cert)
        signals.certifications = certs

        # 5. Awards
        awards = []
        award_matches = re.findall(r"\b(best\s+[a-z\s]+20\d{2}|award\s+winner|top\s+[a-z\s]+20\d{2})\b", text)
        for aw in award_matches[:3]:
            awards.append(aw.title())
        signals.awards = awards

        return signals
