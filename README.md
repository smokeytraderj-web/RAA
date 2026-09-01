# RAA — Research Analyst Agent

RAA is a question-first investment research agent for Gottfried & Somberg Wealth Management.
Instead of forcing every request into a long stock report, it starts with the analyst's actual
question, gathers relevant evidence, runs independent specialist reviews, and returns a direct,
sourced answer with risks and conditions that would change the conclusion.

RAA is a new project inspired by Researcheus Maximus and Reportus. It does not modify either
existing repository.

## Version 0.1 scope

- One publicly traded security per research session
- A specific user question, such as “Should we add to AXON after this pullback?”
- Short, Medium, Long, or All Horizons
- Independent Technical and Fundamental analyst workstreams
- Lead Analyst reconciliation instead of rating averaging
- Explicit evidence gaps, conflicts, confidence, risks, and invalidation conditions
- Structured result ready for a future navy-and-gold desktop experience and PDF export
- No fabricated market data: the starter blocks conclusions when evidence is missing

## Quick start

```bash
python -m venv .venv

# Windows PowerShell
.venv\Scripts\Activate.ps1

python -m pip install -e ".[dev]"
raa ask --ticker AAPL --question "Is this an attractive long-term entry?" \
  --horizon long --evidence examples/evidence.sample.json
```

For the optional Windows desktop shell:

```bash
python -m pip install -e ".[desktop,dev]"
raa-desktop
```

## Why evidence is required

RAA separates observations from analysis. The core will not invent prices, financial metrics,
technical levels, analyst targets, or citations. Version 0.1 accepts a normalized evidence JSON
file. Live SEC, YCharts, TradingView, news, and sentiment adapters are the next implementation
layer and plug into the same typed evidence contract.

## Architecture

```text
src/raa/
  agents/       independent specialist and lead-analysis policies
  core/         typed models and orchestration
  providers/    future source and AI-provider adapters
  ui/           optional PySide6 desktop shell
tests/          deterministic contract and orchestration tests
```

See [CLAUDE.md](CLAUDE.md) for the product and engineering rules Codex or another coding agent
must follow while working in this repository.

## Important

This software is a research workflow, not an autonomous trading system. It must not place trades.
Client distribution requires firm compliance review and approved disclosure language.

