"""
Live Real-World Validation Script for Phase 04 — Decision Maker Discovery.
Fetches and evaluates live target company websites across 10 B2B industry verticals:
Roofing, HVAC, Plumbing, Movers, Landscaping, Law Firms, Dental Clinics, Marketing Agencies, SaaS, Manufacturing.
"""

import asyncio
import json
import time
from pathlib import Path

from src.enrichment.enrichment_pipeline import EnrichmentPipeline
from src.logging.logger import logger

# Real public target domain dataset across 10 industries (10 targets each = 100 domains)
TARGET_DOMAINS_BY_INDUSTRY = {
    "Roofing": [
        "australianroofing.com.au", "roofingpro.com.au", "monier.com.au", "stramit.com.au", "fielders.com.au",
        "metalroofing.com.au", "roofrestoration.com.au", "roofingservices.com.au", "roofworks.com.au", "toproofing.com.au"
    ],
    "HVAC": [
        "daikin.com.au", "fujitsugeneral.com.au", "actronair.com.au", "mitsubishielectric.com.au", "brivis.com.au",
        "seeleyinternational.com", "panasonic.com.au", "temperzone.com.au", "carrier.com.au", "toshiba-aircon.com.au"
    ],
    "Plumbing": [
        "reece.com.au", "tradelink.com.au", "metropolitanplumbing.com.au", "jimsplumbing.com.au", "same-day-plumbing.com.au",
        "plumbingsolutions.com.au", "cityplumbing.com.au", "expressplumbing.com.au", "proplumb.com.au", "masterplumbers.com.au"
    ],
    "Movers": [
        "alliedpickfords.com.au", "grace.com.au", "kentremovalsstorage.com.au", "taxibox.com.au", "chessremovals.com.au",
        "muval.com.au", "smartbox.com.au", "supermanwithavan.com.au", "wridgways.com.au", "crownrelo.com.au"
    ],
    "Landscaping": [
        "landscapingaustralia.com.au", "ecooutdoor.com.au", "secretgardens.com.au", "exquisitegardens.com.au", "flexigarden.com.au",
        "greenvision.com.au", "urbanlandscapes.com.au", "landscapedesign.com.au", "naturegardens.com.au", "heritagegardens.com.au"
    ],
    "Law Firms": [
        "minterellison.com", "kingandwoodmallesons.com", "allens.com.au", "herbertsmithfreehills.com", "ashurst.com",
        "claytonutz.com", "corrs.com.au", "gilberttobin.com.au", "piperalderman.com.au", "thomsongeer.com.au"
    ],
    "Dental Clinics": [
        "pacificsmilesdental.com.au", "nationaldentalcare.com.au", "primarydental.com.au", "bupadental.com.au", "mafdental.com.au",
        "smiledental.com.au", "citydental.com.au", "gentledental.com.au", "totaldental.com.au", "perfectsmile.com.au"
    ],
    "Marketing Agencies": [
        "wpp.com", "ogilvy.com", "clemenger.com.au", "monkeys.com.au", "chepnetwork.com.au",
        "thinkerbell.com.au", "dentsu.com.au", "publicis.groupe", "omnicomgroup.com", "havas.com.au"
    ],
    "SaaS": [
        "atlassian.com", "canva.com", "xero.com", "cultureamp.com", "employmenthero.com",
        "safetyculture.com", "envato.com", "skedulo.com", "siteminder.com", "campaignmonitor.com"
    ],
    "Manufacturing": [
        "bluescopesteel.com.au", "boral.com.au", "csr.com.au", "orora.com", "dulux.com.au",
        "visy.com.au", "jameshardie.com.au", "amcor.com", "incitecpivot.com.au", "brickworks.com.au"
    ]
}


async def validate_domain(pipeline: EnrichmentPipeline, domain: str, industry: str) -> dict:
    """Runs enrichment pipeline for a single target domain and records audit metrics."""
    start_time = time.perf_counter()
    try:
        report = await pipeline.enrich_domain(domain)
        duration = round(time.perf_counter() - start_time, 3)

        dm_report = getattr(report, "decision_maker_discovery", None)
        leadership_pages = len(dm_report.leadership_pages) if dm_report else 0
        decision_makers = len(dm_report.decision_makers) if dm_report else 0

        # Provenance source tracking
        fetch_source = "Live website" if report.fetch_result.is_success else "Live website (HTTP Error)"

        return {
            "domain": domain,
            "industry": industry,
            "fetch_status": report.fetch_result.status_code,
            "is_success": report.is_successful,
            "fetch_source": fetch_source,
            "leadership_pages_found": leadership_pages > 0,
            "leadership_pages_count": leadership_pages,
            "decision_makers_extracted": decision_makers,
            "top_person": dm_report.decision_makers[0].full_name if dm_report and dm_report.decision_makers else None,
            "top_title": dm_report.decision_makers[0].normalized_title if dm_report and dm_report.decision_makers else None,
            "top_priority": dm_report.decision_makers[0].priority if dm_report and dm_report.decision_makers else None,
            "top_confidence": dm_report.decision_makers[0].confidence if dm_report and dm_report.decision_makers else None,
            "duration_seconds": duration,
            "error": report.fetch_result.error
        }
    except Exception as err:
        duration = round(time.perf_counter() - start_time, 3)
        return {
            "domain": domain,
            "industry": industry,
            "fetch_status": 0,
            "is_success": False,
            "fetch_source": "Live website (Exception)",
            "leadership_pages_found": False,
            "leadership_pages_count": 0,
            "decision_makers_extracted": 0,
            "top_person": None,
            "top_title": None,
            "top_priority": None,
            "top_confidence": None,
            "duration_seconds": duration,
            "error": str(err)
        }


async def main():
    logger.info("Starting Phase 04 Live Real-World Validation across 100 target domains...")
    pipeline = EnrichmentPipeline()

    results = []
    total_domains = 0

    for industry, domains in TARGET_DOMAINS_BY_INDUSTRY.items():
        logger.info(f"\n--- Testing Industry Sector: {industry} ({len(domains)} targets) ---")
        for domain in domains:
            total_domains += 1
            res = await validate_domain(pipeline, domain, industry)
            results.append(res)

            status_str = f"HTTP {res['fetch_status']}" if res['is_success'] else "FETCH FAILED"
            logger.info(
                f"[{total_domains:03d}/100] {domain:32s} | {status_str:12s} | "
                f"Pages={res['leadership_pages_count']} | DMs={res['decision_makers_extracted']} | "
                f"Top='{res['top_person'] or 'N/A'}' ({res['top_title'] or 'N/A'}) in {res['duration_seconds']}s"
            )

    # Save summary report
    output_path = Path("logs/phase04_live_validation_results.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    logger.info(f"\nSaved live validation summary dataset to '{output_path}'")


if __name__ == "__main__":
    asyncio.run(main())
