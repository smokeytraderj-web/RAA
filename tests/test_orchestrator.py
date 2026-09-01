from datetime import UTC, datetime
import unittest

from raa.core.models import Evidence, Horizon, ResearchRequest, Security
from raa.core.orchestrator import ResearchOrchestrator


def request() -> ResearchRequest:
    return ResearchRequest(
        security=Security("AAPL", "Apple Inc.", "NASDAQ"),
        question="Is this an attractive long-term entry?",
        horizon=Horizon.LONG,
    )


def evidence(evidence_id: str, area: str) -> Evidence:
    return Evidence(
        evidence_id=evidence_id,
        area=area,
        summary=f"Verified {area} observation.",
        source_name="Synthetic test fixture",
        source_url="https://example.test/evidence",
        retrieved_at=datetime(2026, 9, 1, tzinfo=UTC),
    )


class OrchestratorTests(unittest.TestCase):
    def test_blocks_when_fundamental_evidence_is_missing(self) -> None:
        result = ResearchOrchestrator().run(request(), [evidence("t1", "technical")])
        self.assertTrue(result.is_blocked)
        self.assertIsNone(result.rating)
        self.assertIn("Fundamental Analyst", result.blockers[0])

    def test_moves_to_review_when_both_specialists_have_evidence(self) -> None:
        result = ResearchOrchestrator().run(
            request(), [evidence("t1", "technical"), evidence("f1", "fundamental")]
        )
        self.assertEqual(result.status, "evidence_review")
        self.assertIsNone(result.rating)
        self.assertEqual(len(result.findings), 2)

    def test_rejects_duplicate_evidence_ids(self) -> None:
        with self.assertRaisesRegex(ValueError, "Duplicate evidence IDs"):
            ResearchOrchestrator().run(
                request(), [evidence("same", "technical"), evidence("same", "fundamental")]
            )

    def test_question_must_be_specific(self) -> None:
        with self.assertRaisesRegex(ValueError, "specific investment question"):
            ResearchRequest(
                security=Security("AAPL", "Apple Inc.", "NASDAQ"),
                question="Buy?",
                horizon=Horizon.SHORT,
            )


if __name__ == "__main__":
    unittest.main()
