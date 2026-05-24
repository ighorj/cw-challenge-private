# Investigation Summary — run 20260524-000149-48074c
_Backend: anthropic · Generated: 2026-05-24T03:07:05+00:00_
_ML confidence labels are calibrated relative to the investigated escalation cohort, not the full customer population._

## C100091
**Recommendation:** file_sar_immediate
**Confidence:** high
ML confidence: **Moderate-High** (cohort rank #7)

Customer C100091, declared as a Store Owner with annual income of R$10,173, exhibited total outflows of R$91,349.77 during the review period—approximately 898× the monthly income equivalent (R$847.75/mo), which appears materially inconsistent with the stated economic profile. A PIX passthrough ratio of 4,008.5% (R$57,117.34 out vs R$1,424.90 in) may warrant further review for potential layering activity. A wire transfer of R$11,672.88 to counterparty M200363 in Iran (IR) triggered a transactional sanctions screening event requiring entity-level review. Mixed-rail activity (PIX, Wire, Card), high-risk MCC transactions, network linkage to another flagged subject, and shared merchant convergence collectively suggest a pattern potentially consistent with structured fund movement warranting immediate escalation.

**Triggered typologies:** structuring, income-mismatch, passthrough, high-risk-geography, sanctions-screening, high-risk-merchant, mixed-rail-layering, chargeback-risk, merchant-convergence, network-linkage

### Key facts
- Total outflow R$91,349.77 vs declared annual income R$10,173 (approximately 898× monthly equivalent of R$847.75)
- PIX passthrough ratio 4,008.5%: R$57,117.34 outflow vs R$1,424.90 inflow
- 1 transactional sanctions screening event on wire transfer TJRKHTP81JROK (R$11,672.88 to M200363, geo_country: IR) on 2025-08-07
- 3 cross-border events detected including transactions to IR, DE, and ES
- 18 transactions across 18 distinct counterparties during review period
- Mixed-rail activity: 2 wire transfers, multiple PIX and Card transactions
- High-risk MCC transactions: T1RBG8O7Y6NC6 (MCC 7995 gambling) R$7,680.48; TJZQI83ROKQ81 (MCC 6011 financial institutions) R$11,591.32
- R02_LOW triggered: 1-2 transactions in R$9,000–R$10,000 structuring band (transaction TLF007IGRTEAB R$9,732.08)
- Wire transfer TMGHPD5XFHXCJ to counterparty C100236 (R$1,255.77) triggered network linkage rule R21

### Timeline
- `2025-07-09` — PIX payment R$7,680.48 to C100179, MCC 7995 (gambling), triggering R11 high-risk MCC (tx T1RBG8O7Y6NC6)
- `2025-07-15` — PIX payment R$9,732.08 to M200985, within R$9k-R$10k structuring band, triggering R02_LOW (tx TLF007IGRTEAB)
- `2025-07-18` — Wire transfer R$1,255.77 to flagged customer C100236, triggering R21 network linkage (tx TMGHPD5XFHXCJ)
- `2025-08-07` — Wire transfer R$11,672.88 to M200363 in Iran (IR), sanctions screening event triggered (R08), cross-border high-risk jurisdiction (R06) (tx TJRKHTP81JROK)
- `2025-08-20` — High-value PIX payment R$18,507.97 to M200796 (tx TRD52BHJTAJLQ)
- `2025-08-22` — Cross-border PIX payment R$540.93 to M200527 in Germany (DE) (tx TQWXFJ3VKTJO0)
- `2025-10-03` — Card transaction R$11,591.32 to M200233, MCC 6011 (financial institution/ATM), triggering R11 (tx TJZQI83ROKQ81)
- `2025-10-04` — Cross-border PIX payment R$4,987.69 to M200800 in Spain (ES) (tx TGWER3C1MRCSR)

---

## C101208
**Recommendation:** file_sar_immediate
**Confidence:** high — 9 concurrent rule fires including sanctions screening event, severe income mismatch (1,150% annual), Syria-linked wire transfer, and all facts directly traceable to transaction-level evidence in bundle
ML confidence: **Moderate** (cohort rank #9)

Subject declared as Chef with annual income of R$13,047 exhibited total outflow of R$150,178.09 during review period, representing approximately 1,150% of annual declared income and triggering R03_HIGH (>100× monthly income). Activity involved 29 distinct counterparties (R15), mixed-rail usage across PIX/Card/Wire (R17), 2 VPN anonymization events (R05_VPN), 1 transactional sanctions screening event involving Syria-bound wire (R08), and multiple high-risk MCC transactions (R11). Cross-border activity to jurisdictions including Syria, Russia, and Yemen, combined with card-not-present transactions lacking 3DS authentication (R18) and chargeback indicators (R19), presents a pattern potentially consistent with layered fund movement warranting immediate escalation.

**Triggered typologies:** income-mismatch, anonymization, sanctions-screening, high-risk-merchant, fan-out, mixed-rail-layering, card-fraud-indicators, merchant-convergence

### Key facts
- Total outflow R$150,178.09 vs declared annual income R$13,047 (~1,150% of annual / ~1,150× monthly income ratio triggering R03_HIGH)
- 29 transactions to 29 distinct counterparties during review period (R15 fan-out threshold met)
- 2 VPN anonymization events detected: tx TJZRYWR88WZHJ on 2025-07-22 and tx TQSBX6QW4LBWX on 2025-08-29 (R05_VPN)
- 1 transactional sanctions screening event: tx TNHZDN7D6LYK6 on 2025-08-12, Wire R$2,166.18 to counterparty M200815 in Syria (R08)
- 9 cross-border events identified across jurisdictions including PT, SY, GB, RU, YE
- 3 wire transfers totaling R$21,444.38 to counterparties M200815 (SY), M200524 (GB), M200962 (PT)
- High-risk MCC activity: MCC 7995 (gambling) transactions including R$6,889.49 on 2025-09-08 and R$14,011.86 on 2025-09-23 (R11)
- PIX outflow R$77,634.56 with R$0.00 PIX inflow — no passthrough ratio calculable due to zero inflow
- R20 (merchant convergence) triggered indicating shared receiving merchant with another flagged subject
- R18 (≥3 CNP transactions without 3DS) and R19 (chargeback indicators) triggered

### Timeline
- `2025-07-22` — VPN anonymization event: PIX R$1,241.06 to M200526 (Portugal), MCC 5999 (tx TJZRYWR88WZHJ, R05_VPN)
- `2025-08-12` — Sanctions screening event: Wire R$2,166.18 to M200815 (Syria), MCC 5999 (tx TNHZDN7D6LYK6, R08)
- `2025-08-18` — Wire R$2,234.10 to M200524 (United Kingdom), MCC 5732 (tx TTY9XRY0X3DFN)
- `2025-08-29` — VPN anonymization event: Card R$1,089.07 to M200972 (Russia), MCC 5411 (tx TQSBX6QW4LBWX, R05_VPN)
- `2025-09-08` — High-risk MCC transaction: Card R$6,889.49 to M200212 (Yemen), MCC 7995 gambling (tx TOHDJ4A6OYGZA, R11)
- `2025-09-17` — Largest wire: R$17,044.10 to M200962 (Portugal), MCC 5999 (tx T01OIP42LWSQO)
- `2025-09-23` — High-risk MCC transaction: Card R$14,011.86 to M200637 (Brazil), MCC 7995 gambling (tx TIQS2U9KT1J0U, R11)
- `2025-09-23` — Cross-border PIX R$7,718.63 to M200331 (Russia), MCC 6011 (tx TF9EJQVFQTQJM)

---

## C101028
**Recommendation:** file_sar_immediate
**Confidence:** high
ML confidence: **Moderate** (cohort rank #10)

Customer C101028 presents a confirmed KYC-level sanctions list match combined with PEP status, requiring immediate Enhanced Due Diligence review. The account exhibits a PIX passthrough ratio of 587.3% (R$46,554 outflow vs R$7,927 inflow) and total outflow of R$71,406 against declared annual income of R$47,312, potentially consistent with funds movement inconsistent with stated Designer occupation. Two anonymization events (1 VPN, 1 Proxy) and cross-border activity including a transaction to North Korea (KP) compound the risk profile across nine concurrent rule triggers.

**Triggered typologies:** passthrough, anonymization, sanctions-screening, PEP-EDD, KYC-inconsistency, high-risk-merchant, card-CNP-fraud-risk, chargeback-risk, merchant-convergence

### Key facts
- Confirmed KYC-level sanctions list match (sanctions_status.confirmed_sanctions_match: true)
- PEP status confirmed (kyc.pep: 'Yes'), triggering R09 Enhanced Due Diligence requirement
- PIX passthrough ratio 587.3%: R$46,553.76 outflow vs R$7,927.19 inflow
- Total outflow R$71,406.40 equals approximately 151% of declared annual income (R$47,312)
- 2 anonymization events detected: 1 VPN (tx TQXICCVPO421G, 2025-07-08) and 1 Proxy (tx TCTY4DMIEFHUU, 2025-07-03)
- Cross-border transaction to North Korea (KP): R$4,390.02 Card payment to M200105 on 2025-07-01
- High-risk MCC transactions to MCC 6211 (Securities/Brokers) and MCC 6011 (Financial Institutions)
- 18 transactions to 18 distinct counterparties during review period
- R10 triggered indicating contradictory KYC field combination (Low risk_rating despite PEP status and sanctions match)

### Timeline
- `2025-07-01` — Cross-border Card transaction R$4,390.02 to North Korea (KP), counterparty M200105, MCC 4789 (tx TFNO8A1FBZUMA)
- `2025-07-01` — High-value PIX outflow R$10,557.78 to M200161, MCC 5999 (tx T4ZAVV478VX1Q)
- `2025-07-03` — PIX transaction R$3,376.31 via Proxy anonymization to M200538, MCC 6011 (tx TCTY4DMIEFHUU, triggers R05_VPN)
- `2025-07-05` — Card transaction R$1,381.46 to high-risk MCC 6211 (Securities/Brokers), counterparty M200818 (tx THYRFBT3SQ4RJ, triggers R11)
- `2025-07-08` — Card transaction R$6,975.17 via VPN anonymization to M200118, MCC 6011 (tx TQXICCVPO421G, triggers R05_VPN)
- `2025-07-17` — Card transaction R$3,969.08 to customer C100265, rooted device detected (tx T4DASTQ56M2QJ)
- `2025-08-11` — Card transaction R$4,317.90 to M200980, high-risk MCC 4111 (tx TKFJIS94Y7C0I, triggers R11)
- `2025-09-12` — Cross-border Card transaction R$1,135.20 to Germany (DE), counterparty M200386, MCC 4829 (tx THCF7RXE8PSWC)

---

## C100837
**Recommendation:** file_sar_immediate
**Confidence:** high
ML confidence: **Very High** (cohort rank #2)

PEP-flagged customer (R09) with declared annual income of R$7,577 exhibited total outflow of R$139,083.50 across 29 transactions, representing approximately 18× annual income and potentially consistent with income mismatch typology (R03_HIGH). PIX passthrough ratio of 4,367% (R$104,965.61 out vs R$2,403.44 in) warrants review for potential layering activity. One Tor anonymization event detected (R05_TOR), combined with cross-border activity to high-risk jurisdictions including Myanmar (MM), and mixed-rail usage (PIX/Card/Wire) may indicate efforts to obscure transaction origins and destinations.

**Triggered typologies:** income-mismatch, passthrough, anonymization, geo-high-risk, PEP-EDD, KYC-inconsistency, high-risk-MCC, fan-out, multi-rail, chargeback-risk, merchant-convergence

### Key facts
- Total outflow R$139,083.50 vs declared annual income R$7,577 (approximately 18× annual income) — R03_HIGH triggered
- PIX passthrough ratio 4,367% (R$104,965.61 outflow / R$2,403.44 inflow) — R04 triggered
- 27 distinct counterparties across 29 transactions — R15 fan-out triggered
- 1 Tor anonymization event on 2025-08-04 (tx T4VUTEFNQBUQH, R$2,782.76 to M200806) — R05_TOR triggered
- 6 cross-border events including Myanmar (MM) which is FATF high-risk jurisdiction — R06 triggered
- 5 wire transfers to GB, US, DE destinations totaling significant outflow
- PEP status confirmed requiring Enhanced Due Diligence — R09 triggered
- Mixed-rail activity: PIX, Card, and Wire within review period — R17 triggered
- High-risk MCC activity including MCC 4829 (wire transfer services) and MCC 6051 (quasi-cash) — R11 triggered

### Timeline
- `2025-07-08` — Wire transfer R$1,702.86 to M200513 (US), MCC 4789 (tx TPCPL90MU9SRF)
- `2025-07-22` — Card transaction R$1,361.82 to Myanmar (MM) — high-risk FATF jurisdiction (tx TT94KQ67Q0Q92, R06 cross-border)
- `2025-08-01` — Wire transfer R$12,957.12 to M200053 (GB), MCC 4829 wire transfer services (tx T4MHTBYMYYY0C)
- `2025-08-04` — PIX R$2,782.76 to M200806 executed via Tor anonymization network (tx T4VUTEFNQBUQH, R05_TOR triggered)
- `2025-08-07` — Wire transfer R$1,746.42 to M200849 (DE), MCC 4111 (tx TDU1GAYIB8X9S)
- `2025-08-16` — PIX R$8,638.60 to M200237 (GB), cross-border, MCC 4900 (tx TJ7QJ1RGK5KXZ, R06 cross-border)
- `2025-08-18` — Card transaction R$1,142.06 to M200004, MCC 6051 quasi-cash, rooted device detected (tx TPTMR0FBGXQOB)
- `2025-08-20` — PIX R$27,304.70 to M200309, MCC 4829 wire transfer services — largest single transaction (tx TTP6ORO2Q3V22, R11 high-risk MCC)

---

## C101582
**Recommendation:** file_sar_immediate
**Confidence:** high
ML confidence: **Moderate-High** (cohort rank #8)

Customer C101582 presents a confirmed KYC-level sanctions list match combined with significant income-to-outflow disparity (R$89,473 total outflow against R$10,907 declared annual income, approximately 8.2× annual or ~98× monthly). The account exhibits two Tor anonymization events, cross-border activity including a transaction to Iraq (high-risk jurisdiction), and mixed-rail usage across PIX, Card, and Wire channels. These concurrent signals across income mismatch, anonymization, sanctions, and merchant typologies warrant immediate escalation.

**Triggered typologies:** income-mismatch, anonymization, sanctions, high-risk-merchant, mixed-rail, chargeback-risk, network-convergence

### Key facts
- Confirmed KYC-level sanctions list match (sanctions_status.confirmed_sanctions_match: true)
- Total outflow R$89,473.16 vs declared annual income R$10,907 (~8.2× annual income, triggering R03_LOW >50× monthly threshold)
- Two Tor anonymization events detected: tx T1UADPDDHFJPA on 2025-07-15 (R$13,310.35) and tx T4P4Q65XC570F on 2025-09-08 (R$3,328.57)
- Cross-border activity to Iraq (IQ): tx T1XY2A460O51H on 2025-08-21 for R$3,294.89 to MCC 6051 (quasi-cash)
- Mixed-rail activity: PIX outflow R$46,573.94, Card transactions, and 1 Wire transfer (R$24,230.02 on 2025-09-21)
- High-risk MCC transactions: MCC 4900 (utilities, potential value transfer) on tx TF8F0668QXDKJ and tx TOYX9MA23Q8NW
- 22 distinct counterparties across 23 transactions in review period

### Timeline
- `2025-07-05` — PIX transaction R$506.42 to M200966, MCC 4900 (high-risk merchant) (tx TF8F0668QXDKJ)
- `2025-07-15` — PIX R$13,310.35 to M200696 via Tor anonymization network (tx T1UADPDDHFJPA, rule R05_TOR fires)
- `2025-07-23` — Cross-border Card transaction R$453.81 to France (FR) (tx TG9WZU12O72OV)
- `2025-08-21` — Cross-border Card transaction R$3,294.89 to Iraq (IQ), MCC 6051 quasi-cash (tx T1XY2A460O51H)
- `2025-08-25` — Card transaction R$7,454.37 to C101819, MCC 4900 — merchant convergence with flagged subject (tx TOYX9MA23Q8NW, rule R20 fires)
- `2025-09-08` — PIX R$3,328.57 to M200797 via Tor anonymization network (second Tor event) (tx T4P4Q65XC570F, rule R05_TOR fires)
- `2025-09-21` — Wire transfer R$24,230.02 to M200508 — mixed-rail activity confirmed (tx TMBR17QPP9GD3, rule R17 fires)
- `2025-10-01` — PIX R$4,002.64 to M200282 (tx TARPIXB23P87B)

---

## C102290
**Recommendation:** file_sar_immediate
**Confidence:** high
ML confidence: **Extreme** (cohort rank #1)

Customer C102290 is a PEP-flagged individual with declared occupation 'Driver' and annual income of R$11,177 (approximately R$931/month), yet exhibited total outflows of R$134,318.84 during the review period—approximately 144× monthly declared income—which appears materially inconsistent with stated economic profile. The account demonstrates a PIX passthrough ratio of 2,013% (R$108,041 outflow against R$5,367 inflow), potentially consistent with funds-transit or layering activity. Three anonymization events (1 Tor, 2 VPN) were detected across transaction sessions, and 27 distinct counterparties received funds, warranting further review for fan-out structuring. The combination of PEP status, extreme income mismatch, anonymization tool usage, and high-risk MCC merchant activity across multiple payment rails (PIX, Card, Wire) collectively elevates suspicion and may warrant immediate regulatory notification.

**Triggered typologies:** velocity-burst, income-mismatch, passthrough, anonymization, PEP-EDD, KYC-inconsistency, high-risk-MCC, fan-out, multi-rail, chargeback-risk, merchant-convergence

### Key facts
- Total outflow R$134,318.84 against declared annual income R$11,177 (approximately 144× monthly income of R$931), triggering R03_HIGH
- PIX passthrough ratio 2,013.2%: R$108,041.04 outflow vs R$5,366.76 inflow, triggering R04
- Single-day velocity burst on 2025-08-01: 4 transactions totaling R$42,590.11, triggering R01
- 27 distinct counterparties received funds during review period, triggering R15 fan-out rule
- 3 anonymization events detected: 1 Tor session (tx TNUU7IUG3D1A2 on 2025-10-03) and 2 VPN sessions (tx TB24ZK5RW3PP8 on 2025-08-12, tx TZ76800M19NE3 on 2025-09-28), triggering R05_TOR
- PEP status confirmed in KYC record, triggering R09 Enhanced Due Diligence requirement
- KYC risk score 98/100; ML confidence band 'Extreme' with cohort rank 1; ML probability 0.9998
- Cross-border card transaction to UAE (geo_country: AE) on 2025-07-10 for R$3,196.10 (tx TLRPWM2IMAYPY)
- High-risk MCC transactions detected: MCC 6051 (Quasi-Cash), MCC 6211 (Securities), MCC 6011 (ATM/Cash), MCC 4814 (Telecom), triggering R11
- Multi-rail activity confirmed: PIX, Card, and Wire transactions within review window, triggering R17
- Declared occupation 'Driver' inconsistent with transaction volumes and PEP status, contributing to R10 KYC inconsistency flag

### Timeline
- `2025-07-10` — Cross-border card transaction to UAE merchant M200283, R$3,196.10, MCC 6051 (Quasi-Cash) (tx TLRPWM2IMAYPY, cross_border typology tag)
- `2025-07-29` — Card transaction to M200004, R$3,296.42, MCC 6051 (Quasi-Cash), rooted device detected (tx T4FZR2CAYR4SR)
- `2025-08-01` — Velocity burst day: 4 transactions totaling R$42,590.11 to 3+ counterparties including PIX to M200888 (R$20,509.18), M200489 (R$11,742.01), M200845 (R$8,224.55) (single_day_bursts array, R01 trigger)
- `2025-08-12` — Wire transfer via VPN to M200662, R$1,364.47, MCC 5411 (tx TB24ZK5RW3PP8, anonymization_vpn typology tag)
- `2025-09-28` — PIX transaction via VPN to M200393, R$8,506.10, MCC 4900 (tx TZ76800M19NE3, anonymization_vpn typology tag)
- `2025-10-03` — Card transaction via Tor network to M200122, R$3,834.91, MCC 6011 (ATM/Cash) (tx TNUU7IUG3D1A2, anonymization_tor typology tag, R05_TOR trigger)

---

## C102093
**Recommendation:** file_sar_immediate
**Confidence:** high — 11 concurrent rule fires (R03_HIGH, R04, R05_TOR, R07, R09, R10, R11, R15, R17, R19, R20); ML probability 0.999; all key facts directly traceable to transaction records and KYC data in evidence bundle
ML confidence: **High** (cohort rank #5)

PEP-flagged customer (R09) with declared annual income of R$7,766 exhibited total outflows of R$192,074.54, representing approximately 2,472% of annual income (R03_HIGH). PIX passthrough ratio of 2,944.2% (R$113,519.06 outflow vs R$3,855.62 inflow) is materially inconsistent with legitimate personal finance patterns (R04). Activity includes Tor anonymization (1 event), VPN usage (2 events), and proxy usage (1 event), combined with cross-border transactions to high-risk jurisdiction Myanmar and IP-country mismatches (R05_TOR, R07), warranting immediate escalation review.

**Triggered typologies:** income-mismatch, passthrough, anonymization, PEP-EDD, geo-mismatch, high-risk-mcc, fanout, mixed-rail, chargeback-risk, merchant-convergence, KYC-inconsistency

### Key facts
- Total outflow R$192,074.54 vs declared annual income R$7,766 (approximately 2,472% of annual income) — R03_HIGH triggered
- PIX passthrough ratio 2,944.2% (R$113,519.06 outflow vs R$3,855.62 inflow) — R04 triggered
- 30 distinct counterparties across 30 transactions — R15 fanout triggered
- Anonymization events: 1 Tor (tx T14MV5I9E7I9F), 2 VPN, 1 Proxy — R05_TOR triggered
- Cross-border activity to Myanmar (MM) via tx TOOKNC1OPBY00 on 2025-07-17 — high-risk jurisdiction exposure
- PEP status confirmed in KYC — R09 PEP-EDD requirement triggered
- Mixed-rail activity: PIX + Card + Wire within review window — R17 triggered
- ≥3 transactions to high-risk MCC merchants (MCC 4900, 6051) — R11 triggered
- KYC inconsistency detected (declared occupation 'Chef' with low income rating vs high transaction volumes) — R10 triggered
- Chargeback risk indicator present — R19 triggered
- Shared receiving merchant with another flagged subject — R20 triggered

### Timeline
- `2025-07-08` — Card transaction R$15,825.48 to M200243 executed via Tor anonymization network (MCC 6051) (tx T14MV5I9E7I9F — R05_TOR fires)
- `2025-07-17` — Cross-border card transaction R$3,088.02 to Myanmar (MM) merchant M200684 (tx TOOKNC1OPBY00 — high-risk geo exposure)
- `2025-07-18` — High-value PIX outflow R$28,584.45 to M200989 (MCC 4900 high-risk) (tx T16QYYM1VN5DG — R11 fires)
- `2025-08-03` — Cross-border PIX outflow R$12,385.50 to US merchant M200067 (tx TGKT5KP09AYYH — cross-border activity)
- `2025-08-14` — Card transaction R$8,709.32 to M200446 from rooted device (tx T1Y075FPNVJEF — device integrity concern)
- `2025-09-09` — PIX outflow R$4,578.53 to M200879 via VPN anonymization (tx TOE917V7W7073 — R05_VPN pattern)
- `2025-09-10` — Wire transfer R$1,267.89 to M200402 — mixed-rail escalation (tx TX718NJNNFBJJ — R17 fires)
- `2025-10-04` — PIX outflow R$7,372.49 to M200450 via Proxy anonymization (tx TW909K20R5G5S — anonymization pattern continues)

---

## C100208
**Recommendation:** file_sar_immediate
**Confidence:** high
ML confidence: **High** (cohort rank #3)

Customer C100208, declared as a Dentist with annual income of R$8,756, exhibits total outflow of R$144,242 during the review period—approximately 16.5× annual declared income and materially inconsistent with stated profile. PIX passthrough ratio of 3,674.6% (R$55,600 out vs R$1,513 in) suggests potential flow-through activity. Anonymization events including Tor, VPN, and Proxy usage, combined with cross-border transactions to high-risk jurisdiction Myanmar and mixed-rail activity across PIX, Card, and Wire, warrant further scrutiny. A direct wire transfer to another flagged subject (C102252) and shared merchant activity with another flagged subject indicate potential network linkages requiring enhanced review.

**Triggered typologies:** income-mismatch, passthrough, anonymization, geo-high-risk, kyc-inconsistency, high-risk-merchant, mixed-rail, merchant-convergence, network-linkage

### Key facts
- Total outflow R$144,241.98 vs declared annual income R$8,756 (>100× monthly income threshold per R03_HIGH)
- PIX passthrough ratio 3,674.6%: R$55,600.07 outflow vs R$1,513.10 inflow
- 1 Tor anonymization event on tx TES9D9NM8CEMC (2025-08-19, R$3,410.63 PIX to C100814)
- 1 VPN event on tx TP549PR319CUY (2025-09-22, R$277.05 PIX to M200779)
- 1 Proxy event on tx TMMMDIC9EH6NQ (2025-08-30, R$1,176.03 Wire to M200620)
- 4 cross-border events including Card transaction to Myanmar (MM) for R$51,589.26 on 2025-07-11
- 2 wire transfers recorded; one to flagged subject C102252 (R$1,665.40 on 2025-07-14)
- High-risk MCC transactions: MCC 4111 (R$18,915.77), MCC 4829 (R$22,284.39)
- Mixed-rail activity: PIX, Card, and Wire transactions within review window
- 22 distinct counterparties across 22 transactions
- KYC risk score 89/100 with Low risk rating—potentially inconsistent classification given triggered rules

### Timeline
- `2025-07-03` — PIX R$18,915.77 to merchant M200392 (MCC 4111 high-risk); R11 triggered (tx TDL35CEBX1UUB)
- `2025-07-11` — Card R$51,589.26 to merchant M200535 in Myanmar (MM); R06 cross-border high-risk jurisdiction triggered (tx T7ILZTP10SBFN)
- `2025-07-14` — Wire R$1,665.40 to flagged subject C102252; R21 network linkage triggered (tx TSM9Q0FWI3AUT)
- `2025-08-16` — Card R$22,284.39 to merchant M200042 (MCC 4829 high-risk); R11 triggered (tx T5EHA9CPQOOVG)
- `2025-08-19` — PIX R$3,410.63 to C100814 via Tor network; R05_TOR anonymization triggered (tx TES9D9NM8CEMC)
- `2025-08-30` — Wire R$1,176.03 to M200620 via Proxy; anonymization event recorded (tx TMMMDIC9EH6NQ)
- `2025-09-05` — Card R$1,963.93 to M200234 in Germany (DE); R06 cross-border triggered (tx TIYS64RBC1N8I)
- `2025-09-22` — PIX R$277.05 to M200779 via VPN; anonymization event recorded (tx TP549PR319CUY)

---

## C101445
**Recommendation:** file_sar_immediate
**Confidence:** high — confirmed sanctions match at KYC level, 7 concurrent rule fires (R04, R05_VPN, R08, R11, R17, R19, R20), ML probability 0.999, all behavioral indicators traceable to specific transaction records
ML confidence: **Moderate-High** (cohort rank #6)

Customer C101445, a self-declared Designer with annual income of R$21,304, presents a confirmed KYC-level sanctions list match requiring immediate escalation. The account exhibits an extreme PIX passthrough ratio of 899.2% (R$36,834 outflow vs R$4,096 inflow), total outflows of R$68,070 representing approximately 38× annual declared income, and anonymization events including both VPN and Proxy usage during transactions. Mixed-rail activity across PIX, Card, and Wire channels with cross-border transactions to AE and PT jurisdictions, combined with high-risk MCC merchant activity, presents a risk profile materially inconsistent with the declared low-risk occupation.

**Triggered typologies:** passthrough, anonymization, sanctions-screening, merchant-risk, mixed-rail, chargeback-risk, network-convergence

### Key facts
- Confirmed KYC-level sanctions list match (sanctions_status.confirmed_sanctions_match: true)
- PIX passthrough ratio of 899.2% — R$36,834.19 outflow vs R$4,096.14 inflow
- Total outflow of R$68,070.28 against declared annual income of R$21,304 (approximately 3.2× annual / 38× monthly equivalent)
- 2 anonymization events: 1 VPN (tx T4TCRQ3MZFYUC on 2025-08-03) and 1 Proxy (tx TLDMMIWTI9WSU on 2025-08-03)
- 8 cross-border events including transactions to AE (tx TT1YJJ9T8WM3E, tx T3CTGGX5K9LUR) and PT (tx T4TCRQ3MZFYUC)
- 22 transactions to 22 distinct counterparties across PIX, Card, and Wire rails
- High-risk MCC activity including MCC 6011 (tx TXAZ60SQBYE3A), MCC 6211 (tx T4TCRQ3MZFYUC), and MCC 6051 (tx T3CTGGX5K9LUR)

### Timeline
- `2025-07-04` — PIX to customer C102304 (R$2,975.97) at MCC 6011 — high-risk MCC and potential network convergence (tx TXAZ60SQBYE3A; rules R11, R20)
- `2025-07-18` — High-value PIX to M200256 (R$6,865.46) at MCC 5945 (tx TDEGNII3QCQ6W)
- `2025-07-18` — Cross-border card transaction to AE (R$3,147.06) at MCC 4111 — mixed-rail activity begins (tx TT1YJJ9T8WM3E; rule R17)
- `2025-08-03` — Wire to M200855 (R$4,738.23) via Proxy anonymization (tx TLDMMIWTI9WSU; rule R05_VPN)
- `2025-08-03` — Cross-border card to PT (R$2,121.78) via VPN at MCC 6211 — second anonymization event same day (tx T4TCRQ3MZFYUC; rules R05_VPN, R11)
- `2025-08-26` — PIX to M200736 (R$5,877.53) at MCC 4111 — continued high-risk MCC activity (tx T9DM6GZRCDB2J; rule R11)
- `2025-09-23` — Wire to M200080 (R$7,490.44) — second wire in review period (tx T9OSWZJ1F3HT1; rule R17)
- `2025-09-26` — Cross-border card to AE (R$3,041.49) at MCC 6051 — continued high-risk MCC and cross-border pattern (tx T3CTGGX5K9LUR; rules R11, R17)

---

## C101542
**Recommendation:** file_sar_immediate
**Confidence:** high
ML confidence: **High** (cohort rank #4)

Customer C101542, a self-declared Freelancer with annual income of R$3,687 (approximately R$307/month), presents total outflows of R$103,286.93 during the review period—potentially consistent with income inflation exceeding 336× declared monthly income. The PIX passthrough ratio of 751.2% (R$73,948.90 outflow vs R$9,843.55 inflow) warrants scrutiny as potentially indicative of funds transit activity. Activity includes one Tor-anonymized transaction, one VPN/Proxy event, mixed-rail usage (PIX, Card, Wire), 28 distinct counterparties, and a direct wire transfer to another flagged subject (C100375), collectively presenting a behavioral profile materially inconsistent with a low-risk L1-tier freelancer.

**Triggered typologies:** income-mismatch, passthrough, anonymization, high-risk-merchant, fanout, mixed-rail, chargeback-risk, merchant-convergence, network-linkage

### Key facts
- Total outflow R$103,286.93 vs declared annual income R$3,687 (monthly ~R$307); outflow exceeds 336× monthly income, triggering R03_HIGH (>100× threshold)
- PIX passthrough ratio 751.2%: R$73,948.90 outflow vs R$9,843.55 inflow, triggering R04 (>200% threshold)
- One transaction executed via Tor anonymization network (tx T991C2EOAP061, 2025-07-14, R$5,760.65 to M200971, MCC 7995), triggering R05_TOR
- One transaction via Proxy service (tx TUI6B5CHKXRA8, 2025-09-24, R$779.48 to M200196, geo US)
- 28 distinct counterparties across 28 transactions, triggering R15 (≥25 threshold)
- Mixed-rail activity: PIX + Card + Wire within review window (3 wire transfers logged), triggering R17
- ≥3 transactions to high-risk MCC merchants including MCC 7995 (gambling), MCC 4829 (wire transfer), MCC 4900 (utilities—potential bill-pay structuring), triggering R11
- Direct wire transfer to flagged subject C100375 on 2025-07-27, R$1,423.60, triggering R21
- Chargeback history or repeat use of high-chargeback merchants indicated by R19 trigger
- Shared receiving merchant with another flagged subject indicated by R20 trigger
- 7 cross-border transaction events including jurisdictions AE, US, and LY (Libya—high-risk)

### Timeline
- `2025-07-09` — Cross-border PIX R$3,103.97 to M200841, geo AE (UAE) (tx TRK1KEG424MBN)
- `2025-07-14` — Tor-anonymized PIX R$5,760.65 to gambling merchant M200971 (MCC 7995) (tx T991C2EOAP061; triggers R05_TOR, R11)
- `2025-07-20` — Cross-border Card transaction R$6,530.17 to M200260, geo US (tx TTFTKZBP4CFMG)
- `2025-07-27` — Wire transfer R$1,423.60 to flagged subject C100375 (tx T8XYRVKV8AGM2; triggers R21)
- `2025-08-04` — High-value PIX R$25,848.82 to M200966 (MCC 4900) (tx TSWFX3XIHOF2R; triggers R11)
- `2025-08-17` — PIX R$11,121.30 to M200616 (MCC 4829 — wire transfer services) (tx TCIOVP5V3QUJF; triggers R11)
- `2025-09-24` — Proxy-anonymized PIX R$779.48 to M200196, geo US (tx TUI6B5CHKXRA8)
- `2025-10-04` — Wire transfer R$6,257.41 to M200776, high-risk jurisdiction (Libya) (tx TESLWHQ8LG92B)

---
