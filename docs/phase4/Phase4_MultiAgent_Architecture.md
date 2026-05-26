# Phase 4 — Multi-Agent AML/FT Orchestration

_CloudWalk AML/FT Investigation Pipeline · Architecture_

---

## 1. What this is

A six-agent pipeline wrapping the Phase 2 rules engine and Phase 3 ML prioritizer in an evidence-grounded investigation → SAR drafting → compliance-review workflow. Sequential, contract-driven, fully auditable.

```
data_agent → detection_agent → investigation_agent → sar_agent → compliance_agent
```

The LLM is **not** the system. Each LLM-using agent ships a deterministic template backend producing the same JSON contract. Backend selection is a runtime flag.

For per-agent contracts see [`agents/README.md`](../../agents/README.md).

---

## 2. Run directory and artifact lineage

All artifacts for one run live in `outputs/phase4_demo/runs/<run_id>/`. Lineage is linear:

```
data_quality_report.json
processed_*.parquet ─────────────────► alerts_output.csv
                                        ml_ranked_output.csv
                                        prioritized_alert_queue.json ─► evidence_bundle.json
                                                                        investigation_case.json
                                                                        investigation_summary.md ─► sar_structured.json
                                                                                                    sar_draft.md ─► compliance_review.json
                                                                                                                    final_decision.json

audit_log.json  (appended throughout)
```

`--run-id <existing>` resumes from cached artifacts. Failed stages preserve all upstream outputs for forensic review.

---

## 3. Communication contracts

Agents exchange **JSON only**. Three high-value contracts (full schemas inlined in each agent's `prompt.md`):

| Contract | Key fields |
|---|---|
| `prioritized_alert_queue.json` | `customers[].{rank, customer_id, rules_score, ml_probability, escalation_band, hard_alert, triggered_rules[]}` |
| `investigation_case.json`      | `cases[].{customer_id, summary, triggered_typologies[], key_facts[], entity_links[], timeline[], confidence, recommended_next_step}` |
| `sar_structured.json`          | `sars[].{customer_id, sar_reference, executive_summary, triggered_alerts[], detailed_findings[], regulatory_basis[], recommended_actions[], key_metrics, linked_entities[]}` |

The investigation agent's prompt mandates "every factual claim must trace to an item in the evidence bundle." The bundle is deterministically built from raw transactions — there is no path for the LLM to fabricate evidence.

---

## 4. Failure handling and audit

- Per-stage `try/except` in the orchestrator catches any exception, writes `stage_failed` with full traceback to `audit_log.json`, and re-raises. No silent retries.
- `audit_log.json` is append-only per entry. Every artifact write, backend choice, and decision is logged with ISO timestamp + agent + event.
- Backend choice logged per LLM-using agent (`backend_selected: anthropic | template`) so reviewers can see whether a given SAR was LLM-augmented.

---

## 5. Operational rationale

- **Determinism where it counts** — rules, scoring, policy checks are deterministic Python. Auditable in any compliance review.
- **LLM augments, never decides** — narrative quality only. Filing decisions come from deterministic check outcomes.
- **Contract-first** — every interface is a JSON schema. Backends are swappable per agent.
- **Single run directory** — `audit_log.json` reconstructs the full decision chain without context outside the run folder.
- **n8n parity** — `agents/orchestrator/n8n_workflow.json` mirrors the Python DAG node-for-node with identical contracts. Migration is a config swap.

---

## 6. End-to-end demo

```
RUN 20260523-210007-99a97c · top_n=10 · backend=template

▶ data_agent           ✓  validated 52,000 txs, 2,500 customers, 1,000 merchants
▶ detection_agent      ✓  rules + XGBoost; 10 prioritized
▶ investigation_agent  ✓  10 evidence bundles, 10 cases
▶ sar_agent            ✓  10 SAR drafts (all file_sar_immediate)
▶ compliance_agent     ✓  10 SARs reviewed; 10 approved, 0 revisions, 0 rejections

47 audit entries · 14 artifacts in run directory
```

Run with the Anthropic LLM:

```bash
ANTHROPIC_API_KEY=sk-... python3 agents/orchestrator/orchestrator.py --top-n 10 --use-llm
```

JSON contract is unchanged. Each artifact carries `_backend: anthropic | template`.

---

## 7. Phase 1 / 2 / 3 reuse

| Phase | Phase 4 entry |
|---|---|
| Phase 1 (manual SAR) | Markdown SAR template mirrors `docs/phase1/SAR-2025-C102290-01.md` |
| Phase 2 (rules engine) | Imported by `detection_agent.py` |
| Phase 3 (XGBoost regression on `behavioral_risk_score` + Isolation Forest + SHAP, all 2,500 customers, isotonic calibration) | Imported by `detection_agent.py`; ML outputs `predicted_probability`, `predicted_band`, `predicted_score`, `behavioral_risk_score`, `composite_score`, `hard_alert`, `iforest_anomaly_score` — consumed by `detection_agent` and `investigation_agent` |

Phase 4 adds orchestration, evidence-grounded narrative generation, SAR templating, deterministic compliance review, and an immutable audit trail.
