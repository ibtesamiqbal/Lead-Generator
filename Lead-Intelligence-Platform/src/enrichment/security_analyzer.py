"""
Passive Security Header Analyzer Module.
Passively inspects HTTP response security headers (HSTS, CSP, X-Frame-Options, X-Content-Type-Options, Referrer-Policy, Permissions-Policy).
"""

import time
from src.enrichment.fetcher import FetchResult
from src.enrichment.models import AnalyzerResult, PassiveSecurityHeaders
from src.logging.logger import logger


class PassiveSecurityAnalyzer:
    """Audits HTTP security response headers passively without active network vulnerability probing."""

    def analyze(self, fetch_result: FetchResult) -> AnalyzerResult[PassiveSecurityHeaders]:
        """
        Passively inspects HTTP response headers for essential security controls.
        """
        start_time = time.perf_counter()
        findings = []
        warnings = []
        errors = []

        headers = {k.lower(): v for k, v in fetch_result.headers.items()}
        score = 0.0

        # 1. HSTS
        hsts_val = headers.get("strict-transport-security")
        has_hsts = bool(hsts_val)
        if has_hsts:
            score += 25.0
            findings.append("Strict-Transport-Security (HSTS) header present.")
        else:
            warnings.append("Missing Strict-Transport-Security (HSTS) header.")

        # 2. CSP
        csp_val = headers.get("content-security-policy")
        has_csp = bool(csp_val)
        if has_csp:
            score += 25.0
            findings.append("Content-Security-Policy (CSP) header present.")
        else:
            warnings.append("Missing Content-Security-Policy (CSP) header.")

        # 3. X-Frame-Options
        xfo_val = headers.get("x-frame-options")
        has_xfo = bool(xfo_val)
        if has_xfo:
            score += 15.0
            findings.append("X-Frame-Options header present (Clickjacking protection).")
        else:
            warnings.append("Missing X-Frame-Options header.")

        # 4. X-Content-Type-Options
        xcto_val = headers.get("x-content-type-options")
        has_xcto = bool(xcto_val and "nosniff" in xcto_val.lower())
        if has_xcto:
            score += 15.0
            findings.append("X-Content-Type-Options: nosniff present.")
        else:
            warnings.append("Missing X-Content-Type-Options: nosniff header.")

        # 5. Referrer-Policy
        ref_val = headers.get("referrer-policy")
        has_ref = bool(ref_val)
        if has_ref:
            score += 10.0
            findings.append("Referrer-Policy header present.")
        else:
            warnings.append("Missing Referrer-Policy header.")

        # 6. Permissions-Policy
        perm_val = headers.get("permissions-policy") or headers.get("feature-policy")
        has_perm = bool(perm_val)
        if has_perm:
            score += 10.0
            findings.append("Permissions-Policy header present.")

        security_data = PassiveSecurityHeaders(
            has_strict_transport_security=has_hsts,
            hsts_value=hsts_val,
            has_content_security_policy=has_csp,
            csp_value=csp_val,
            has_x_frame_options=has_xfo,
            x_frame_options_value=xfo_val,
            has_x_content_type_options=has_xcto,
            has_referrer_policy=has_ref,
            has_permissions_policy=has_perm,
            security_score=round(score, 1)
        )

        elapsed = round(time.perf_counter() - start_time, 4)

        return AnalyzerResult[PassiveSecurityHeaders](
            analyzer_name="PassiveSecurityAnalyzer",
            analyzer_version="1.0.0",
            execution_time_seconds=elapsed,
            data=security_data,
            findings=findings,
            warnings=warnings,
            errors=errors
        )
