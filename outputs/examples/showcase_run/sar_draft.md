# SUSPICIOUS ACTIVITY REPORT (SAR)

## Case Identification

| Field | Value |
|-------|-------|
| **SAR Reference** | SAR-20260526-120114-87e097-C100091-01 |
| **Customer ID** | C100091 |
| **Run ID** | 20260526-120114-87e097 |
| **Prepared At** | 2026-05-26T15:01:32+00:00 |
| **Priority Score** | 73.19 |
| **Severity** | critical |
| **Escalation Band** | Tier 1 — Hard alert |
| **ML Confidence Band** | Moderate |

---

## 1. Executive Summary

Customer with KYC risk score 66/100. declared income R$10,173/yr versus R$91,350 in 18 outflows (≈108× declared monthly income). PIX passthrough ratio 4008%. Activity appears materially inconsistent with the declared customer profile.

---

## 2. Triggered Alerts

| Alert Code | Detection logic | Relevance |
|---|---|---|
| R02-STRUCT-BAND | 1–2 transactions in R$9,000–R$10,000 band | Contributes to composite risk indicator |
| R03-INCOME-MISMATCH | Total outflow >100× declared monthly income | Contributes to composite risk indicator |
| R04-PASSTHRU | PIX outflow-to-inflow ratio >200% | Contributes to composite risk indicator |
| R06-GEO-HIGH-RISK | Cross-border activity involving high-risk jurisdiction | Contributes to composite risk indicator |
| R08-SANCTIONS-SCREEN | Transactional sanctions screening event detected | Contributes to composite risk indicator |
| R11-MCC-HIGH-RISK | ≥3 transactions to high-risk MCC merchants | Contributes to composite risk indicator |
| R17-MULTI-RAIL | Mixed-rail activity: PIX + Card + Wire within review window | Contributes to composite risk indicator |
| R19-CHARGEBACK | Chargeback history or repeat use of high-chargeback merchants | Contributes to composite risk indicator |
| R20-MERCHANT-CONVERGE | Shared receiving merchant with another flagged subject | Contributes to composite risk indicator |
| R21-NETWORK-LINK | Direct wire transfer to another flagged subject | Contributes to composite risk indicator |

---

## 3. Detailed Findings

- R$91,350 total outflow vs R$848/month declared income (108×)
- PIX passthrough 4008% (R$57,117 out / R$1,425 in)

---

## 4. Regulatory Basis

- FATF Recommendation 10 — CDD applies
- FATF Recommendation 19 — Cross-border monitoring (where applicable)
- Circular BACEN 3.978/2020 — Activity materially inconsistent with declared profile is a reportable indicator
- COAF — Suspicious Activity Report filing obligation

---

## 5. Recommended Actions

1. Submit SAR to COAF following institutional policy (file_sar_immediate).
2. Initiate Enhanced Due Diligence: source-of-funds and source-of-wealth documentation.
3. Elevate to enhanced monitoring tier; reduce thresholds for ongoing alerting.
4. Initiate merchant-level review for any shared receiving merchants.
5. Compliance Officer to assess transactional restrictions pending EDD outcome.

---

## 6. Linked Entities

| Entity | Relationship | Status |
|---|---|---|
| C100179 | PIX recipient of R$7,680 | Identified during this investigation |
| M200985 | PIX recipient of R$9,732 | Identified during this investigation |
| C100236 | Wire recipient of R$1,256 | Identified during this investigation |
| M200363 | Wire recipient of R$11,673 | Identified during this investigation |
| M200796 | PIX recipient of R$18,508 | Identified during this investigation |

---

_This report constitutes an internal compliance escalation. Conclusions are based on transactional and KYC data available at preparation time. Final SAR filing determination is subject to Compliance Officer and MLRO review._

_ML confidence labels are calibrated relative to the investigated escalation cohort, not the full customer population._

---

# SUSPICIOUS ACTIVITY REPORT (SAR)

## Case Identification

| Field | Value |
|-------|-------|
| **SAR Reference** | SAR-20260526-120114-87e097-C101208-01 |
| **Customer ID** | C101208 |
| **Run ID** | 20260526-120114-87e097 |
| **Prepared At** | 2026-05-26T15:01:32+00:00 |
| **Priority Score** | 70.12 |
| **Severity** | critical |
| **Escalation Band** | Tier 1 — Hard alert |
| **ML Confidence Band** | Moderate-High |

---

## 1. Executive Summary

Customer with KYC risk score 51/100. declared income R$13,047/yr versus R$150,178 in 29 outflows (≈138× declared monthly income). anonymization events (2 VPN). Activity appears materially inconsistent with the declared customer profile.

---

## 2. Triggered Alerts

| Alert Code | Detection logic | Relevance |
|---|---|---|
| R03-INCOME-MISMATCH | Total outflow >100× declared monthly income | Contributes to composite risk indicator |
| R05-ANON-VPN | ≥2 transactions via VPN or proxy service | Contributes to composite risk indicator |
| R08-SANCTIONS-SCREEN | Transactional sanctions screening event detected | Contributes to composite risk indicator |
| R11-MCC-HIGH-RISK | ≥3 transactions to high-risk MCC merchants | Contributes to composite risk indicator |
| R15-FAN-OUT | ≥25 distinct receiving counterparties in review period | Contributes to composite risk indicator |
| R17-MULTI-RAIL | Mixed-rail activity: PIX + Card + Wire within review window | Contributes to composite risk indicator |
| R18-CARD-NO-3DS | ≥3 card-not-present transactions without 3DS authentication | Contributes to composite risk indicator |
| R19-CHARGEBACK | Chargeback history or repeat use of high-chargeback merchants | Contributes to composite risk indicator |
| R20-MERCHANT-CONVERGE | Shared receiving merchant with another flagged subject | Contributes to composite risk indicator |

---

## 3. Detailed Findings

- R$150,178 total outflow vs R$1,087/month declared income (138×)
- Anonymization breakdown: {'VPN': 2}

---

## 4. Regulatory Basis

- FATF Recommendation 10 — CDD applies
- FATF Recommendation 19 — Cross-border monitoring (where applicable)
- Circular BACEN 3.978/2020 — Activity materially inconsistent with declared profile is a reportable indicator
- COAF — Suspicious Activity Report filing obligation

---

## 5. Recommended Actions

1. Submit SAR to COAF following institutional policy (file_sar_immediate).
2. Initiate Enhanced Due Diligence: source-of-funds and source-of-wealth documentation.
3. Elevate to enhanced monitoring tier; reduce thresholds for ongoing alerting.
4. Initiate merchant-level review for any shared receiving merchants.
5. Compliance Officer to assess transactional restrictions pending EDD outcome.

---

## 6. Linked Entities

| Entity | Relationship | Status |
|---|---|---|
| M200526 | PIX recipient of R$1,241 via VPN | Identified during this investigation |
| M200815 | Wire recipient of R$2,166 | Identified during this investigation |
| M200524 | Wire recipient of R$2,234 | Identified during this investigation |
| M200972 | Card recipient of R$1,089 via VPN | Identified during this investigation |
| M200212 | Card recipient of R$6,889 | Identified during this investigation |

---

_This report constitutes an internal compliance escalation. Conclusions are based on transactional and KYC data available at preparation time. Final SAR filing determination is subject to Compliance Officer and MLRO review._

_ML confidence labels are calibrated relative to the investigated escalation cohort, not the full customer population._

---

# SUSPICIOUS ACTIVITY REPORT (SAR)

## Case Identification

| Field | Value |
|-------|-------|
| **SAR Reference** | SAR-20260526-120114-87e097-C100837-01 |
| **Customer ID** | C100837 |
| **Run ID** | 20260526-120114-87e097 |
| **Prepared At** | 2026-05-26T15:01:32+00:00 |
| **Priority Score** | 67.40 |
| **Severity** | high |
| **Escalation Band** | Tier 1 — SAR immediate |
| **ML Confidence Band** | High |

---

## 1. Executive Summary

PEP-flagged customer (KYC risk score 59/100). declared income R$7,577/yr versus R$139,084 in 29 outflows (≈220× declared monthly income). PIX passthrough ratio 4367%. anonymization events (1 Tor). Activity appears materially inconsistent with the declared customer profile.

---

## 2. Triggered Alerts

| Alert Code | Detection logic | Relevance |
|---|---|---|
| R03-INCOME-MISMATCH | Total outflow >100× declared monthly income | Contributes to composite risk indicator |
| R04-PASSTHRU | PIX outflow-to-inflow ratio >200% | Contributes to composite risk indicator |
| R05-ANON-TOR | Transaction executed via Tor anonymization network | Contributes to composite risk indicator |
| R06-GEO-HIGH-RISK | Cross-border activity involving high-risk jurisdiction | Contributes to composite risk indicator |
| R09-PEP-EDD | PEP status — Enhanced Due Diligence required (FATF Rec. 12) | Contributes to composite risk indicator |
| R10-KYC-INCONSIST | Contradictory KYC field combination (e.g. PEP + Low risk rating) | Contributes to composite risk indicator |
| R11-MCC-HIGH-RISK | ≥3 transactions to high-risk MCC merchants | Contributes to composite risk indicator |
| R14-ROOTED-DEVICE | ≥3 transactions from rooted or jailbroken device | Contributes to composite risk indicator |
| R15-FAN-OUT | ≥25 distinct receiving counterparties in review period | Contributes to composite risk indicator |
| R17-MULTI-RAIL | Mixed-rail activity: PIX + Card + Wire within review window | Contributes to composite risk indicator |
| R19-CHARGEBACK | Chargeback history or repeat use of high-chargeback merchants | Contributes to composite risk indicator |
| R20-MERCHANT-CONVERGE | Shared receiving merchant with another flagged subject | Contributes to composite risk indicator |

---

## 3. Detailed Findings

- R$139,084 total outflow vs R$631/month declared income (220×)
- PIX passthrough 4367% (R$104,966 out / R$2,403 in)
- Anonymization breakdown: {'Tor': 1}
- KYC inconsistency: PEP=Yes, score=59, risk_rating=Medium, tier=L2

---

## 4. Regulatory Basis

- FATF Recommendation 12 — PEP customers require Enhanced Due Diligence
- FATF Recommendation 19 — Cross-border monitoring (where applicable)
- Circular BACEN 3.978/2020 — Activity materially inconsistent with declared profile is a reportable indicator
- COAF — Suspicious Activity Report filing obligation

---

## 5. Recommended Actions

1. Submit SAR to COAF following institutional policy (file_sar_immediate).
2. Initiate Enhanced Due Diligence: source-of-funds and source-of-wealth documentation.
3. Elevate to enhanced monitoring tier; reduce thresholds for ongoing alerting.
4. Initiate merchant-level review for any shared receiving merchants.
5. Compliance Officer to assess transactional restrictions pending EDD outcome.

---

## 6. Linked Entities

| Entity | Relationship | Status |
|---|---|---|
| M200513 | Wire recipient of R$1,703 | Identified during this investigation |
| M200684 | Card recipient of R$1,362 | Identified during this investigation |
| M200053 | Wire recipient of R$12,957 | Identified during this investigation |
| M200806 | PIX recipient of R$2,783 via Tor | Identified during this investigation |
| M200849 | Wire recipient of R$1,746 | Identified during this investigation |

---

_This report constitutes an internal compliance escalation. Conclusions are based on transactional and KYC data available at preparation time. Final SAR filing determination is subject to Compliance Officer and MLRO review._

_ML confidence labels are calibrated relative to the investigated escalation cohort, not the full customer population._