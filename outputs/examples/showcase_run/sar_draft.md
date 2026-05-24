# SUSPICIOUS ACTIVITY REPORT (SAR)

## Case Identification

| Field | Value |
|-------|-------|
| **SAR Reference** | SAR-20260524-000149-48074c-C100091-01 |
| **Customer ID** | C100091 |
| **Prepared Date** | 2026-05-24 |
| **Run ID** | 20260524-000149-48074c |
| **Priority Score** | 80.46 (Critical Severity) |
| **Escalation Band** | Tier 1 — Hard Alert |

---

## 1. Executive Summary

Customer C100091, a declared Store Owner with annual income of R$10,173, exhibited total outflows of R$91,349.77 during the review period—approximately 898× the monthly income equivalent (R$847.75/mo), which appears materially inconsistent with the stated economic profile. A wire transfer of R$11,672.88 to counterparty M200363 in Iran (IR) on 2025-08-07 triggered a transactional sanctions screening event requiring entity-level review. The PIX passthrough ratio of 4,008.5% (R$57,117.34 outflow vs R$1,424.90 inflow) may warrant further review for potential layering activity. Mixed-rail activity across PIX, Wire, and Card channels, combined with high-risk MCC transactions (gambling MCC 7995, financial institution MCC 6011), network linkage to flagged customer C100236, and cross-border transactions to high-risk jurisdictions, collectively suggest a pattern potentially consistent with structured fund movement warranting immediate SAR filing.

---

## 2. Triggered Alerts

| Alert Code | Detection Logic | Date/Aggregate | Relevance |
|------------|-----------------|----------------|-----------|
| **R03_HIGH** | [R03-INCOME-MISMATCH] Total outflow >100× declared monthly income | 898× monthly equivalent | Primary quantitative indicator of funds inconsistent with declared economic profile |
| **R04** | [R04-PASSTHRU] PIX outflow-to-inflow ratio >200% | 4,008.5% | May indicate potential layering or pass-through activity |
| **R08** | [R08-SANCTIONS-SCREEN] Transactional sanctions screening event | 2025-08-07 (tx TJRKHTP81JROK) | Wire transfer to Iran-based counterparty requires immediate entity-level review |
| **R06** | [R06-GEO-HIGH-RISK] Cross-border to high-risk jurisdiction | 3 events (IR, DE, ES) | Iran transaction presents elevated jurisdictional risk |
| **R02_LOW** | [R02-STRUCT-BAND] Transactions in R$9,000–R$10,000 band | 2025-07-15 (tx TLF007IGRTEAB) | May indicate potential structuring behavior |
| **R11** | [R11-MCC-HIGH-RISK] ≥3 transactions to high-risk MCC merchants | MCC 7995, 6011 | High-risk merchant categories associated with ML vulnerabilities |
| **R17** | [R17-MULTI-RAIL] Mixed-rail: PIX + Card + Wire within window | Review period | Multi-channel activity may obscure transaction trail |
| **R21** | [R21-NETWORK-LINK] Direct wire to another flagged subject | 2025-07-18 (tx TMGHPD5XFHXCJ) | Network connection to C100236 under review |
| **R19** | [R19-CHARGEBACK] Chargeback history or high-CB merchant use | Review period | Elevated fraud risk indicator |
| **R20** | [R20-MERCHANT-CONVERGE] Shared merchant with another flagged subject | Review period | Potential network convergence pattern |

---

## 3. Detailed Analysis

### 3.1 Income-Transaction Disparity and Passthrough Activity

The customer's declared annual income of R$10,173 (monthly equivalent R$847.75) stands in stark contrast to total outflows of R$91,349.77—a disparity of approximately 898× the monthly income. This appears materially inconsistent with the stated occupation of Store Owner and may warrant review for undisclosed income sources or nominee account activity. The PIX passthrough ratio of 4,008.5% (R$57,117.34 outflow vs R$1,424.90 inflow) suggests the account may be functioning primarily as a conduit rather than for legitimate commercial purposes, a pattern potentially consistent with layering techniques.

### 3.2 Sanctions Screening Event and Cross-Border Activity

Wire transfer TJRKHTP81JROK dated 2025-08-07 for R$11,672.88 to counterparty M200363 in Iran (IR) triggered a transactional sanctions screening event requiring entity-level review. Iran represents a high-risk jurisdiction subject to multiple international sanctions regimes. Additional cross-border activity included PIX transfers to Germany (tx TQWXFJ3VKTJO0, R$540.93 on 2025-08-22) and Spain (tx TGWER3C1MRCSR, R$4,987.69 on 2025-10-04), demonstrating international fund movement patterns that warrant further scrutiny given the customer's domestic retail profile.

### 3.3 Network Linkage and High-Risk Merchant Activity

Wire transfer TMGHPD5XFHXCJ dated 2025-07-18 for R$1,255.77 to customer C100236 triggered network linkage rule R21, as C100236 is a separately flagged subject. High-risk MCC transactions included PIX payment T1RBG8O7Y6NC6 (R$7,680.48 to C100179, MCC 7995

---

# SUSPICIOUS ACTIVITY REPORT (SAR)

---

## 1. Case Identification

| Field | Value |
|-------|-------|
| **SAR Reference** | SAR-20260524-000149-48074c-C101208-01 |
| **Customer ID** | C101208 |
| **Run ID** | 20260524-000149-48074c |
| **Prepared At** | 2026-05-24T00:01:49Z |
| **Severity Classification** | Critical |
| **Escalation Band** | Tier 1 — Hard alert |
| **ML Confidence Band** | Moderate |

---

## 2. Executive Summary

Subject C101208, declared occupation Chef with annual income of R$13,047, exhibited total outflow of R$150,178.09 during the review period, representing approximately 1,150% of annual declared income and triggering R03_HIGH (>100× monthly income threshold). Activity involved 29 transactions to 29 distinct counterparties (R15), mixed-rail usage across PIX, Card, and Wire channels (R17), 2 VPN anonymization events (R05_VPN), and 1 transactional sanctions screening event involving a Wire transfer of R$2,166.18 to counterparty M200815 in Syria (R08). Cross-border activity spanned jurisdictions including Syria, Russia, Yemen, Portugal, and the United Kingdom, with high-risk MCC 7995 (gambling) transactions totaling R$20,901.35. The convergence of severe income mismatch, sanctions screening event, anonymization indicators, and high-risk merchant activity presents a pattern potentially consistent with layered fund movement warranting immediate SAR filing.

---

## 3. Triggered Alerts

| Alert Code | Detection Logic | Date/Aggregate | Relevance |
|------------|-----------------|----------------|-----------|
| **R03-INCOME-MISMATCH** | Total outflow >100× declared monthly income | ~1,150× monthly / 1,150% annual | Primary quantitative indicator — R$150,178.09 outflow vs R$13,047 annual declared income |
| **R08-SANCTIONS-SCREEN** | Transactional sanctions screening event | 2025-08-12 | Wire R$2,166.18 to counterparty M200815 in Syria — transactional screening event requiring review |
| **R05-ANON-VPN** | ≥2 transactions via VPN or proxy service | 2025-07-22, 2025-08-29 | 2 VPN anonymization events: tx TJZRYWR88WZHJ and tx TQSBX6QW4LBWX |
| **R11-MCC-HIGH-RISK** | ≥3 transactions to high-risk MCC merchants | 2025-09-08, 2025-09-23 | MCC 7995 (gambling) transactions to Yemen (R$6,889.49) and Brazil (R$14,011.86) |
| **R15-FAN-OUT** | ≥25 distinct receiving counterparties | 29 counterparties | Funds dispersed across 29 distinct recipients during review period |
| **R17-MULTI-RAIL** | Mixed-rail: PIX + Card + Wire within window | Review period | PIX R$77,634.56 + Wire R$21,444.38 + Card activity |
| **R18-CNP-NO-3DS** | ≥3 CNP transactions without 3DS authentication | Review period | Card-not-present transactions lacking strong customer authentication |
| **R19-CHARGEBACK** | Chargeback history or high-CB merchant use | Review period | Chargeback indicators detected |
| **R20-MERCHANT-CONVERGE** | Shared merchant with another flagged subject | Review period | Potential network linkage with another flagged subject |

---

## 4. Detailed Analysis

### 4.1 Income Mismatch and Economic Profile Inconsistency

Subject declared occupation as Chef with annual income of R$13,047. Total observed outflow of R$150,178.09 represents approximately 1,150% of stated annual income, a disparity materially inconsistent with the declared economic profile. PIX outflow alone totaled R$77,634.56 with R$0.00 PIX inflow, while 3 wire transfers totaled R$21,444.38 to cross-border counterparties. The KYC tier (L1) and risk rating (Low) appear inconsistent with the observed transactional behavior, warranting immediate KYC refresh and source-of-funds documentation.

### 4.2 Sanctions Screening Event and High-Risk Jurisdiction Activity

On 2025-08-12, tx TNHZDN7D6LYK6 recorded a Wire transfer of R$2,166.18 to counterparty M200815 in Syria (geo_country: SY), MCC 5999, triggering R08 with sanctions_hit=true. This constitutes a transactional screening event requiring entity-level review. Additional cross-border activity included: tx TQSBX6QW4LBWX on 2025-08-29, Card R$1,089.07 to M

---

# SUSPICIOUS ACTIVITY REPORT (SAR)

---

## 1. Case Identification

| Field | Value |
|-------|-------|
| **SAR Reference** | SAR-20260524-000149-48074c-C101028-01 |
| **Run ID** | 20260524-000149-48074c |
| **Customer ID** | C101028 |
| **Prepared At** | 2026-05-24T00:01:49Z |
| **Escalation Band** | Tier 1 — Hard alert |
| **Priority Score** | 74.36 |
| **Severity** | Critical |
| **ML Confidence Band** | Moderate |

---

## 2. Executive Summary

Customer C101028 presents a confirmed KYC-level sanctions list match combined with PEP status, triggering immediate regulatory review obligations under FATF Recommendation 12 and COAF filing requirements. The account exhibits a PIX passthrough ratio of 587.3% (R$46,553.76 outflow vs R$7,927.19 inflow) and total outflow of R$71,406.40 against declared annual income of R$47,312, representing approximately 151% of stated income and appearing materially inconsistent with the declared Designer occupation. Two anonymization events (1 VPN, 1 Proxy) and cross-border activity including a Card transaction of R$4,390.02 to North Korea (KP) on 2025-07-01 compound the risk profile. Nine concurrent rule triggers across five typology families—passthrough, anonymization, sanctions/PEP, merchant risk, and card/e-commerce—warrant immediate SAR filing and Enhanced Due Diligence review.

---

## 3. Triggered Alerts

| Alert Code | Detection Logic | Date/Aggregate | Relevance |
|------------|-----------------|----------------|-----------|
| **R08** | [R08-SANCTIONS-SCREEN] Confirmed KYC-level sanctions list match | KYC-level confirmed match | Primary hard alert trigger requiring immediate regulatory action |
| **R09** | [R09-PEP-EDD] PEP status — Enhanced Due Diligence required | KYC PEP status: Yes | Mandatory EDD trigger per FATF Recommendation 12 |
| **R04** | [R04-PASSTHRU] PIX outflow-to-inflow ratio >200% | 587.3% | Potentially consistent with funds passthrough or layering activity |
| **R05_VPN** | [R05-ANON-VPN] ≥2 transactions via VPN or proxy service | 2 events (1 VPN, 1 Proxy) | Anonymization may warrant review for transaction origin obfuscation |
| **R10** | [R10-KYC-INCONSIST] Contradictory KYC field combination | Low risk_rating despite PEP and sanctions match | Internal control gap requiring remediation |
| **R11** | [R11-MCC-HIGH-RISK] ≥3 transactions to high-risk MCC merchants | MCC 6211, 6011, 4111 | High-risk merchant categories including securities/brokers and financial institutions |
| **R18** | [R18-CNP-RISK] Card-not-present transaction risk indicator | Aggregate | Elevated CNP fraud risk profile |
| **R19** | [R19-CHARGEBACK] Chargeback history or high-CB merchant use | Aggregate | Chargeback risk potentially consistent with dispute patterns |
| **R20** | [R20-MERCHANT-CONVERGE] Shared merchant with another flagged subject | Merchant convergence detected | Network linkage may warrant coordinated review |

---

## 4. Detailed Analysis

### 4.1 Sanctions and PEP Status

Customer C101028 presents a confirmed KYC-level sanctions list match (sanctions_status.confirmed_sanctions_match: true) combined with active PEP status (kyc.pep: 'Yes'), creating a dual regulatory obligation requiring immediate SAR filing under COAF Resolution 40/2021 and Enhanced Due Diligence procedures per FATF Recommendation 12. The concurrent R10 trigger indicates a contradictory KYC configuration whereby the customer carries a 'Low' risk_rating despite these confirmed risk factors, potentially consistent with a control gap in the institution's risk rating assignment process that warrants remediation.

### 4.2 Transaction Volume and Income Inconsistency

Total outflow of R$71,406.40 across 18 transactions to 18 distinct counterparties during the review period represents approximately 151% of the declared annual income of R$47,312. This volume appears materially inconsistent with the stated Designer occupation. The PIX passthrough ratio of 587.3% (R$46,553.76 PIX outflow vs R$7,927.19 PIX inflow) may be potentially consistent with funds movement patterns associated with layering or passthrough activity, warranting further review of the economic rationale for these fund flows.

### 4.3 High-Risk Transaction Patterns

Cross-border activity includes Card transaction TFNO8A1FBZUMA dated 2025-07-01 for R$4,390.02 to counterparty M200105 located in North Korea (KP), MCC 4789—a jurisdiction subject to comprehensive international sanctions. Two anonymization events were detected: VPN-routed Card transaction TQXICCVPO421G (2025-07-08, R$6,975.17, M200118, MCC 6011) and Proxy-routed PIX

---

# SUSPICIOUS ACTIVITY REPORT (SAR)

## 1. Case Identification

| Field | Value |
|-------|-------|
| SAR Reference | SAR-20260524-000149-48074c-C100837-01 |
| Customer ID | C100837 |
| Run ID | 20260524-000149-48074c |
| Prepared At | 2026-05-24T00:01:49Z |
| Severity Classification | High |
| Escalation Band | Tier 1 — SAR immediate |
| ML Confidence Band | Very High |

---

## 2. Executive Summary

Customer C100837, a confirmed Politically Exposed Person (PEP) with declared annual income of R$7,577, exhibited total outflow of R$139,083.50 across 29 transactions during the review period, representing approximately 18× annual income and potentially consistent with income mismatch typology. PIX passthrough ratio of 4,367% (R$104,965.61 outflow versus R$2,403.44 inflow) may warrant review for potential layering activity. One transaction (T4VUTEFNQBUQH, R$2,782.76) was executed via Tor anonymization network, and six cross-border events were detected including activity to Myanmar (MM), a FATF high-risk jurisdiction. The convergence of PEP status, extreme income-outflow disparity, anonymization usage, high-risk jurisdiction activity, and mixed-rail transaction patterns across 27 distinct counterparties presents materially concerning indicators warranting immediate SAR filing.

---

## 3. Triggered Alerts Summary

| Alert Code | Detection Logic | Date/Aggregate | Relevance |
|------------|-----------------|----------------|-----------|
| R03-INCOME-MISMATCH | Total outflow >100× declared monthly income | R$139,083.50 vs R$7,577 annual (~18× annual) | Primary quantitative indicator |
| R04-PASSTHRU | PIX outflow-to-inflow ratio >200% | 4,367% | Potentially consistent with layering |
| R05-ANON-TOR | Transaction via Tor anonymization network | 2025-08-04, tx T4VUTEFNQBUQH | May indicate intent to obscure origin |
| R06-GEO-HIGH-RISK | Cross-border to high-risk jurisdiction | 6 events incl. Myanmar (MM) | FATF high-risk jurisdiction |
| R09-PEP-EDD | PEP status — Enhanced Due Diligence required | Confirmed PEP | Regulatory EDD requirement |
| R10-KYC-INCONSIST | Contradictory KYC field combination | Aggregate | Volume inconsistent with profile |
| R11-MCC-HIGH-RISK | ≥3 transactions to high-risk MCC merchants | MCC 4829, MCC 6051 | Value transfer MCCs |
| R15-FAN-OUT | ≥25 distinct receiving counterparties | 27 counterparties | Distribution pattern |
| R17-MULTI-RAIL | Mixed-rail: PIX + Card + Wire | Review period | Diversified pathways |
| R19-CHARGEBACK | Chargeback history or high-CB merchant use | Aggregate | Transaction integrity |
| R20-MERCHANT-CONVERGE | Shared merchant with another flagged subject | Aggregate | Network linkage |

**Total Triggered Rules:** 12

---

## 4. Detailed Analysis

### 4.1 Income Mismatch and Transaction Volume

Customer C100837, with declared occupation of Accountant and confirmed PEP status, reported annual income of R$7,577. Total observed outflow of R$139,083.50 across 29 transactions represents approximately 18× declared annual income. PIX channel exhibited passthrough ratio of 4,367%, calculated from R$104,965.61 outflow versus R$2,403.44 inflow, which may warrant review for potential layering activity. The extreme disparity between declared income and transaction volume appears materially inconsistent with stated customer profile.

### 4.2 Anonymization and High-Risk Geographic Activity

Transaction T4VUTEFNQBUQH on 2025-08-04 for R$2,782.76 to counterparty M200806 (MCC 5812) was executed via Tor anonymization network, potentially indicating intent to obscure transaction origin. Six cross-border events were detected during the review period, including card transaction TT94KQ67Q0Q92 on 2025-07-22 for R$1,361.82 to counterparty M200684 in Myanmar (MM), which is a FATF-identified high-risk jurisdiction. Additional international wire activity included transfers to GB (R$12,957.12 via tx T4MHTBYMYYY0C), US (R$1,702.86 via tx TPCPL90MU9SRF), and DE (R$1,746.42 via tx TDU1GAYIB8X9S).

### 4.3 Distribution Patterns and Mixed-Rail Usage

The customer transacted with 27 distinct counterparties across 29 transactions, triggering fan-out detection (R15). Mixed-rail activity utilized PIX, Card, and Wire channels within the review period. The largest single transaction was PIX transfer TTP6ORO2Q3V22 on 2025-08-20 for R$27,304.70 to counterparty M200309 (MCC 4829 wire transfer services). Additional high-risk MCC activity included card transaction TPTMR0FBGXQOB on 2025

---

# SUSPICIOUS ACTIVITY REPORT (SAR)

## SAR-20260524-000149-48074c-C101582-01

---

## 1. Case Identification

| Field | Value |
|-------|-------|
| **SAR Reference** | SAR-20260524-000149-48074c-C101582-01 |
| **Customer ID** | C101582 |
| **Run ID** | 20260524-000149-48074c |
| **Prepared Date** | 2026-05-24 |
| **Analyst System** | AML/FT Automated Investigation Pipeline |
| **Escalation Band** | Tier 1 — Hard alert |
| **ML Confidence Band** | Moderate-High |

---

## 2. Executive Summary

Customer C101582 presents a **confirmed KYC-level sanctions list match** requiring immediate regulatory notification. The account exhibits total outflow of **R$89,473.16** against declared annual income of **R$10,907** (approximately 8.2× annual income, triggering the R03_LOW threshold of >50× monthly income). Two distinct Tor anonymization events were detected on 2025-07-15 (R$13,310.35) and 2025-09-08 (R$3,328.57), potentially consistent with deliberate identity obfuscation. Cross-border activity includes a transaction to Iraq (high-risk jurisdiction) on 2025-08-21 for R$3,294.89 via MCC 6051 (quasi-cash), and mixed-rail usage across PIX, Card, and Wire channels warrants further review for layering typology. The convergence of sanctions exposure, income mismatch, anonymization, and high-risk merchant activity across **7 triggered rules** supports immediate SAR filing.

---

## 3. Triggered Alerts Summary

| Alert Code | Detection Logic | Date/Aggregate | Relevance |
|------------|-----------------|----------------|-----------|
| **R08-SANCTIONS-SCREEN** | Confirmed KYC-level sanctions list match | KYC-level confirmed | Primary regulatory trigger requiring immediate escalation |
| **R03-INCOME-MISMATCH** | Total outflow >50× declared monthly income | R$89,473.16 vs R$10,907 annual (~98× monthly) | Quantitative indicator of funds inconsistent with economic profile |
| **R05-ANON-TOR** | Transaction via Tor anonymization network | 2 events: 2025-07-15, 2025-09-08 | Identity obfuscation potentially consistent with illicit fund movement |
| **R11-MCC-HIGH-RISK** | ≥3 transactions to high-risk MCC merchants | MCC 4900, MCC 6051 | Merchant categories associated with value transfer |
| **R17-MULTI-RAIL** | Mixed-rail: PIX + Card + Wire within window | PIX + Card + Wire R$24,230.02 | Multi-channel activity potentially consistent with layering |
| **R19-CHARGEBACK** | Chargeback history or high-CB merchant use | Review period | Potential fraud or merchant risk exposure |
| **R20-MERCHANT-CONVERGE** | Shared merchant with another flagged subject | 2025-08-25 (tx TOYX9MA23Q8NW) | Network linkage to customer C101819 |

---

## 4. Detailed Analysis

### 4.1 Sanctions Exposure

The customer profile reflects a **confirmed KYC-level sanctions list match** (sanctions_status.confirmed_sanctions_match: true, severity: "confirmed"). This designation requires immediate regulatory notification under COAF Resolution 40/2021 and potential account blocking action pending sanctions compliance verification. No transactional screening events were recorded during the review period, indicating the match was identified at onboarding or periodic KYC refresh rather than through transaction-level screening.

### 4.2 Income-to-Outflow Disparity and Transactional Behavior

Total documented outflow of **R$89,473.16** across 23 transactions appears materially inconsistent with the declared annual income of **R$10,907** (stated occupation: Nurse). This represents approximately 8.2× annual income or ~98× monthly income, exceeding the R03_LOW threshold. The funds were distributed across **22 distinct counterparties**, with PIX channel accounting for R$46,573.94, a single Wire transfer of R$24,230.02 (tx TMBR17QPP9GD3 on 2025-09-21), and multiple Card transactions including cross-border activity to France and Iraq. The mixed-rail pattern across PIX, Card, and Wire channels within the review period may warrant further review for potential layering activity.

### 4.3 Anonymization and High-Risk Jurisdiction Activity

Two Tor anonymization events were detected: (1) tx T1UADPDDHFJPA on 2025-07-15 for R$13,310.35 to merchant M200696 and (2) tx T4P4Q65XC570F on 2025-09-08 for R$3,328.57 to merchant M200797. The use of Tor network infrastructure for financial transactions is potentially consistent with deliberate identity obfuscation. Additionally, cross-border Card transaction tx T1XY2A460O51H on 2025-08-21 for R$3,294.89 was directed to counterparty M200390 in **Iraq (IQ)**, a high-risk jurisdiction, via MCC 6051 (quasi-cash category). The merchant convergence with flagged customer C101819 via tx TOYX9MA23Q8NW (R$7,454.37 on 2025-08-25) suggests potential network-level coordination warranting coordinated investigation.

---

## 5. Key Transaction Timeline

| Date | Event | Transaction ID | Amount (R$) |
|------|-------|----------------|-------------|
| 2025-07-05 | PIX to M200966, MCC 4900 (high-risk merchant) | TF8F0668QXDKJ | 506.42 |
| 2025-07-15 | PIX via Tor to M200696 | T1UADPDDHFJPA | 13,310.35 |
| 2025-07-23 | Cross-border Card to France | TG9WZU12O72OV | 453.81 |
| 2025-08-21 | Cross-border Card to Iraq, MCC 6051 quasi-cash | T1XY2A460O51H | 3,294.89 |
| 2025-08-25 | Card to C101819, merchant convergence trigger | TOYX9MA23Q8NW | 7,454.37 |
| 2025-09-08 | PIX via Tor to M200797 (second Tor event) | T4P4Q65XC570F | 3,328.57 |
| 2025-09-21 | Wire transfer to M200508 | T

---

# SUSPICIOUS ACTIVITY REPORT (SAR)

---

## 1. Case Identification

| Field | Value |
|-------|-------|
| **SAR Reference** | SAR-20260524-000149-48074c-C102290-01 |
| **Customer ID** | C102290 |
| **Run ID** | 20260524-000149-48074c |
| **Prepared At** | 2026-05-24T00:01:49Z |
| **Severity** | High |
| **Priority Score** | 66.0 |
| **Escalation Band** | Tier 1 — SAR immediate |

---

## 2. Executive Summary

Customer C102290, a PEP-flagged individual with declared occupation 'Driver' and monthly income of approximately R$931, exhibited total outflows of R$134,318.84 during the review period—approximately 144× monthly declared income—which appears materially inconsistent with the stated economic profile. The account demonstrates a PIX passthrough ratio of 2,013% (R$108,041.04 outflow against R$5,366.76 inflow), potentially consistent with funds-transit or layering activity. Three anonymization events (1 Tor, 2 VPN) were detected across transaction sessions, and 27 distinct counterparties received funds, warranting further review for fan-out structuring. The combination of PEP status, extreme income mismatch, anonymization tool usage, high-risk MCC merchant activity, and multi-rail transaction patterns collectively elevates suspicion and may warrant immediate regulatory notification.

---

## 3. Triggered Alerts Summary

| Alert Code | Detection Logic | Date/Aggregate | Relevance |
|------------|-----------------|----------------|-----------|
| R01-VEL-BURST | ≥4 transactions in a single calendar day | 2025-08-01: 4 tx, R$42,590.11 | Velocity pattern potentially consistent with rapid fund movement |
| R03-INCOME-MISMATCH | Total outflow >100× monthly declared income | 144× monthly income | Primary quantitative indicator of income inconsistency |
| R04-PASSTHRU | PIX outflow-to-inflow ratio >200% | 2,013.2% | Pattern potentially consistent with funds-transit activity |
| R05-ANON-TOR | Transaction via Tor anonymization network | 2025-10-03: tx TNUU7IUG3D1A2 | Anonymization may warrant review for intent to obscure origin |
| R09-PEP-EDD | PEP status — Enhanced Due Diligence required | KYC confirmed | Elevated regulatory scrutiny per FATF Recommendation 12 |
| R10-KYC-INCONSIST | Contradictory KYC field combination | Aggregate | Occupation appears inconsistent with volumes and PEP status |
| R11-MCC-HIGH-RISK | ≥3 transactions to high-risk MCC merchants | Multiple MCCs | Potentially consistent with cash-out or value conversion |
| R15-FAN-OUT | ≥25 distinct receiving counterparties | 27 counterparties | Distribution potentially consistent with structuring |
| R17-MULTI-RAIL | Mixed-rail: PIX + Card + Wire within window | Review period | Multi-channel may complicate transaction tracing |
| R19-CHARGEBACK | Chargeback history or high-CB merchant use | Aggregate | Elevated fraud risk indicator |
| R20-MERCHANT-CONVERGE | Shared merchant with another flagged subject | Aggregate | Network linkage potentially consistent with coordination |

---

## 4. Detailed Analysis

### 4.1 Income Mismatch and Economic Profile Inconsistency

Customer C102290 declared annual income of R$11,177 (approximately R$931/month) with occupation 'Driver', yet total outflows of R$134,318.84 were recorded during the review period—approximately 144× the declared monthly income. This disparity appears materially inconsistent with the stated economic profile and triggers R03-INCOME-MISMATCH at the HIGH threshold. The confirmed PEP status further compounds concerns, as the combination of political exposure and unexplained wealth flow may warrant enhanced regulatory scrutiny under FATF Recommendation 12.

### 4.2 Passthrough Pattern and Transaction Velocity

The PIX channel exhibits a passthrough ratio of 2,013.2% (R$108,041.04 outflow against R$5,366.76 inflow), potentially consistent with the account serving as a transit point for funds rather than as a destination for legitimate economic activity. A single-day velocity burst on 2025-08-01 recorded 4 transactions totaling R$42,590.11 to multiple counterparties including M200888 (R$20,

---

# SUSPICIOUS ACTIVITY REPORT (SAR)

## Case Identification

| Field | Value |
|-------|-------|
| **SAR Reference** | SAR-20260524-000149-48074c-C102093-01 |
| **Customer ID** | C102093 |
| **Preparation Date** | 2026-05-24 |
| **Run ID** | 20260524-000149-48074c |
| **Escalation Band** | Tier 1 — SAR immediate |
| **ML Confidence Band** | High |

---

## 1. Executive Summary

Customer C102093, a confirmed Politically Exposed Person (PEP) with declared occupation "Chef" and annual income of R$7,766, exhibited total outflows of R$192,074.54 during the review period—approximately 2,472% of declared annual income—a pattern potentially consistent with undisclosed income sources or layering activity. PIX passthrough ratio of 2,944.2% (R$113,519.06 outflow versus R$3,855.62 inflow) appears materially inconsistent with legitimate personal finance patterns and may warrant consideration as potential flow-through or layering behavior. The subject's activity includes Tor anonymization (tx T14MV5I9E7I9F, R$15,825.48), VPN usage (2 events), proxy usage (1 event), and cross-border transactions to high-risk jurisdiction Myanmar (tx TOOKNC1OPBY00, R$3,088.02), combined with fanout to 30 distinct counterparties across mixed payment rails (PIX, Card, Wire). The confluence of 11 concurrent rule fires (R03_HIGH, R04, R05_TOR, R07, R09, R10, R11, R15, R17, R19, R20), High ML confidence band classification, and PEP status collectively warrant immediate SAR filing and enhanced due diligence measures.

---

## 2. Triggered Alerts Summary

| Alert Code | Detection Logic | Date/Aggregate | Relevance |
|------------|-----------------|----------------|-----------|
| **R03-INCOME-MISMATCH** | Total outflow >100× declared monthly income | 2,472% of annual income (R$192,074.54 vs R$7,766) | Primary quantitative indicator of potential undisclosed income or layering |
| **R04-PASSTHRU** | PIX outflow-to-inflow ratio >200% | 2,944.2% ratio (R$113,519.06 out / R$3,855.62 in) | Potentially consistent with flow-through or layering behavior |
| **R05-ANON-TOR** | Transaction via Tor anonymization network | 2025-07-08, tx T14MV5I9E7I9F | Deliberate source obfuscation warranting enhanced scrutiny |
| **R05-ANON-VPN** | ≥2 transactions via VPN or proxy service | 2 VPN events, 1 Proxy event | Pattern of anonymization techniques across multiple transactions |
| **R07-GEO-MISMATCH** | IP-country mismatch or geographic anomaly | Cross-border to Myanmar (MM) and US | Geographic inconsistency with declared Brazil-based profile |
| **R09-PEP-EDD** | PEP status — Enhanced Due Diligence required | KYC-confirmed PEP status | Elevated regulatory scrutiny obligation per FATF Recommendation 12 |
| **R10-KYC-INCONSIST** | Contradictory KYC field combination | Declared 'Chef', Low risk rating vs high volumes | Profile inconsistency warranting source-of-funds verification |
| **R11-MCC-HIGH-RISK** | ≥3 transactions to high-risk MCC merchants | Multiple to MCC 4900, MCC 6051 | Elevated exposure to money service and utility payment categories |
| **R15-FAN-OUT** | ≥25 distinct receiving counterparties | 30 distinct counterparties across 30 transactions | Dispersion pattern potentially consistent with layering or smurfing |
| **R17-

---

# SUSPICIOUS ACTIVITY REPORT (SAR)

## SAR-20260524-000149-48074c-C100208-01

---

## 1. Case Identification

| Field | Value |
|-------|-------|
| **SAR Reference** | SAR-20260524-000149-48074c-C100208-01 |
| **Customer ID** | C100208 |
| **Prepared Date** | 2026-05-24 |
| **Run ID** | 20260524-000149-48074c |
| **Classification** | Tier 1 — Hard Alert |
| **ML Confidence Band** | High |

---

## 2. Executive Summary

Customer C100208, a declared Dentist with annual income of R$8,756, exhibits total outflow of R$144,241.98 during the review period—approximately 197× monthly declared income—which appears materially inconsistent with the stated occupational profile. PIX passthrough ratio of 3,674.6% (R$55,600.07 outflow vs R$1,513.10 inflow) may warrant consideration as potential flow-through activity. The account demonstrates anonymization events including Tor, VPN, and Proxy usage, combined with cross-border transactions to high-risk jurisdiction Myanmar (R$51,589.26) and mixed-rail activity across PIX, Card, and Wire channels. A direct wire transfer to another flagged subject (C102252) and network linkage indicators suggest potential coordinated activity requiring enhanced review.

---

## 3. Triggered Alerts

| Alert Code | Detection Logic | Date/Aggregate | Relevance |
|------------|-----------------|----------------|-----------|
| **R03-INCOME-MISMATCH** | Total outflow >100× declared monthly income | R$144,241.98 vs R$729.67/mo (~197×) | Primary quantitative indicator |
| **R04-PASSTHRU** | PIX outflow-to-inflow ratio >200% | 3,674.6% | Potential flow-through activity |
| **R05-ANON-TOR** | Transaction via Tor anonymization network | 2025-08-19 (tx TES9D9NM8CEMC) | Obstructed traceability |
| **R06-GEO-HIGH-RISK** | Cross-border to high-risk jurisdiction | Myanmar R$51,589.26 on 2025-07-11 | FATF-monitored jurisdiction |
| **R10-KYC-INCONSIST** | Contradictory KYC field combination | Score 89 / Rating Low | Classification inconsistency |
| **R11-MCC-HIGH-RISK** | ≥3 transactions to high-risk MCC merchants | MCC 4111, MCC 4829 | Money transfer/payment MCCs |
| **R17-MULTI-RAIL** | Mixed-rail: PIX + Card + Wire within window | 22 transactions multi-channel | Potential layering |
| **R20-MERCHANT-CONVERGE** | Shared merchant with another flagged subject | Aggregate period | Network convergence |
| **R21-NETWORK-LINK** | Direct wire to another flagged subject | 2025-07-14 to C102252 | Direct financial linkage |

---

## 4. Detailed Analysis

### 4.1 Income Inconsistency and Transaction Volume

The subject's declared annual income of R$8,756 (approximately R$729.67 monthly) appears materially inconsistent with total outflow of R$144,241.98 across 22 transactions during the review period. This represents approximately 16.5× annual income and triggers the R03_HIGH threshold (>100× monthly income). The activity pattern, spanning 22 distinct counterparties across multiple payment rails, warrants further review regarding source of funds.

### 4.2 Anonymization, Cross-Border, and Network Indicators

Three distinct anonymization events were recorded: a Tor network transaction (tx TES9D9NM8CEMC, R$3,410.63 PIX to C100814 on 2025-08-19), a VPN transaction (tx TP549PR319CUY, R$277.05 PIX to M200779 on 2025-09-22), and a Proxy transaction (tx TMMMDIC9EH6NQ, R$1,176.03 Wire to M200620 on 2025-08-30). Cross-border activity includes a Card transaction of R$51,589.26 to merchant M200535 in Myanmar (tx T7ILZTP10SBFN on 2025-07-11), a FATF-monitored jurisdiction. The combination of anonymization techniques and high-risk jurisdiction exposure may warrant enhanced scrutiny.

### 4.3 Network Linkages and Merchant Risk

A direct wire transfer of R$1,665.40 to flagged subject C102252 (tx TSM9Q0FWI3AUT on 2025-07-14) establishes a financial linkage to another subject under enhanced review, triggering R21. High-risk MCC transactions totaling R$41,200.16 include payments to MCC 4111 (Transportation, R$18,915.77 to M200392) and MCC 4829 (Wire Transfer/Money Orders, R$22,284.39 to M200042). The mixed-rail pattern across PIX, Card, and Wire channels within the review window, combined with merchant convergence indicators, is potentially consistent with layering techniques.

---

## 5. Regulatory Basis

- **FATF Recommendation 20** — Suspicious Transaction Reporting obligation
- **FATF Recommendation 10** — Customer Due Diligence requirements including income verification
- **Circular BACEN 3.978/2020** — AML/CFT obligations for regulated financial institutions
- **COAF Normative Instruction 1/2014** — SAR filing obligation for transactions inconsistent with customer profile
- **COAF Communication Threshold** — Activity materially inconsistent with declared occupation and income

---

## 6. Recommended Actions

1. **Submit SAR to COAF** within regulatory timeframe citing income-mismatch, passthrough, anonymization, geo-risk, and network linkage indicators
2. **Initiate Enhanced Due Diligence (EDD)** requesting source of funds

---

# SUSPICIOUS ACTIVITY REPORT (SAR)

## Case Identification

| Field | Value |
|-------|-------|
| SAR Reference | SAR-20260524-000149-48074c-C101445-01 |
| Customer ID | C101445 |
| Run ID | 20260524-000149-48074c |
| Prepared At | 2026-05-24T00:01:49Z |
| Classification | CRITICAL — Confirmed Sanctions Match |
| Escalation Band | Tier 1 — Hard Alert |

---

## 1. Executive Summary

Customer C101445, a self-declared Designer with annual income of R$21,304, presents a **confirmed KYC-level sanctions list match** requiring immediate regulatory escalation. The account exhibits an extreme PIX passthrough ratio of 899.2% (R$36,834.19 outflow versus R$4,096.14 inflow) and total outflows of R$68,070.28 representing approximately 38× monthly declared income equivalent, patterns materially inconsistent with the declared low-risk occupation. Anonymization events including VPN (tx T4TCRQ3MZFYUC) and Proxy (tx TLDMMIWTI9WSU) usage on 2025-08-03, combined with cross-border transactions to AE and PT jurisdictions and high-risk MCC activity (6011, 6211, 6051), may warrant further review for potential layering or integration activity. Network convergence with flagged customer C102304 via tx TXAZ60SQBYE3A and mixed-rail activity across PIX, Card, and Wire channels present additional risk indicators requiring immediate SAR filing.

---

## 2. Triggered Alerts

| Alert Code | Detection Logic | Date/Aggregate | Relevance |
|------------|-----------------|----------------|-----------|
| **R08-SANCTIONS-SCREEN** | Confirmed KYC-level sanctions list match | KYC record | Primary compliance trigger — confirmed sanctions match requiring immediate escalation |
| **R04-PASSTHRU** | PIX outflow-to-inflow ratio >200% | 899.2% | Indicates potential passthrough activity — R$36,834.19 out vs R$4,096.14 in |
| **R05-ANON-VPN** | ≥2 transactions via VPN or proxy service | 2025-08-03 | Two anonymization events same day — VPN and Proxy usage |
| **R11-MCC-HIGH-RISK** | ≥3 transactions to high-risk MCC merchants | MCC 6011, 6211, 6051 | Financial services MCCs potentially consistent with layering |
| **R17-MULTI-RAIL** | Mixed-rail: PIX + Card + Wire within window | 2025-07-04 to 2025-09-26 | Diversified payment rails may warrant review |
| **R19-CHARGEBACK** | Chargeback history or high-CB merchant use | Aggregate | Potential indicator of fraudulent patterns |
| **R20-MERCHANT-CONVERGE** | Shared merchant with another flagged subject | 2025-07-04 | Network link to flagged customer C102304 |

---

## 3. Detailed Analysis

### 3.1 Sanctions Status

The customer presents a **confirmed KYC-level sanctions list match** (sanctions_status.confirmed_sanctions_match: true, severity: "confirmed"). This constitutes the primary compliance trigger requiring immediate SAR filing within 24 hours per COAF Resolution 40/2021 and potential transaction blocking pending verification against OFAC/UN consolidated sanctions lists.

### 3.2 Transactional Behavior Analysis

The account demonstrates behavioral patterns materially inconsistent with the declared Designer occupation and R$21,304 annual income. Total outflows of R$68,070.28 represent approximately 3.2× annual declared income (equivalent to approximately 38× monthly income). The PIX passthrough ratio of 899.2% — with R$36,834.19 in outflows versus only R$4,096.14 in inflows — may warrant review for potential layering or passthrough activity. Mixed-rail activity across 22 transactions to 22 distinct counterparties utilizing PIX, Card, and Wire channels, including 2 wire transfers (tx TLDMMIWTI9WSU for R$4,738.23 and tx T9OSWZJ1F3HT1 for R$7,490.44), demonstrates sophisticated channel diversification potentially consistent with layering techniques.

### 3.3 Anonymization and Cross-Border Patterns

Two anonymization events occurred on 2025-08-03: a wire transfer via Proxy to M200855 (tx TLDMMIWTI9WSU, R$4,738.23) and a cross-border card transaction to PT via VPN (tx T4TCRQ3MZFYUC, R$2,121.78, MCC 6211 Securities). Cross-border activity includes transactions to AE (tx TT1YJJ9T8WM3E on 2025-07-18 for R$3,147.06; tx T3CTGGX5K9LUR on 2025-09-26 for R$3,041.49 at MCC 6051 Quasi-Cash) and PT. High-risk MCC activity at financial services codes 6011, 6211, and 6051 may warrant further review for potential value extraction patterns. Network convergence with flagged customer C102304 via tx TXAZ60SQBYE3A (R$2,975.97, MCC 6011) on 2025-07-04 suggests potential coordinated activity requiring investigation.

---

## 4. Regulatory Basis

- **UN Security Council Consolidated Sanctions List** — Confirmed match requiring immediate notification per COAF Normative Instruction
- **Circular BACEN 3.978/2020 Art. 27** — Suspicious activity reporting obligation for

---

# SUSPICIOUS ACTIVITY REPORT (SAR)

---

## 1. Case Identification

| Field | Value |
|-------|-------|
| **SAR Reference** | SAR-20260524-000149-48074c-C101542-01 |
| **Customer ID** | C101542 |
| **Run ID** | 20260524-000149-48074c |
| **Report Prepared** | 2026-05-24T00:01:49Z |
| **Severity Rating** | High |
| **Priority Score** | 61.79 |
| **ML Confidence Band** | High |
| **Escalation Band** | Tier 1 — Hard alert |

---

## 2. Executive Summary

Customer C101542, a self-declared Freelancer with declared annual income of R$3,687 (approximately R$307/month), presents total outflows of R$103,286.93 during the review period—potentially consistent with income inflation exceeding 336× declared monthly income, which warrants further review. The PIX passthrough ratio of 751.2% (R$73,948.90 outflow vs R$9,843.55 inflow) may indicate funds transit activity. Activity includes one Tor-anonymized transaction to a gambling merchant (MCC 7995), mixed-rail usage across PIX, Card, and Wire channels, 28 distinct counterparties, and a direct wire transfer to another flagged subject (C100375), collectively presenting a behavioral profile materially inconsistent with a low-risk L1-tier freelancer. Cross-border activity includes a wire transfer of R$6,257.41 to Libya (high-risk jurisdiction), warranting heightened regulatory attention.

---

## 3. Triggered Alerts

| Alert Code | Detection Logic | Date/Aggregate | Relevance |
|------------|-----------------|----------------|-----------|
| **R03-INCOME-MISMATCH** | Total outflow >100× declared monthly income | 336× (R$103,286.93 vs R$307/month) | Primary quantitative indicator of economic activity materially inconsistent with declared income profile |
| **R04-PASSTHRU** | PIX outflow-to-inflow ratio >200% | 751.2% | May indicate funds transit or layering activity through the account |
| **R05-ANON-TOR** | Transaction via Tor anonymization network | 2025-07-14 (tx T991C2EOAP061) | Tor-anonymized transaction to gambling merchant potentially consistent with concealment intent |
| **R11-MCC-HIGH-RISK** | ≥3 transactions to high-risk MCC merchants | MCC 7995, 4829, 4900 | Pattern of transactions to high-risk merchant categories warrants scrutiny |
| **R15-FAN-OUT** | ≥25 distinct receiving counterparties | 28 counterparties | High counterparty diversity may indicate structuring or layering behavior |
| **R17-MULTI-RAIL** | Mixed-rail: PIX + Card + Wire within window | 3 wire transfers | Multi-channel activity potentially consistent with layering across payment rails |
| **R19-CHARGEBACK** | Chargeback history or high-CB merchant use | Aggregate | Potential association with disputed or fraudulent transaction patterns |
| **R20-MERCHANT-CONVERGE** | Shared merchant with another flagged subject | Aggregate | Network overlap with other subjects under review may indicate coordinated activity |
| **R21-NETWORK-LINK** | Direct wire to another flagged subject | 2025-07-27 (tx T8XYRVKV8AGM2) | Direct financial linkage to another flagged subject warrants coordinated investigation |

---

## 4. Detailed Analysis

### 4.1 Income and Transaction Volume Disparity

The customer's declared annual income of R$3,687 (approximately R$307/month) appears materially inconsistent with total outflows of R$103,286.93 during the review period—a disparity of approximately 336× monthly income. This significantly exceeds the R03_HIGH threshold (>100× monthly income). The customer's L1 KYC tier and "Low" risk rating were assigned based on stated freelancer occupation, yet observed transaction volumes warrant enhanced scrutiny and potential income verification.

### 4.2 Passthrough and Layering Indicators

PIX activity demonstrates a passthrough ratio of 751.2%: outflows of R$73,948.90 versus inflows of R$9,843.55, triggering R04 (>200% threshold). This pattern, combined with 28 distinct counterparties (triggering R15) and mixed-rail activity across PIX, Card, and Wire channels (triggering R17), may indicate the account is being used for funds transit or layering purposes. Notable transactions include: tx TSWFX3XIHOF2R on 2025-08-04 for R$25,848.82 to merchant M200966 (MCC 4900); tx TCIOVP5V3QUJF on 2025-08-17 for R$11,121.30 to merchant M200616 (MCC 4829—wire transfer services); and wire transfer TESLWHQ8LG92B on 2025-10-04 for R$6,257.41 to merchant M200776 with destination geo-country Libya (LY), a FATF grey-list jurisdiction.

### 4.3 Anonymization and Network Linkage

Transaction T991C2EOAP061 on 2025-07-14 for R$5,760.65 to merchant M200971 (MCC 7995—gambling) was executed via Tor anonymization network, triggering R05_TOR. A separate transaction (TUI6B5CHKXRA8 on 2025-09-24 for R$779.48) was executed via Proxy service. Most significantly, wire transfer T