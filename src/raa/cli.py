from __future__ import annotations

import argparse
from pathlib import Path

from raa.core.models import Horizon, ResearchRequest, Security
from raa.core.orchestrator import ResearchOrchestrator
from raa.providers.json_evidence import load_evidence


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="raa", description="Research Analyst Agent")
    subparsers = parser.add_subparsers(dest="command", required=True)
    ask = subparsers.add_parser("ask", help="Ask a security-specific research question")
    ask.add_argument("--ticker", required=True)
    ask.add_argument("--company", default=None)
    ask.add_argument("--exchange", default="NASDAQ")
    ask.add_argument("--question", required=True)
    ask.add_argument("--horizon", choices=[item.value for item in Horizon], default="medium")
    ask.add_argument("--evidence", type=Path, required=True)
    return parser


def main() -> int:
    args = _parser().parse_args()
    security = Security(
        ticker=args.ticker.upper(),
        company_name=args.company or args.ticker.upper(),
        exchange=args.exchange.upper(),
    )
    request = ResearchRequest(
        security=security,
        question=args.question,
        horizon=Horizon(args.horizon),
    )
    result = ResearchOrchestrator().run(request, load_evidence(args.evidence))
    print(f"QUESTION: {request.question}")
    print(f"SECURITY: {security.company_name} ({security.ticker})")
    print(f"STATUS: {result.status}")
    print(f"ANSWER: {result.direct_answer}")
    if result.blockers:
        print("BLOCKERS:")
        for blocker in result.blockers:
            print(f"- {blocker}")
    return 2 if result.is_blocked else 0


if __name__ == "__main__":
    raise SystemExit(main())

