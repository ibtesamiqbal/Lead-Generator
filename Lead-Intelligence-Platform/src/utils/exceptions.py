"""
Custom Exception Hierarchy for Lead Intelligence Platform.
"""

class LeadIntelException(Exception):
    """Base exception for all Lead Intelligence Platform errors."""
    def __init__(self, message: str, details: dict | None = None):
        super().__init__(message)
        self.message = message
        self.details = details or {}

    def __str__(self) -> str:
        if self.details:
            return f"{self.message} | Details: {self.details}"
        return self.message


class DiscoveryError(LeadIntelException):
    """Raised when company discovery or target ingestion fails."""
    pass


class InvalidDomainError(DiscoveryError):
    """Raised when a domain string is malformed or invalid."""
    pass


class RepositoryError(LeadIntelException):
    """Raised when database or repository operations fail."""
    pass


class DuplicateDomainError(RepositoryError):
    """Raised when attempting to insert a target domain that already exists."""
    pass
