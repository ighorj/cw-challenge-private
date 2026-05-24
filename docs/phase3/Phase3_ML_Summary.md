# Phase 3 — ML Prioritization Layer

_CloudWalk AML/FT Investigation Pipeline · Executive Summary_

---

## 1. Objective & Positioning

The ML layer is a **prioritization** model layered on top of the Phase 2 rules engine. It produces a continuous risk probability per customer that re-ranks the rules-engine alert queue and provides per-customer explainability for analyst review.

It is **not** framed as autonomous laundering detection.

- **Labels:** weak supervision from the Phase 2 composite score.
- **Task:** risk-profile classification — not forward-looking event prediction.
- **Temporal split:** attempted and abandoned. A 2-month label window on Phase 2's 4-month-calibrated thresholds yielded only 64 positives and ROC-AUC ≈ 0.50. The dataset horizon does not support a stable train-future-predict design.

---

## 2. Architecture

```
Raw transactions + KYC
        ↓
[ Phase 2 — Rules engine ] ──► 21-rule alert set · composite score · escalation band
        ↓
[ Phase 3 — XGBoost ]     ──► continuous probability · top-3 SHAP drivers
        ↓
[ Analyst triage queue ]  ──► re-ranked, explained
```

The ML layer **never** suppresses a rule-driven escalation. It only re-orders the queue and surfaces interpretive context.

---

## 3. Features & Validation

39 raw behavioral features across 9 groups. Derived rule indicators (income-mismatch ratio, passthrough ratio, structuring-band count) are explicitly excluded to prevent label leakage.

| Group | Example features | n |
|---|---|---|
| Behavioral | `tx_count`, `distinct_active_days`, `max_txs_per_day` | 6 |
| Financial | `log_total_outflow`, `log_pix_out`, `log_pix_in`, `log_wire_outflow` | 7 |
| Geo | `distinct_geo_countries`, `count_high_risk_geo`, `count_ip_mismatch` | 4 |
| Merchant | `distinct_merchants`, `mean_merchant_chargeback`, `fraction_high_mcc` | 4 |
| Network | `count_c2c_tx`, `distinct_c2c_counterparties`, `count_wire_sent` | 3 |
| Device / IP | `distinct_devices`, `count_tor_events`, `count_rooted_tx` | 5 |
| Card / e-com | `count_cnp`, `count_no_3ds`, `count_chargeback_status` | 3 |
| Temporal | `fraction_night_activity`, `fraction_weekend_activity` | 2 |
| KYC static | `log_annual_income`, `pep_flag`, `kyc_risk_score`, `age` | 5 |

**Validation.** Customer-level random 70/30 split, stratified on label. Internal 25 % validation cut drives early stopping (30 rounds). Test set held out.

**Labeled cohort.** 557 positives (`composite_score ≥ 13` or hard alert) · 217 negatives (`composite_score ≤ 4`) · 1,726 excluded (middle bands).

---

## 4. Metrics & Calibration

### Rules-only vs XGBoost — held-out test set

| Metric | Phase 2 score | XGBoost | Δ |
|---|---|---|---|
| PR-AUC | **1.0000** | 0.9981 | −0.0019 |
| Precision@Top50 | 1.0000 | 1.0000 | 0.0000 |
| Recall@Top50 | 0.2976 | 0.2976 | 0.0000 |
| Spearman vs label | 0.7852 | 0.7686 | −0.0166 |

> **XGBoost does not outperform the deterministic rules engine on labeled extremes.** The labels are derived from the composite score, so it is the optimal ranker on this task by construction. The ML layer adds **interpretive lift** and **intra-band tie-breaking**, not predictive lift.

Full-population Spearman between ML probability and composite score: **0.82**.

### Escalation band calibration

Percentile cutoffs sized to realistic analyst review capacity. Fixed-probability bands (`p ≥ 0.75 = Tier 1`) placed 1,439 customers in Tier 1 and were operationally meaningless.

| Band | Cutoff | Customers | Use case |
|---|---|---|---|
| ML Tier 1 | top 1 % | 25 | Immediate review queue |
| ML Tier 2 | top 5 % | 100 | Priority review |
| ML Tier 3 | top 20 % | 375 | Enhanced monitoring |
| Routine | rest | 2,000 | No active flag |

---

## 5. Explainability

![SHAP summary — global feature impact](../../outputs/figures/ml_shap_summary.png)

Top drivers map cleanly to AML typologies: PIX inflow, income mismatch, Wire outflow, anonymization counts, merchant variety. No single dominant feature — top gain is 34 %.

**Income ablation.** Dropping `log_annual_income` changes PR-AUC by +0.0006 with ranking stability of 0.957. Income is not driving predictions.

### Local explanations — Phase 1 cohort subjects

| Subject | Priority | Probability | Top SHAP drivers |
|---|---|---|---|
| **C100091** | #1 · 80.46 | 0.9962 | `log_pix_in` · `log_annual_income` · `log_wire_outflow` |
| **C101208** | #2 · 74.39 | 0.9889 | `log_pix_in` · `count_anon_events` · `tx_count` |
| **C101028** | #3 · 74.36 | 0.9862 | `log_pix_in` · `count_anon_events` · `count_chargeback_status` |
| **C100837** | #4 · 67.40 | 0.9996 | `log_pix_in` · `log_annual_income` · `count_tor_events` |
| **C101582** | #5 · 66.96 | 0.9955 | `log_pix_in` · `log_annual_income` · `count_anon_events` |
| **C102290** | #6 · 66.00 ★ | 0.9998 | `log_pix_in` · `log_annual_income` · `count_anon_events` |
| **C102093** | #7 · 64.59 | 0.9991 | `log_pix_in` · `log_annual_income` · `count_anon_events` |
| **C100208** | #8 · 63.20 | 0.9996 | `log_pix_in` · `log_annual_income` · `count_anon_events` |
| **C101445** | #9 · 62.49 | 0.9987 | `log_pix_in` · `log_wire_outflow` · `count_anon_events` |
| **C101542** | #10 · 61.79 | 0.9993 | `log_annual_income` · `count_anon_events` · `log_pix_in` |

All 10 subjects score ≥ 0.986 ML probability. SHAP drivers align with the SAR reasoning for each: PIX passthrough (`log_pix_in`), income mismatch (`log_annual_income`), anonymization events (`count_anon_events`), and wire outflow for subjects with network-link or wire sanctions events.

---

## 6. Behavioral Space

![PCA — customer behavioral space (PC1 20.8 % + PC2 9.3 % variance)](../../outputs/figures/ml_pca_clusters.png)

High-risk customers concentrate in the upper-right region of the projection. All 10 production top-10 subjects sit within this concentrated band — confirming shared behavioral typologies, not isolated outliers.

---

## 7. Limitations & Operations

**Limitations**

- Labels are derived from the Phase 2 rules engine (weak supervision); the model approximates the rules in expectation.
- Synthetic dataset density: ~22 % of customers are positives — far higher than real-world AML prevalence.
- No forward prediction — risk-profile classification only, due to the 4-month horizon.
- No empirical near-miss surfacing: zero Tier 2/3 customers reach ML top 100.

**Operations**

- **Behavior drift** — monthly feature-distribution checks; alert if drift > 2σ.
- **Threshold decay** — quarterly re-validation of rule cutoffs against current percentiles.
- **Geo-pattern shifts** — refresh country-risk and sanctions tables against live FATF / OFAC feeds.
- **Alert-rate inflation** — weekly volume monitoring; escalate to threshold review if > 1.5× rolling baseline.
- **Retraining cadence** — re-train on each rule-recalibration cycle (quarterly minimum); regenerate SHAP baselines.
- **Analyst feedback loop** — capture SAR-filing dispositions; accumulate confirmed-SAR customers as a slow-growing genuine-positive set for future supervised refinement.

---

## 8. Conclusion

The ML layer is a defensible prioritization tool with three honest contributions: continuous ranking within rules-engine bands, per-customer SHAP attributions usable in SAR narratives, and a disagreement signal when ML and rules diverge on a specific customer. It does not beat the rule engine on labeled extremes — and is not framed as if it did. C102290 ranks #2 of 2,500 by ML probability, and SHAP drivers for all 10 Phase 1 cohort subjects align with the manual analyst reasoning. The pipeline is designed to be re-tuned, not rebuilt.
