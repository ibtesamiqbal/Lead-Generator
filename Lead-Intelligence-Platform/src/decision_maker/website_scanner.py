"""
Leadership & Team Webpage Discovery Scanner (Phase 04).
Discovers dedicated leadership, executive, team, about, and staff pages on company websites.
Implements relevance scoring and strict path exclusion filtering.
"""

import re
from urllib.parse import urljoin, urlparse
from src.decision_maker.models import LeadershipPage
from src.decision_maker.validators import DecisionMakerValidator
from src.enrichment.parser import HTMLParserDocument


class LeadershipPageScanner:
    """Scans DOM, menus, footers, internal links, and sitemaps to locate leadership pages."""

    # High-priority exact leadership path tokens
    HIGH_PRIORITY_PATH_TOKENS = [
        "about", "about-us", "leadership", "executives", "management",
        "our-team", "team", "people", "our-people", "staff", "our-staff",
        "board", "company", "company/about", "who-we-are", "attorneys", "doctors", "founders"
    ]

    # Priority anchor text keywords
    TARGET_ANCHOR_KEYWORDS = [
        "leadership", "executive", "management", "team", "staff", "people",
        "board", "founders", "attorneys", "lawyers", "doctors", "about us", "who we are"
    ]

    # Strict exclusions: product, marketing, playbook, docs, software, and tool sub-paths
    EXCLUDED_PATH_KEYWORDS = [
        "project", "projects", "product", "products", "playbook", "docs", "documentation",
        "pricing", "features", "blog", "article", "academy", "learn", "support", "help",
        "solutions", "resources", "templates", "guides", "webinars", "case-studies",
        "collections", "work-management", "task-management", "time-tracking", "collaboration",
        "software", "integration", "integrations", "community", "forum", "downloads", "app"
    ]

    def find_leadership_pages(
        self,
        doc: HTMLParserDocument,
        base_url: str,
        sitemap_urls: list[str] | None = None
    ) -> list[LeadershipPage]:
        """
        Discovers and ranks candidate leadership/team page URLs from webpage DOM and sitemap.
        Filters out low-relevance non-leadership pages (< 0.65 confidence).
        """
        discovered_pages: dict[str, LeadershipPage] = {}
        if not doc or not doc.soup:
            return []

        parsed_base = urlparse(base_url)
        base_domain = parsed_base.netloc.lower()

        # 1. Inspect Navigation Menus and Header Links
        nav_links = doc.soup.select("nav a[href], header a[href]") if doc.soup else []
        for a in nav_links:
            href = a.get("href")
            text = a.get_text(strip=True)
            page = self._evaluate_candidate_link(href, text, base_url, base_domain, source="Navigation Menu")
            if page and page.confidence >= 0.65:
                discovered_pages[page.url] = page

        # 2. Inspect Footer Links
        footer_links = doc.soup.select("footer a[href]") if doc.soup else []
        for a in footer_links:
            href = a.get("href")
            text = a.get_text(strip=True)
            page = self._evaluate_candidate_link(href, text, base_url, base_domain, source="Footer Link")
            if page and page.confidence >= 0.65 and page.url not in discovered_pages:
                discovered_pages[page.url] = page

        # 3. Inspect All Internal Links in Document
        all_links = doc.soup.find_all("a", href=True) if doc.soup else []
        for a in all_links:
            href = a.get("href")
            text = a.get_text(strip=True)
            page = self._evaluate_candidate_link(href, text, base_url, base_domain, source="Internal Link")
            if page and page.confidence >= 0.65 and page.url not in discovered_pages:
                discovered_pages[page.url] = page

        # 4. Inspect Sitemap URLs if provided
        if sitemap_urls:
            for s_url in sitemap_urls:
                page = self._evaluate_candidate_link(s_url, "", base_url, base_domain, source="Sitemap XML")
                if page and page.confidence >= 0.65 and page.url not in discovered_pages:
                    discovered_pages[page.url] = page

        # Sort pages by confidence score descending
        sorted_pages = sorted(discovered_pages.values(), key=lambda p: p.confidence, reverse=True)
        return sorted_pages[:5]

    def _evaluate_candidate_link(
        self,
        href: str | None,
        anchor_text: str,
        base_url: str,
        base_domain: str,
        source: str
    ) -> LeadershipPage | None:
        """Evaluates if a link is a candidate leadership/team page URL and calculates relevance score."""
        if not href or not isinstance(href, str) or href.startswith(("javascript:", "mailto:", "tel:", "#")):
            return None

        abs_url = urljoin(base_url, href)
        if not DecisionMakerValidator.is_safe_url(abs_url):
            return None

        parsed = urlparse(abs_url)

        # Must match base domain and be an HTML page (not static image/asset)
        if parsed.netloc.lower() != base_domain:
            return None

        if parsed.path.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".pdf", ".css", ".js", ".zip", ".ico", ".xml")):
            return None

        path_lower = parsed.path.lower().rstrip("/")
        anchor_lower = anchor_text.lower() if isinstance(anchor_text, str) else ""

        # Reject if path contains any excluded non-leadership terms
        for exc in self.EXCLUDED_PATH_KEYWORDS:
            if re.search(rf"\b{exc}\b|/{exc}", path_lower):
                return None

        # Check path keyword match and anchor text match
        path_matched = any(re.search(rf"/{kw}$|/{kw}/", path_lower) or path_lower.endswith(kw) for kw in self.HIGH_PRIORITY_PATH_TOKENS)
        anchor_matched = any(kw in anchor_lower for kw in self.TARGET_ANCHOR_KEYWORDS)

        if not (path_matched or anchor_matched):
            return None

        # Relevance scoring algorithm
        confidence = 0.40
        if anchor_matched:
            if any(term in anchor_lower for term in ["leadership", "team", "executive", "management", "about", "people", "staff", "attorney", "doctor"]):
                confidence += 0.30
        if path_matched:
            if any(term in path_lower for term in ["leadership", "team", "executive", "management", "about", "people", "staff", "attorney", "doctor"]):
                confidence += 0.25

        if source in ("Navigation Menu", "Footer Link"):
            confidence += 0.10

        confidence = round(min(1.0, confidence), 2)

        return LeadershipPage(
            url=abs_url,
            title=anchor_text if anchor_text else path_lower,
            confidence=confidence,
            source=source
        )
