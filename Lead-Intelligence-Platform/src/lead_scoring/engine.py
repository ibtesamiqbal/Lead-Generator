"""
Master Lead Scoring Engine Orchestrator (Phase 08).
Coordinates zero-crawl, sub-millisecond, deterministic lead scoring & prioritization.
"""

import time
from src.enrichment.models import CompanyEnrichmentReport
from src.lead_scoring.config import ScoringWeightsConfig
from src.lead_scoring.models import LeadScoringReport
from src.lead_scoring.scoring_engine import ScoringEngine
from src.logging.logger import logger


class LeadScoringEngine:
    """Orchestrates end-to-end Lead Scoring & Prioritization for Phase 08."""

    def __init__(self, config: ScoringWeightsConfig | None = None):
        self.scoring_engine = ScoringEngine(config=config)

    async def analyze(self, report: CompanyEnrichmentReport) -> LeadScoringReport:
        """
        Synthesizes LeadScoringReport consuming structured outputs from Phases 01-07.
        """
        start_time = time.perf_counter()

        scoring_report = self.scoring_engine.score_report(report)

        elapsed = round(time.perf_counter() - start_time, 4)
        logger.info(
            f"Completed Lead Scoring analysis for '{report.domain}': "
            f"Score={scoring_report.overall_score}/100, Grade={scoring_report.grade.value}, "
            f"Priority={scoring_report.priority.value} in {elapsed}s"
        )

        return scoring_report
