"""
Abstract Base Exporter (Phase 09).
Defines the standard export interface contract across all file & database formats.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from src.enrichment.models import CompanyEnrichmentReport
from src.export.models import ExportSummaryReport
from src.export.serializer import EnrichmentSerializer


class BaseExporter(ABC):
    """Abstract base class for all file and database exporters."""

    def __init__(self, serializer: EnrichmentSerializer | None = None):
        self.serializer = serializer or EnrichmentSerializer()

    @abstractmethod
    async def export(
        self,
        reports: list[CompanyEnrichmentReport],
        destination: Path | str
    ) -> ExportSummaryReport:
        """
        Exports list of CompanyEnrichmentReport objects to destination.
        """
        pass
