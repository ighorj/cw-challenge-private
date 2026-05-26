# ML FEATURE CATALOG — Phase 3 (v2)

**Total features:** 43 · **Modeling unit:** customer · **Source window:** full review period (Jul–Oct 2025)

v2 changes from v1: `pep_flag` removed (1:1 mechanical mapping to R09 in the target); five new features added (one IF anomaly score, four counterparty / merchant network-exposure features).

## 1. Final feature list

| # | Feature | Source | Type | New in v2? |
|---|---|---|---|---|
| 1 | `tx_count` | transactions agg | count | |
| 2 | `distinct_active_days` | transactions agg | count | |
| 3 | `log_total_outflow` | sum amount_brl | log | |
| 4 | `mean_tx_amount` | transactions agg | mean | |
| 5 | `std_tx_amount` | transactions agg | std | |
| 6 | `max_tx_amount` | transactions agg | max | |
| 7 | `distinct_geo_countries` | geo_country | count | |
| 8 | `distinct_merchants` | receiver_id | count | |
| 9 | `distinct_devices` | device_fingerprint | count | |
| 10 | `distinct_ip_addresses` | ip_address | count | |
| 11 | `distinct_mccs` | mcc | count | |
| 12 | `log_card_outflow` | rail-grouped | log | |
| 13 | `log_pix_outflow` | rail-grouped | log | |
| 14 | `log_wire_outflow` | rail-grouped | log | |
| 15 | `max_txs_per_day` | daily groupby | max | |
| 16 | `log_pix_out` | pix_flow=cash_out | log | |
| 17 | `log_pix_in` | pix_flow=cash_in | log | |
| 18 | `count_high_risk_geo` | country_risk_geo='High' | count | |
| 19 | `fraction_cross_border` | cross_border='Yes' | ratio | |
| 20 | `count_ip_mismatch` | ip_country≠sender_country | count | |
| 21 | `mean_merchant_chargeback` | merchant join | mean | |
| 22 | `fraction_high_mcc` | mcc_risk='High' | ratio | |
| 23 | `count_c2c_tx` | receiver_entity=customer | count | |
| 24 | `distinct_c2c_counterparties` | receiver_id (C2C) | count | |
| 25 | `count_wire_sent` | transaction_type=Wire | count | |
| 26 | `count_anon_events` | ip_proxy_vpn_tor ∈ {Tor,VPN,Proxy} | count | |
| 27 | `count_tor_events` | ip_proxy_vpn_tor=Tor | count | |
| 28 | `count_rooted_tx` | device_rooted=Yes | count | |
| 29 | `count_cnp` | Card + card_present=No | count | |
| 30 | `count_no_3ds` | auth_3ds=No | count | |
| 31 | `count_chargeback_status` | status=Chargeback | count | |
| 32 | `fraction_night_activity` | hour ∈ [22,6) | ratio | |
| 33 | `fraction_weekend_activity` | dow ≥ 5 | ratio | |
| 34 | `log_annual_income` | KYC | log | |
| 35 | `risk_rating_ord` | KYC (Low=1, Med=2, High=3) | ordinal | |
| 36 | `kyc_tier_ord` | KYC (L1=1, L2=2, L3=3) | ordinal | |
| 37 | `kyc_risk_score` | KYC | continuous | |
| 38 | `age` | derived from DOB | continuous | |
| 39 | `count_high_score_counterparties` | c2c receivers with composite_score ≥ 10 | count | **yes** |
| 40 | `max_counterparty_score` | max composite_score among c2c receivers | continuous | **yes** |
| 41 | `fraction_outflow_to_high_score` | c2c outflow share to high-score receivers | ratio | **yes** |
| 42 | `count_high_chargeback_merchants` | merchants paid with chargeback_ratio_90d ≥ 0.10 | count | **yes** |
| 43 | `iforest_anomaly_score` | Isolation Forest output (no labels) | continuous | **yes** |

## 2. Rationale by group

| Group | Features | Why |
|---|---|---|
| **Behavioral** | 1, 2, 4–6, 15 | Volume, variance, intensity — captures activity profile |
| **Financial** | 3, 12–14, 16–17, 34 | Raw flow magnitudes; passthrough / mismatch are learned non-linearly |
| **Geo** | 7, 18–20 | Jurisdiction exposure + IP / location consistency |
| **Merchant** | 8, 11, 21–22 | Recipient risk; merchant variety and chargeback profile |
| **Network — counterparty mix** | 23–25 | C2C connectivity and Wire activity (Phase 1's primary network signal) |
| **Network — exposure (new)** | 39–42 | Risk-weighted counterparty and merchant exposure: how much of this customer's behavior involves entities the rules engine independently flags? |
| **Device / IP** | 9–10, 26–28 | Anonymization tools and device hygiene |
| **Card / e-com** | 29–31 | CNP abuse and chargeback exposure |
| **Temporal** | 32–33 | Off-hours / weekend concentration |
| **KYC static** | 35–38 | Profile facts known at enrollment (`pep_flag` removed) |
| **Unsupervised (new)** | 43 | Isolation Forest anomaly score — independent of rules and labels |

## 3. Dropped features (deliberate)

| Dropped | Reason |
|---|---|
| `sanctions_list_hit`, `sanctions_screening_hit` | R08 is held out from the target; including these would be either label leakage (under v1) or trivial pass-throughs (under v2). The rules engine owns the sanctions signal. |
| Self-merchant flag | R16 is held out — rules engine owns this. |
| Phase 2 composite score, escalation band, triggered rules | Target proxy under v1; remains excluded under v2 to keep the model honest about behavioral signal. |
| Income-to-outflow ratio | Direct R03 indicator; raw inputs (`log_total_outflow`, `log_annual_income`) used instead so the model derives the relationship. |
| Structuring-band count | Direct R02 indicator. |
| Passthrough ratio | Direct R04 indicator. |
| Multi-rail boolean | Direct R17 indicator. |
| `pep_flag` *(new in v2)* | 1:1 mechanical mapping to R09, which is in the target. Including it would short-circuit the model's learning. `log_annual_income` and `kyc_risk_score` remain because they participate in many rules, not just one. |
| `declared_occupation` | Target-encoding leaks; one-hot at 80+ levels not informative at this dataset size. |
| `cpf_cnpj`, `full_name`, `registration_date`, addresses | Identity / PII; no risk signal. |

## 4. Leakage prevention principle

The v2 design extends the v1 principle ("raw aggregates over derived rule indicators") with a stricter rule-holdout: **only 6 of 21 rules contribute to the target**, and of those six the three Tier-A hard alerts (R08, R16, R21) are excluded entirely. The remaining 15 rules survive as raw aggregates the model must rediscover; the corresponding "rule output" boolean is never a feature. R09's mechanical input (`pep_flag`) is removed for the same reason.

## 5. New features — empirical contribution

The four network-exposure features and the IF anomaly score appear in the top SHAP drivers for several Phase 1 cohort subjects under v2:

- `count_high_score_counterparties` — top-5 SHAP driver for C100091 (4 high-score counterparties) and C101582 (3 high-score counterparties)
- `max_counterparty_score` — top-5 SHAP driver for C101542
- `iforest_anomaly_score` — top-5 SHAP driver for C100208

The IF feature's contribution is small but non-zero (rank ~25 by gain); its operational value is in providing a divergence signal — customers with high IF score but low ML probability (or vice versa) warrant secondary review.

## 6. Observed top features (XGBoost gain, v2)

| Rank | Feature | Gain |
|---|---|---|
| 1 | `log_annual_income` | 0.197 |
| 2 | `log_total_outflow` | 0.123 |
| 3 | `log_pix_out` | 0.047 |
| 4 | `distinct_c2c_counterparties` | 0.028 |
| 5 | `count_wire_sent` | 0.027 |
| 6 | `log_pix_outflow` | 0.026 |
| 7 | `max_txs_per_day` | 0.024 |
| 8 | `max_tx_amount` | 0.024 |
| 9 | `fraction_weekend_activity` | 0.023 |
| 10 | `mean_tx_amount` | 0.022 |
| 11 | `count_rooted_tx` | 0.021 |
| 12 | `count_tor_events` | 0.021 |

Gain is distributed across 30+ features (no single feature dominates), and the income-outflow pair concentrates ~32% of the gain — which is consistent with R03 (the highest-weight rule in the target) being the dominant soft signal.
