# Final Summary — AML/FT Multi-Agent Investigation System

_CloudWalk INC challenge · End-to-end deliverable summary_

---

## Business problem

A Brazilian fintech operating PIX, Card, and Wire rails needs to detect, investigate, and report potentially suspicious activity within regulatory windows (COAF / Circular BACEN 3.978/2020). Manual review does not scale; pure ML models lack auditability. The system must combine deterministic rules with explainable ML scoring and produce defensible SAR drafts for human compliance review.

## AML typologies detected

The rules engine implements 21 detection rules grouped into 11 typology families:

- **structuring** (R02) — transactions in R$9,000–R$10,000 band
- **velocity-burst** (R01) — ≥4 transactions in single calendar day
- **income-mismatch** (R03) — outflow > 50× or 100× declared monthly income
- **passthrough / layering** (R04) — PIX outflow/inflow ratio >200%
- **anonymization** (R05, R14) — Tor, VPN, Proxy, rooted device
- **geo / cross-border** (R06, R07) — high-risk jurisdictions, IP mismatch
- **sanctions / PEP** (R08, R09, R10) — screening, EDD trigger, KYC inconsistency
- **merchant** (R11, R16, R19, R20) — high-MCC, self-merchant, chargeback, convergence
- **device / IP reuse** (R12, R13) — shared identifiers across accounts
- **fan-out** (R15) — ≥25 distinct counterparties
- **network linkage** (R21) — direct wire to another flagged subject

## Rules approach

Each rule produces a boolean fire plus a contribution score. Per-customer aggregation yields `rules_score`, which combines with critical-rule bonuses (R08=+15, R16=+8, R05_TOR=+5) and a multiplicative escalator for dangerous combos (anonymization × income mismatch × passthrough). Five severity bands: routine / low / medium / high / critical. Hard alerts (sanctions, self-merchant) escalate independently of score.

Rules are deterministic, auditable, and explain every fire by transaction. The composite score is a `priority.py` pure function — no hidden state.

## ML approach

XGBoost classifier trained on weak labels derived from the rules engine outputs (intentional weak supervision — labels reflect institutional risk policy, not ground truth). Features: aggregate transaction statistics, KYC fields, rail/anonymization/geo counts. SHAP explanations are produced per-customer for the top-3 drivers.

**Important methodological note:** ML probabilities in the top cohort are compressed in the 0.98–0.9999 range due to weak-label correlation with the rules. The presentation layer therefore uses **cohort-relative confidence bands** (Extreme / Very High / High / Moderate-High / Moderate) calibrated to the queue distribution, not the full population.

**Dual-model approach — XGBoost + Isolation Forest:** Because XGBoost is trained on rules-derived labels, its confidence scores reflect agreement with existing typologies rather than an independent view of the data. To address this, a complementary **Isolation Forest** model (`src/ml/isolation_forest.py`) was added, trained exclusively on nine raw transaction features — amount, hour, MCC risk, geo risk, anonymization type, device root status, rail, card-present flag, and 3DS status — with no access to rule scores or labels. When both models flag the same customer, the signals reinforce each other from structurally independent evidence bases, which materially strengthens the case for escalation. When they diverge — a customer ranks high in XGBoost but mid-population in Isolation Forest, as with C102290 — it indicates that the risk comes from composite rule convergence rather than raw transaction-level outlier behavior. That distinction is operationally useful: a purely transaction-anomaly customer (high IF, low XGBoost) may represent an emerging typology the rules have not yet codified.

## Operational vs investigative distinction

Two distinct ranking concepts are surfaced explicitly:

| Concept | Driver | Use case |
|---|---|---|
| **Operational escalation priority** | Sanctions-weighted `priority_score` | Determines filing urgency / hard-alert routing |
| **Investigative richness** | Multi-typology convergence + evidence depth | Determines which case best demonstrates the system |

The Phase 1 showcase case **C102290** ranks #1 by investigative richness (PEP + Tor + multi-typology + explainable timeline) but #6 by priority score (no sanctions hit). C100091 ranks #1 by priority because a single transaction triggers a sanctions screening event — but the customer's KYC profile shows no sanctions match, suggesting the screening hit may be a false positive. Both signals are preserved and the distinction is documented in `aml_constants.PRIMARY_SHOWCASE_CASE`.

## Multi-agent orchestration

Five agents in a sequential DAG, each with an Anthropic LLM backend and a deterministic template fallback producing the same JSON contract:

1. **Data Agent** — ingestion, schema validation, rail coherence, enrichment, LLM quality assessment
2. **Detection Agent** — 21 rules + XGBoost + priority scoring + LLM triage memo
3. **Investigation Agent** — evidence bundle, evidence-weighted timeline selection, LLM case narrative
4. **SAR Agent** — structured JSON + markdown SAR draft using canonical rule descriptions
5. **Compliance Agent** — deterministic policy checks (mandatory fields, SLA, jurisdiction) + LLM regulatory review

A separate **Orchestrator** routes stages, propagates the `--use-llm` flag, and appends every event to a per-run `audit_log.json`. Each run is fully reproducible — same inputs, same artifacts.

## Key findings

- **C102290** (Driver, PEP, KYC=98): 144× income mismatch, 2,013% passthrough, Tor+2VPN, single-day burst (R$42k), shared merchants with C100880. Strongest investigative case; full SAR in `docs/phase1/SAR-2025-C102290-01.md`.
- **C100091** (Store Owner): Single transactional sanctions screening event (KYC shows no confirmed match), 107× income mismatch, Wire to a high-risk geography. Highest operational escalation score.
- **Network linkage discovered:** C101848 → C102360 direct Wire (only confirmed inter-subject Wire in the cohort), same-day as a 4-tx velocity burst.
- **100 secondary mule-pattern entities** identified via receive-few/distribute-many screening for follow-up.

## Lessons learned

- **Weak-label ML inflates confidence inside the top cohort.** Solved at the presentation layer with cohort-relative bands rather than retraining.
- **Priority scoring must distinguish hard alerts from investigative depth.** A single sanctions screening event should not silently dominate ranking — surface both dimensions.
- **Sanctions concepts must be separated** at the data model level: transactional screening events ≠ confirmed KYC-level entity matches. Conflating them produces misleading SARs.
- **Cautious AML language is non-negotiable** in regulatory outputs. The `soften_language()` utility post-processes any assertive phrasing to hedged investigative wording.
- **Rule semantics drift across LLM outputs** unless the canonical mapping is injected into the prompt. `aml_constants.RULE_DESCRIPTIONS` is the single source of truth referenced by every agent.

## Limitations

- Synthetic dataset; no real customer behavior validated against ground truth
- Weak-label ML training (labels derived from rules, not analyst feedback)
- No live sanctions list verification (OFAC/BACEN/EU lists not integrated)
- No human-in-the-loop feedback collection
- No production drift monitoring or model recalibration cadence
- Network-graph analysis is shallow (direct wires only; no transitive paths)

## Reproducibility

```bash
# Template backend (deterministic, no API calls)
python -m agents.orchestrator.orchestrator --top-n 10

# LLM backend (requires ANTHROPIC_API_KEY in .env)
python -m agents.orchestrator.orchestrator --top-n 10 --use-llm
```

Each invocation creates a fresh timestamped run directory under `outputs/phase4_demo/runs/`. The canonical example output for review lives at `outputs/examples/showcase_run/`.
