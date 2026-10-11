"""Plain data containers shared between modules."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ValidationResult:
    """Outcome of input validation."""

    is_valid: bool
    error_message: str | None = None
    notices: tuple[str, ...] = ()


@dataclass(frozen=True)
class Finding:
    """One analysis rule outcome. status is 'pass', 'warn' or 'fail'."""

    rule_id: str
    status: str
    points: int
    message: str


@dataclass(frozen=True)
class AnalysisResult:
    """Complete result of analyzing one password (contains no password text)."""

    score: int
    category: str
    findings: tuple[Finding, ...]
    recommendations: tuple[str, ...]
    applied_caps: tuple[str, ...]
