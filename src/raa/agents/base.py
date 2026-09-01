from __future__ import annotations

from typing import Protocol, Sequence

from raa.core.models import AnalystFinding, Evidence, ResearchRequest, ResearchResult


class Specialist(Protocol):
    def analyze(self, request: ResearchRequest, evidence: Sequence[Evidence]) -> AnalystFinding: ...


class LeadAnalyst(Protocol):
    def reconcile(
        self,
        request: ResearchRequest,
        evidence: Sequence[Evidence],
        findings: Sequence[AnalystFinding],
    ) -> ResearchResult: ...

