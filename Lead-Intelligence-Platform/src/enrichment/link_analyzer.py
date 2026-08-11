"""
Link Intelligence Analyzer Module.
Audits document link distribution (internal vs external), duplicate links, anchor text diversity, and malformed URL candidate issues.
"""

import time
from urllib.parse import urlparse
from src.enrichment.models import AnalyzerResult, LinkIntelligence
from src.enrichment.parser import HTMLParserDocument
from src.logging.logger import logger


class LinkAnalyzer:
    """Evaluates link structure, internal/external categorization, anchor diversity, and malformed URL detection."""

    def analyze(self, doc: HTMLParserDocument, base_url: str = "") -> AnalyzerResult[LinkIntelligence]:
        """
        Runs link distribution and anchor analysis on parsed document.
        """
        start_time = time.perf_counter()
        findings = []
        warnings = []
        errors = []

        all_links = doc.get_all_links()
        total_count = len(all_links)

        internal_links = set()
        external_links = set()
        seen_hrefs = set()
        duplicate_count = 0
        anchor_texts = []
        candidate_broken = set()

        base_domain = ""
        if base_url:
            base_domain = urlparse(base_url).netloc.lower()

        for link in all_links:
            href = link["href"].strip()
            text = link["text"].strip()

            if text:
                anchor_texts.append(text.lower())

            # Check duplicate URLs
            if href in seen_hrefs:
                duplicate_count += 1
            seen_hrefs.add(href)

            # Check malformed link candidates
            if not href or href in ("#", "javascript:void(0)", "javascript:;") or href.startswith("http:///"):
                candidate_broken.add(href or "[empty href]")

            if href.startswith(("http://", "https://")):
                netloc = urlparse(href).netloc.lower()
                if base_domain and base_domain in netloc:
                    internal_links.add(href)
                else:
                    external_links.add(href)
            elif href.startswith(("/", ".")):
                internal_links.add(href)

        unique_anchors = len(set(anchor_texts))
        diversity_score = round(unique_anchors / len(anchor_texts), 2) if anchor_texts else 1.0

        if total_count == 0:
            warnings.append("No hyperlinks detected on target document.")
        else:
            findings.append(f"Discovered {total_count} total hyperlinks ({len(internal_links)} internal, {len(external_links)} external).")

        if duplicate_count > 5:
            warnings.append(f"High duplicate hyperlink target count ({duplicate_count} duplicates).")

        if candidate_broken:
            warnings.append(f"Discovered {len(candidate_broken)} candidate malformed or placeholder URL(s).")

        link_data = LinkIntelligence(
            total_links=total_count,
            internal_links=sorted(list(internal_links)),
            external_links=sorted(list(external_links)),
            duplicate_links_count=duplicate_count,
            anchor_diversity_score=diversity_score,
            candidate_broken_links=sorted(list(candidate_broken))
        )

        elapsed = round(time.perf_counter() - start_time, 4)

        return AnalyzerResult[LinkIntelligence](
            analyzer_name="LinkAnalyzer",
            analyzer_version="1.0.0",
            execution_time_seconds=elapsed,
            data=link_data,
            findings=findings,
            warnings=warnings,
            errors=errors
        )
