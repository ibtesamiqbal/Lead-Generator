"""
Master AI Insights Engine Orchestrator (Phase 07).
Coordinates executive summary, digital maturity scoring, strengths/weaknesses,
opportunities, recommended services, outreach strategy, and risk assessment.
"""

import time
from src.ai_insights.digital_maturity import DigitalMaturityAnalyzer
from src.ai_insights.executive_summary import ExecutiveSummaryGenerator
from src.ai_insights.models import AIInsightsReport
from src.ai_insights.opportunities import OpportunityAnalyzer
from src.ai_insights.outreach import OutreachStrategyGenerator
from src.ai_insights.recommendations import ServiceRecommendationEngine
from src.ai_insights.risks import RiskAssessmentAnalyzer
from src.ai_insights.strengths import StrengthsWeaknessesAnalyzer
from src.ai_insights.validators import InsightValidator
from src.enrichment.models import CompanyEnrichmentReport
from src.logging.logger import logger


class AIInsightsEngine:
    """Orchestrates end-to-end AI Insights & Opportunity Analysis for Phase 07."""

    def __init__(self):
        self.summary_gen = ExecutiveSummaryGenerator()
        self.maturity_analyzer = DigitalMaturityAnalyzer()
        self.sw_analyzer = StrengthsWeaknessesAnalyzer()
        self.opp_analyzer = OpportunityAnalyzer()
        self.service_engine = ServiceRecommendationEngine()
        self.outreach_gen = OutreachStrategyGenerator()
        self.risk_analyzer = RiskAssessmentAnalyzer()

    async def analyze(self, report: CompanyEnrichmentReport) -> AIInsightsReport:
        """
        Synthesizes AIInsightsReport consuming only structured outputs from Phases 01-06.
        """
        start_time = time.perf_counter()
        notes = []

        # 1. Executive Summary
        exec_summary = self.summary_gen.generate_summary(report)

        # 2. Overall Digital Maturity
        digital_maturity = self.maturity_analyzer.calculate_overall_maturity(report)

        # 3. Strengths & Weaknesses
        strengths, weaknesses = self.sw_analyzer.analyze_strengths_and_weaknesses(report)

        # 4. Opportunities Breakdown
        opportunities = self.opp_analyzer.analyze_opportunities(report)

        # 5. Service Recommendations
        recommended_services = self.service_engine.generate_recommendations(report)

        # 6. Outreach Strategy
        outreach_strategy = self.outreach_gen.generate_strategy(report)

        # 7. Risk Assessment
        risks = self.risk_analyzer.assess_risks(report)

        # 8. Composite Confidence
        active_signal_count = sum(1 for x in [
            report.fetch_result, report.metadata, report.seo,
            report.contact_discovery, report.decision_maker_discovery,
            report.business_intelligence, report.marketing_intelligence
        ] if x is not None)
        confidence = InsightValidator.calculate_confidence(active_signal_count)

        report_out = AIInsightsReport(
            domain=report.domain,
            executive_summary=exec_summary,
            digital_maturity=digital_maturity,
            strengths=strengths,
            weaknesses=weaknesses,
            opportunities=opportunities,
            recommended_services=recommended_services,
            outreach_strategy=outreach_strategy,
            risks=risks,
            confidence=confidence,
            is_successful=True,
            notes=notes
        )

        elapsed = round(time.perf_counter() - start_time, 4)
        logger.info(f"Completed AI Insights analysis for '{report.domain}': Maturity={digital_maturity.level.value} ({digital_maturity.score}/100), Recs={len(recommended_services)} in {elapsed}s")
        return report_out
