# PHASE 3 — ML PRIORITIZATION LAYER · STRATEGY DOCUMENT
**Project:** CloudWalk AML/FT Investigation Pipeline
**Status:** v1 strategy preserved below for traceability. v2 strategy is documented in the addendum at the bottom of this file and implemented in `src/ml/ml_pipeline.py`. See [`Phase3_ML_Summary.md`](Phase3_ML_Summary.md) and [`ml_results.md`](ml_results.md) for the v2 executive summary and results.

---

## 1. Positioning

The ML layer does **not** detect money laundering. It is a prioritization model that sits **on top of** the Phase 2 rules engine, producing a continuous risk probability per customer to (a) re-order the alerted population for analyst review, and (b) surface near-miss customers whose behavior resembles Tier 1 subjects without triggering a hard rule.

Operational defensibility takes precedence over benchmark metrics. The model must be explainable to a compliance officer and traceable to recognizable AML typologies.

**Algorithm:** XGBoost binary classifier. Chosen for tabular signal handling, native missing-value support, fast SHAP, and operational track record in financial-crime tooling. No deep learning, no ensembling beyond the boosted-tree itself.

---

## 2. Labeling strategy — weak supervision from Phase 2

No ground-truth confirmed launderers exist in the dataset. Labels are derived from the Phase 2 alert engine using a **two-extreme** scheme — high-confidence positives and high-confidence negatives only — to maximize label quality at the cost of training set size.

| Class | Definition | Count (current run) |
|---|---|---|
| **Positive (y=1)** | `escalation_band == 'Tier 1 — SAR immediate'` OR `hard_alert_flag == True` | ~1,300 |
| **Negative (y=0)** | `escalation_band == 'Routine'` AND no rule fires | ~50 |
| **Uncertain (excluded)** | Tier 2 / Tier 3 | ~1,140 |

The Tier 2/3 middle band is deliberately removed from training. Including it would inject ambiguous labels into the model and is the single largest source of weak-supervision noise.

### Leakage risks (named explicitly)

| Risk | Mitigation |
|---|---|
| Labels defined by R08 (sanctions) | Drop `sanctions_list_hit`, `sanctions_screening_hit` from features |
| Labels defined by R16 (self-merchant) | Drop binary self-merchant flag from features |
| Labels defined by composite score | Never include `total_score`, `escalation_band`, fired-rule list, or any Tier-B/C output as a feature |
| Rule inputs ≈ direct label proxies | Use **raw** aggregates (e.g. `log(total_outflow)`, `log(annual_income)`) instead of derived rule indicators (e.g. `income_mismatch_ratio`, `structuring_band_count`). The model learns equivalent capacity through non-linear combinations of upstream features. |
| Tier 2/3 contamination | Strictly exclude — do not relabel or impute |

### Honest limitation
Because positives ultimately trace back to Phase 2 rules, the model will, in expectation, **approximate the rule engine** on the training distribution. The added value lies in (a) continuous ranking within bands, (b) generalization to feature combinations not explicitly rule-encoded, and (c) flagging of Tier 2/3 customers whose feature profile matches Tier 1. The model is not an independent detector — and is not framed as one.

---

## 3. Modeling unit — customer-level

One row per customer, with features aggregated over the observation window. SARs are filed on customers, not transactions, and the Phase 2 alerts already operate at customer granularity. Transaction-level modeling would produce noisy per-tx alerts on otherwise normal accounts and does not match the operational use case (offline analyst triage). Reserved for a future real-time scoring layer if needed.

---

## 4. Candidate feature catalog

Grouped by category. **Counts and statistics only** — no derived rule indicators. ~50 features total target; final selection trimmed during implementation.

| Category | Example features | Signal intuition | Leakage flag |
|---|---|---|---|
| **Behavioral** | total_outflow, mean/median/std/max tx amount, distinct active days, max_txs_in_single_day, tx_count, mean_inter_arrival_hours | Captures volume, intensity, burst patterns | Safe |
| **Financial** | log(annual_income), log(total_outflow), log(pix_out_brl), log(pix_in_brl), card_outflow, wire_outflow, mean installments | Raw flow magnitudes — model derives mismatch / passthrough internally | Safe (raw, not ratios) |
| **Geo** | distinct_geo_countries, count_high_risk_geo_tx, fraction_cross_border, count_ip_country_mismatch | Cross-border and jurisdiction exposure | Safe |
| **Merchant** | distinct_merchants_paid, mean_merchant_chargeback_ratio_90d, fraction_high_mcc_risk, count_distinct_mccs | Recipient risk profile | Safe |
| **Network** | count_c2c_tx, distinct_c2c_counterparties, count_wire_sent, count_wire_received | Cross-customer activity | Safe (cohort flag excluded) |
| **Device / IP** | distinct_devices, distinct_ip_addresses, count_anon_events, count_tor_events, count_rooted_device_tx | Operational concealment | Safe |
| **Card / e-com** | count_card_present_no, count_auth_3ds_no, fraction_card_no_3ds, count_chargeback_status | CNP abuse pattern | Safe |
| **Temporal** | activity_HHI (Herfindahl of daily volumes), fraction_night_activity, fraction_weekend_activity, days_with_3plus_tx | Concentration / off-hours behavior | Safe |
| **Static (KYC)** | declared_occupation (target-encoded), kyc_risk_score, kyc_tier, pep_flag, risk_rating, age_at_window_start | Profile features known at enrollment | PEP is a label contributor via R09 — flagged for review during ablation |

PEP is **kept** in the feature set despite being an R09 input. It is a profile fact known at enrollment, not derived from activity, and excluding it would hide a regulatorily required signal. Ablation in implementation will quantify its weight.

---

## 5. Validation strategy

**Temporal split — forward-looking labels.** The dataset spans 4 months, which is too short for multi-fold temporal cross-validation. The cleanest single-cut approach:

| Window | Use | Time range |
|---|---|---|
| **Feature window** | Compute all aggregates | 2025-07-01 → 2025-09-30 (3 months) |
| **Label window** | Re-run Phase 2 engine on Sep–Oct activity; label customer status as of period end | 2025-09-01 → 2025-10-31 |
| **Train / test split** | 70/30 random customer-level split, **stratified on label** | — |

The feature window precedes the label window's mid-point, so the model is predicting forward, not memorizing concurrent state. Customer-level split (not row-level) prevents row-wise leakage on per-customer features.

### Imbalance handling
~30:1 positive-to-negative ratio after extreme-labeling. Approach: `scale_pos_weight = neg/pos` in XGBoost (built-in, no SMOTE / no synthetic oversampling — synthetic positives would dilute label quality further).

### Metrics
| Tier | Metric | Why |
|---|---|---|
| Primary | **PR-AUC** | Imbalanced classification; ROC-AUC is misleading at this prevalence |
| Primary | **Recall@Top50** | Top 50 = realistic monthly analyst review capacity |
| Primary | **Precision@Top50** | False positive cost is high (analyst time) |
| Secondary | ROC-AUC | Reported for completeness, not optimized against |

Target: PR-AUC ≥ 0.85, Recall@Top50 ≥ 0.7 on test set. These are realism floors, not stretch goals — over-optimizing them on this dataset is a red flag for overfitting given the synthetic label distribution.

---

## 6. Explainability plan

| Method | Use |
|---|---|
| **XGBoost gain importance** | Global feature ranking — first-pass sanity check |
| **SHAP (TreeExplainer)** | Per-feature global summary + per-customer waterfall plots for case-by-case explanation |
| **Top-feature concordance with SAR narrative** | For each Phase 1 cohort subject, verify that the top-3 SHAP contributors map to rule categories that fired for them (e.g., C102290's top SHAP features should include anonymization, income mismatch, fan-out — matching their actual SAR) |

The concordance check is the qualitative acceptance test: if SHAP explanations don't align with SAR-tier reasoning, the model is not deployable regardless of metrics.

---

## 7. Operational integration

Three independent signals feed the analyst queue sequentially, not in competition:

```
                  ┌──────────────────────────┐
  Dataset ───────►│   Phase 2 rules engine   │── deterministic alerts
                  └──────┬───────────────────┘    + composite_score + hard_alert flag
                         │
                         ├──────────────────────────────────────────────────────────────►
                         │         ┌──────────────────────────────┐
                         │         │  Phase 3 Isolation Forest    │── anomaly_score
                         │         │  (unsupervised, no labels)   │   (independent signal)
                         │         └──────────────────────────────┘
                         │
                         ▼
                  ┌──────────────────────────┐
                  │  Phase 3 XGBoost (v2)    │── predicted_probability ∈ [0,1]
                  │  regression + isotonic   │   (behavioral signal only)
                  └──────────────┬───────────┘
                                 │
                                 ▼
                  ┌──────────────────────────┐
                  │   Analyst triage queue   │── priority_score (rules + ML + hard-alert bonuses)
                  └──────────────────────────┘    + SHAP top-3 drivers per customer
```

**Triage logic (v2 implementation):**
- **Hard alerts** (R08 sanctions, R16 self-merchant, R21 network-link) → mandatory escalation regardless of ML score; `predicted_probability` informational only.
- **Tier 1 — SAR immediate** (escalation band from rules engine) → analyst queue, re-ranked by `priority_score` descending.
- **Tier 2 / Tier 3** → escalated to Tier 1 queue if `predicted_probability` ≥ 0.75 (behavioral near-miss).
- **Routine** → surfaced for analyst review if `predicted_probability` ≥ 0.90 or `iforest_anomaly_score` is in top 5%; otherwise suppressed.

The ML layer **never overrides** a rule-driven decision downward (it cannot suppress a SAR). It only re-orders within bands and escalates upward. Divergence between the three signals (rules / XGBoost / Isolation Forest) is explicitly informative: a hard-alert customer with low ML probability is regulatory-fact-driven, not behavioral-pattern-driven.

---

## 8. Feasibility assessment

| Concern | Status | Mitigation |
|---|---|---|
| No real laundering labels | Acknowledged | Weak supervision from rules; extreme-class labeling |
| Label–feature leakage | High risk | Raw aggregates instead of rule-equivalent ratios; explicit feature blocklist |
| Small dataset (2,500 customers) | Manageable | Customer-level model is appropriately sized for XGBoost; risk of overfit addressed via early stopping + regularization |
| Short time window (4 months) | Constraining | Single-cut temporal split with forward labels; multi-fold not viable |
| Model trivially replicates rules | Likely outcome | Framed honestly — value is in continuous ranking + near-miss detection, not novel patterns |
| Synthetic dataset over-saturation | Known | Production deployment would re-tune thresholds against real customer distributions |

The pipeline is feasible and defensible at this scale. Approval requested before moving to implementation.

---

**Stops here.** No training, no code, no notebook started.

---

# ADDENDUM — v2 STRATEGY (regression-based behavioral risk)

After v1 was implemented and evaluated, three issues motivated a redesign:

1. **Headline metrics were inflated by label–feature proximity.** PR-AUC 0.998 was driven by the rules-derived label being a function of the very features the model received.
2. **1,726 customers (69 % of the population) were excluded from training** because the bimodal labeling scheme could not assign them a clean positive or negative label.
3. **`pep_flag` short-circuited R09 learning** — a single binary feature reproduced ~half the positive-label population.

The v2 redesign keeps the operational positioning ("prioritization layer on top of rules") but redefines the modeling task to address all three issues at once.

## v2.1 New target — `behavioral_risk_score`

The regression target is the sum of weights for the **soft behavioral core rules only**:
- R02 STRUCT-BAND (HIGH=3, LOW=1)
- R03 INCOME-MISMATCH (HIGH=3, LOW=1)
- R09 PEP-EDD (=3)

Range: 0–9 (integer-valued discrete; max if all three families fire HIGH).

**Hard regulatory alerts (R08 sanctions, R16 self-merchant, R21 network linkage) are explicitly excluded from the target.** They are binary regulatory facts owned by the rules engine; the ML model is not asked to predict them from transactional behavior.

The remaining 15 rules (R01, R04–R07, R10–R15, R17–R20) are held out — they do not appear in the target and their boolean output is never a feature; their underlying signals survive only as raw aggregates the model must rediscover.

## v2.2 Training set

**All 2,500 customers.** Every customer has a defined `behavioral_risk_score` (most are 0; the distribution is documented in `ml_results.md`). No grey-zone exclusion.

## v2.3 Feature additions

| New feature | Purpose | Source |
|---|---|---|
| `iforest_anomaly_score` | Unsupervised anomaly signal that does not see any labels or rules | `src/ml/isolation_forest.py` |
| `count_high_score_counterparties` | Risk-weighted counterparty exposure | rules engine `composite_score` of receivers |
| `max_counterparty_score` | Worst c2c receiver | same |
| `fraction_outflow_to_high_score` | Share of outflow to high-score receivers | same |
| `count_high_chargeback_merchants` | Merchant exposure | merchant table |

The counterparty exposure features deliberately use **rules-engine output** as the counterparty signal — not the model's own predictions, which would create a feedback loop. This is documented as a known trade-off: replacing it with confirmed-launderer status would require ground truth that does not exist in the synthetic dataset.

## v2.4 Feature removals

- `pep_flag` — 1:1 mechanical mapping to R09 (the only soft rule with a direct binary KYC feature). Removed to prevent short-circuit learning.

## v2.5 Model and calibration

- **Algorithm:** XGBoost regressor (`reg:squarederror`), max_depth=4, lr=0.08, n_estimators=800 with early stopping at 40 rounds.
- **Calibration:** Isotonic regression on the training set, mapping raw regression score to `P(composite_score ≥ 90th percentile OR hard_alert)`. Monotone, clipped to [0,1].
- **Output `predicted_probability`** consumed by downstream agents is the calibrated probability; downstream contracts (detection_agent → investigation_agent → SAR agent) are unchanged.

## v2.6 Validation

Customer-level random 70/30 split on all 2,500 customers; XGBoost internal 75/25 train-val for early stopping. Temporal split remains unavailable (see § 5 above — unchanged justification under v2).

### Metrics

| Tier | Metric | Why |
|---|---|---|
| Primary | **R²** | Genuine regression quality on the new continuous target |
| Primary | **Spearman ρ (test and full)** | Rank quality on the actual ranking task |
| Secondary | PR-AUC / ROC-AUC on v1-labeled subset | Apples-to-apples comparison with v1 |
| Secondary | Top-50 / Top-100 overlap with composite_score top customers | Operational sanity check |

The new metrics are documented in `ml_results.md`; v2 achieves R² = 0.70 on the test set, Spearman = 0.87 on the full population.

## v2.7 Honest framing — what v2 gives up and what it gains

| Gives up | Gains |
|---|---|
| 4 pp of PR-AUC on the v1-labeled task (0.998 → 0.957) | 3.2× more training data (774 → 2,500) |
| 10 pp of ROC-AUC (inflated by leakage in v1) | R² = 0.70 on a continuous, non-trivial regression target |
| The illusion that ML "predicts" sanctions and network linkage | Calibrated probabilities |
| | Clean separation: rules own regulatory facts, ML owns behavioral patterns |
| | Network-exposure features and IF anomaly score in top SHAP drivers |
| | Phase 1 sanctions-driven cohort correctly drops to low ML probability while remaining hard_alert=True from the rules layer (the layered behavior the design targets) |

This is a deliberate trade. v1 looked stronger on the headline number, but the strength was leakage-driven. v2 is more honest, more useful, and more defensible in front of a compliance officer who asks "what is the model actually learning?".

**Implemented in v2; this addendum is the design record for the change.**
