"""
Content Intelligence Analyzer (Phase 06).
Detects blog sections, case studies, whitepapers, guides, videos, FAQs, and content freshness.
"""

import re
from urllib.parse import urljoin
from src.enrichment.parser import HTMLParserDocument
from src.marketing_intelligence.models import ContentIntelligence


class ContentIntelligenceAnalyzer:
    """Detects content assets, resource centers, blog freshness, and video assets."""

    def analyze_content(self, doc: HTMLParserDocument | None, base_url: str = "") -> ContentIntelligence:
        """
        Returns populated ContentIntelligence model.
        """
        content = ContentIntelligence()
        if not doc or not doc.soup:
            return content

        soup = doc.soup
        text = soup.get_text(separator=" ").lower()
        resources: set[str] = set()

        # 1. Blog Detection
        blog_link = soup.find("a", href=re.compile(r"/blog|/news|/articles|/insights|/journal", re.IGNORECASE))
        if blog_link:
            content.has_blog = True
            href = blog_link.get("href")
            if href and isinstance(href, str):
                content.blog_url = urljoin(base_url, href)

        # 2. Resource Assets Detection
        if any(kw in text for kw in ["case study", "case studies", "customer stories"]):
            content.has_case_studies = True
            resources.add("Case Studies")

        if any(kw in text for kw in ["whitepaper", "white paper", "ebook", "e-book", "reports"]):
            content.has_whitepapers = True
            resources.add("Whitepapers & Ebooks")

        if any(kw in text for kw in ["guide", "guides", "checklist", "playbook", "documentation"]):
            content.has_guides = True
            resources.add("Guides & Documentation")

        if any(kw in text for kw in ["faq", "frequently asked questions", "q&a"]):
            content.has_faqs = True
            resources.add("FAQs")

        # 3. Video Assets
        video_tags = soup.find_all(["video", "iframe"])
        for v in video_tags:
            src = (v.get("src") or "").lower()
            if "youtube" in src or "vimeo" in src or "wistia" in src or "loom" in src:
                content.has_video_content = True
                resources.add("Video Assets")
                break

        content.resources_detected = sorted(list(resources))
        content.content_freshness_rating = "Fresh (Active Content)" if (content.has_blog or content.has_case_studies) else "Static Content"
        return content
