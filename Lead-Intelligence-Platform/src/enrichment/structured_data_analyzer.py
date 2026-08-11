"""
Structured Data & Schema.org Analyzer Module.
Detects JSON-LD, Microdata, and RDFa structured data payloads and schema types.
"""

import json
import time
from bs4 import Tag
from src.enrichment.models import AnalyzerResult, StructuredDataResult
from src.enrichment.parser import HTMLParserDocument
from src.logging.logger import logger


class StructuredDataAnalyzer:
    """Detects and parses JSON-LD, Microdata, and RDFa schema.org markup."""

    KNOWN_SCHEMA_TYPES = {
        "Organization", "LocalBusiness", "WebSite", "Article",
        "Product", "FAQPage", "BreadcrumbList", "RoofingContractor",
        "MovingCompany", "Service", "PostalAddress", "ContactPoint"
    }

    def analyze(self, doc: HTMLParserDocument) -> AnalyzerResult[StructuredDataResult]:
        """
        Extracts structured data formats and schema.org type declarations.
        """
        start_time = time.perf_counter()
        findings = []
        warnings = []
        errors = []

        detected_formats = set()
        detected_types = set()
        item_count = 0

        # 1. JSON-LD Extraction
        json_ld_scripts = doc.soup.find_all("script", attrs={"type": "application/ld+json"})
        if json_ld_scripts:
            detected_formats.add("JSON-LD")
            for script in json_ld_scripts:
                if isinstance(script, Tag) and script.string:
                    raw_json = script.string.strip()
                    if not raw_json:
                        continue
                    try:
                        data = json.loads(raw_json)
                        item_count += 1
                        self._extract_schema_types(data, detected_types)
                    except json.JSONDecodeError as err:
                        errors.append(f"Malformed JSON-LD payload: {err}")

        # 2. Microdata Extraction
        microdata_items = doc.soup.find_all(attrs={"itemscope": True})
        if microdata_items:
            detected_formats.add("Microdata")
            for item in microdata_items:
                if isinstance(item, Tag):
                    itemtype = item.get("itemtype")
                    if itemtype:
                        type_str = str(itemtype).split("/")[-1]
                        detected_types.add(type_str)
                        item_count += 1

        # 3. RDFa Extraction
        rdfa_items = doc.soup.find_all(attrs={"typeof": True})
        if rdfa_items:
            detected_formats.add("RDFa")
            for item in rdfa_items:
                if isinstance(item, Tag):
                    typeof_val = item.get("typeof")
                    if typeof_val:
                        type_str = str(typeof_val).split(":")[-1]
                        detected_types.add(type_str)
                        item_count += 1

        is_valid = len(errors) == 0 and item_count > 0

        if item_count == 0:
            warnings.append("No structured data (JSON-LD, Microdata, or RDFa) detected.")
        else:
            findings.append(f"Detected {item_count} structured data items across formats: {', '.join(detected_formats)}.")

        matched_known = detected_types.intersection(self.KNOWN_SCHEMA_TYPES)
        if matched_known:
            findings.append(f"Recognized Schema.org types: {', '.join(sorted(list(matched_known)))}.")

        result_data = StructuredDataResult(
            detected_formats=sorted(list(detected_formats)),
            detected_schema_types=sorted(list(detected_types)),
            is_valid=is_valid,
            item_count=item_count
        )

        elapsed = round(time.perf_counter() - start_time, 4)

        return AnalyzerResult[StructuredDataResult](
            analyzer_name="StructuredDataAnalyzer",
            analyzer_version="1.0.0",
            execution_time_seconds=elapsed,
            data=result_data,
            findings=findings,
            warnings=warnings,
            errors=errors
        )

    def _extract_schema_types(self, data: object, type_set: set[str]):
        """Recursively parses JSON-LD object structures for @type fields."""
        if isinstance(data, dict):
            if "@type" in data:
                val = data["@type"]
                if isinstance(val, str):
                    type_set.add(val)
                elif isinstance(val, list):
                    for item in val:
                        if isinstance(item, str):
                            type_set.add(item)
            for v in data.values():
                self._extract_schema_types(v, type_set)
        elif isinstance(data, list):
            for elem in data:
                self._extract_schema_types(elem, type_set)
