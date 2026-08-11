"""
Multi-Heuristic CMS Detector Module.
Detects WordPress, Shopify, Wix, Squarespace, Webflow, Drupal, Joomla, Ghost, Magento, or Unknown.
"""

from bs4 import Tag
from src.enrichment.models import CMSDetectionResult, CMSType
from src.enrichment.parser import HTMLParserDocument

# Fingerprint patterns mapping CMS platforms to evidence rules
CMS_FINGERPRINTS = {
    CMSType.WORDPRESS: {
        "generator": ["wordpress"],
        "scripts": ["wp-content", "wp-includes", "wp-json"],
        "headers": ["wp-super-cache", "x-pingback"],
        "dom": ["body.wordpress", "link[rel*='wp-json']"],
    },
    CMSType.SHOPIFY: {
        "generator": ["shopify"],
        "scripts": ["cdn.shopify.com", "shopify.js"],
        "headers": ["x-shopify-stage"],
        "dom": ["content='shopify'"],
    },
    CMSType.WIX: {
        "generator": ["wix"],
        "scripts": ["static.wixstatic.com", "wix-parastorage.com"],
        "headers": ["x-wix-request-id"],
        "dom": ["meta[name='generator'][content*='wix']"],
    },
    CMSType.SQUARESPACE: {
        "generator": ["squarespace"],
        "scripts": ["static1.squarespace.com"],
        "headers": ["x-sqsp-site"],
        "dom": ["body.squarespace"],
    },
    CMSType.WEBFLOW: {
        "generator": ["webflow"],
        "scripts": ["uploads-ssl.webflow.com", "webflow.js"],
        "headers": ["x-webflow-site"],
        "dom": ["html[data-wf-page]"],
    },
    CMSType.DRUPAL: {
        "generator": ["drupal"],
        "scripts": ["sites/default/files", "drupal.js"],
        "headers": ["x-drupal-cache"],
        "dom": ["meta[name='generator'][content*='drupal']"],
    },
    CMSType.JOOMLA: {
        "generator": ["joomla"],
        "scripts": ["/media/system/js/", "joomla.js"],
        "headers": [],
        "dom": ["meta[name='generator'][content*='joomla']"],
    },
    CMSType.GHOST: {
        "generator": ["ghost"],
        "scripts": ["ghost.js"],
        "headers": ["x-ghost-cache"],
        "dom": ["meta[name='generator'][content*='ghost']"],
    },
    CMSType.MAGENTO: {
        "generator": ["magento"],
        "scripts": ["mage/cookies.js", "static/frontend/Magento"],
        "headers": [],
        "dom": ["script[src*='mage/']"],
    },
}


class CMSDetector:
    """Multi-heuristic detector evaluating HTML signatures, scripts, headers, and generator meta tags."""

    def detect(self, doc: HTMLParserDocument, headers: dict[str, str] | None = None) -> CMSDetectionResult:
        """
        Detects CMS platform from parsed HTML document and response headers.
        """
        resp_headers = {k.lower(): str(v).lower() for k, v in (headers or {}).items()}
        generator = (doc.get_meta_content("generator") or "").lower()

        scores: dict[CMSType, float] = {cms: 0.0 for cms in CMS_FINGERPRINTS}
        evidences: dict[CMSType, list[str]] = {cms: [] for cms in CMS_FINGERPRINTS}

        for cms, fp in CMS_FINGERPRINTS.items():
            # 1. Generator meta tag check (+0.6)
            if generator and any(g in generator for g in fp["generator"]):
                scores[cms] += 0.6
                evidences[cms].append(f"Meta generator: '{generator}'")

            # 2. Script tag & asset URL check (+0.4)
            for script in doc.soup.find_all(["script", "link"], src=True):
                src = str(script.get("src", "")).lower()
                if any(s in src for s in fp["scripts"]):
                    scores[cms] += 0.4
                    evidences[cms].append(f"Asset URL: '{src[:80]}'")
                    break

            for link in doc.soup.find_all("link", href=True):
                href = str(link.get("href", "")).lower()
                if any(s in href for s in fp["scripts"]):
                    scores[cms] += 0.4
                    evidences[cms].append(f"Link asset: '{href[:80]}'")
                    break

            # 3. HTTP Header check (+0.3)
            for hdr in fp["headers"]:
                if hdr in resp_headers:
                    scores[cms] += 0.3
                    evidences[cms].append(f"Header: '{hdr}'")

        best_cms = CMSType.UNKNOWN
        best_score = 0.0

        for cms, score in scores.items():
            if score > best_score:
                best_score = score
                best_cms = cms

        confidence = max(0.0, min(1.0, round(best_score, 2))) if best_score > 0.0 else 0.0

        return CMSDetectionResult(
            cms_name=best_cms if confidence >= 0.3 else CMSType.UNKNOWN,
            confidence=confidence if confidence >= 0.3 else 0.0,
            evidence=evidences[best_cms] if confidence >= 0.3 else []
        )
