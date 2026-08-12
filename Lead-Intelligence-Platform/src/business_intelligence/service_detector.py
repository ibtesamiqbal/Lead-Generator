"""
Service Detection Engine (Phase 05).
Detects primary and secondary services offered by the target company.
"""

import re
from src.business_intelligence.models import IndustryCategory
from src.enrichment.parser import HTMLParserDocument


class ServiceDetector:
    """Detects primary and secondary services offered based on industry taxonomy and page DOM."""

    SERVICE_TAXONOMY: dict[IndustryCategory, list[str]] = {
        IndustryCategory.ROOFING: [
            "Roof Repair", "Roof Replacement", "Commercial Roofing", "Residential Roofing",
            "Metal Roofing", "Gutter Installation", "Roof Maintenance", "Emergency Roof Repair"
        ],
        IndustryCategory.HVAC: [
            "Air Conditioning Repair", "AC Installation", "Heating System Maintenance",
            "Duct Cleaning", "Heat Pump Services", "Commercial HVAC", "Indoor Air Quality"
        ],
        IndustryCategory.PLUMBING: [
            "Drain Cleaning", "Water Heater Repair", "Leak Detection", "Pipe Repair",
            "Emergency Plumbing", "Commercial Plumbing", "Sewer Line Repair", "Bathroom Plumbing"
        ],
        IndustryCategory.ELECTRICAL: [
            "Electrical Wiring", "EV Charger Installation", "Generator Installation",
            "Circuit Breaker Repair", "Commercial Electrical", "Lighting Installation"
        ],
        IndustryCategory.LANDSCAPING: [
            "Lawn Care", "Landscape Design", "Hardscaping", "Irrigation Systems",
            "Tree Trimming", "Garden Maintenance", "Commercial Landscaping"
        ],
        IndustryCategory.SAAS: [
            "Cloud Platform", "Workflow Automation", "API Integration", "Customer Analytics",
            "Enterprise Software", "Security Management", "Collaboration Tools"
        ],
        IndustryCategory.MARKETING_AGENCY: [
            "SEO", "PPC Advertising", "Web Design", "Branding", "Email Marketing",
            "Social Media Management", "Content Marketing", "CRO"
        ],
        IndustryCategory.LAW_FIRM: [
            "Personal Injury", "Corporate Law", "Litigation", "Family Law",
            "Estate Planning", "Criminal Defense", "Intellectual Property"
        ],
        IndustryCategory.DENTAL_CLINIC: [
            "Teeth Whitening", "Dental Implants", "Cosmetic Dentistry", "Root Canal Therapy",
            "Orthodontics", "Pediatric Dentistry", "General Dentistry"
        ],
        IndustryCategory.MANUFACTURING: [
            "Custom Metal Fabrication", "CNC Machining", "Assembly Services",
            "Industrial Equipment Manufacturing", "OEM Manufacturing", "Packaging Solutions"
        ],
    }

    def detect_services(
        self,
        doc: HTMLParserDocument | None,
        industry: IndustryCategory
    ) -> tuple[list[str], list[str]]:
        """
        Extracts (primary_services, secondary_services) for the target company.
        """
        if not doc or not doc.soup:
            return ([], [])

        text = doc.soup.get_text(separator=" ").lower()
        matched_services: list[str] = []

        possible_services = self.SERVICE_TAXONOMY.get(industry, [
            "Consulting", "Implementation", "Support Services", "Custom Solutions", "Maintenance"
        ])

        for svc in possible_services:
            if re.search(rf"\b{re.escape(svc.lower())}\b", text):
                matched_services.append(svc)

        # Fallback service extraction from DOM link titles under /services/ or /solutions/
        service_links = doc.soup.select("a[href*='service'], a[href*='solution'], nav a")
        for link in service_links:
            lbl = link.get_text(strip=True)
            if lbl and 4 <= len(lbl) <= 40 and not any(kw in lbl.lower() for kw in ["home", "about", "contact", "blog", "privacy"]):
                if lbl not in matched_services and len(matched_services) < 10:
                    matched_services.append(lbl.title())

        if not matched_services:
            return (["General Business Services"], [])

        primary = matched_services[:3]
        secondary = matched_services[3:8]
        return (primary, secondary)
