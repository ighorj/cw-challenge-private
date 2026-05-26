# SUSPICIOUS ACTIVITY REPORT (SAR)

## Case Identification

| Field | Value |
|-------|-------|
| **SAR Reference** | SAR-20260526-041414-4aa919-C100091-01 |
| **Customer ID** | C100091 |
| **Run ID** | 20260526-041414-4aa919 |
| **Prepared At** | 2026-05-26T04:14:37+00:00 |
| **Priority Score** | 73.19 |
| **Severity** | critical |
| **Escalation Band** | Tier 1 — Hard alert |
| **ML Confidence Band** | Moderate-High |

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
| **SAR Reference** | SAR-20260526-041414-4aa919-C101208-01 |
| **Customer ID** | C101208 |
| **Run ID** | 20260526-041414-4aa919 |
| **Prepared At** | 2026-05-26T04:14:37+00:00 |
| **Priority Score** | 70.12 |
| **Severity** | critical |
| **Escalation Band** | Tier 1 — Hard alert |
| **ML Confidence Band** | High |

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
| **SAR Reference** | SAR-20260526-041414-4aa919-C100837-01 |
| **Customer ID** | C100837 |
| **Run ID** | 20260526-041414-4aa919 |
| **Prepared At** | 2026-05-26T04:14:37+00:00 |
| **Priority Score** | 67.40 |
| **Severity** | high |
| **Escalation Band** | Tier 1 — SAR immediate |
| **ML Confidence Band** | Extreme |

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

---

# SUSPICIOUS ACTIVITY REPORT (SAR)

## Case Identification

| Field | Value |
|-------|-------|
| **SAR Reference** | SAR-20260526-041414-4aa919-C102290-01 |
| **Customer ID** | C102290 |
| **Run ID** | 20260526-041414-4aa919 |
| **Prepared At** | 2026-05-26T04:14:37+00:00 |
| **Priority Score** | 66.00 |
| **Severity** | high |
| **Escalation Band** | Tier 1 — SAR immediate |
| **ML Confidence Band** | Very High |

---

## 1. Executive Summary

PEP-flagged customer (KYC risk score 98/100). declared income R$11,177/yr versus R$134,319 in 27 outflows (≈144× declared monthly income). PIX passthrough ratio 2013%. anonymization events (2 VPN, 1 Tor). Activity appears materially inconsistent with the declared customer profile.

---

## 2. Triggered Alerts

| Alert Code | Detection logic | Relevance |
|---|---|---|
| R01-VEL-BURST | ≥4 transactions in a single calendar day | Contributes to composite risk indicator |
| R03-INCOME-MISMATCH | Total outflow >100× declared monthly income | Contributes to composite risk indicator |
| R04-PASSTHRU | PIX outflow-to-inflow ratio >200% | Contributes to composite risk indicator |
| R05-ANON-TOR | Transaction executed via Tor anonymization network | Contributes to composite risk indicator |
| R09-PEP-EDD | PEP status — Enhanced Due Diligence required (FATF Rec. 12) | Contributes to composite risk indicator |
| R10-KYC-INCONSIST | Contradictory KYC field combination (e.g. PEP + Low risk rating) | Contributes to composite risk indicator |
| R11-MCC-HIGH-RISK | ≥3 transactions to high-risk MCC merchants | Contributes to composite risk indicator |
| R15-FAN-OUT | ≥25 distinct receiving counterparties in review period | Contributes to composite risk indicator |
| R17-MULTI-RAIL | Mixed-rail activity: PIX + Card + Wire within review window | Contributes to composite risk indicator |
| R19-CHARGEBACK | Chargeback history or repeat use of high-chargeback merchants | Contributes to composite risk indicator |
| R20-MERCHANT-CONVERGE | Shared receiving merchant with another flagged subject | Contributes to composite risk indicator |

---

## 3. Detailed Findings

- R$134,319 total outflow vs R$931/month declared income (144×)
- PIX passthrough 2013% (R$108,041 out / R$5,367 in)
- Anonymization breakdown: {'VPN': 2, 'Tor': 1}
- Single-day burst 2025-08-01: 4 txs / R$42,590
- KYC inconsistency: PEP=Yes, score=98, risk_rating=Medium, tier=L1

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
| M200283 | Card recipient of R$3,196 | Identified during this investigation |
| M200004 | Card recipient of R$3,296 | Identified during this investigation |
| M200888 | PIX recipient of R$20,509 | Identified during this investigation |
| M200489 | PIX recipient of R$11,742 | Identified during this investigation |
| M200845 | PIX recipient of R$8,225 | Identified during this investigation |

---

_This report constitutes an internal compliance escalation. Conclusions are based on transactional and KYC data available at preparation time. Final SAR filing determination is subject to Compliance Officer and MLRO review._

_ML confidence labels are calibrated relative to the investigated escalation cohort, not the full customer population._

---

# SUSPICIOUS ACTIVITY REPORT (SAR)

## Case Identification

| Field | Value |
|-------|-------|
| **SAR Reference** | SAR-20260526-041414-4aa919-C101028-01 |
| **Customer ID** | C101028 |
| **Run ID** | 20260526-041414-4aa919 |
| **Prepared At** | 2026-05-26T04:14:37+00:00 |
| **Priority Score** | 65.72 |
| **Severity** | critical |
| **Escalation Band** | Tier 1 — Hard alert |
| **ML Confidence Band** | Moderate |

---

## 1. Executive Summary

PEP-flagged customer (KYC risk score 64/100). declared income R$47,312/yr versus R$71,406 in 18 outflows (≈18× declared monthly income). PIX passthrough ratio 587%. anonymization events (1 Proxy, 1 VPN). Activity appears materially inconsistent with the declared customer profile.

---

## 2. Triggered Alerts

| Alert Code | Detection logic | Relevance |
|---|---|---|
| R04-PASSTHRU | PIX outflow-to-inflow ratio >200% | Contributes to composite risk indicator |
| R05-ANON-VPN | ≥2 transactions via VPN or proxy service | Contributes to composite risk indicator |
| R08-SANCTIONS-SCREEN | Transactional sanctions screening event detected | Contributes to composite risk indicator |
| R09-PEP-EDD | PEP status — Enhanced Due Diligence required (FATF Rec. 12) | Contributes to composite risk indicator |
| R10-KYC-INCONSIST | Contradictory KYC field combination (e.g. PEP + Low risk rating) | Contributes to composite risk indicator |
| R11-MCC-HIGH-RISK | ≥3 transactions to high-risk MCC merchants | Contributes to composite risk indicator |
| R18-CARD-NO-3DS | ≥3 card-not-present transactions without 3DS authentication | Contributes to composite risk indicator |
| R19-CHARGEBACK | Chargeback history or repeat use of high-chargeback merchants | Contributes to composite risk indicator |
| R20-MERCHANT-CONVERGE | Shared receiving merchant with another flagged subject | Contributes to composite risk indicator |

---

## 3. Detailed Findings

- R$71,406 total outflow vs R$3,943/month declared income (18×)
- PIX passthrough 587% (R$46,554 out / R$7,927 in)
- Anonymization breakdown: {'Proxy': 1, 'VPN': 1}
- KYC inconsistency: PEP=Yes, score=64, risk_rating=Low, tier=L3

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
| M200105 | Card recipient of R$4,390 | Identified during this investigation |
| M200161 | PIX recipient of R$10,558 | Identified during this investigation |
| M200538 | PIX recipient of R$3,376 via Proxy | Identified during this investigation |
| M200818 | Card recipient of R$1,381 | Identified during this investigation |
| M200118 | Card recipient of R$6,975 via VPN | Identified during this investigation |

---

_This report constitutes an internal compliance escalation. Conclusions are based on transactional and KYC data available at preparation time. Final SAR filing determination is subject to Compliance Officer and MLRO review._

_ML confidence labels are calibrated relative to the investigated escalation cohort, not the full customer population._

---

# SUSPICIOUS ACTIVITY REPORT (SAR)

## Case Identification

| Field | Value |
|-------|-------|
| **SAR Reference** | SAR-20260526-041414-4aa919-C102093-01 |
| **Customer ID** | C102093 |
| **Run ID** | 20260526-041414-4aa919 |
| **Prepared At** | 2026-05-26T04:14:37+00:00 |
| **Priority Score** | 62.60 |
| **Severity** | high |
| **Escalation Band** | Tier 1 — SAR immediate |
| **ML Confidence Band** | High |

---

## 1. Executive Summary

PEP-flagged customer (KYC risk score 63/100). declared income R$7,766/yr versus R$192,075 in 30 outflows (≈297× declared monthly income). PIX passthrough ratio 2944%. anonymization events (2 VPN, 1 Tor, 1 Proxy). Activity appears materially inconsistent with the declared customer profile.

---

## 2. Triggered Alerts

| Alert Code | Detection logic | Relevance |
|---|---|---|
| R03-INCOME-MISMATCH | Total outflow >100× declared monthly income | Contributes to composite risk indicator |
| R04-PASSTHRU | PIX outflow-to-inflow ratio >200% | Contributes to composite risk indicator |
| R05-ANON-TOR | Transaction executed via Tor anonymization network | Contributes to composite risk indicator |
| R07-GEO-IP-MISMATCH | IP country differs from declared country (≥2 events) | Contributes to composite risk indicator |
| R09-PEP-EDD | PEP status — Enhanced Due Diligence required (FATF Rec. 12) | Contributes to composite risk indicator |
| R10-KYC-INCONSIST | Contradictory KYC field combination (e.g. PEP + Low risk rating) | Contributes to composite risk indicator |
| R11-MCC-HIGH-RISK | ≥3 transactions to high-risk MCC merchants | Contributes to composite risk indicator |
| R15-FAN-OUT | ≥25 distinct receiving counterparties in review period | Contributes to composite risk indicator |
| R17-MULTI-RAIL | Mixed-rail activity: PIX + Card + Wire within review window | Contributes to composite risk indicator |
| R19-CHARGEBACK | Chargeback history or repeat use of high-chargeback merchants | Contributes to composite risk indicator |
| R20-MERCHANT-CONVERGE | Shared receiving merchant with another flagged subject | Contributes to composite risk indicator |

---

## 3. Detailed Findings

- R$192,075 total outflow vs R$647/month declared income (297×)
- PIX passthrough 2944% (R$113,519 out / R$3,856 in)
- Anonymization breakdown: {'VPN': 2, 'Tor': 1, 'Proxy': 1}
- KYC inconsistency: PEP=Yes, score=63, risk_rating=Low, tier=L2

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
| M200243 | Card recipient of R$15,825 via Tor | Identified during this investigation |
| M200684 | Card recipient of R$3,088 | Identified during this investigation |
| M200989 | PIX recipient of R$28,584 | Identified during this investigation |
| M200067 | PIX recipient of R$12,386 | Identified during this investigation |
| M200446 | Card recipient of R$8,709 | Identified during this investigation |

---

_This report constitutes an internal compliance escalation. Conclusions are based on transactional and KYC data available at preparation time. Final SAR filing determination is subject to Compliance Officer and MLRO review._

_ML confidence labels are calibrated relative to the investigated escalation cohort, not the full customer population._

---

# SUSPICIOUS ACTIVITY REPORT (SAR)

## Case Identification

| Field | Value |
|-------|-------|
| **SAR Reference** | SAR-20260526-041414-4aa919-C102040-01 |
| **Customer ID** | C102040 |
| **Run ID** | 20260526-041414-4aa919 |
| **Prepared At** | 2026-05-26T04:14:37+00:00 |
| **Priority Score** | 60.40 |
| **Severity** | high |
| **Escalation Band** | Tier 1 — SAR immediate |
| **ML Confidence Band** | High |

---

## 1. Executive Summary

PEP-flagged customer (KYC risk score 60/100). declared income R$7,288/yr versus R$61,862 in 17 outflows (≈102× declared monthly income). PIX passthrough ratio 5044%. anonymization events (1 Tor, 1 Proxy). Activity appears materially inconsistent with the declared customer profile.

---

## 2. Triggered Alerts

| Alert Code | Detection logic | Relevance |
|---|---|---|
| R02-STRUCT-BAND | 1–2 transactions in R$9,000–R$10,000 band | Contributes to composite risk indicator |
| R03-INCOME-MISMATCH | Total outflow >100× declared monthly income | Contributes to composite risk indicator |
| R04-PASSTHRU | PIX outflow-to-inflow ratio >200% | Contributes to composite risk indicator |
| R05-ANON-TOR | Transaction executed via Tor anonymization network | Contributes to composite risk indicator |
| R09-PEP-EDD | PEP status — Enhanced Due Diligence required (FATF Rec. 12) | Contributes to composite risk indicator |
| R10-KYC-INCONSIST | Contradictory KYC field combination (e.g. PEP + Low risk rating) | Contributes to composite risk indicator |
| R11-MCC-HIGH-RISK | ≥3 transactions to high-risk MCC merchants | Contributes to composite risk indicator |
| R14-ROOTED-DEVICE | ≥3 transactions from rooted or jailbroken device | Contributes to composite risk indicator |
| R17-MULTI-RAIL | Mixed-rail activity: PIX + Card + Wire within review window | Contributes to composite risk indicator |
| R19-CHARGEBACK | Chargeback history or repeat use of high-chargeback merchants | Contributes to composite risk indicator |
| R20-MERCHANT-CONVERGE | Shared receiving merchant with another flagged subject | Contributes to composite risk indicator |

---

## 3. Detailed Findings

- R$61,862 total outflow vs R$607/month declared income (102×)
- PIX passthrough 5044% (R$43,385 out / R$860 in)
- Anonymization breakdown: {'Tor': 1, 'Proxy': 1}
- KYC inconsistency: PEP=Yes, score=60, risk_rating=Low, tier=L3

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
| M200567 | Card recipient of R$3,343 | Identified during this investigation |
| M200302 | Wire recipient of R$3,474 | Identified during this investigation |
| C100517 | PIX recipient of R$9,292 | Identified during this investigation |
| M200049 | Wire recipient of R$6,349 | Identified during this investigation |
| M200695 | PIX recipient of R$7,031 via Tor | Identified during this investigation |

---

_This report constitutes an internal compliance escalation. Conclusions are based on transactional and KYC data available at preparation time. Final SAR filing determination is subject to Compliance Officer and MLRO review._

_ML confidence labels are calibrated relative to the investigated escalation cohort, not the full customer population._

---

# SUSPICIOUS ACTIVITY REPORT (SAR)

## Case Identification

| Field | Value |
|-------|-------|
| **SAR Reference** | SAR-20260526-041414-4aa919-C101582-01 |
| **Customer ID** | C101582 |
| **Run ID** | 20260526-041414-4aa919 |
| **Prepared At** | 2026-05-26T04:14:37+00:00 |
| **Priority Score** | 59.69 |
| **Severity** | critical |
| **Escalation Band** | Tier 1 — Hard alert |
| **ML Confidence Band** | Moderate |

---

## 1. Executive Summary

Customer with KYC risk score 73/100. declared income R$10,907/yr versus R$89,473 in 23 outflows (≈98× declared monthly income). anonymization events (2 Tor). Activity appears materially inconsistent with the declared customer profile.

---

## 2. Triggered Alerts

| Alert Code | Detection logic | Relevance |
|---|---|---|
| R03-INCOME-MISMATCH | Total outflow >50× declared monthly income | Contributes to composite risk indicator |
| R05-ANON-TOR | Transaction executed via Tor anonymization network | Contributes to composite risk indicator |
| R08-SANCTIONS-SCREEN | Transactional sanctions screening event detected | Contributes to composite risk indicator |
| R11-MCC-HIGH-RISK | ≥3 transactions to high-risk MCC merchants | Contributes to composite risk indicator |
| R17-MULTI-RAIL | Mixed-rail activity: PIX + Card + Wire within review window | Contributes to composite risk indicator |
| R19-CHARGEBACK | Chargeback history or repeat use of high-chargeback merchants | Contributes to composite risk indicator |
| R20-MERCHANT-CONVERGE | Shared receiving merchant with another flagged subject | Contributes to composite risk indicator |

---

## 3. Detailed Findings

- R$89,473 total outflow vs R$909/month declared income (98×)
- Anonymization breakdown: {'Tor': 2}

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
| M200966 | PIX recipient of R$506 | Identified during this investigation |
| M200696 | PIX recipient of R$13,310 via Tor | Identified during this investigation |
| M200449 | Card recipient of R$454 | Identified during this investigation |
| M200390 | Card recipient of R$3,295 | Identified during this investigation |
| C101819 | Card recipient of R$7,454 | Identified during this investigation |

---

_This report constitutes an internal compliance escalation. Conclusions are based on transactional and KYC data available at preparation time. Final SAR filing determination is subject to Compliance Officer and MLRO review._

_ML confidence labels are calibrated relative to the investigated escalation cohort, not the full customer population._

---

# SUSPICIOUS ACTIVITY REPORT (SAR)

## Case Identification

| Field | Value |
|-------|-------|
| **SAR Reference** | SAR-20260526-041414-4aa919-C101542-01 |
| **Customer ID** | C101542 |
| **Run ID** | 20260526-041414-4aa919 |
| **Prepared At** | 2026-05-26T04:14:37+00:00 |
| **Priority Score** | 57.42 |
| **Severity** | high |
| **Escalation Band** | Tier 1 — Hard alert |
| **ML Confidence Band** | Moderate-High |

---

## 1. Executive Summary

Customer with KYC risk score 59/100. declared income R$3,687/yr versus R$103,287 in 28 outflows (≈336× declared monthly income). PIX passthrough ratio 751%. anonymization events (1 Tor, 1 Proxy, 1 VPN). Activity appears materially inconsistent with the declared customer profile.

---

## 2. Triggered Alerts

| Alert Code | Detection logic | Relevance |
|---|---|---|
| R03-INCOME-MISMATCH | Total outflow >100× declared monthly income | Contributes to composite risk indicator |
| R04-PASSTHRU | PIX outflow-to-inflow ratio >200% | Contributes to composite risk indicator |
| R05-ANON-TOR | Transaction executed via Tor anonymization network | Contributes to composite risk indicator |
| R11-MCC-HIGH-RISK | ≥3 transactions to high-risk MCC merchants | Contributes to composite risk indicator |
| R15-FAN-OUT | ≥25 distinct receiving counterparties in review period | Contributes to composite risk indicator |
| R17-MULTI-RAIL | Mixed-rail activity: PIX + Card + Wire within review window | Contributes to composite risk indicator |
| R19-CHARGEBACK | Chargeback history or repeat use of high-chargeback merchants | Contributes to composite risk indicator |
| R20-MERCHANT-CONVERGE | Shared receiving merchant with another flagged subject | Contributes to composite risk indicator |
| R21-NETWORK-LINK | Direct wire transfer to another flagged subject | Contributes to composite risk indicator |

---

## 3. Detailed Findings

- R$103,287 total outflow vs R$307/month declared income (336×)
- PIX passthrough 751% (R$73,949 out / R$9,844 in)
- Anonymization breakdown: {'Tor': 1, 'Proxy': 1, 'VPN': 1}

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
| M200841 | PIX recipient of R$3,104 | Identified during this investigation |
| M200971 | PIX recipient of R$5,761 via Tor | Identified during this investigation |
| M200260 | Card recipient of R$6,530 | Identified during this investigation |
| C100375 | Wire recipient of R$1,424 | Identified during this investigation |
| M200966 | PIX recipient of R$25,849 | Identified during this investigation |

---

_This report constitutes an internal compliance escalation. Conclusions are based on transactional and KYC data available at preparation time. Final SAR filing determination is subject to Compliance Officer and MLRO review._

_ML confidence labels are calibrated relative to the investigated escalation cohort, not the full customer population._

---

# SUSPICIOUS ACTIVITY REPORT (SAR)

## Case Identification

| Field | Value |
|-------|-------|
| **SAR Reference** | SAR-20260526-041414-4aa919-C100208-01 |
| **Customer ID** | C100208 |
| **Run ID** | 20260526-041414-4aa919 |
| **Prepared At** | 2026-05-26T04:14:37+00:00 |
| **Priority Score** | 56.95 |
| **Severity** | high |
| **Escalation Band** | Tier 1 — Hard alert |
| **ML Confidence Band** | Moderate-High |

---

## 1. Executive Summary

Customer with KYC risk score 89/100. declared income R$8,756/yr versus R$144,242 in 22 outflows (≈198× declared monthly income). PIX passthrough ratio 3675%. anonymization events (1 Tor, 1 Proxy, 1 VPN). Activity appears materially inconsistent with the declared customer profile.

---

## 2. Triggered Alerts

| Alert Code | Detection logic | Relevance |
|---|---|---|
| R03-INCOME-MISMATCH | Total outflow >100× declared monthly income | Contributes to composite risk indicator |
| R04-PASSTHRU | PIX outflow-to-inflow ratio >200% | Contributes to composite risk indicator |
| R05-ANON-TOR | Transaction executed via Tor anonymization network | Contributes to composite risk indicator |
| R06-GEO-HIGH-RISK | Cross-border activity involving high-risk jurisdiction | Contributes to composite risk indicator |
| R10-KYC-INCONSIST | Contradictory KYC field combination (e.g. PEP + Low risk rating) | Contributes to composite risk indicator |
| R11-MCC-HIGH-RISK | ≥3 transactions to high-risk MCC merchants | Contributes to composite risk indicator |
| R17-MULTI-RAIL | Mixed-rail activity: PIX + Card + Wire within review window | Contributes to composite risk indicator |
| R20-MERCHANT-CONVERGE | Shared receiving merchant with another flagged subject | Contributes to composite risk indicator |
| R21-NETWORK-LINK | Direct wire transfer to another flagged subject | Contributes to composite risk indicator |

---

## 3. Detailed Findings

- R$144,242 total outflow vs R$730/month declared income (198×)
- PIX passthrough 3675% (R$55,600 out / R$1,513 in)
- Anonymization breakdown: {'Tor': 1, 'Proxy': 1, 'VPN': 1}

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
| M200392 | PIX recipient of R$18,916 | Identified during this investigation |
| M200535 | Card recipient of R$51,589 | Identified during this investigation |
| C102252 | Wire recipient of R$1,665 | Identified during this investigation |
| M200042 | Card recipient of R$22,284 | Identified during this investigation |
| C100814 | PIX recipient of R$3,411 via Tor | Identified during this investigation |

---

_This report constitutes an internal compliance escalation. Conclusions are based on transactional and KYC data available at preparation time. Final SAR filing determination is subject to Compliance Officer and MLRO review._

_ML confidence labels are calibrated relative to the investigated escalation cohort, not the full customer population._