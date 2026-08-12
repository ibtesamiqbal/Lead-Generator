"""
Industry Classification Engine (Phase 05).
Classifies target company into core B2B industry verticals using multi-signal scoring.
"""

import re
from src.business_intelligence.models import IndustryCategory
from src.enrichment.parser import HTMLParserDocument


class IndustryClassifier:
    """Classifies target company industry category based on DOM content, titles, headings, and meta."""

    INDUSTRY_TAXONOMY: dict[IndustryCategory, list[str]] = {
        IndustryCategory.ROOFING: [
            "roofing", "roof repair", "roof replacement", "metal roofing", "shingle", "gutter",
            "re-roofing", "roof restoration", "roofers", "commercial roofing", "residential roofing"
        ],
        IndustryCategory.HVAC: [
            "hvac", "air conditioning", "heating", "cooling", "furnace", "heat pump",
            "ventilation", "climatisation", "ac repair", "ductwork", "daikin", "fujitsu"
        ],
        IndustryCategory.PLUMBING: [
            "plumbing", "plumber", "drain cleaning", "water heater", "leak detection",
            "pipe repair", "sewer", "clogged drain", "master plumber", "backflow"
        ],
        IndustryCategory.ELECTRICAL: [
            "electrician", "electrical", "wiring", "circuit breaker", "lighting installation",
            "ev charger", "generator", "electrical contractor"
        ],
        IndustryCategory.LANDSCAPING: [
            "landscaping", "lawn care", "garden design", "hardscaping", "irrigation",
            "tree service", "landscape architecture", "patio", "turf"
        ],
        IndustryCategory.SAAS: [
            "saas", "software", "cloud platform", "automation software", "workflow", "crm",
            "api", "developer tools", "analytics platform", "b2b software", "app"
        ],
        IndustryCategory.MARKETING_AGENCY: [
            "marketing agency", "digital marketing", "seo agency", "ppc", "advertising agency",
            "branding agency", "web design agency", "public relations", "growth agency"
        ],
        IndustryCategory.LAW_FIRM: [
            "law firm", "attorney", "lawyer", "legal services", "litigation", "personal injury",
            "family law", "corporate law", "legal practice", "counsel"
        ],
        IndustryCategory.DENTAL_CLINIC: [
            "dental", "dentist", "orthodontics", "teeth whitening", "dental implants",
            "cosmetic dentistry", "dental care", "oral surgery", "pediatric dentist"
        ],
        IndustryCategory.MANUFACTURING: [
            "manufacturing", "manufacturer", "steel fabrication", "industrial equipment",
            "machining", "oem", "assembly", "materials handling", "packaging"
        ],
        IndustryCategory.FINANCIAL_SERVICES: [
            "accounting", "wealth management", "financial planning", "tax services",
            "cpa", "investment banking", "mortgage broker", "insurance agency"
        ],
        IndustryCategory.HEALTHCARE: [
            "healthcare", "clinic", "medical center", "physician", "hospital",
            "physical therapy", "dermatology", "chiropractor"
        ],
        IndustryCategory.REAL_ESTATE: [
            "real estate", "realtor", "property management", "commercial real estate",
            "residential sales", "realty", "property listings"
        ],
        IndustryCategory.CONSTRUCTION: [
            "construction", "general contractor", "building contractor", "renovation",
            "remodeling", "civil engineering", "excavation", "builder"
        ],
    }

    def classify_industry(
        self,
        doc: HTMLParserDocument | None,
        title: str | None = None,
        meta_desc: str | None = None
    ) -> tuple[IndustryCategory, float]:
        """
        Classifies target domain industry and returns (IndustryCategory, confidence_score).
        """
        scores: dict[IndustryCategory, float] = {ind: 0.0 for ind in IndustryCategory}

        combined_text = ""
        if title:
            combined_text += title + " "
        if meta_desc:
            combined_text += meta_desc + " "

        if doc and doc.soup:
            headings = " ".join([h.get_text(strip=True) for h in doc.soup.find_all(["h1", "h2", "h3"])])
            nav = " ".join([a.get_text(strip=True) for a in doc.soup.find_all("a")])
            combined_text += headings + " " + nav

        text_lower = combined_text.lower()
        if not text_lower.strip():
            return (IndustryCategory.OTHER_B2B, 0.40)

        for industry, keywords in self.INDUSTRY_TAXONOMY.items():
            for kw in keywords:
                matches = len(re.findall(rf"\b{re.escape(kw)}\b", text_lower))
                if matches > 0:
                    # Title & meta matches receive higher weight
                    title_match = 1 if (title and kw in title.lower()) else 0
                    scores[industry] += matches * 0.25 + title_match * 0.50

        best_industry = max(scores, key=scores.get)
        max_score = scores[best_industry]

        if max_score == 0.0:
            return (IndustryCategory.OTHER_B2B, 0.50)

        # Normalize confidence (max 0.95)
        confidence = round(min(0.95, 0.60 + (max_score * 0.10)), 2)
        return (best_industry, confidence)
