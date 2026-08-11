"""
SEO Intelligence Analyzer Module.
Audits title/description quality, heading hierarchy, indexing directives, OpenGraph, ALT coverage, and link counts.
"""

import time
from bs4 import Tag
from src.enrichment.models import AnalyzerResult, SEOIntelligence
from src.enrichment.parser import HTMLParserDocument
from src.logging.logger import logger


class SEOAnalyzer:
    """Evaluates technical on-page SEO signals and indexing directives."""

    def analyze(self, doc: HTMLParserDocument, base_url: str = "") -> AnalyzerResult[SEOIntelligence]:
        """
        Executes on-page SEO analysis on the parsed document.
        """
        start_time = time.perf_counter()
        findings = []
        warnings = []
        errors = []

        # 1. Title Tag Audit
        title = doc.get_title() or ""
        title_len = len(title)
        is_title_optimal = 30 <= title_len <= 60
        if not title:
            warnings.append("Missing <title> tag.")
        elif not is_title_optimal:
            warnings.append(f"Title length ({title_len} chars) is outside optimal 30-60 char range.")
        else:
            findings.append(f"Title tag is optimal ({title_len} chars).")

        # 2. Meta Description Audit
        desc = doc.get_meta_content("description") or ""
        desc_len = len(desc)
        is_desc_optimal = 120 <= desc_len <= 160
        if not desc:
            warnings.append("Missing meta description tag.")
        elif not is_desc_optimal:
            warnings.append(f"Meta description length ({desc_len} chars) is outside optimal 120-160 char range.")
        else:
            findings.append(f"Meta description is optimal ({desc_len} chars).")

        # 3. Meta Keywords
        keywords_str = doc.get_meta_content("keywords")
        has_keywords = bool(keywords_str and keywords_str.strip())

        # 4. Heading Hierarchy Audit
        h1_tags = doc.get_headings("h1")
        h2_tags = doc.get_headings("h2")
        h1_count = len(h1_tags)
        h2_count = len(h2_tags)
        heading_valid = (h1_count == 1)

        if h1_count == 0:
            warnings.append("Missing H1 tag.")
        elif h1_count > 1:
            warnings.append(f"Multiple H1 tags detected ({h1_count}). Best practice is exactly 1 H1 tag.")
        else:
            findings.append("Single H1 tag detected.")

        # 5. Indexing & Follow Directives
        robots_meta = (doc.get_meta_content("robots") or "").lower()
        is_indexable = "noindex" not in robots_meta
        is_followable = "nofollow" not in robots_meta

        if not is_indexable:
            warnings.append("Page has 'noindex' meta directive restricting search engine indexing.")
        if not is_followable:
            warnings.append("Page has 'nofollow' meta directive restricting link equity flow.")

        # 6. OpenGraph & Twitter Card Completeness
        og_title = doc.get_meta_content("og:title")
        og_image = doc.get_meta_content("og:image")
        og_complete = bool(og_title and og_image)
        if not og_complete:
            warnings.append("Incomplete OpenGraph tags (missing og:title or og:image).")
        else:
            findings.append("Open Graph social tags complete.")

        twitter_card = doc.get_meta_content("twitter:card")
        twitter_complete = bool(twitter_card)

        # 7. Canonical URL Validation
        canonical_tag = doc.soup.find("link", attrs={"rel": "canonical"})
        canonical_valid = bool(isinstance(canonical_tag, Tag) and canonical_tag.get("href"))
        if not canonical_valid:
            warnings.append("Missing rel='canonical' link tag.")

        # 8. Image ALT Attribute Coverage
        images = doc.soup.find_all("img")
        total_imgs = len(images)
        missing_alt = 0
        for img in images:
            if isinstance(img, Tag):
                alt = img.get("alt")
                if alt is None or not str(alt).strip():
                    missing_alt += 1

        alt_coverage = round((total_imgs - missing_alt) / total_imgs, 2) if total_imgs > 0 else 1.0
        if missing_alt > 0:
            warnings.append(f"{missing_alt}/{total_imgs} images are missing ALT descriptive attributes.")

        # 9. Link Distribution
        links = doc.get_all_links()
        internal_count = 0
        external_count = 0

        for link in links:
            href = link["href"].lower()
            if href.startswith(("http://", "https://")):
                if base_url and base_url.lower() in href:
                    internal_count += 1
                else:
                    external_count += 1
            elif href.startswith(("/", "#", ".")):
                internal_count += 1

        seo_data = SEOIntelligence(
            title_length=title_len,
            is_title_optimal=is_title_optimal,
            meta_description_length=desc_len,
            is_meta_description_optimal=is_desc_optimal,
            has_meta_keywords=has_keywords,
            heading_structure_valid=heading_valid,
            h1_count=h1_count,
            h2_count=h2_count,
            canonical_url_valid=canonical_valid,
            is_indexable=is_indexable,
            is_followable=is_followable,
            open_graph_complete=og_complete,
            twitter_card_complete=twitter_complete,
            image_alt_coverage_ratio=alt_coverage,
            total_images=total_imgs,
            missing_alt_images=missing_alt,
            internal_links_count=internal_count,
            external_links_count=external_count,
            has_duplicate_metadata=False
        )

        elapsed = round(time.perf_counter() - start_time, 4)

        return AnalyzerResult[SEOIntelligence](
            analyzer_name="SEOAnalyzer",
            analyzer_version="1.0.0",
            execution_time_seconds=elapsed,
            data=seo_data,
            findings=findings,
            warnings=warnings,
            errors=errors
        )
