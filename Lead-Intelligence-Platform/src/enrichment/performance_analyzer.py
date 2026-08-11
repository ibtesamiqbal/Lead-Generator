"""
Performance Intelligence Analyzer Module.
Audits response latency, page size, compression headers, caching, and DOM asset resource counts without browser automation.
"""

import time
from bs4 import Tag
from src.enrichment.fetcher import FetchResult
from src.enrichment.models import AnalyzerResult, PerformanceIntelligence
from src.enrichment.parser import HTMLParserDocument
from src.logging.logger import logger


class PerformanceAnalyzer:
    """Evaluates non-browser network performance and page weight metrics."""

    def analyze(self, fetch_result: FetchResult, doc: HTMLParserDocument) -> AnalyzerResult[PerformanceIntelligence]:
        """
        Executes performance evaluation using response metadata and parsed DOM.
        """
        start_time = time.perf_counter()
        findings = []
        warnings = []
        errors = []

        headers_lower = {k.lower(): v for k, v in fetch_result.headers.items()}

        # 1. Latency & Size
        resp_ms = round(fetch_result.response_time_ms, 2)
        page_bytes = len(fetch_result.content.encode("utf-8"))

        if resp_ms > 2000:
            warnings.append(f"High server response latency: {resp_ms} ms.")
        else:
            findings.append(f"Server response time: {resp_ms} ms.")

        if page_bytes > 3_000_000:  # 3 MB
            warnings.append(f"Large HTML document size: {round(page_bytes / 1024 / 1024, 2)} MB.")

        # 2. Compression & Caching Headers
        content_encoding = headers_lower.get("content-encoding", "").lower()
        compression_supported = []
        if "gzip" in content_encoding:
            compression_supported.append("gzip")
        if "br" in content_encoding:
            compression_supported.append("br")
        if "deflate" in content_encoding:
            compression_supported.append("deflate")

        if not compression_supported:
            warnings.append("HTTP response is uncompressed (missing gzip/brotli content-encoding).")
        else:
            findings.append(f"Compression enabled: {', '.join(compression_supported)}.")

        cache_control = headers_lower.get("cache-control")
        expires = headers_lower.get("expires")

        if not cache_control:
            warnings.append("Missing 'Cache-Control' HTTP response header.")

        # 3. DOM Asset Resource Counts
        js_scripts = [s for s in doc.soup.find_all("script") if isinstance(s, Tag) and s.get("src")]
        css_links = [l for l in doc.soup.find_all("link") if isinstance(l, Tag) and l.get("rel") and "stylesheet" in l.get("rel")]
        images = doc.soup.find_all("img")

        js_count = len(js_scripts)
        css_count = len(css_links)
        img_count = len(images)
        total_resources = js_count + css_count + img_count

        if js_count > 20:
            warnings.append(f"High external JavaScript file count ({js_count} scripts).")
        if css_count > 10:
            warnings.append(f"High CSS stylesheet count ({css_count} files).")

        perf_data = PerformanceIntelligence(
            response_time_ms=resp_ms,
            redirect_chain=[fetch_result.url],
            redirect_count=0,
            http_version="HTTP/1.1",
            page_size_bytes=page_bytes,
            compression_supported=compression_supported,
            cache_control=cache_control,
            expires=expires,
            js_resource_count=js_count,
            css_resource_count=css_count,
            image_resource_count=img_count,
            total_resource_count=total_resources
        )

        elapsed = round(time.perf_counter() - start_time, 4)

        return AnalyzerResult[PerformanceIntelligence](
            analyzer_name="PerformanceAnalyzer",
            analyzer_version="1.0.0",
            execution_time_seconds=elapsed,
            data=perf_data,
            findings=findings,
            warnings=warnings,
            errors=errors
        )
