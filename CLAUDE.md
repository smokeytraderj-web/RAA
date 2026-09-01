# RAA Project Instructions

## Product

**RAA (Research Analyst Agent)** is a question-first research application for answering specific
investment questions about one publicly traded security at a time. It is a separate public GitHub
project owned by `smokeytraderj-web` and must not modify Reportus or Researcheus Maximus.

Display the firm name as **Gottfried & Somberg Wealth Management**. The visual direction is minimal,
professional, navy, white, and restrained gold.

## Primary behavior

1. Start with the user's exact question.
2. Resolve and confirm the security identity.
3. Ask for Short Term, Medium Term, Long Term, or All Horizons.
4. Collect only question-relevant evidence with provenance and timestamps.
5. Run independent Technical and Fundamental Analyst workstreams.
6. Use a Lead Analyst to reconcile disagreements; never average ratings mechanically.
7. Lead with a direct answer, confidence, and concise reasoning.
8. Show relevant action scenarios, risks, evidence gaps, and what would change the answer.
9. Never fabricate or silently repair missing market or financial data.

## Answer contract

Every completed answer contains:

- the question and confirmed security;
- a direct answer;
- Strong Buy, Buy, Add, Hold, Reduce, Sell, or Avoid when a rating is justified;
- High, Medium, or Low confidence;
- decisive evidence and specialist disagreement;
- risks and invalidation/change conditions;
- citations with retrieval timestamps;
- a clear blocked status when evidence is insufficient or materially conflicting.

## Architecture rules

- Keep source retrieval separate from analyst reasoning.
- Use typed, structured objects at subsystem boundaries.
- Use deterministic code for validation, calculations, provenance, freshness, and QA.
- Treat generated prose as interpretation, never as evidence for another agent.
- Never expose credentials, cookies, API keys, or authenticated browser state.
- Do not place trades or connect to brokerage execution.
- Keep providers replaceable. Support cloud AI in production and deterministic fakes in tests.
- Use isolated temporary sessions and delete temporary research data after completion or cancel.
- Keep long-running research off the desktop UI thread.

## Initial source roadmap

Priority order: security-master identity; SEC and company IR; licensed YCharts data; public
TradingView evidence; reputable news and analyst commentary; X, Reddit, and Stocktwits for
supporting sentiment only. Material source conflicts block synthesis until resolved.

## Definition of done for a feature

A feature is not complete until it has deterministic tests, structured failure behavior, source
provenance where relevant, safe logging, and a verified user-facing result. Use synthetic or public
non-client data in all tests.

