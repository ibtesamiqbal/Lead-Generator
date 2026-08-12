"""
Conversion Optimization Analyzer (Phase 06).
Detects contact forms, quote requests, demo requests, booking systems, live chat, and downloadable assets.
"""

import re
from src.enrichment.parser import HTMLParserDocument
from src.marketing_intelligence.models import ConversionOptimization


class ConversionOptimizationAnalyzer:
    """Detects lead generation forms, live chat, booking widgets, and conversion assets."""

    def analyze_conversion(self, doc: HTMLParserDocument | None) -> ConversionOptimization:
        """
        Returns populated ConversionOptimization model.
        """
        conv = ConversionOptimization()
        if not doc or not doc.soup:
            return conv

        soup = doc.soup
        text = soup.get_text(separator=" ").lower()
        html_str = str(soup).lower()

        # 1. Contact Form Detection
        forms = soup.find_all("form")
        if forms:
            conv.has_contact_form = True

        # 2. Quote Request & Demo Request
        if any(kw in text for kw in ["request a quote", "get a quote", "free estimate", "instant quote"]):
            conv.has_quote_request = True
        if any(kw in text for kw in ["schedule a demo", "request demo", "book a demo", "free trial"]):
            conv.has_demo_request = True

        # 3. Booking Systems
        if any(kw in text for kw in ["book online", "schedule appointment", "calendly.com", "hubspot.com/meetings", "acuityscheduling"]):
            conv.has_booking_system = True

        # 4. Newsletter Signup
        if any(kw in text for kw in ["subscribe to newsletter", "sign up for updates", "join our mailing list", "newsletter"]):
            conv.has_newsletter_signup = True

        # 5. Live Chat Widgets (Intercom, Drift, Crisp, Tidio, Zendesk, HubSpot Chat, LiveChat)
        if any(tool in html_str for tool in ["intercom", "drift", "crisp.chat", "tidio", "zendesk", "hubspot-messages", "livechat"]):
            conv.has_live_chat = True

        # 6. Downloadable Assets
        if any(kw in text for kw in ["download pdf", "download ebook", "download guide", "download whitepaper"]):
            conv.has_downloadable_assets = True

        score = 0.0
        if conv.has_contact_form: score += 30.0
        if conv.has_quote_request or conv.has_demo_request: score += 25.0
        if conv.has_booking_system: score += 20.0
        if conv.has_live_chat: score += 15.0
        if conv.has_newsletter_signup or conv.has_downloadable_assets: score += 10.0

        conv.conversion_score = round(min(100.0, score), 1)
        return conv
