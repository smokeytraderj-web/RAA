from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Sequence

from raa.core.models import (
    AnalystFinding,
    Confidence,
    Evidence,
    EvidenceKind,
    ResearchRequest,
    ResearchResult,
)


def _usable(evidence: Sequence[Evidence], area: str) -> list[Evidence]:
    return [item for item in evidence if item.area == area and item.kind != EvidenceKind.UNVERIFIED]


@dataclass(slots=True)
class EvidenceSummarySpecialist:
    name: str
    area: str

    def analyze(self, request: ResearchRequest, evidence: Sequence[Evidence]) -> AnalystFinding:
        relevant = _usable(evidence, self.area)
        if not relevant:
            return AnalystFinding(
                analyst=self.name,
                conclusion=f"No verified {self.area} evidence was supplied.",
                rating=None,
                confidence=Confidence.LOW,
                evidence_ids=(),
                risks=(f"The {self.area} view is unavailable.",),
                change_conditions=(f"Add current, sourced {self.area} evidence.",),
            )

        summaries = "; ".join(item.summary for item in relevant[:3])
        return AnalystFinding(
            analyst=self.name,
            conclusion=summaries,
            rating=None,
            confidence=Confidence.MEDIUM,
            evidence_ids=tuple(item.evidence_id for item in relevant),
            risks=("The supplied evidence has not yet been converted into a rated specialist model.",),
            change_conditions=("Refresh the evidence if its market or filing context changes.",),
        )


class ConservativeLeadAnalyst:
    def reconcile(
        self,
        request: ResearchRequest,
        evidence: Sequence[Evidence],
        findings: Sequence[AnalystFinding],
    ) -> ResearchResult:
        missing = [finding.analyst for finding in findings if not finding.evidence_ids]
        if missing:
            blockers = tuple(f"Missing verified evidence for {name}." for name in missing)
            return ResearchResult(
                request=request,
                status="blocked",
                direct_answer=(
                    "RAA cannot give a defensible investment answer yet because required evidence "
                    "is missing."
                ),
                rating=None,
                confidence=Confidence.LOW,
                findings=tuple(findings),
                evidence=tuple(evidence),
                blockers=blockers,
                generated_at=datetime.now(UTC),
            )

        return ResearchResult(
            request=request,
            status="evidence_review",
            direct_answer=(
                "The evidence has been organized for review, but a rating is intentionally withheld "
                "until a configured Lead Analyst model evaluates the sourced specialist findings."
            ),
            rating=None,
            confidence=Confidence.LOW,
            findings=tuple(findings),
            evidence=tuple(evidence),
            blockers=("Lead Analyst model/provider is not configured.",),
            generated_at=datetime.now(UTC),
        )


class DeterministicAnalystTeam:
    """Safe starter team: organizes evidence and refuses to manufacture a recommendation."""

    def __init__(self) -> None:
        self.specialists = (
            EvidenceSummarySpecialist("Technical Analyst", "technical"),
            EvidenceSummarySpecialist("Fundamental Analyst", "fundamental"),
        )
        self.lead = ConservativeLeadAnalyst()

