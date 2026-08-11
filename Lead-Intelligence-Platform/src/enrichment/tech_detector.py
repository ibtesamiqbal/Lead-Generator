"""
Expanded Technology Detector Module.
Multi-heuristic technology detection for Analytics, Advertising, JS Frameworks, CSS Frameworks, Infrastructure, Marketing, and Live Chat.
"""

import time
from bs4 import Tag
from src.enrichment.cms_detector import CMSDetector
from src.enrichment.models import AnalyzerResult, DetectedTechnology, ExpandedTechStack
from src.enrichment.parser import HTMLParserDocument
from src.logging.logger import logger


class ExpandedTechDetector:
    """Detects front-end frameworks, analytics, advertising pixels, infrastructure, and marketing widgets."""

    def __init__(self):
        self.cms_detector = CMSDetector()

    def analyze(self, doc: HTMLParserDocument, headers: dict[str, str] | None = None) -> AnalyzerResult[ExpandedTechStack]:
        """
        Runs signature pattern matching against HTML content, script tags, DOM attributes, and response headers.
        """
        start_time = time.perf_counter()
        findings = []
        warnings = []
        errors = []
        headers = headers or {}
        html_content = doc.raw_html.lower()

        # Collect script src and link href attributes
        scripts = [s.get("src") for s in doc.soup.find_all("script") if isinstance(s, Tag) and s.get("src")]
        links = [l.get("href") for l in doc.soup.find_all("link") if isinstance(l, Tag) and l.get("href")]
        all_asset_urls = [str(url).lower() for url in (scripts + links) if url]

        # 1. Analytics
        analytics = []
        if any("googletagmanager.com/gtag/js" in u or "google-analytics.com" in u for u in all_asset_urls) or "gtag(" in html_content:
            analytics.append(DetectedTechnology(name="Google Analytics 4", category="Analytics", confidence=0.9, evidence=["gtag.js signature"]))
        if any("googletagmanager.com/gtm.js" in u for u in all_asset_urls) or "gtm-container" in html_content:
            analytics.append(DetectedTechnology(name="Google Tag Manager", category="Analytics", confidence=0.95, evidence=["gtm.js script URL"]))
        if any("clarity.ms" in u for u in all_asset_urls) or "clarity(" in html_content:
            analytics.append(DetectedTechnology(name="Microsoft Clarity", category="Analytics", confidence=0.95, evidence=["clarity.ms asset"]))

        # 2. Advertising
        advertising = []
        if any("googleadservices.com" in u or "pagead2.googlesyndication.com" in u for u in all_asset_urls):
            advertising.append(DetectedTechnology(name="Google Ads", category="Advertising", confidence=0.9, evidence=["googleadservices asset"]))
        if any("connect.facebook.net" in u and "fbevents.js" in u for u in all_asset_urls) or "fbq(" in html_content:
            advertising.append(DetectedTechnology(name="Meta Pixel", category="Advertising", confidence=0.95, evidence=["fbevents.js script"]))

        # 3. JavaScript Frameworks
        js_frameworks = []
        if "__next_data__" in html_content or any("_next/static" in u for u in all_asset_urls):
            js_frameworks.append(DetectedTechnology(name="Next.js", category="JS Framework", confidence=1.0, evidence=["__NEXT_DATA__ DOM id"]))
        elif "react-dom" in html_content or any("react" in u for u in all_asset_urls):
            js_frameworks.append(DetectedTechnology(name="React", category="JS Framework", confidence=0.8, evidence=["react bundle link"]))

        if "__nuxt__" in html_content or any("_nuxt/" in u for u in all_asset_urls):
            js_frameworks.append(DetectedTechnology(name="Nuxt.js", category="JS Framework", confidence=1.0, evidence=["__NUXT__ DOM id"]))
        elif "vue.js" in html_content or "data-v-" in html_content:
            js_frameworks.append(DetectedTechnology(name="Vue.js", category="JS Framework", confidence=0.85, evidence=["Vue DOM data attribute"]))

        if "ng-version" in html_content or "ng-app" in html_content:
            js_frameworks.append(DetectedTechnology(name="Angular", category="JS Framework", confidence=0.9, evidence=["ng-version attribute"]))

        # 4. CSS Frameworks
        css_frameworks = []
        if any("bootstrap" in u for u in all_asset_urls) or "class=\"btn btn-" in html_content:
            css_frameworks.append(DetectedTechnology(name="Bootstrap", category="CSS Framework", confidence=0.85, evidence=["bootstrap CSS/JS asset"]))
        if any("tailwind" in u for u in all_asset_urls) or "tailwindcss" in html_content:
            css_frameworks.append(DetectedTechnology(name="Tailwind CSS", category="CSS Framework", confidence=0.85, evidence=["tailwind asset signature"]))

        # 5. Infrastructure / CDN
        infrastructure = []
        headers_lower = {k.lower(): v.lower() for k, v in headers.items()}
        if "cf-ray" in headers_lower or any("cloudflare" in u for u in all_asset_urls):
            infrastructure.append(DetectedTechnology(name="Cloudflare", category="CDN / Infrastructure", confidence=1.0, evidence=["cf-ray HTTP header"]))
        if "x-amz-cf-id" in headers_lower or any("cloudfront.net" in u for u in all_asset_urls):
            infrastructure.append(DetectedTechnology(name="Amazon CloudFront", category="CDN / Infrastructure", confidence=1.0, evidence=["CloudFront CDN signature"]))

        # 6. Marketing Platforms
        marketing = []
        if any("hs-scripts.com" in u or "hubspot.com" in u for u in all_asset_urls):
            marketing.append(DetectedTechnology(name="HubSpot", category="Marketing Automation", confidence=0.95, evidence=["HubSpot script loader"]))
        if any("chimpstatic.com" in u or "mc-validate.js" in u for u in all_asset_urls):
            marketing.append(DetectedTechnology(name="Mailchimp", category="Marketing Automation", confidence=0.9, evidence=["Mailchimp static script"]))

        # 7. Live Chat
        live_chat = []
        if any("intercom.io" in u or "custom.intercom.cdn" in u for u in all_asset_urls):
            live_chat.append(DetectedTechnology(name="Intercom", category="Live Chat", confidence=0.95, evidence=["Intercom widget URL"]))
        if any("crisp.chat" in u for u in all_asset_urls):
            live_chat.append(DetectedTechnology(name="Crisp", category="Live Chat", confidence=0.95, evidence=["Crisp chat script"]))
        if any("tidio.co" in u for u in all_asset_urls):
            live_chat.append(DetectedTechnology(name="Tidio", category="Live Chat", confidence=0.95, evidence=["Tidio live chat URL"]))

        # 8. CMS Detection
        cms_result = self.cms_detector.detect(doc, headers=headers)

        all_detected = analytics + advertising + js_frameworks + css_frameworks + infrastructure + marketing + live_chat
        for tech in all_detected:
            findings.append(f"Detected {tech.category}: {tech.name} (Confidence: {tech.confidence})")

        tech_stack = ExpandedTechStack(
            analytics=analytics,
            advertising=advertising,
            js_frameworks=js_frameworks,
            css_frameworks=css_frameworks,
            infrastructure=infrastructure,
            marketing_platforms=marketing,
            live_chat=live_chat,
            cms=cms_result
        )

        elapsed = round(time.perf_counter() - start_time, 4)

        return AnalyzerResult[ExpandedTechStack](
            analyzer_name="ExpandedTechDetector",
            analyzer_version="1.0.0",
            execution_time_seconds=elapsed,
            data=tech_stack,
            findings=findings,
            warnings=warnings,
            errors=errors
        )
