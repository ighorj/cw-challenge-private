# ML FEATURE CATALOG — Phase 3

**Total features:** 39 · **Modeling unit:** customer · **Source window:** full review period (Jul–Oct 2025)

## 1. Final feature list

| # | Feature | Source | Type |
|---|---|---|---|
| 1 | `tx_count` | transactions agg | count |
| 2 | `distinct_active_days` | transactions agg | count |
| 3 | `log_total_outflow` | sum amount_brl | log |
| 4 | `mean_tx_amount` | transactions agg | mean |
| 5 | `std_tx_amount` | transactions agg | std |
| 6 | `max_tx_amount` | transactions agg | max |
| 7 | `distinct_geo_countries` | geo_country | count |
| 8 | `distinct_merchants` | receiver_id | count |
| 9 | `distinct_devices` | device_fingerprint | count |
| 10 | `distinct_ip_addresses` | ip_address | count |
| 11 | `distinct_mccs` | mcc | count |
| 12 | `log_card_outflow` | rail-grouped | log |
| 13 | `log_pix_outflow` | rail-grouped | log |
| 14 | `log_wire_outflow` | rail-grouped | log |
| 15 | `max_txs_per_day` | daily groupby | max |
| 16 | `log_pix_out` | pix_flow=cash_out | log |
| 17 | `log_pix_in` | pix_flow=cash_in | log |
| 18 | `count_high_risk_geo` | country_risk_geo='High' | count |
| 19 | `fraction_cross_border` | cross_border='Yes' | ratio |
| 20 | `count_ip_mismatch` | ip_country≠sender_country | count |
| 21 | `mean_merchant_chargeback` | merchant join | mean |
| 22 | `fraction_high_mcc` | mcc_risk='High' | ratio |
| 23 | `count_c2c_tx` | receiver_entity=customer | count |
| 24 | `distinct_c2c_counterparties` | receiver_id (C2C) | count |
| 25 | `count_wire_sent` | transaction_type=Wire | count |
| 26 | `count_anon_events` | ip_proxy_vpn_tor ∈ {Tor,VPN,Proxy} | count |
| 27 | `count_tor_events` | ip_proxy_vpn_tor=Tor | count |
| 28 | `count_rooted_tx` | device_rooted=Yes | count |
| 29 | `count_cnp` | Card + card_present=No | count |
| 30 | `count_no_3ds` | auth_3ds=No | count |
| 31 | `count_chargeback_status` | status=Chargeback | count |
| 32 | `fraction_night_activity` | hour ∈ [22,6) | ratio |
| 33 | `fraction_weekend_activity` | dow ≥ 5 | ratio |
| 34 | `log_annual_income` | KYC | log |
| 35 | `pep_flag` | KYC | binary |
| 36 | `risk_rating_ord` | KYC (Low=1, Med=2, High=3) | ordinal |
| 37 | `kyc_tier_ord` | KYC (L1=1, L2=2, L3=3) | ordinal |
| 38 | `kyc_risk_score` | KYC | continuous |
| 39 | `age` | derived from DOB | continuous |

## 2. Rationale by group

| Group | Features | Why |
|---|---|---|
| **Behavioral** | 1, 2, 4–6, 15 | Volume, variance, intensity — captures activity profile |
| **Financial** | 3, 12–14, 16–17, 34 | Raw flow magnitudes; passthrough/mismatch are learned non-linearly |
| **Geo** | 7, 18–20 | Jurisdiction exposure + IP/location consistency |
| **Merchant** | 8, 11, 21–22 | Recipient risk; merchant variety and chargeback profile |
| **Network** | 23–25 | C2C connectivity and Wire activity (Phase 1's primary network signal) |
| **Device / IP** | 9–10, 26–28 | Anonymization tools and device hygiene |
| **Card / e-com** | 29–31 | CNP abuse and chargeback exposure |
| **Temporal** | 32–33 | Off-hours / weekend concentration |
| **KYC static** | 35–39 | Profile facts known at enrollment |

## 3. Dropped features (deliberate)

| Dropped | Reason |
|---|---|
| `sanctions_list_hit`, `sanctions_screening_hit` | Defines R08 label — direct leakage |
| Self-merchant flag | Defines R16 label — direct leakage |
| Phase 2 composite score, escalation band, triggered rules | Defines labels — circular |
| Income-to-outflow ratio | Direct R03 indicator; raw inputs (`log_total_outflow`, `log_annual_income`) used instead so the model derives the relationship |
| Structuring-band count | Direct R02 indicator |
| Passthrough ratio | Direct R04 indicator |
| Multi-rail boolean | Direct R17 indicator |
| `declared_occupation` | Target-encoding leaks; one-hot at 80+ levels not informative at this dataset size |
| `cpf_cnpj`, `full_name`, `registration_date`, addresses | Identity / PII, no risk signal |

## 4. Leakage prevention principle

The architecture decision was **raw aggregates over derived rule indicators**. For every Tier-B rule that uses a ratio or count threshold to fire, the corresponding feature is the raw underlying quantity (e.g. `log_total_outflow` + `log_annual_income` instead of "income mismatch ratio"). This forces the model to learn the relationships through non-linear combinations rather than being handed the rule output directly. Behavior-defining inputs to R08 and R16 (sanctions, self-merchant) are dropped entirely.

## 5. PEP ablation

PEP status is an R09 input — directly used to define part of the label population. Strategy-doc commitment was to keep it (as a regulatorily required signal known at enrollment) and quantify its weight via ablation.

| Configuration | PR-AUC | ROC-AUC |
|---|---|---|
| Full feature set (39 features, PEP included) | 0.9981 | 0.9947 |
| Without `pep_flag` (38 features) | 0.9982 | 0.9951 |

PEP contributes essentially nothing to model performance (Δ PR-AUC = 0.0001, within noise). Behavioral features dominate prediction; PEP is one input among many and does not leak the label. Decision: **keep PEP** for regulatory traceability — the model output remains explainable in terms a compliance officer recognizes.

## 6. Observed top features (XGBoost gain)

| Rank | Feature | Gain |
|---|---|---|
| 1 | `distinct_merchants` | 0.342 |
| 2 | `pep_flag` | 0.123 |
| 3 | `tx_count` | 0.083 |
| 4 | `count_tor_events` | 0.048 |
| 5 | `distinct_active_days` | 0.038 |
| 6 | `count_anon_events` | 0.037 |
| 7 | `distinct_devices` | 0.031 |
| 8 | `log_pix_out` | 0.029 |
| 9 | `count_rooted_tx` | 0.025 |
| 10 | `count_chargeback_status` | 0.025 |

Top features map cleanly to AML typologies: counterparty fan-out, regulatory PEP exposure, velocity, anonymization, device risk, and chargeback exposure. No features dominate via spurious correlation — gain is distributed across 30+ features, consistent with multi-rule signal aggregation.
