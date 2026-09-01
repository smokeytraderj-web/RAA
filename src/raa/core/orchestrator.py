from __future__ import annotations

from collections import Counter
from typing import Iterable

from raa.agents.deterministic import DeterministicAnalystTeam
from raa.core.models import Evidence, ResearchRequest, ResearchResult


class ResearchOrchestrator:
    def __init__(self, team: DeterministicAnalystTeam | None = None) -> None:
        self.team = team or DeterministicAnalystTeam()

    def run(self, request: ResearchRequest, evidence: Iterable[Evidence]) -> ResearchResult:
        evidence_items = tuple(evidence)
        self._validate_evidence(evidence_items)
        findings = tuple(
            specialist.analyze(request, evidence_items) for specialist in self.team.specialists
        )
        return self.team.lead.reconcile(request, evidence_items, findings)

    @staticmethod
    def _validate_evidence(evidence: tuple[Evidence, ...]) -> None:
        counts = Counter(item.evidence_id for item in evidence)
        duplicates = sorted(item for item, count in counts.items() if count > 1)
        if duplicates:
            raise ValueError(f"Duplicate evidence IDs: {', '.join(duplicates)}")

