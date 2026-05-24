# Agents

Sequential AML pipeline. Each agent reads/writes JSON artifacts in a per-run directory under `outputs/phase4_demo/runs/<run_id>/`. No free-form agent-to-agent chat — only contract-driven artifact exchange.

```
data_agent → detection_agent → investigation_agent → sar_agent → compliance_agent
```

## Agent contracts

| Agent | Backend | Inputs | Outputs |
|---|---|---|---|
| **data_agent**          | deterministic | source xlsx | `processed_transactions.parquet`, `processed_customers.parquet`, `data_quality_report.json` |
| **detection_agent**     | deterministic (wraps Phase 2 + 3) | processed parquets | `alerts_output.csv`, `ml_ranked_output.csv`, `prioritized_alert_queue.json` |
| **investigation_agent** | LLM ∥ template | queue + raw artifacts | `evidence_bundle.json`, `investigation_case.json`, `investigation_summary.md` |
| **sar_agent**           | LLM ∥ template | investigation + bundle | `sar_structured.json`, `sar_draft.md` |
| **compliance_agent**    | hybrid (deterministic + LLM/template) | SAR + investigation + bundle | `compliance_review.json`, `final_decision.json` |
| **orchestrator**        | deterministic Python DAG | — | run dir, `audit_log.json` |

## Per-agent details

**data_agent** — Validates required columns on Transactions / KYC_Profiles / Merchants, checks rail coherence (PIX has `pix_flow`, Card has `card_present`), adds two enrichment columns (`enrich_high_risk_geo`, `enrich_anonymized`). No external feeds.

**detection_agent** — Imports `src/rules/alerts_engine.py` and `src/ml/ml_pipeline.py`; does not reimplement. Priority key = `hard_alert_flag * 100 + rules_score + ml_probability * 10`.

**investigation_agent** — For each customer in the queue, builds an evidence bundle deterministically from raw data (KYC, aggregates, key transactions, single-day bursts, timeline). LLM or template produces investigation case grounded strictly in that bundle.

**sar_agent** — Drafts SAR for customers recommended `file_sar_immediate` or `file_sar_standard_window`. Markdown layout mirrors `docs/phase1/SAR-2025-C102290-01.md`. Structured JSON + markdown emitted together.

**compliance_agent** — Seven deterministic policy checks (mandatory fields, SAR ref format, quantitative evidence, investigation-SAR alignment, PEP→FATF Rec 12, high-risk-geo→FATF Rec 19, SLA) run first. LLM or template then adds narrative assessment. Decision policy: 0 failures → `approve`; 1–2 non-critical → `revise`; mandatory-field failure or >2 → `revise` (substantive).

**orchestrator** — Calls each stage in order, catches per-stage exceptions (logs `stage_failed` with traceback, halts), maintains `audit_log.json`. Re-run with `--run-id <id>` to resume.

## Backend selection

| Condition | Backend |
|---|---|
| `--use-llm` flag AND `ANTHROPIC_API_KEY` set AND `anthropic` importable | Anthropic API |
| Otherwise | Deterministic template |

JSON contract is identical either way. Each artifact carries `_backend` for audit. The LLM augments narrative quality; it cannot bypass deterministic checks or fabricate evidence (the prompt mandates bundle-only sourcing).

## Run

```bash
# Default (template backend)
python3 agents/orchestrator/orchestrator.py --top-n 10

# Live Anthropic API
ANTHROPIC_API_KEY=sk-... python3 agents/orchestrator/orchestrator.py --top-n 10 --use-llm

# Resume an existing run
python3 agents/orchestrator/orchestrator.py --run-id 20260523-210007-99a97c
```

LLM agents (`investigation_agent`, `sar_agent`, `compliance_agent`) each ship a `prompt.md` containing both the prompt template and the expected output schema. n8n parity workflow lives at `agents/orchestrator/n8n_workflow.json`.
