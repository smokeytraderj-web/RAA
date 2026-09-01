from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum


class Horizon(StrEnum):
    SHORT = "short"
    MEDIUM = "medium"
    LONG = "long"
    ALL = "all"


class Rating(StrEnum):
    STRONG_BUY = "Strong Buy"
    BUY = "Buy"
    ADD = "Add"
    HOLD = "Hold"
    REDUCE = "Reduce"
    SELL = "Sell"
    AVOID = "Avoid"


class Confidence(StrEnum):
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"


class EvidenceKind(StrEnum):
    FACT = "observed_fact"
    CALCULATION = "deterministic_calculation"
    UNVERIFIED = "unverified_claim"


@dataclass(frozen=True, slots=True)
class Security:
    ticker: str
    company_name: str
    exchange: str
    currency: str = "USD"
    security_type: str = "Common Stock"

    def __post_init__(self) -> None:
        if not self.ticker.strip() or not self.company_name.strip() or not self.exchange.strip():
            raise ValueError("Ticker, company name, and exchange are required.")


@dataclass(frozen=True, slots=True)
class Evidence:
    evidence_id: str
    area: str
    summary: str
    source_name: str
    source_url: str
    retrieved_at: datetime
    kind: EvidenceKind = EvidenceKind.FACT
    value: str | float | int | None = None
    unit: str | None = None

    def __post_init__(self) -> None:
        required = (self.evidence_id, self.area, self.summary, self.source_name, self.source_url)
        if any(not item.strip() for item in required):
            raise ValueError("Evidence identity, area, summary, source, and URL are required.")
        if self.retrieved_at.tzinfo is None:
            raise ValueError("Evidence timestamps must include a timezone.")


@dataclass(frozen=True, slots=True)
class ResearchRequest:
    security: Security
    question: str
    horizon: Horizon
    position_context: str | None = None

    def __post_init__(self) -> None:
        if len(self.question.strip()) < 8:
            raise ValueError("Ask a specific investment question of at least 8 characters.")


@dataclass(frozen=True, slots=True)
class AnalystFinding:
    analyst: str
    conclusion: str
    rating: Rating | None
    confidence: Confidence
    evidence_ids: tuple[str, ...]
    risks: tuple[str, ...] = ()
    change_conditions: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class ResearchResult:
    request: ResearchRequest
    status: str
    direct_answer: str
    rating: Rating | None
    confidence: Confidence
    findings: tuple[AnalystFinding, ...] = ()
    evidence: tuple[Evidence, ...] = ()
    disagreements: tuple[str, ...] = ()
    blockers: tuple[str, ...] = ()
    generated_at: datetime | None = None

    @property
    def is_blocked(self) -> bool:
        return self.status == "blocked"

