"""
Accessibility Intelligence Analyzer Module.
Audits missing image ALT text, missing form labels, html lang attributes, heading progression, iframe titles, button text, and generic anchor text.
"""

import time
from bs4 import Tag
from src.enrichment.models import AccessibilityIntelligence, AnalyzerResult
from src.enrichment.parser import HTMLParserDocument
from src.logging.logger import logger


class AccessibilityAnalyzer:
    """Audits DOM accessibility signals for compliance with WCAG basics."""

    GENERIC_ANCHOR_TEXTS = {"click here", "read more", "learn more", "link", "here", "more", "view"}

    def analyze(self, doc: HTMLParserDocument) -> AnalyzerResult[AccessibilityIntelligence]:
        """
        Runs DOM accessibility rules against parsed HTML document.
        """
        start_time = time.perf_counter()
        findings = []
        warnings = []
        errors = []

        penalty_points = 0.0

        # 1. Missing Language Declaration
        html_tag = doc.soup.find("html")
        has_lang = bool(isinstance(html_tag, Tag) and html_tag.get("lang"))
        missing_lang = not has_lang
        if missing_lang:
            warnings.append("Missing 'lang' attribute on <html> element.")
            penalty_points += 15.0

        # 2. Missing Image ALT Attributes
        images = doc.soup.find_all("img")
        missing_alt_count = 0
        for img in images:
            if isinstance(img, Tag):
                alt = img.get("alt")
                if alt is None or not str(alt).strip():
                    missing_alt_count += 1
        if missing_alt_count > 0:
            warnings.append(f"{missing_alt_count} image(s) are missing ALT description attributes.")
            penalty_points += min(missing_alt_count * 3.0, 25.0)

        # 3. Form Input Labels
        inputs = doc.soup.find_all(["input", "select", "textarea"])
        missing_labels_count = 0
        for inp in inputs:
            if isinstance(inp, Tag):
                inp_type = inp.get("type", "text")
                if inp_type in ("hidden", "submit", "button", "image"):
                    continue
                inp_id = inp.get("id")
                has_label = False
                if inp_id and doc.soup.find("label", attrs={"for": inp_id}):
                    has_label = True
                elif inp.find_parent("label"):
                    has_label = True
                elif inp.get("aria-label") or inp.get("aria-labelledby") or inp.get("placeholder"):
                    has_label = True

                if not has_label:
                    missing_labels_count += 1

        if missing_labels_count > 0:
            warnings.append(f"{missing_labels_count} form input field(s) lack accessible labels.")
            penalty_points += min(missing_labels_count * 5.0, 20.0)

        # 4. Heading Sequence Progression
        headings = doc.soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])
        heading_sequence_valid = True
        prev_level = 0
        for h in headings:
            if isinstance(h, Tag):
                level = int(h.name[1])
                if prev_level > 0 and level > prev_level + 1:
                    heading_sequence_valid = False
                    break
                prev_level = level

        if not heading_sequence_valid:
            warnings.append("Skipped heading levels detected (e.g. H1 followed directly by H3).")
            penalty_points += 10.0

        # 5. Unlabeled IFrames
        iframes = doc.soup.find_all("iframe")
        unlabeled_iframes = 0
        for iframe in iframes:
            if isinstance(iframe, Tag):
                if not iframe.get("title") and not iframe.get("aria-label"):
                    unlabeled_iframes += 1

        if unlabeled_iframes > 0:
            warnings.append(f"{unlabeled_iframes} iframe(s) missing descriptive 'title' attribute.")
            penalty_points += min(unlabeled_iframes * 5.0, 15.0)

        # 6. Unlabeled Buttons
        buttons = doc.soup.find_all("button")
        unlabeled_buttons = 0
        for btn in buttons:
            if isinstance(btn, Tag):
                txt = btn.get_text(strip=True)
                if not txt and not btn.get("aria-label") and not btn.find("img"):
                    unlabeled_buttons += 1

        if unlabeled_buttons > 0:
            warnings.append(f"{unlabeled_buttons} button(s) lack accessible text or aria-label.")
            penalty_points += min(unlabeled_buttons * 5.0, 15.0)

        # 7. Generic Anchor Text Quality
        links = doc.get_all_links()
        generic_anchors = 0
        for link in links:
            t = link["text"].strip().lower()
            if t in self.GENERIC_ANCHOR_TEXTS:
                generic_anchors += 1

        if generic_anchors > 0:
            warnings.append(f"{generic_anchors} link(s) use non-descriptive generic text (e.g. 'click here').")
            penalty_points += min(generic_anchors * 2.0, 10.0)

        score = max(0.0, round(100.0 - penalty_points, 1))
        if score >= 90.0:
            findings.append(f"Excellent DOM accessibility posture (Score: {score}/100).")

        access_data = AccessibilityIntelligence(
            missing_alt_count=missing_alt_count,
            missing_form_labels_count=missing_labels_count,
            missing_html_lang=missing_lang,
            heading_sequence_valid=heading_sequence_valid,
            unlabeled_iframes_count=unlabeled_iframes,
            unlabeled_buttons_count=unlabeled_buttons,
            generic_anchor_count=generic_anchors,
            accessibility_score=score
        )

        elapsed = round(time.perf_counter() - start_time, 4)

        return AnalyzerResult[AccessibilityIntelligence](
            analyzer_name="AccessibilityAnalyzer",
            analyzer_version="1.0.0",
            execution_time_seconds=elapsed,
            data=access_data,
            findings=findings,
            warnings=warnings,
            errors=errors
        )
