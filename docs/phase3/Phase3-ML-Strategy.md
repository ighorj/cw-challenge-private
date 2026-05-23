# PHASE 3 — ML PRIORITIZATION LAYER · STRATEGY DOCUMENT
**Project:** CloudWalk AML/FT Investigation Pipeline
**Status:** Design only — no training, no code, no notebook yet.

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

The two layers operate sequentially, not in competition:

```
                  ┌──────────────────────────┐
  Dataset ───────►│   Phase 2 rules engine   │── deterministic alerts
                  └──────────────┬───────────┘    + composite score
                                 │
                                 ▼
                  ┌──────────────────────────┐
                  │  Phase 3 ML prioritizer  │── continuous probability
                  └──────────────┬───────────┘    per customer
                                 │
                                 ▼
                  ┌──────────────────────────┐
                  │   Analyst triage queue   │
                  └──────────────────────────┘
```

**Triage logic (proposed):**
- **Tier A hard alerts** → file SAR; ML score informational only.
- **Tier 1 SAR (score ≥10)** → analyst queue, ranked by ML probability descending.
- **Tier 2 SAR (6–9)** → standard window, but escalated to Tier 1 queue if ML probability > 0.75.
- **Tier 3 / Routine** → ML probability > 0.90 surfaces customer for review as near-miss; otherwise routine.

The ML layer **never overrides** a rule-driven decision downward (it cannot suppress a SAR). It only escalates upward and re-orders within bands.

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
