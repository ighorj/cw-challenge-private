# SUSPICIOUS ACTIVITY REPORT (SAR)

## Case Identification

| Field | Value |
|-------|-------|
| **SAR Reference** | SAR-20260524-000149-48074c-C100091-01 |
| **Customer ID** | C100091 |
| **Run ID** | 20260524-000149-48074c |
| **Prepared At** | 2026-05-24 |
| **Priority Score** | 80.46 |
| **Severity** | critical |
| **Escalation Band** | Tier 1 — Hard alert |
| **ML Confidence Band** | Moderate-High |

---

## 1. Executive Summary

Customer C100091, a declared Store Owner with annual income of R$10,173, exhibited total outflows of R$91,349.77 during the review period—approximately 898× the monthly income equivalent (R$847.75/mo), which appears materially inconsistent with the stated economic profile. A wire transfer of R$11,672.88 to counterparty M200363 in Iran (IR) on 2025-08-07 triggered a transactional sanctions screening event requiring entity-level review. The PIX passthrough ratio of 4,008.5% (R$57,117.34 outflow vs R$1,424.90 inflow) may warrant further review for potential layering activity. Mixed-rail activity across PIX, Wire, and Card channels, combined with high-risk MCC transactions (gambling MCC 7995, financial institution MCC 6011), network linkage to flagged customer C100236, and cross-border transactions to high-risk jurisdictions, collectively suggest a pattern potentially consistent with structured fund movement warranting immediate SAR filing.

---

## 2. Triggered Alerts

| Alert Code | Detection Logic | Relevance |
|---|---|---|
| R03_HIGH | [R03-INCOME-MISMATCH] Total outflow >100× declared monthly income | Primary quantitative indicator of funds inconsistent with declared economic profile |
| R04 | [R04-PASSTHRU] PIX outflow-to-inflow ratio >200% | May indicate potential layering or pass-through activity |
| R08 | [R08-SANCTIONS-SCREEN] Transactional sanctions screening event | Wire transfer to Iran-based counterparty requires immediate entity-level review |
| R06 | [R06-GEO-HIGH-RISK] Cross-border to high-risk jurisdiction | Iran transaction presents elevated jurisdictional risk |
| R02_LOW | [R02-STRUCT-BAND] Transactions in R$9,000–R$10,000 band | May indicate potential structuring behavior near reporting thresholds |
| R11 | [R11-MCC-HIGH-RISK] ≥3 transactions to high-risk MCC merchants | High-risk merchant categories associated with ML vulnerabilities |
| R17 | [R17-MULTI-RAIL] Mixed-rail: PIX + Card + Wire within window | Multi-channel activity may indicate attempt to obscure transaction trail |
| R21 | [R21-NETWORK-LINK] Direct wire to another flagged subject | Network connection to another subject under review |
| R19 | [R19-CHARGEBACK] Chargeback history or high-CB merchant use | Elevated fraud risk indicator |
| R20 | [R20-MERCHANT-CONVERGE] Shared merchant with another flagged subject | Potential network convergence pattern |

---

## 3. Detailed Findings

- Total outflow of R$91,349.77 during the review period represents approximately 898× the declared monthly income of R$847.75 (annual income R$10,173), appearing materially inconsistent with the customer's stated occupation as Store Owner.
- Wire transfer TJRKHTP81JROK dated 2025-08-07 for R$11,672.88 to counterparty M200363 in Iran (IR) triggered a transactional sanctions screening event requiring entity-level review.
- PIX passthrough ratio of 4,008.5% (R$57,117.34 outflow vs R$1,424.90 inflow) may warrant further review for potential layering activity.
- Transaction TLF007IGRTEAB dated 2025-07-15 for R$9,732.08 to M200985 falls within the R$9,000–R$10,000 structuring band.
- Wire transfer TMGHPD5XFHXCJ dated 2025-07-18 for R$1,255.77 to customer C100236 triggered network linkage rule, as C100236 is a flagged subject.
- PIX transaction T1RBG8O7Y6NC6 dated 2025-07-09 for R$7,680.48 to C100179 involved MCC 7995 (gambling), a high-risk merchant category.
- Card transaction TJZQI83ROKQ81 dated 2025-10-03 for R$11,591.32 to M200233 involved MCC 6011 (financial institution/ATM), a high-risk merchant category.
- Cross-border activity included 3 events: Iran (tx TJRKHTP81JROK, R$11,672.88), Germany (tx TQWXFJ3VKTJO0, R$540.93), and Spain (tx TGWER3C1MRCSR, R$4,987.69).
- Mixed-rail activity observed: 2 wire transfers, multiple PIX transactions, and Card transactions during the review period across 18 distinct counterparties.
- ML confidence band assessed as Moderate-High; customer KYC risk score of 66 with L2 KYC tier and Low risk rating inconsistent with observed transactional behavior.

---

## 4. Regulatory Basis

- FATF Recommendation 20 — Reporting of suspicious transactions
- FATF Recommendation 10 — Customer due diligence and ongoing monitoring
- Circular BACEN 3.978/2020 — AML/CFT policies and procedures for financial institutions
- COAF Instruction 1/2014 — Mandatory SAR filing for suspicious activity indicators
- UN Security Council Resolutions — Iran-related sanctions compliance

---

## 5. Recommended Actions

1. File SAR with COAF immediately citing income-transaction disparity, sanctions screening event, and network linkage
2. Escalate sanctions screening event on counterparty M200363 (Iran) for entity-level OFAC/UN sanctions verification
3. Initiate Enhanced Due Diligence: request source of funds documentation for transactions exceeding declared income capacity
4. Conduct KYC refresh including updated income verification and beneficial ownership review
5. Apply enhanced monitoring tier with 30-day transaction review cycle
6. Investigate network linkage with flagged customer C100236 for potential coordinated activity
7. Review high-risk MCC transactions (gambling, financial institution) for underlying business purpose

---

## 6. Linked Entities

| Entity | Relationship | Status |
|---|---|---|
| M200363 | Wire recipient in sanctioned jurisdiction (Iran) | Pending entity-level sanctions verification |
| C100236 | Wire transfer recipient flagged under R21 network linkage | Flagged subject — coordinated review recommended |
| C100179 | PIX counterparty receiving high-risk MCC payment (gambling) | Pending merchant/counterparty review |
| M200796 | Largest single PIX recipient (R$18,507.97) | Pending merchant review |
| M200233 | High-risk MCC card recipient (MCC 6011 financial institution) | Pending merchant review |

---

# SUSPICIOUS ACTIVITY REPORT (SAR)

## Case Identification

| Field | Value |
|-------|-------|
| **SAR Reference** | SAR-20260524-000149-48074c-C101208-01 |
| **Customer ID** | C101208 |
| **Run ID** | 20260524-000149-48074c |
| **Prepared At** | 2026-05-24 |
| **Priority Score** | 74.39 |
| **Severity** | critical |
| **Escalation Band** | Tier 1 — Hard alert |
| **ML Confidence Band** | Moderate |

---

## 1. Executive Summary

Subject C101208, declared occupation Chef with annual income of R$13,047, exhibited total outflow of R$150,178.09 during the review period, representing approximately 1,150% of annual declared income and triggering R03_HIGH (>100× monthly income threshold). Activity involved 29 transactions to 29 distinct counterparties (R15), mixed-rail usage across PIX, Card, and Wire channels (R17), 2 VPN anonymization events (R05_VPN), and 1 transactional sanctions screening event involving a Wire transfer of R$2,166.18 to counterparty M200815 in Syria (R08). Cross-border activity spanned jurisdictions including Syria, Russia, Yemen, Portugal, and the United Kingdom, with high-risk MCC 7995 (gambling) transactions totaling R$20,901.35. The convergence of severe income mismatch, sanctions screening event, anonymization indicators, and high-risk merchant activity presents a pattern potentially consistent with layered fund movement warranting immediate SAR filing.

---

## 2. Triggered Alerts

| Alert Code | Detection Logic | Relevance |
|---|---|---|
| R03-INCOME-MISMATCH | Total outflow >100× declared monthly income | Primary quantitative indicator — R$150,178.09 outflow vs R$13,047 annual declared income |
| R08-SANCTIONS-SCREEN | Transactional sanctions screening event | Wire R$2,166.18 to counterparty M200815 in Syria — transactional screening event requiring review |
| R05-ANON-VPN | ≥2 transactions via VPN or proxy service | 2 VPN anonymization events: tx TJZRYWR88WZHJ (PIX R$1,241.06) and tx TQSBX6QW4LBWX (Card R$1,089.07 to Russia) |
| R11-MCC-HIGH-RISK | ≥3 transactions to high-risk MCC merchants | MCC 7995 (gambling) transactions including R$6,889.49 to Yemen and R$14,011.86 domestically |
| R15-FAN-OUT | ≥25 distinct receiving counterparties | Funds dispersed across 29 distinct recipients during review period |
| R17-MULTI-RAIL | Mixed-rail: PIX + Card + Wire within window | Activity across PIX (R$77,634.56), Card, and Wire (3 transfers totaling R$21,444.38) |
| R18-CNP-NO-3DS | ≥3 CNP transactions without 3DS authentication | Card-not-present transactions lacking strong customer authentication |
| R19-CHARGEBACK | Chargeback history or high-CB merchant use | Chargeback indicators detected in transaction pattern |
| R20-MERCHANT-CONVERGE | Shared merchant with another flagged subject | Merchant convergence with another flagged subject — potential network linkage |

---

## 3. Detailed Findings

- Total outflow of R$150,178.09 against declared annual income of R$13,047 (occupation: Chef) represents approximately 1,150% of annual income, a disparity materially inconsistent with stated economic profile (R03_HIGH).
- Transactional sanctions screening event on 2025-08-12: tx TNHZDN7D6LYK6, Wire R$2,166.18 to counterparty M200815 in Syria (geo_country: SY), MCC 5999, sanctions_hit=true (R08).
- Two VPN anonymization events detected: tx TJZRYWR88WZHJ on 2025-07-22 (PIX R$1,241.06 to M200526 in Portugal) and tx TQSBX6QW4LBWX on 2025-08-29 (Card R$1,089.07 to M200972 in Russia), both flagged ip_anon=VPN (R05_VPN).
- High-risk MCC 7995 (gambling) activity: tx TOHDJ4A6OYGZA on 2025-09-08, Card R$6,889.49 to M200212 in Yemen; tx TIQS2U9KT1J0U on 2025-09-23, Card R$14,011.86 to M200637 in Brazil (R11).
- 29 transactions distributed across 29 distinct counterparties during review period, exceeding R15 fan-out threshold of 25 recipients.
- Mixed-rail activity: PIX outflow R$77,634.56 (with R$0.00 inflow), 3 wire transfers totaling R$21,444.38 to counterparties in Syria (M200815), United Kingdom (M200524), and Portugal (M200962), plus card transactions (R17).
- 9 cross-border events spanning Portugal (PT), Syria (SY), United Kingdom (GB), Russia (RU), and Yemen (YE).
- Largest single wire transfer: tx T01OIP42LWSQO on 2025-09-17, R$17,044.10 to counterparty M200962 in Portugal, MCC 5999.
- R20 (merchant convergence) triggered indicating shared receiving merchant with another flagged subject — specific linked subject ID not disclosed in evidence bundle.
- R18 and R19 triggered: card-not-present transactions without 3DS authentication and chargeback indicators present.

---

## 4. Regulatory Basis

- FATF Recommendation 20 — Suspicious Transaction Reporting obligation
- FATF Recommendation 6 — Targeted Financial Sanctions (Syria nexus)
- Circular BACEN 3.978/2020 Art. 27 — SAR filing criteria for activity inconsistent with economic profile
- COAF Instruction 40/2021 — Mandatory reporting of transactions involving high-risk jurisdictions
- COAF Resolution 36/2021 — Enhanced monitoring for sanctions screening events
- Lei 9.613/1998 Art. 11 — Obligation to report suspicious transactions to competent authorities

---

## 5. Recommended Actions

1. Submit SAR to COAF within regulatory timeframe citing R08 (sanctions screening event), R03_HIGH (income mismatch), and R05_VPN (anonymization)
2. Initiate Enhanced Due Diligence (EDD): request documented source of funds for R$150,178.09 outflow and justification for Syria-bound wire transfer
3. Escalate counterparty M200815 (Syria) for entity-level sanctions review and potential relationship termination assessment
4. Place account under enhanced transaction monitoring with real-time alerts for additional Syria/Russia/Yemen activity
5. Request KYC refresh including updated income documentation and employment verification given declared Chef occupation vs observed transaction volume
6. Conduct network analysis on R20 merchant convergence to identify potential coordinated activity with other flagged subjects
7. Review cross-border wire activity to Portugal (M200962, M200526) and United Kingdom (M200524) for economic rationale

---

## 6. Linked Entities

| Entity | Relationship | Status |
|---|---|---|
| M200815 | wire recipient with transactional sanctions screening hit (Syria) | pending entity-level sanctions review |
| M200962 | largest single wire recipient (Portugal) | pending EDD review |
| M200637 | high-risk MCC 7995 recipient (gambling, Brazil) | flagged for merchant review |
| M200212 | high-risk MCC 7995 recipient (gambling, Yemen) | flagged for merchant and jurisdiction review |
| M200972 | VPN anonymization event recipient (Russia) | flagged for enhanced monitoring |
| unknown | shared merchant convergence (R20) — linked flagged subject | pending network identification |

---

# SUSPICIOUS ACTIVITY REPORT (SAR)

## Case Identification

| Field | Value |
|-------|-------|
| **SAR Reference** | SAR-20260524-000149-48074c-C101028-01 |
| **Customer ID** | C101028 |
| **Run ID** | 20260524-000149-48074c |
| **Prepared At** | 2026-05-24 |
| **Priority Score** | 74.36 |
| **Severity** | critical |
| **Escalation Band** | Tier 1 — Hard alert |
| **ML Confidence Band** | Moderate |

---

## 1. Executive Summary

Customer C101028 presents a confirmed KYC-level sanctions list match combined with PEP status, triggering immediate regulatory review obligations under FATF Recommendation 12 and COAF filing requirements. The account exhibits a PIX passthrough ratio of 587.3% (R$46,553.76 outflow vs R$7,927.19 inflow) and total outflow of R$71,406.40 against declared annual income of R$47,312, representing approximately 151% of stated income and appearing materially inconsistent with the declared Designer occupation. Two anonymization events (1 VPN, 1 Proxy) and cross-border activity including a Card transaction of R$4,390.02 to North Korea (KP) on 2025-07-01 compound the risk profile. Nine concurrent rule triggers across five typology families—passthrough, anonymization, sanctions/PEP, merchant risk, and card/e-commerce—warrant immediate SAR filing and Enhanced Due Diligence review.

---

## 2. Triggered Alerts

| Alert Code | Detection Logic | Relevance |
|---|---|---|
| R08 | [R08-SANCTIONS-SCREEN] Confirmed KYC-level sanctions list match | Primary hard alert trigger requiring immediate regulatory action |
| R09 | [R09-PEP-EDD] PEP status — Enhanced Due Diligence required | Mandatory EDD trigger per FATF Recommendation 12 |
| R04 | [R04-PASSTHRU] PIX outflow-to-inflow ratio >200% | Potentially consistent with funds passthrough or layering activity |
| R05_VPN | [R05-ANON-VPN] ≥2 transactions via VPN or proxy service | Anonymization may warrant review for transaction origin obfuscation |
| R10 | [R10-KYC-INCONSIST] Contradictory KYC field combination | Internal control gap requiring remediation |
| R11 | [R11-MCC-HIGH-RISK] ≥3 transactions to high-risk MCC merchants | High-risk merchant categories including securities/brokers and financial institutions |
| R18 | [R18-CNP-RISK] Card-not-present transaction risk indicator | Elevated CNP fraud risk profile |
| R19 | [R19-CHARGEBACK] Chargeback history or high-CB merchant use | Chargeback risk potentially consistent with dispute patterns |
| R20 | [R20-MERCHANT-CONVERGE] Shared merchant with another flagged subject | Network linkage may warrant coordinated review |

---

## 3. Detailed Findings

- Confirmed KYC-level sanctions list match (sanctions_status.confirmed_sanctions_match: true) combined with PEP status (kyc.pep: 'Yes') creates dual regulatory obligation for immediate SAR filing and Enhanced Due Diligence.
- Total outflow of R$71,406.40 across 18 transactions to 18 distinct counterparties against declared annual income of R$47,312 (151% of annual income) appears materially inconsistent with stated Designer occupation.
- PIX passthrough ratio of 587.3% (R$46,553.76 outflow vs R$7,927.19 inflow) may be potentially consistent with funds layering or passthrough activity patterns.
- Cross-border Card transaction TFNO8A1FBZUMA dated 2025-07-01 for R$4,390.02 to counterparty M200105 in North Korea (KP), MCC 4789, represents high-risk jurisdiction exposure.
- Two anonymization events detected: (1) VPN-routed Card transaction TQXICCVPO421G dated 2025-07-08 for R$6,975.17 to M200118, MCC 6011; (2) Proxy-routed PIX transaction TCTY4DMIEFHUU dated 2025-07-03 for R$3,376.31 to M200538, MCC 6011.
- High-risk MCC activity includes Card transaction THYRFBT3SQ4RJ dated 2025-07-05 for R$1,381.46 to M200818 (MCC 6211 Securities/Brokers) and Card transaction TKFJIS94Y7C0I dated 2025-08-11 for R$4,317.90 to M200980 (MCC 4111).
- KYC inconsistency (R10 trigger): Customer carries 'Low' risk_rating despite confirmed sanctions match and PEP status, indicating potential control gap in risk rating assignment.
- Card transaction T4DASTQ56M2QJ dated 2025-07-17 for R$3,969.08 to customer C100265 flagged with rooted_device tag, potentially consistent with compromised device risk.
- Additional cross-border Card transaction THCF7RXE8PSWC dated 2025-09-12 for R$1,135.20 to counterparty M200386 in Germany (DE), MCC 4829.

---

## 4. Regulatory Basis

- FATF Recommendation 12 — Enhanced Due Diligence for Politically Exposed Persons
- FATF Recommendation 6 — Targeted Financial Sanctions related to terrorism and terrorist financing
- Circular BACEN 3.978/2020 — AML/CFT procedures for financial institutions
- COAF Resolution 40/2021 — Suspicious activity reporting obligations
- Lei 9.613/1998 — Brazilian Anti-Money Laundering Law, Art. 11 reporting requirement
- Circular BACEN 4.001/2020 — Sanctions compliance procedures

---

## 5. Recommended Actions

1. File SAR with COAF immediately citing confirmed sanctions match and PEP status as primary triggers
2. Initiate Enhanced Due Diligence review: request documented source of funds for outflows totaling R$71,406.40
3. Escalate to Sanctions/Compliance team for confirmed KYC-level sanctions match assessment and potential account restriction
4. Remediate R10 KYC inconsistency: review and correct risk_rating from 'Low' given PEP status and sanctions match
5. Request beneficial ownership documentation and verify stated Designer occupation income reasonableness
6. Place account under enhanced transaction monitoring with reduced alert thresholds
7. Review linked merchant M200161 (received R$10,557.78 via PIX) and R20-flagged shared merchant for coordinated suspicious activity
8. Consider voluntary information sharing with regulatory authorities regarding North Korea (KP) cross-border transaction

---

## 6. Linked Entities

| Entity | Relationship | Status |
|---|---|---|
| M200161 | Largest single PIX recipient (R$10,557.78) | pending merchant review |
| M200105 | Cross-border recipient in North Korea (KP) (R$4,390.02) | high-risk jurisdiction — requires escalation |
| M200818 | High-risk MCC 6211 recipient (R$1,381.46) | pending merchant review |
| M200538 | MCC 6011 recipient via Proxy anonymization (R$3,376.31) | pending merchant review |
| M200118 | MCC 6011 recipient via VPN anonymization (R$6,975.17) | pending merchant review |
| C100265 | P2P transfer recipient with rooted device (R$3,969.08) | pending customer review |
| shared_merchant_R20 | R20 merchant convergence with another flagged subject | pending coordinated review |

---

# SUSPICIOUS ACTIVITY REPORT (SAR)

## Case Identification

| Field | Value |
|-------|-------|
| **SAR Reference** | SAR-20260524-000149-48074c-C100837-01 |
| **Customer ID** | C100837 |
| **Run ID** | 20260524-000149-48074c |
| **Prepared At** | 2026-05-24 |
| **Priority Score** | 67.40 |
| **Severity** | high |
| **Escalation Band** | Tier 1 — SAR immediate |
| **ML Confidence Band** | Very High |

---

## 1. Executive Summary

Customer C100837, a confirmed Politically Exposed Person (PEP) with declared annual income of R$7,577, exhibited total outflow of R$139,083.50 across 29 transactions during the review period, representing approximately 18× annual income and potentially consistent with income mismatch typology. PIX passthrough ratio of 4,367% (R$104,965.61 outflow versus R$2,403.44 inflow) may warrant review for potential layering activity. One transaction (T4VUTEFNQBUQH, R$2,782.76) was executed via Tor anonymization network, and six cross-border events were detected including activity to Myanmar (MM), a FATF high-risk jurisdiction. The convergence of PEP status, extreme income-outflow disparity, anonymization usage, high-risk jurisdiction activity, and mixed-rail transaction patterns across 27 distinct counterparties presents materially concerning indicators warranting immediate SAR filing.

---

## 2. Triggered Alerts

| Alert Code | Detection Logic | Relevance |
|---|---|---|
| R03-INCOME-MISMATCH | Total outflow >100× declared monthly income | Primary quantitative indicator of potential undeclared income sources |
| R04-PASSTHRU | PIX outflow-to-inflow ratio >200% | Potentially consistent with layering or pass-through activity |
| R05-ANON-TOR | Transaction via Tor anonymization network | May indicate intent to obscure transaction origin |
| R06-GEO-HIGH-RISK | Cross-border to high-risk jurisdiction | Myanmar is FATF-identified high-risk jurisdiction |
| R09-PEP-EDD | PEP status — Enhanced Due Diligence required | Regulatory requirement for enhanced monitoring and source of funds verification |
| R10-KYC-INCONSIST | Contradictory KYC field combination | Transaction volume appears materially inconsistent with declared occupation and income |
| R11-MCC-HIGH-RISK | ≥3 transactions to high-risk MCC merchants | MCCs associated with value transfer and cash-equivalent instruments |
| R15-FAN-OUT | ≥25 distinct receiving counterparties | Potentially consistent with structuring or distribution patterns |
| R17-MULTI-RAIL | Mixed-rail: PIX + Card + Wire within window | May indicate efforts to diversify transaction pathways |
| R19-CHARGEBACK | Chargeback history or high-CB merchant use | May warrant review for transaction integrity |
| R20-MERCHANT-CONVERGE | Shared merchant with another flagged subject | Potential network linkage requiring further investigation |

---

## 3. Detailed Findings

- Customer C100837 total outflow of R$139,083.50 across 29 transactions represents approximately 18× declared annual income of R$7,577, potentially consistent with income mismatch typology (R03_HIGH triggered).
- PIX passthrough ratio of 4,367% calculated from R$104,965.61 PIX outflow versus R$2,403.44 PIX inflow may warrant review for potential layering activity (R04 triggered).
- Transaction T4VUTEFNQBUQH on 2025-08-04 for R$2,782.76 to counterparty M200806 (MCC 5812) was executed via Tor anonymization network (R05_TOR triggered).
- Card transaction TT94KQ67Q0Q92 on 2025-07-22 for R$1,361.82 to counterparty M200684 in Myanmar (MM), a FATF-identified high-risk jurisdiction (R06 triggered).
- Five wire transfers detected to international destinations: R$12,957.12 to M200053 (GB) on 2025-08-01 via tx T4MHTBYMYYY0C; R$1,702.86 to M200513 (US) on 2025-07-08 via tx TPCPL90MU9SRF; R$1,746.42 to M200849 (DE) on 2025-08-07 via tx TDU1GAYIB8X9S.
- Largest single transaction: PIX transfer TTP6ORO2Q3V22 on 2025-08-20 for R$27,304.70 to counterparty M200309 (MCC 4829 wire transfer services).
- Card transaction TPTMR0FBGXQOB on 2025-08-18 for R$1,142.06 to counterparty M200004 (MCC 6051 quasi-cash) executed from device flagged as rooted.
- Customer confirmed as Politically Exposed Person (PEP) with KYC risk score of 59 (Medium rating), L2 KYC tier, declared occupation Accountant.
- ML confidence band: Very High; ML cohort rank: 2; Escalation band: Tier 1 — SAR immediate.
- 27 distinct counterparties identified across 29 transactions during review period (R15 fan-out triggered).

---

## 4. Regulatory Basis

- FATF Recommendation 12 — Enhanced Due Diligence requirements for Politically Exposed Persons
- FATF Recommendation 19 — Higher-risk countries including Myanmar (MM) on FATF high-risk jurisdiction list
- Circular BACEN 3.978/2020 — AML/CFT procedures for financial institutions including transaction monitoring and SAR filing obligations
- COAF Resolution 40/2021 — SAR filing requirements for suspicious activity indicators
- COAF Normative Instruction — Reporting obligations for transactions inconsistent with customer profile

---

## 5. Recommended Actions

1. Submit SAR to COAF within regulatory timeframe citing converging indicators across 12 triggered detection rules
2. Initiate Enhanced Due Diligence review for PEP customer including formal request for source of funds documentation
3. Escalate to enhanced transaction monitoring tier with real-time alerting
4. Request updated KYC documentation to reconcile declared income with observed transaction volumes
5. Conduct counterparty analysis on M200309 (largest PIX recipient) and M200806 (Tor-anonymized transaction recipient)
6. Review merchant M200684 (Myanmar counterparty) for potential sanctions or adverse media indicators
7. Consider account activity restrictions pending EDD completion

---

## 6. Linked Entities

| Entity | Relationship | Status |
|---|---|---|
| M200309 | largest single PIX recipient (R$27,304.70) | pending counterparty review |
| M200053 | largest wire recipient (R$12,957.12 to GB) | pending counterparty review |
| M200806 | Tor-anonymized transaction recipient | requires enhanced review |
| M200684 | high-risk jurisdiction counterparty (Myanmar) | requires sanctions and adverse media screening |
| M200004 | quasi-cash MCC recipient (MCC 6051) | pending merchant review |

---

# SUSPICIOUS ACTIVITY REPORT (SAR)

## Case Identification

| Field | Value |
|-------|-------|
| **SAR Reference** | SAR-20260524-000149-48074c-C101582-01 |
| **Customer ID** | C101582 |
| **Run ID** | 20260524-000149-48074c |
| **Prepared At** | 2026-05-24 |
| **Priority Score** | 66.96 |
| **Severity** | critical |
| **Escalation Band** | Tier 1 — Hard alert |
| **ML Confidence Band** | Moderate-High |

---

## 1. Executive Summary

Customer C101582 presents a confirmed KYC-level sanctions list match requiring immediate regulatory notification. The account exhibits total outflow of R$89,473.16 against declared annual income of R$10,907 (approximately 8.2× annual income, triggering the R03_LOW threshold of >50× monthly income). Two distinct Tor anonymization events were detected on 2025-07-15 (R$13,310.35) and 2025-09-08 (R$3,328.57), potentially consistent with deliberate identity obfuscation. Cross-border activity includes a transaction to Iraq (high-risk jurisdiction) on 2025-08-21 for R$3,294.89 via MCC 6051 (quasi-cash), and mixed-rail usage across PIX, Card, and Wire channels warrants further review for layering typology. The convergence of sanctions exposure, income mismatch, anonymization, and high-risk merchant activity across 7 triggered rules supports immediate SAR filing.

---

## 2. Triggered Alerts

| Alert Code | Detection Logic | Relevance |
|---|---|---|
| R08-SANCTIONS-SCREEN | Confirmed KYC-level sanctions list match (sanctions_status.confirmed_sanctions_match: true) | Primary regulatory trigger requiring immediate escalation |
| R03-INCOME-MISMATCH | Total outflow >50× declared monthly income | Quantitative indicator of funds inconsistent with declared economic profile |
| R05-ANON-TOR | Transaction via Tor anonymization network | Identity obfuscation potentially consistent with illicit fund movement |
| R11-MCC-HIGH-RISK | ≥3 transactions to high-risk MCC merchants | Merchant categories associated with value transfer and cash-equivalent services |
| R17-MULTI-RAIL | Mixed-rail: PIX + Card + Wire within window | Multi-channel activity potentially consistent with layering techniques |
| R19-CHARGEBACK | Chargeback history or high-CB merchant use | Potential fraud or merchant risk exposure |
| R20-MERCHANT-CONVERGE | Shared merchant with another flagged subject | Network linkage to customer C101819 warrants coordinated review |

---

## 3. Detailed Findings

- Confirmed KYC-level sanctions list match per kyc.sanctions_status.confirmed_sanctions_match field; severity classified as 'confirmed' requiring immediate regulatory notification under COAF guidelines.
- Total outflow R$89,473.16 across 23 transactions against declared annual income of R$10,907 (occupation: Nurse) represents approximately 8.2× annual income or ~98× monthly income, materially inconsistent with stated economic profile.
- Two Tor anonymization network events: tx T1UADPDDHFJPA on 2025-07-15 for R$13,310.35 to counterparty M200696 (MCC 4111) and tx T4P4Q65XC570F on 2025-09-08 for R$3,328.57 to counterparty M200797 (MCC 4829).
- Cross-border Card transaction tx T1XY2A460O51H on 2025-08-21 for R$3,294.89 to counterparty M200390 in Iraq (IQ), a high-risk jurisdiction, via MCC 6051 (quasi-cash category).
- Mixed-rail activity confirmed: PIX outflow R$46,573.94, multiple Card transactions, and Wire transfer tx TMBR17QPP9GD3 on 2025-09-21 for R$24,230.02 to counterparty M200508.
- High-risk MCC activity: tx TF8F0668QXDKJ on 2025-07-05 for R$506.42 to MCC 4900 (utilities) and tx TOYX9MA23Q8NW on 2025-08-25 for R$7,454.37 to MCC 4900.
- Merchant convergence with flagged customer C101819 via tx TOYX9MA23Q8NW on 2025-08-25 (R$7,454.37, MCC 4900), triggering R20 network analysis requirement.
- Account exhibits 22 distinct counterparties across 23 transactions, with ML confidence band classified as Moderate-High and escalation status as Tier 1 — Hard alert.

---

## 4. Regulatory Basis

- FATF Recommendation 6 — Targeted Financial Sanctions (confirmed sanctions list match)
- FATF Recommendation 10 — Customer Due Diligence (income inconsistency)
- FATF Recommendation 20 — Suspicious Transaction Reporting
- Circular BACEN 3.978/2020 Art. 27 — Enhanced monitoring for high-risk indicators
- COAF Resolution 40/2021 — SAR filing obligation within 24 hours for confirmed sanctions matches
- Lei 9.613/1998 Art. 11 — Mandatory communication of suspicious operations

---

## 5. Recommended Actions

1. Submit SAR to COAF within 24 hours citing confirmed sanctions list match and concurrent typology triggers
2. Initiate immediate account restriction pending sanctions compliance review
3. Request source of funds documentation for transactions exceeding declared income capacity
4. Conduct coordinated review with customer C101819 due to merchant convergence linkage
5. Escalate to sanctions compliance team for OFAC/UN list verification and potential blocking action
6. Apply enhanced transaction monitoring with real-time alerts for any further Tor or cross-border activity
7. Document all Tor anonymization events in permanent customer risk file

---

## 6. Linked Entities

| Entity | Relationship | Status |
|---|---|---|
| M200696 | Recipient of largest PIX transaction via Tor (R$13,310.35) | pending merchant review |
| M200508 | Wire transfer recipient (R$24,230.02) | pending merchant review |
| M200390 | Cross-border recipient in Iraq (R$3,294.89, MCC 6051) | high-risk jurisdiction — enhanced review required |
| C101819 | Shared merchant convergence via R20 trigger | flagged subject — coordinated review required |
| M200797 | Recipient of second Tor anonymization transaction (R$3,328.57) | pending merchant review |

---

# SUSPICIOUS ACTIVITY REPORT (SAR)

## Case Identification

| Field | Value |
|-------|-------|
| **SAR Reference** | SAR-20260524-000149-48074c-C102290-01 |
| **Customer ID** | C102290 |
| **Run ID** | 20260524-000149-48074c |
| **Prepared At** | 2026-05-24 |
| **Priority Score** | 66.00 |
| **Severity** | high |
| **Escalation Band** | Tier 1 — SAR immediate |
| **ML Confidence Band** | Extreme |

---

## 1. Executive Summary

Customer C102290, a PEP-flagged individual with declared occupation 'Driver' and monthly income of approximately R$931, exhibited total outflows of R$134,318.84 during the review period—approximately 144× monthly declared income—which appears materially inconsistent with the stated economic profile. The account demonstrates a PIX passthrough ratio of 2,013% (R$108,041.04 outflow against R$5,366.76 inflow), potentially consistent with funds-transit or layering activity. Three anonymization events (1 Tor, 2 VPN) were detected across transaction sessions, and 27 distinct counterparties received funds, warranting further review for fan-out structuring. The combination of PEP status, extreme income mismatch, anonymization tool usage, high-risk MCC merchant activity, and multi-rail transaction patterns collectively elevates suspicion and may warrant immediate regulatory notification.

---

## 2. Triggered Alerts

| Alert Code | Detection Logic | Relevance |
|---|---|---|
| R01-VEL-BURST | ≥4 transactions in a single calendar day | Velocity pattern potentially consistent with rapid fund movement to evade monitoring thresholds |
| R03-INCOME-MISMATCH | Total outflow >100× declared monthly income | Primary quantitative indicator of activity materially inconsistent with stated economic profile |
| R04-PASSTHRU | PIX outflow-to-inflow ratio >200% | Pattern potentially consistent with funds-transit or layering activity |
| R05-ANON-TOR | Transaction via Tor anonymization network | Anonymization tool usage may warrant review for intent to obscure transaction origin |
| R09-PEP-EDD | PEP status — Enhanced Due Diligence required | Elevated regulatory scrutiny requirement under FATF Recommendation 12 |
| R10-KYC-INCONSIST | Contradictory KYC field combination | Declared occupation 'Driver' appears inconsistent with transaction volumes and PEP status |
| R11-MCC-HIGH-RISK | ≥3 transactions to high-risk MCC merchants | High-risk merchant categories potentially consistent with cash-out or value conversion activity |
| R15-FAN-OUT | ≥25 distinct receiving counterparties | Distribution pattern potentially consistent with structuring or layering activity |
| R17-MULTI-RAIL | Mixed-rail: PIX + Card + Wire within window | Multi-channel activity may warrant review for attempt to complicate transaction tracing |
| R19-CHARGEBACK | Chargeback history or high-CB merchant use | Elevated fraud risk indicator |
| R20-MERCHANT-CONVERGE | Shared merchant with another flagged subject | Network linkage potentially consistent with coordinated activity |

---

## 3. Detailed Findings

- Total outflow of R$134,318.84 recorded against declared annual income of R$11,177 (approximately R$931/month), representing approximately 144× monthly income, triggering R03-INCOME-MISMATCH at HIGH threshold.
- PIX passthrough ratio of 2,013.2% observed: R$108,041.04 outflow versus R$5,366.76 inflow, triggering R04-PASSTHRU and potentially consistent with funds-transit activity.
- Single-day velocity burst on 2025-08-01: 4 transactions totaling R$42,590.11, including PIX to M200888 (R$20,509.18, MCC 4814), M200489 (R$11,742.01, MCC 6211), and M200845 (R$8,224.55, MCC 4111), triggering R01-VEL-BURST.
- 27 distinct counterparties received funds during the review period, triggering R15-FAN-OUT rule for potential structuring review.
- Three anonymization events detected: 1 Tor session (tx TNUU7IUG3D1A2 on 2025-10-03, R$3,834.91 to M200122, MCC 6011) and 2 VPN sessions (tx TB24ZK5RW3PP8 on 2025-08-12, R$1,364.47 to M200662; tx TZ76800M19NE3 on 2025-09-28, R$8,506.10 to M200393), triggering R05-ANON-TOR.
- Cross-border card transaction to UAE (geo_country: AE) on 2025-07-10 for R$3,196.10 (tx TLRPWM2IMAYPY) to merchant M200283, MCC 6051 (Quasi-Cash).
- High-risk MCC transactions detected across multiple merchants: MCC 6051 (Quasi-Cash), MCC 6211 (Securities), MCC 6011 (ATM/Cash), MCC 4814 (Telecom), triggering R11-MCC-HIGH-RISK.
- Multi-rail activity confirmed: PIX, Card, and Wire transactions within review window, triggering R17-MULTI-RAIL.
- PEP status confirmed in KYC record, triggering R09-PEP-EDD requirement for Enhanced Due Diligence.
- KYC risk score 98/100; ML confidence band 'Extreme' with cohort rank 1, corroborating rule-based findings.
- Declared occupation 'Driver' appears inconsistent with transaction volumes and PEP status, contributing to R10-KYC-INCONSIST flag.

---

## 4. Regulatory Basis

- FATF Recommendation 12 — Enhanced Due Diligence for Politically Exposed Persons
- FATF Recommendation 20 — Suspicious Transaction Reporting
- Circular BACEN 3.978/2020 — AML/CFT policies and procedures for financial institutions
- COAF Instruction 1/2014 — SAR filing obligations and thresholds
- Law 9.613/1998 (Brazilian AML Law) — Money laundering prevention and reporting requirements

---

## 5. Recommended Actions

1. Submit SAR to COAF within regulatory timeline citing velocity burst, income mismatch, passthrough ratio, anonymization events, PEP status, and fan-out patterns
2. Initiate Enhanced Due Diligence per PEP requirements: request documentary evidence of source of funds for outflows exceeding declared income
3. Escalate account to enhanced monitoring tier with real-time transaction alerts
4. Conduct network analysis on merchant M200888 (largest PIX recipient) and other high-value counterparties for potential coordinated activity
5. Review cross-border transaction to UAE merchant M200283 for sanctions exposure and business justification
6. Consider account restrictions pending EDD completion and source-of-funds verification

---

## 6. Linked Entities

| Entity | Relationship | Status |
|---|---|---|
| M200888 | largest single PIX recipient | pending merchant review |
| M200489 | high-value PIX recipient on burst day | pending merchant review |
| M200845 | high-risk MCC recipient | pending merchant review |
| M200283 | cross-border card recipient (UAE) | pending cross-border review |
| M200122 | Tor-anonymized transaction recipient | elevated scrutiny |
| M200393 | VPN-anonymized transaction recipient | elevated scrutiny |
| M200662 | Wire transfer recipient via VPN | elevated scrutiny |

---

# SUSPICIOUS ACTIVITY REPORT (SAR)

## Case Identification

| Field | Value |
|-------|-------|
| **SAR Reference** | SAR-20260524-000149-48074c-C102093-01 |
| **Customer ID** | C102093 |
| **Run ID** | 20260524-000149-48074c |
| **Prepared At** | 2026-05-24 |
| **Priority Score** | 64.59 |
| **Severity** | high |
| **Escalation Band** | Tier 1 — SAR immediate |
| **ML Confidence Band** | High |

---

## 1. Executive Summary

Customer C102093, a confirmed Politically Exposed Person (PEP) with declared occupation 'Chef' and annual income of R$7,766, exhibited total outflows of R$192,074.54 during the review period—approximately 2,472% of declared annual income—a pattern potentially consistent with undisclosed income sources or layering activity. PIX passthrough ratio of 2,944.2% (R$113,519.06 outflow versus R$3,855.62 inflow) appears materially inconsistent with legitimate personal finance patterns and may warrant consideration as potential flow-through or layering behavior. The subject's activity includes Tor anonymization (tx T14MV5I9E7I9F, R$15,825.48), VPN usage (2 events), proxy usage (1 event), and cross-border transactions to high-risk jurisdiction Myanmar (tx TOOKNC1OPBY00, R$3,088.02), combined with fanout to 30 distinct counterparties across mixed payment rails (PIX, Card, Wire). The confluence of 11 concurrent rule fires (R03_HIGH, R04, R05_TOR, R07, R09, R10, R11, R15, R17, R19, R20), High ML confidence band classification, and PEP status collectively warrant immediate SAR filing and enhanced due diligence measures.

---

## 2. Triggered Alerts

| Alert Code | Detection Logic | Relevance |
|---|---|---|
| R03-INCOME-MISMATCH | Total outflow >100× declared monthly income | Primary quantitative indicator of potential undisclosed income or layering |
| R04-PASSTHRU | PIX outflow-to-inflow ratio >200% | Potentially consistent with flow-through or layering behavior |
| R05-ANON-TOR | Transaction via Tor anonymization network | Deliberate source obfuscation warranting enhanced scrutiny |
| R05-ANON-VPN | ≥2 transactions via VPN or proxy service | Pattern of anonymization techniques across multiple transactions |
| R07-GEO-MISMATCH | IP-country mismatch or geographic anomaly | Geographic inconsistency with declared Brazil-based profile |
| R09-PEP-EDD | PEP status — Enhanced Due Diligence required | Elevated regulatory scrutiny obligation per FATF Recommendation 12 |
| R10-KYC-INCONSIST | Contradictory KYC field combination | Profile inconsistency warranting source-of-funds verification |
| R11-MCC-HIGH-RISK | ≥3 transactions to high-risk MCC merchants | Elevated exposure to money service and utility payment categories |
| R15-FAN-OUT | ≥25 distinct receiving counterparties | Dispersion pattern potentially consistent with layering or smurfing |
| R17-MULTI-RAIL | Mixed-rail: PIX + Card + Wire within window | Multi-channel activity may indicate deliberate audit trail obfuscation |
| R19-CHARGEBACK | Chargeback history or high-CB merchant use | Potential association with disputed or fraudulent merchant activity |
| R20-MERCHANT-CONVERGE | Shared merchant with another flagged subject | Network linkage to separate suspicious activity investigation |

---

## 3. Detailed Findings

- Customer C102093, PEP-confirmed with declared occupation 'Chef' and annual income R$7,766, executed total outflows of R$192,074.54 across 30 transactions—representing approximately 2,472% of declared annual income, triggering R03_HIGH income-mismatch threshold.
- PIX channel exhibited passthrough ratio of 2,944.2% (R$113,519.06 outflow versus R$3,855.62 inflow), a pattern materially inconsistent with legitimate personal finance and potentially consistent with flow-through layering activity (R04).
- Transaction T14MV5I9E7I9F on 2025-07-08 (R$15,825.48 to merchant M200243, MCC 6051) was executed via Tor anonymization network, with additional anonymization events including 2 VPN transactions and 1 Proxy transaction, indicating deliberate source obfuscation pattern (R05_TOR, R05_VPN).
- Cross-border exposure includes transaction TOOKNC1OPBY00 on 2025-07-17 (R$3,088.02 to merchant M200684 in Myanmar, MCC 4900) and transaction TGKT5KP09AYYH on 2025-08-03 (R$12,385.50 to merchant M200067 in US, MCC 4814), representing high-risk jurisdiction activity inconsistent with declared Brazil-based profile.
- Fanout to 30 distinct counterparties across 30 transactions may warrant consideration as potential dispersion or layering behavior (R15), compounded by mixed-rail usage across PIX, Card, and Wire channels within the review window (R17).
- KYC inconsistency identified: declared occupation 'Chef' with Low risk rating versus observed high-volume, high-complexity transactional behavior; KYC risk score 63 with L2 tier classification (R10).
- Transaction T1Y075FPNVJEF on 2025-08-14 (R$8,709.32 to merchant M200446) originated from a rooted device, introducing device integrity concerns.
- Merchant convergence detected (R20): subject shares receiving merchant with another separately flagged subject, indicating potential network-level suspicious activity.
- High-risk MCC exposure confirmed across multiple transactions to MCC 4900 (utilities/money services) including tx T16QYYM1VN5DG (R$28,584.45) and MCC 6051 (quasi-cash) including tx T14MV5I9E7I9F (R15,825.48) (R11).

---

## 4. Regulatory Basis

- FATF Recommendation 12 — Enhanced Due Diligence for Politically Exposed Persons
- FATF Recommendation 20 — Suspicious Transaction Reporting
- Circular BACEN 3.978/2020 — AML/CFT compliance requirements for financial institutions
- COAF Resolution 40/2021 — SAR filing obligations and reporting thresholds
- FATF Recommendation 10 — Customer Due Diligence and source-of-funds verification

---

## 5. Recommended Actions

1. Submit SAR to COAF within regulatory timeframe citing R03_HIGH income disparity, R04 passthrough, R05_TOR anonymization, and R09 PEP status as primary indicators
2. Initiate Enhanced Due Diligence (EDD) protocol: request documentary evidence of source of funds for R$192,074.54 in outflows
3. Escalate to PEP review committee for determination of continued relationship viability given income-activity disparity
4. Place account on enhanced monitoring tier with real-time transaction alerts for cross-border and anonymization activity
5. Coordinate with network analysis team regarding R20 merchant convergence linkage to related flagged subject
6. Request clarification on declared occupation 'Chef' versus observed transactional complexity and volume
7. Consider temporary outbound transaction limits pending EDD completion

---

## 6. Linked Entities

| Entity | Relationship | Status |
|---|---|---|
| M200989 | largest single PIX recipient | high-risk MCC 4900 merchant — requires merchant-level review |
| M200243 | Tor-anonymized card transaction recipient | MCC 6051 quasi-cash — elevated ML/TF risk category |
| M200684 | cross-border recipient in Myanmar | high-risk jurisdiction exposure — requires geographic risk assessment |
| M200067 | cross-border recipient in US | cross-border PIX activity — monitoring |
| M200402 | wire transfer recipient | mixed-rail endpoint — pending review |
| unknown | shared merchant with another flagged subject | R20 convergence — network investigation pending |

---

# SUSPICIOUS ACTIVITY REPORT (SAR)

## Case Identification

| Field | Value |
|-------|-------|
| **SAR Reference** | SAR-20260524-000149-48074c-C100208-01 |
| **Customer ID** | C100208 |
| **Run ID** | 20260524-000149-48074c |
| **Prepared At** | 2026-05-24 |
| **Priority Score** | 63.20 |
| **Severity** | high |
| **Escalation Band** | Tier 1 — Hard alert |
| **ML Confidence Band** | High |

---

## 1. Executive Summary

Customer C100208, a declared Dentist with annual income of R$8,756, exhibits total outflow of R$144,241.98 during the review period—approximately 197× monthly declared income—which appears materially inconsistent with the stated occupational profile. PIX passthrough ratio of 3,674.6% (R$55,600.07 outflow vs R$1,513.10 inflow) may warrant consideration as potential flow-through activity. The account demonstrates anonymization events including Tor, VPN, and Proxy usage, combined with cross-border transactions to high-risk jurisdiction Myanmar (R$51,589.26) and mixed-rail activity across PIX, Card, and Wire channels. A direct wire transfer to another flagged subject (C102252) and network linkage indicators suggest potential coordinated activity requiring enhanced review.

---

## 2. Triggered Alerts

| Alert Code | Detection Logic | Relevance |
|---|---|---|
| R03-INCOME-MISMATCH | Total outflow >100× declared monthly income | Primary quantitative indicator of activity inconsistent with declared profile |
| R04-PASSTHRU | PIX outflow-to-inflow ratio >200% | Potentially consistent with flow-through or layering activity |
| R05-ANON-TOR | Transaction via Tor anonymization network | Anonymization technique potentially obstructing transaction traceability |
| R06-GEO-HIGH-RISK | Cross-border to high-risk jurisdiction | Transaction to FATF-monitored jurisdiction warrants enhanced scrutiny |
| R10-KYC-INCONSIST | Contradictory KYC field combination | Classification potentially inconsistent with behavioral indicators |
| R11-MCC-HIGH-RISK | ≥3 transactions to high-risk MCC merchants | High-risk merchant category codes associated with money transfer/payment services |
| R17-MULTI-RAIL | Mixed-rail: PIX + Card + Wire within window | Multi-channel activity potentially consistent with layering techniques |
| R20-MERCHANT-CONVERGE | Shared merchant with another flagged subject | Network convergence indicator warranting further review |
| R21-NETWORK-LINK | Direct wire to another flagged subject | Direct financial linkage to another subject under review |

---

## 3. Detailed Findings

- Total outflow of R$144,241.98 across 22 transactions to 22 distinct counterparties during the review period represents approximately 16.5× annual declared income (R$8,756) and approximately 197× monthly income, triggering R03_HIGH threshold.
- PIX channel exhibits passthrough ratio of 3,674.6%: R$55,600.07 outflow versus R$1,513.10 inflow, which may warrant consideration as potential flow-through activity per R04 detection logic.
- Anonymization events recorded: (1) Tor network on tx TES9D9NM8CEMC dated 2025-08-19 for R$3,410.63 PIX to C100814; (2) VPN on tx TP549PR319CUY dated 2025-09-22 for R$277.05 PIX to M200779; (3) Proxy on tx TMMMDIC9EH6NQ dated 2025-08-30 for R$1,176.03 Wire to M200620.
- Cross-border transaction to Myanmar (MM), a FATF-monitored jurisdiction, recorded on tx T7ILZTP10SBFN dated 2025-07-11 for R$51,589.26 via Card to merchant M200535 (MCC 5732).
- Wire transfer of R$1,665.40 to flagged subject C102252 on tx TSM9Q0FWI3AUT dated 2025-07-14 establishes direct financial linkage to another subject under enhanced review.
- High-risk MCC transactions include: R$18,915.77 PIX to M200392 (MCC 4111—Transportation) on tx TDL35CEBX1UUB dated 2025-07-03; R$22,284.39 Card to M200042 (MCC 4829—Wire Transfer/Money Orders) on tx T5EHA9CPQOOVG dated 2025-08-16.
- Mixed-rail activity across PIX, Card, and Wire channels within the review window, with 2 wire transfers recorded, potentially consistent with layering across payment rails.
- ML model classification: High confidence band with Tier 1 hard alert designation; 9 concurrent rule fires across income mismatch, passthrough, anonymization, geo-risk, KYC inconsistency, merchant risk, and network linkage typology families.

---

## 4. Regulatory Basis

- FATF Recommendation 20 — Suspicious Transaction Reporting
- FATF Recommendation 10 — Customer Due Diligence (income verification)
- Circular BACEN 3.978/2020 — AML/CFT obligations for payment institutions
- COAF Normative Instruction 1/2014 — SAR filing obligation for transactions inconsistent with customer profile
- COAF Communication Threshold — Activity materially inconsistent with declared occupation and income

---

## 5. Recommended Actions

1. Submit SAR to COAF within regulatory timeframe citing income-mismatch, passthrough, anonymization, geo-risk, and network linkage indicators
2. Initiate Enhanced Due Diligence (EDD) requesting source of funds documentation for outflows exceeding declared income capacity
3. Request supporting documentation for Myanmar cross-border transaction (R$51,589.26) including commercial purpose and beneficiary relationship
4. Escalate linked subject C102252 for coordinated review given direct wire transfer relationship
5. Apply enhanced monitoring tier with transaction limits pending EDD completion
6. Consider account restriction if source of funds documentation not provided within 30 days

---

## 6. Linked Entities

| Entity | Relationship | Status |
|---|---|---|
| C102252 | Direct wire transfer recipient; flagged subject | Pending coordinated review |
| C100814 | PIX recipient via Tor anonymization | Requires counterparty assessment |
| M200535 | Cross-border merchant recipient (Myanmar) | High-risk jurisdiction merchant |
| M200392 | High-risk MCC recipient (MCC 4111) | Pending merchant review |
| M200042 | High-risk MCC recipient (MCC 4829) | Pending merchant review |

---

# SUSPICIOUS ACTIVITY REPORT (SAR)

## Case Identification

| Field | Value |
|-------|-------|
| **SAR Reference** | SAR-20260524-000149-48074c-C101445-01 |
| **Customer ID** | C101445 |
| **Run ID** | 20260524-000149-48074c |
| **Prepared At** | 2026-05-24 |
| **Priority Score** | 62.49 |
| **Severity** | critical |
| **Escalation Band** | Tier 1 — Hard alert |
| **ML Confidence Band** | Moderate-High |

---

## 1. Executive Summary

Customer C101445, a self-declared Designer with annual income of R$21,304, presents a confirmed KYC-level sanctions list match requiring immediate regulatory escalation. The account exhibits an extreme PIX passthrough ratio of 899.2% (R$36,834.19 outflow versus R$4,096.14 inflow) and total outflows of R$68,070.28 representing approximately 38× monthly declared income equivalent, patterns materially inconsistent with the declared low-risk occupation. Anonymization events including VPN (tx T4TCRQ3MZFYUC) and Proxy (tx TLDMMIWTI9WSU) usage on 2025-08-03, combined with cross-border transactions to AE and PT jurisdictions and high-risk MCC activity (6011, 6211, 6051), may warrant further review for potential layering or integration activity. Network convergence with flagged customer C102304 via tx TXAZ60SQBYE3A and mixed-rail activity across PIX, Card, and Wire channels present additional risk indicators requiring immediate SAR filing.

---

## 2. Triggered Alerts

| Alert Code | Detection Logic | Relevance |
|---|---|---|
| R08-SANCTIONS-SCREEN | Confirmed KYC-level sanctions list match | Primary compliance trigger — confirmed sanctions match at KYC level requiring immediate escalation |
| R04-PASSTHRU | PIX outflow-to-inflow ratio >200% | Indicates potential passthrough or layering activity — R$36,834.19 outflow vs R$4,096.14 inflow |
| R05-ANON-VPN | ≥2 transactions via VPN or proxy service | Two anonymization events same day — VPN (tx T4TCRQ3MZFYUC) and Proxy (tx TLDMMIWTI9WSU) |
| R11-MCC-HIGH-RISK | ≥3 transactions to high-risk MCC merchants | Financial services MCCs potentially consistent with layering — ATM/Cash (6011), Securities (6211), Quasi-Cash (6051) |
| R17-MULTI-RAIL | Mixed-rail: PIX + Card + Wire within window | Diversified payment rails may warrant review for potential layering across channels |
| R19-CHARGEBACK | Chargeback history or high-CB merchant use | Potential indicator of fraudulent transaction patterns |
| R20-MERCHANT-CONVERGE | Shared merchant with another flagged subject | Network link to flagged customer C102304 via tx TXAZ60SQBYE3A (R$2,975.97) |

---

## 3. Detailed Findings

- Confirmed KYC-level sanctions list match (sanctions_status.confirmed_sanctions_match: true) — severity 'confirmed' per KYC record requiring immediate regulatory notification.
- Total outflow of R$68,070.28 against declared annual income of R$21,304 (approximately 3.2× annual income, equivalent to approximately 38× monthly income) appears materially inconsistent with Designer occupation.
- PIX passthrough ratio of 899.2% — R$36,834.19 outflow versus R$4,096.14 inflow — potentially consistent with layering or passthrough activity patterns.
- Anonymization events on 2025-08-03: VPN usage during cross-border card transaction to PT (tx T4TCRQ3MZFYUC, R$2,121.78, MCC 6211) and Proxy usage during wire transfer (tx TLDMMIWTI9WSU, R$4,738.23, MCC 5945).
- Cross-border activity to high-risk jurisdictions: AE (tx TT1YJJ9T8WM3E on 2025-07-18, R$3,147.06; tx T3CTGGX5K9LUR on 2025-09-26, R$3,041.49) and PT (tx T4TCRQ3MZFYUC on 2025-08-03, R$2,121.78).
- High-risk MCC activity: MCC 6011 (tx TXAZ60SQBYE3A, R$2,975.97), MCC 6211 (tx T4TCRQ3MZFYUC, R$2,121.78), MCC 6051 (tx T3CTGGX5K9LUR, R$3,041.49).
- Network convergence with flagged customer C102304 via PIX transaction TXAZ60SQBYE3A on 2025-07-04 (R$2,975.97, MCC 6011).
- Mixed-rail activity across 22 transactions to 22 distinct counterparties: PIX, Card, and Wire channels including 2 wire transfers (tx TLDMMIWTI9WSU R$4,738.23; tx T9OSWZJ1F3HT1 R$7,490.44).
- ML confidence band: Moderate-High; ML probability 0.999; escalation band Tier 1 — Hard alert.

---

## 4. Regulatory Basis

- UN Security Council Consolidated Sanctions List — Confirmed match requiring immediate notification per COAF Normative Instruction
- Circular BACEN 3.978/2020 Art. 27 — Suspicious activity reporting obligation for sanctions matches
- COAF Resolution 40/2021 — SAR filing within 24 hours for confirmed sanctions matches
- FATF Recommendation 6 — Targeted financial sanctions for terrorism and proliferation financing
- FATF Recommendation 20 — Suspicious transaction reporting obligations
- Lei 9.613/1998 Art. 11 — Money laundering reporting requirements
- Circular BACEN 3.461/2009 — Cross-border transaction monitoring and reporting

---

## 5. Recommended Actions

1. File SAR with COAF immediately — confirmed sanctions match triggers 24-hour reporting obligation
2. Implement immediate transaction blocking pending sanctions verification per OFAC/UN list cross-reference
3. Escalate to Compliance Officer and Legal for sanctions implications assessment
4. Initiate Enhanced Due Diligence — request source of funds documentation for R$68,070.28 in outflows
5. Place account under enhanced monitoring tier with real-time transaction alerts
6. Investigate network link to flagged customer C102304 — assess potential coordinated activity
7. Request documentation for cross-border transactions to AE and PT jurisdictions
8. Consider relationship termination pending sanctions list confirmation and EDD outcome

---

## 6. Linked Entities

| Entity | Relationship | Status |
|---|---|---|
| C102304 | PIX recipient flagged under R20 network convergence | flagged customer — investigate potential coordinated activity |
| M200256 | high-value PIX recipient (R$6,865.46) | pending merchant review |
| M200835 | cross-border card recipient AE (R$3,147.06) | pending merchant review |
| M200855 | wire recipient with Proxy anonymization (R$4,738.23) | pending merchant review — anonymization concern |
| M200502 | cross-border card recipient PT with VPN (R$2,121.78) | pending merchant review — anonymization concern |
| M200080 | high-value wire recipient (R$7,490.44) | pending merchant review |
| M200329 | cross-border card recipient AE (R$3,041.49) | pending merchant review |

---

# SUSPICIOUS ACTIVITY REPORT (SAR)

## Case Identification

| Field | Value |
|-------|-------|
| **SAR Reference** | SAR-20260524-000149-48074c-C101542-01 |
| **Customer ID** | C101542 |
| **Run ID** | 20260524-000149-48074c |
| **Prepared At** | 2026-05-24 |
| **Priority Score** | 61.79 |
| **Severity** | high |
| **Escalation Band** | Tier 1 — Hard alert |
| **ML Confidence Band** | High |

---

## 1. Executive Summary

Customer C101542, a self-declared Freelancer with declared annual income of R$3,687 (approximately R$307/month), presents total outflows of R$103,286.93 during the review period—potentially consistent with income inflation exceeding 336× declared monthly income, which warrants further review. The PIX passthrough ratio of 751.2% (R$73,948.90 outflow vs R$9,843.55 inflow) may indicate funds transit activity. Activity includes one Tor-anonymized transaction to a gambling merchant (MCC 7995), mixed-rail usage across PIX, Card, and Wire channels, 28 distinct counterparties, and a direct wire transfer to another flagged subject (C100375), collectively presenting a behavioral profile materially inconsistent with a low-risk L1-tier freelancer. Cross-border activity includes a wire transfer of R$6,257.41 to Libya (high-risk jurisdiction), warranting heightened regulatory attention. Nine concurrent detection rules triggered with ML confidence band rated High, supporting immediate SAR filing.

---

## 2. Triggered Alerts

| Alert Code | Detection Logic | Relevance |
|---|---|---|
| R03-INCOME-MISMATCH | Total outflow >100× declared monthly income | Primary quantitative indicator of economic activity materially inconsistent with declared income profile |
| R04-PASSTHRU | PIX outflow-to-inflow ratio >200% | May indicate funds transit or layering activity through the account |
| R05-ANON-TOR | Transaction via Tor anonymization network | Tor-anonymized transaction to gambling merchant potentially consistent with concealment intent |
| R11-MCC-HIGH-RISK | ≥3 transactions to high-risk MCC merchants | Pattern of transactions to high-risk merchant categories warrants scrutiny |
| R15-FAN-OUT | ≥25 distinct receiving counterparties | High counterparty diversity may indicate structuring or layering behavior |
| R17-MULTI-RAIL | Mixed-rail: PIX + Card + Wire within window | Multi-channel activity potentially consistent with layering across payment rails |
| R19-CHARGEBACK | Chargeback history or high-CB merchant use | Potential association with disputed or fraudulent transaction patterns |
| R20-MERCHANT-CONVERGE | Shared merchant with another flagged subject | Network overlap with other subjects under review may indicate coordinated activity |
| R21-NETWORK-LINK | Direct wire to another flagged subject | Direct financial linkage to another flagged subject warrants coordinated investigation |

---

## 3. Detailed Findings

- Total outflow of R$103,286.93 against declared annual income of R$3,687 (monthly ~R$307) represents a disparity of approximately 336× monthly income, triggering R03_HIGH (>100× threshold).
- PIX passthrough ratio of 751.2%: R$73,948.90 PIX outflow versus R$9,843.55 PIX inflow, triggering R04 (>200% threshold), potentially indicative of funds transit activity.
- Transaction T991C2EOAP061 on 2025-07-14 for R$5,760.65 to merchant M200971 (MCC 7995—gambling) was executed via Tor anonymization network, triggering R05_TOR.
- Transaction TUI6B5CHKXRA8 on 2025-09-24 for R$779.48 to merchant M200196 (geo US) was executed via Proxy service.
- 28 distinct counterparties identified across 28 transactions during the review period, triggering R15 (≥25 threshold).
- Mixed-rail activity observed: PIX, Card, and Wire transactions within the review window, including 3 wire transfers totaling R$14,938.42, triggering R17.
- High-risk MCC transactions include: tx TSWFX3XIHOF2R (R$25,848.82, MCC 4900) on 2025-08-04; tx TCIOVP5V3QUJF (R$11,121.30, MCC 4829) on 2025-08-17; tx T991C2EOAP061 (R$5,760.65, MCC 7995) on 2025-07-14—triggering R11.
- Direct wire transfer T8XYRVKV8AGM2 on 2025-07-27 for R$1,423.60 to flagged subject C100375, triggering R21.
- Wire transfer TESLWHQ8LG92B on 2025-10-04 for R$6,257.41 to merchant M200776 with geo-country Libya (LY), a high-risk jurisdiction per FATF grey list.
- 7 cross-border transaction events identified, including jurisdictions AE (UAE), US, and LY (Libya).
- KYC tier L1 (basic) with risk score 59 rated 'Low'; no PEP status; no sanctions indicators; ML confidence band rated High with cohort rank 4.

---

## 4. Regulatory Basis

- FATF Recommendation 10 — Customer Due Diligence regarding unusual transaction patterns inconsistent with customer profile
- FATF Recommendation 20 — Suspicious Transaction Reporting obligation
- Circular BACEN 3.978/2020 Art. 27 — Suspicious activity indicators including income inconsistency and anonymization usage
- COAF Resolution 40/2021 — SAR filing obligation for transactions potentially indicative of money laundering
- COAF Normative Instruction — High-risk jurisdiction monitoring requirements (Libya cross-border activity)

---

## 5. Recommended Actions

1. Submit SAR to COAF within regulatory timeframe citing income mismatch, passthrough pattern, anonymization, and network linkage typologies
2. Initiate Enhanced Due Diligence (EDD) review: request source of funds documentation and economic justification for transaction volume
3. Escalate KYC tier from L1 to L2; obtain updated occupation verification and income substantiation
4. Coordinate investigation with case file for linked subject C100375 (R21 trigger)
5. Apply enhanced transaction monitoring with real-time alerts for cross-border and anonymization events
6. Review merchant relationships M200971 (gambling), M200616 (wire services), and M200776 (Libya recipient) for potential network expansion

---

## 6. Linked Entities

| Entity | Relationship | Status |
|---|---|---|
| C100375 | direct wire recipient — flagged subject | active investigation — R21 trigger |
| M200966 | largest single PIX recipient (R$25,848.82, MCC 4900) | pending merchant review |
| M200616 | high-value PIX recipient — wire transfer services MCC 4829 | pending merchant review |
| M200971 | recipient of Tor-anonymized transaction — gambling MCC 7995 | high-risk merchant flag |
| M200776 | wire recipient — high-risk jurisdiction (Libya) | high-risk jurisdiction flag |

---

_This report constitutes an internal compliance escalation. Conclusions are based on transactional and KYC data available at preparation time. Final SAR filing determination is subject to Compliance Officer and MLRO review._

_ML confidence labels are calibrated relative to the investigated escalation cohort, not the full customer population._