# AML ALERTING FRAMEWORK — EXECUTIVE SUMMARY
**Project:** CloudWalk AML/FT Investigation Pipeline · Phase 2

---

## 1. Architecture overview

A production-grade rule engine implementing **21 alerts** across **17 AML typologies**. Designed for explainability over algorithmic sophistication: every alert decomposes into named rules with explicit weights and dataset-calibrated thresholds. The engine separates concerns across three operational tiers:

| Tier | Mechanism | Purpose |
|---|---|---|
| **A — Hard alerts** | Bypass scoring; immediate review | Single-event severity (sanctions, self-routing, confirmed network linkage) |
| **B — Score contributors** | Weighted points (HIGH=3 · MED=2 · LOW=1) | Aggregated risk from independent indicators |
| **C — Amplifiers** | +1 only when ≥1 Tier-B fires | Confirming / strengthening signals |

This separation reflects operational reality — sanctions exposure and confirmed network linkage warrant different handling than aggregated indicators, and weak-standalone signals should not generate alerts in isolation.

## 2. Typology coverage

The 21 rules group cleanly into seven AML categories:

| Category | Rules | Coverage |
|---|---|---|
| **Behavioral anomalies** | R01 velocity burst · R03 income mismatch · R04 passthrough · R15 fan-out | Activity inconsistent with declared profile or platform inflows |
| **Structuring** | R02 R$9k–R$10k band recurrence | Threshold-evasion behavior |
| **Geo-risk** | R06 high-risk jurisdiction · R07 IP–origin mismatch | FATF Rec. 19 compliance |
| **Anonymization** | R05 Tor/VPN/Proxy · R14 rooted device · R12 device reuse · R13 IP reuse | Operational concealment indicators |
| **Merchant / network** | R11 high-MCC · R16 self-merchant · R19 chargeback merchant · R20 merchant convergence · R21 confirmed Wire link | Routing and coordination signals |
| **Sanctions / PEP / KYC** | R08 sanctions hit · R09 PEP-EDD · R10 KYC inconsistency | Regulatory & internal control |
| **Card / e-commerce** | R18 CNP without 3DS · R17 multi-rail | Card-not-present abuse & layering |

R12 and R13 are retained for production parity; this dataset has a 1:1 device-and-IP-to-customer mapping and they do not fire.

## 3. Composite scoring

Integer weights (1 / 2 / 3) keep scoring auditable — finer granularity implies false precision and is difficult to defend in compliance review. Hard alerts bypass scoring entirely, so severity-1 events cannot be diluted by the absence of secondary indicators. Amplifiers contribute +1 only when a Tier-B rule has already fired for the same subject; this prevents structurally common signals (multi-rail use is the dataset norm at 59% of senders) from inflating scores in isolation. Cohort-dependent rules (R20 merchant convergence, R21 network link) are evaluated in a second pass against customers already alerted in pass one — preventing recursive cascades while preserving the original detection intent.

**Escalation bands:**

| Score | Outcome |
|---|---|
| Any Tier A fire | Immediate SAR — hard alert |
| ≥ 10 | Tier 1 SAR — immediate review |
| 6 – 9 | Tier 2 SAR — standard window |
| 3 – 5 | Tier 3 — enhanced monitoring |
| < 3 | Routine |

Output is ranked by composite score (severity), with hard-alert as a tiebreaker rather than a priority override — a high-individual-risk customer correctly outranks a lower-scoring subject hard-flagged on network linkage alone.

## 4. Production cohort validation

The engine was validated by confirming that the production top-10 risk-ranked cohort is reproduced algorithmically:

- All **10 production top-10 subjects** land in **Tier 1** of the engine's output.
- **C100837** ranks #1 by composite score (25); **C102290** (primary SAR showcase) ranks #2 (24, same probability tier).
- The hard-alert triggers (R08 sanctions, R21 network linkage) correctly identify subjects requiring escalation: C100091 and C101542 fire R21; C101028, C101208, C101445, C101582 fire R08.
- The framework produces the operational priority ranking algorithmically across multiple concurrent indicators.

**Why C102290 was selected as primary SAR subject.** The engine fires ten concurrent rules on this customer — R01, R03_HIGH, R04, R05_TOR, R09, R10, R11, R15, R17, R19, R20 — placing them in the top 0.2% of the scored population. Operationally, the case combines mandatory regulatory exposure (R09 PEP-EDD), deliberate operational concealment (R05_TOR), an extreme income-to-volume disparity (R03_HIGH at 144× monthly declared income), funds distribution materially exceeding observable platform inflows (R04 passthrough at 2,013%), velocity burst (R01), and layered behavioral convergence across fan-out, MCC and merchant-network indicators. No single rule defines the case; the constellation does — which is precisely the pattern the SAR-tier framework is designed to surface. C102290 also demonstrates the highest investigative richness (7 concurrent typologies) despite ranking #2 operationally.

## 5. Operational realism

**Threshold calibration.** Every threshold was validated against observed dataset percentiles before adoption. Where Phase 1's initial cutoffs proved too lax against the full distribution — notably R03 income-mismatch at 50× would have flagged 59% of the base — the standalone threshold was tightened (to 100×) and the looser cutoff retained only as a composite trigger. R05 anonymization, R15 fan-out, R19 chargeback, and R11 high-MCC underwent similar recalibration. All rationale is documented in `alert_rules.md`.

**Alert density.** The engine places ~50% of the customer base in Tier 2+, which is elevated relative to real-world AML systems. This reflects the synthetic dataset's structural skew: mean income-to-volume ratio is 74× across the population, and 74% of customers register at least one anonymization event. In a production environment with realistic customer distributions, the same rule logic and thresholds would yield single-digit Tier 1 percentages — no architectural change required.

**Production tuning levers.** Alert volume can be reduced without modifying rule semantics by (i) raising the multiplier on weight-3 rules (e.g. R03 from 100× to 200×), (ii) increasing recurrence thresholds on R02 / R11 / R14 / R18, or (iii) elevating the Tier 1 score threshold from 10 to 12. These are calibration choices, not architectural rewrites — the framework is designed to be retuned, not rebuilt.

---

**Phase 2 deliverables:** `alert_rules.md` (catalog) · `alerts_engine.py` (pandas implementation) · `alerts_output.csv` (per-customer scored output).
