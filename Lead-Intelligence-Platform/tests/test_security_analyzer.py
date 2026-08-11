"""
Unit Tests for PassiveSecurityAnalyzer.
"""

from src.enrichment.fetcher import FetchResult
from src.enrichment.security_analyzer import PassiveSecurityAnalyzer


def test_passive_security_analyzer():
    """Verify inspection of HTTP response security headers."""
    fetch_res = FetchResult(
        url="https://example.com",
        status_code=200,
        content="",
        headers={
            "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
            "Content-Security-Policy": "default-src 'self'",
            "X-Frame-Options": "SAMEORIGIN",
            "X-Content-Type-Options": "nosniff",
            "Referrer-Policy": "strict-origin-when-cross-origin"
        },
        is_success=True
    )
    analyzer = PassiveSecurityAnalyzer()
    res = analyzer.analyze(fetch_res)

    assert res.data.has_strict_transport_security is True
    assert res.data.has_content_security_policy is True
    assert res.data.has_x_frame_options is True
    assert res.data.has_x_content_type_options is True
    assert res.data.has_referrer_policy is True
    assert res.data.security_score == 90.0
