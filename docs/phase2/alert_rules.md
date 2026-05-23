# AML ALERT RULES — Phase 2 Catalog

**Project:** CloudWalk AML/FT Investigation Pipeline
**Phase:** 2 — Rule-based alerting layer
**Coverage:** 21 rules · 17 typologies · dataset-calibrated thresholds

---

## 1. ARCHITECTURE

Three-tier alerting design — each tier serves a distinct purpose and cannot be conflated.

| Tier | Mechanism | Purpose |
|---|---|---|
| **A — Hard alerts** | Bypass scoring; trigger immediate review | Single-event severity (sanctions exposure, self-routing, confirmed network linkage) |
| **B — Score contributors** | Weighted points (HIGH=3, MEDIUM=2, LOW=1) | Aggregated risk from independent indicators |
| **C — Contextual amplifiers** | +1 only when ≥1 Tier-B rule fires | Confirms / strengthens existing alerts; does not raise alone |

### Escalation bands

| Score | Outcome |
|---|---|
| Tier A fire (any) | **SAR — immediate** |
| ≥10 | **Tier 1 SAR — immediate review** |
| 6–9 | **Tier 2 SAR — standard window** |
| 3–5 | **Tier 3 — Enhanced monitoring** |
| <3 | Routine |

---

## 2. RULE CATALOG

### Tier A — Hard Alerts

#### R08 — SANCTIONS-HIT
- **Logic:** `kyc.sanctions_list_hit == 'Yes'` OR `tx.sanctions_screening_hit == 'Yes'`
- **Calibration:** 9 KYC + 2 tx hits dataset-wide. Hard regulatory block.
- **Rationale:** Sanctioned-party exposure is highest-severity individual signal; never thresholded.

#### R16 — SELF-MERCHANT
- **Logic:** Customer transacts to merchant where `owner_customer_id == sender_id`.
- **Threshold:** any single occurrence.
- **Calibration:** 2 events in dataset; rare → high signal-to-noise.
- **Rationale:** Round-tripping through self-owned merchant — common fictitious-revenue typology.

#### R21 — NETWORK-LINK
- **Logic:** Direct customer→customer **Wire** transaction where **both** parties already score ≥10 (Tier 1) on standalone indicators.
- **Calibration:** Restricted to Wire rail and Tier-1-scored cohort. Unrestricted C2C would cascade across this dataset's wide alerted population.
- **Rationale:** Strongest non-anonymized coordination indicator. Elevates individual SARs to network-level review.
- **Example:** C101848 → C102360 (Wire `TAAUIOJCM76S3`, R$2,857, 2025-09-23) — Phase 1's only confirmed inter-subject Wire; reproduced by the engine.

---

### Tier B — Score Contributors

#### R01 — VEL-BURST · weight 3
- **Logic:** Sender executes ≥4 transactions in single calendar day.
- **Calibration:** p99.9 of population is 3 txs/day; ≥4 is rare (12 sender-days dataset-wide).
- **Examples:** C102290 (2025-08-01, R$42,590), C101848 (2025-09-23, R$39,268), C101328 (2025-08-21, R$37,236).

#### R02 — STRUCT-BAND · weight 3 (≥3 hits) / 1 (1–2 hits)
- **Logic:** Transactions in R$9,000–R$9,999 band (just below R$10k reporting threshold).
- **Calibration:** 17 senders with ≥3 band hits; 143 with ≥2.
- **Examples:** C101854 (4 hits), C102360 / C101534 / C100880 (3 hits each).

#### R03 — INCOME-MISMATCH · weight 3 (≥100×) / 1 (50–99×)
- **Logic:** Total outflow ÷ declared monthly income.
- **Calibration:** Population mean = 74× (dataset has structurally elevated baseline); ≥100× ≈ p79 selectivity (~540 customers).
- **Examples:** C102360 (299×), C102290 (144×), C100880 (141×), C101848 (117×).

#### R04 — PASSTHRU · weight 3
- **Logic:** PIX outflow ÷ PIX inflow > 200%, with volume floor `pix_out ≥ R$20,000`.
- **Rationale:** Indicates funds distributed materially exceed funds received on monitored platform.
- **Examples:** C102290 (2,013%), C100740 (834%), C101534 (660%), C101328 (537%).

#### R05 — ANON-IP · weight 3 (Tor) / 2 (VPN/Proxy ≥2)
- **Logic:** Tor use (any single event) OR VPN/Proxy with recurrence ≥2.
- **Calibration:** 74% of customers have ≥1 anonymization event; recurrence/Tor filter isolates pattern from incidental.
- **Examples:** C102290 (Tor on Card MCC 6011, 2025-10-03), C100880 (Tor), C101162 (VPN+Proxy).

#### R06 — GEO-HIGH-RISK · weight 2
- **Logic:** `country_risk_geo == 'High'` AND `amount_brl ≥ R$5,000`, OR ≥2 high-risk geo events per sender.
- **Examples:** C101328 (Belarus + Afghanistan), C101534 (Afghanistan + UAE), C101848 (Afghanistan).

#### R07 — GEO-IP-MISMATCH · weight 2
- **Logic:** `ip_country ≠ sender_country` with recurrence ≥2.
- **Calibration:** ≥2 reduces 598 raw mismatches to 72 customers — selective.
- **Rationale:** Consistent with VPN-like obfuscation or remote-controlled accounts.

#### R09 — PEP-EDD · weight 3
- **Logic:** `kyc.pep == 'Yes'` (regulatory always-on).
- **Calibration:** 80 PEPs in dataset.
- **Rationale:** FATF Recommendation 12 — mandatory EDD regardless of activity level.
- **Examples:** C102290 (PEP + KYC=98).

#### R11 — MCC-HIGH-RISK · weight 2
- **Logic:** ≥3 transactions to merchants with `mcc_risk == 'High'`.
- **Calibration:** Single-tx flag = 2,492 customers (99.7%); recurrence required.
- **Rationale:** Repeated ATM / gambling / cash-out-adjacent MCC activity consistent with extraction or routing.

#### R14 — ROOTED-DEVICE · weight 2
- **Logic:** ≥3 transactions from devices flagged `device_rooted == 'Yes'`.
- **Calibration:** 43% of customers have ≥1 rooted-device tx in dataset; recurrence-based threshold.
- **Rationale:** Rooted devices bypass mobile security controls — common in mule rings.

#### R15 — FAN-OUT · weight 2
- **Logic:** ≥25 distinct receivers per sender (≈p95 of distribution).
- **Calibration:** Population median = 18 receivers; baseline dispersion is high.
- **Examples:** C102290 (27 receivers).

#### R18 — CARD-NO-3DS · weight 1
- **Logic:** Card-not-present + `auth_3ds != 'Yes'` + `amount_brl ≥ R$2,000`, ≥3 txs per sender.
- **Calibration:** Recurrence reduces 2,582 raw to 211 customers — selective.
- **Rationale:** Repeated unauthenticated high-value CNP consistent with stolen-card cashout.

#### R19 — CHARGEBACK-MERCHANT · weight 2
- **Logic:** ≥3 txs to merchants with `merchant_chargeback_ratio_90d ≥ 0.10`, OR any tx with `status == 'Chargeback'` initiated by sender.
- **Calibration:** Dataset mean cb ratio = 6.2% (elevated baseline); ≥10% ≈ p70 of merchants.
- **Examples:** C100880 (chargeback on structuring-band tx).

---

### Tier C — Amplifiers (+1, only if ≥1 Tier-B fires)

#### R10 — KYC-INCONSISTENCY
- **Logic:** Any of: `pep=Yes` AND `risk_rating ∈ {Low, Medium}` · `kyc_risk_score ≥ 80` AND `risk_rating == 'Low'` · `pep=Yes` AND `kyc_tier == 'L1'`.
- **Rationale:** Internal control gap — KYC fields contradict each other on same profile. Phase 1 finding (C102290).

#### R12 — DEVICE-REUSE
- **Logic:** Single `device_fingerprint` shared across ≥2 customers.
- **Calibration:** **0 fires on this dataset** (perfect 1:1 mapping). Retained for production parity.

#### R13 — IP-REUSE
- **Logic:** Single `ip_address` shared across ≥2 customers.
- **Calibration:** **0 fires on this dataset**. Retained for production parity.

#### R17 — MULTI-RAIL
- **Logic:** Same sender uses PIX + Card + Wire within review window.
- **Rationale:** 59% of senders use all 3 rails — dataset norm, not standalone signal. Confirms layering when paired with other indicators.

#### R20 — MERCHANT-CONVERGENCE
- **Logic:** Receiving merchant gets funds from ≥2 customers already in the Tier 2+ alerted cohort (score ≥6).
- **Calibration:** Cohort-relative — absolute sender counts per merchant are uninformative (population median = 39).
- **Examples:** M200964 (C101328, C101534, C101848), M200460 / M200186 (C102290, C100880), M200894 (C102360, C100740).

---

## 3. COMPOSITE SCORING — EXAMPLE FLOW

Phase 1 subjects scored using the framework:

| Subject | Hard | Tier B fires (weight) | Tier C (+) | Score | Band |
|---|---|---|---|---|---|
| **C102290** | — | R01·3, R03·3, R04·3, R05_TOR·3, R09·3, R11·2, R15·2 | R10, R17, R20 (+3) | **22** | Tier 1 |
| **C101848** | **R21** | R01·3, R03·3, R04·3, R06·2 | R17, R20 (+2) | **13** + hard | Tier 1 |
| **C102360** | **R21** | R02·3, R03·3, R04·3 | R17 (+1) | **10** + hard | Tier 1 |
| **C100880** | — | R02·3, R04·3, R05_TOR·3, R19·2 | R17, R20 (+2) | **13** | Tier 1 |
| **C101328** | — | R01·3, R04·3, R06·2, R15·2 | R17, R20 (+2) | **12** | Tier 1 |
| **C101534** | — | R02·3, R04·3, R05_VPN·2, R06·2 | R17, R20 (+2) | **12** | Tier 1 |
| **C101854** | — | R02·3, R05_VPN·2 | R17 (+1) | **6** | Tier 2 |
| **C101162** | — | R01·3, R05_VPN·2 | R17 (+1) | **6** | Tier 2 |
| **C100740** | — | R01·3, R04·3 | R17 (+1) | **7** | Tier 2 |

Framework reproduces Phase 1's analyst-driven escalation shortlist algorithmically — Tier 1/2/3 banding aligns with the manually determined ranking.

---

## 4. DESIGN PRINCIPLES

- **Coarse integer weights** — auditable, no false precision.
- **Hard alerts bypass scoring** — severity-1 events cannot be diluted by indicator absence.
- **Amplifiers don't fire alone** — structurally common signals (multi-rail, merchant convergence) cannot inflate scores in isolation.
- **Thresholds dataset-calibrated** — each threshold validated against observed percentiles.
- **No ML opacity** — every score decomposes into named rules.

---

**Next phase:** ML risk scoring layer (Phase 3) will complement, not replace, this rules engine.
