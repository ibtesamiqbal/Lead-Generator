"""
Job Title Normalizer, Department Classifier, and Seniority Classifier for Phase 04.
"""

import re
from src.decision_maker.models import Department, Seniority

# Map of exact or abbreviation aliases to standardized normalized titles
EXACT_TITLE_MAPPINGS: dict[str, str] = {
    "ceo": "Chief Executive Officer",
    "chief executive officer": "Chief Executive Officer",
    "interim ceo": "Chief Executive Officer",
    "group ceo": "Chief Executive Officer",
    "coo": "Chief Operating Officer",
    "chief operating officer": "Chief Operating Officer",
    "cto": "Chief Technology Officer",
    "chief technology officer": "Chief Technology Officer",
    "cfo": "Chief Financial Officer",
    "chief financial officer": "Chief Financial Officer",
    "cmo": "Chief Marketing Officer",
    "chief marketing officer": "Chief Marketing Officer",
    "cio": "Chief Information Officer",
    "chief information officer": "Chief Information Officer",
    "chro": "Chief Human Resources Officer",
    "chief human resources officer": "Chief Human Resources Officer",
    "cro": "Chief Revenue Officer",
    "chief revenue officer": "Chief Revenue Officer",
    "owner": "Owner",
    "founder": "Founder",
    "co-founder": "Co-Founder",
    "cofounder": "Co-Founder",
    "president": "President",
    "managing director": "Managing Director",
    "group managing director": "Managing Director",
    "partner": "Partner",
    "managing partner": "Partner",
    "general manager": "General Manager",
    "vp sales": "Vice President Sales",
    "vp of sales": "Vice President Sales",
    "vice president sales": "Vice President Sales",
    "vice president of sales": "Vice President Sales",
    "head of sales": "Head of Sales",
    "sales director": "Sales Director",
    "business development director": "Business Development Director",
    "vp business development": "Vice President Business Development",
    "operations director": "Operations Director",
    "marketing director": "Marketing Director",
    "growth director": "Growth Director",
    "vp marketing": "Vice President Marketing",
    "vp operations": "Vice President Operations",
    "vp engineering": "Vice President Engineering",
    "head of engineering": "Head of Engineering",
    "head of marketing": "Head of Marketing",
    "head of operations": "Head of Operations",
    "head of finance": "Head of Finance",
    "head of people": "Head of People",
    "head of hr": "Head of Human Resources",
}


class TitleNormalizer:
    """Normalizes job titles, assigns departments, and calculates seniority level."""

    @staticmethod
    def normalize_title(raw_title: str | None) -> str:
        """
        Normalizes raw job title string into standardized representation.
        """
        if not raw_title or not isinstance(raw_title, str):
            return "Unknown"

        cleaned = re.sub(r"\s+", " ", raw_title.strip())
        lower_title = cleaned.lower()

        # Check exact lookup dictionary
        if lower_title in EXACT_TITLE_MAPPINGS:
            return EXACT_TITLE_MAPPINGS[lower_title]

        # Standard replacement patterns
        normalized = cleaned
        normalized = re.sub(r"\bCEO\b", "Chief Executive Officer", normalized, flags=re.IGNORECASE)
        normalized = re.sub(r"\bCTO\b", "Chief Technology Officer", normalized, flags=re.IGNORECASE)
        normalized = re.sub(r"\bCOO\b", "Chief Operating Officer", normalized, flags=re.IGNORECASE)
        normalized = re.sub(r"\bCFO\b", "Chief Financial Officer", normalized, flags=re.IGNORECASE)
        normalized = re.sub(r"\bCMO\b", "Chief Marketing Officer", normalized, flags=re.IGNORECASE)
        normalized = re.sub(r"\bCIO\b", "Chief Information Officer", normalized, flags=re.IGNORECASE)
        normalized = re.sub(r"\bVP\b", "Vice President", normalized, flags=re.IGNORECASE)
        normalized = re.sub(r"\bCo-Founder\b", "Co-Founder", normalized, flags=re.IGNORECASE)
        normalized = re.sub(r"\bCofounder\b", "Co-Founder", normalized, flags=re.IGNORECASE)

        # Capitalize words neatly, preserving hyphens (e.g. Co-Founder)
        words = normalized.split()
        capitalized_words = []
        for w in words:
            if "-" in w:
                parts = [p.capitalize() if p.lower() not in {"of", "and", "&", "the"} else p.lower() for p in w.split("-")]
                capitalized_words.append("-".join(parts))
            elif w.lower() in {"of", "and", "&", "the", "in", "for", "at", "/"}:
                capitalized_words.append(w.lower())
            else:
                capitalized_words.append(w.capitalize())

        final_title = " ".join(capitalized_words)
        return final_title if final_title else "Unknown"

    @staticmethod
    def classify_department(title: str | None) -> Department:
        """
        Classifies job title into business department sector.
        """
        if not title or not isinstance(title, str):
            return Department.UNKNOWN

        lower = title.lower()

        # Specific functional departments checked first so "VP Sales" becomes SALES, not EXECUTIVE
        if any(term in lower for term in [
            "sales", "business development", "account executive", "commercial", "revenue"
        ]) or re.search(r"\bcro\b", lower):
            return Department.SALES

        if any(term in lower for term in [
            "technology", "tech", "engineering", "software", "it ", "information technology",
            "developer", "architect", "data science"
        ]) or any(re.search(rf"\b{term}\b", lower) for term in ["cto", "cio"]):
            return Department.TECHNOLOGY

        if any(term in lower for term in [
            "marketing", "growth", "brand", "communications", "content", "digital marketing"
        ]) or re.search(r"\bcmo\b", lower):
            return Department.MARKETING

        if any(term in lower for term in [
            "operations", "general manager", "logistics", "supply chain", "chief operating"
        ]) or re.search(r"\bcoo\b", lower):
            return Department.OPERATIONS

        if any(term in lower for term in [
            "finance", "financial", "accounting", "treasurer", "controller", "chief financial"
        ]) or re.search(r"\bcfo\b", lower):
            return Department.FINANCE

        if any(term in lower for term in [
            "human resources", "hr ", "people", "talent", "recruitment", "chief human resources"
        ]) or re.search(r"\bchro\b", lower):
            return Department.HUMAN_RESOURCES

        # Executive (CEO, Founder, Owner, President without Vice, Managing Director, Partner)
        if any(term in lower for term in [
            "chief executive", "founder", "owner", "managing director",
            "co-founder", "partner", "principal", "managing partner", "chairman", "chairwoman"
        ]) or re.search(r"\bceo\b", lower) or (re.search(r"\bpresident\b", lower) and "vice" not in lower and "vp" not in lower):
            return Department.EXECUTIVE

        return Department.UNKNOWN

    @staticmethod
    def classify_seniority(title: str | None) -> Seniority:
        """
        Determines seniority level from job title.
        """
        if not title or not isinstance(title, str):
            return Seniority.UNKNOWN

        lower = title.lower()

        # Vice President check before general executive
        if "vice president" in lower or re.search(r"\bvp\b", lower) or "evp" in lower or "svp" in lower:
            return Seniority.VP

        # C-Level & Top Executives (use word boundary for acronyms to prevent 'cto' matching inside 'director')
        if any(re.search(rf"\b{term}\b", lower) for term in ["chief", "ceo", "cto", "coo", "cfo", "cmo", "cio", "chro", "cro"]) or \
           any(term in lower for term in ["founder", "owner", "president", "managing director", "partner", "co-founder"]):
            return Seniority.EXECUTIVE

        # Director
        if "director" in lower:
            return Seniority.DIRECTOR

        # Head of
        if "head" in lower or "lead" in lower:
            return Seniority.HEAD

        # Manager
        if "manager" in lower or "general manager" in lower:
            return Seniority.MANAGER

        return Seniority.STAFF
