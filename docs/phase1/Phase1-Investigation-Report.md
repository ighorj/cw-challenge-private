# AML/FT INVESTIGATION — PHASE 1 REPORT (EXECUTIVE)
**Dataset:** CloudWalk INC — 52,000 transactions · 2,500 customers · Jul–Oct 2025
**Phase:** 1 — Risk-Ranked Suspicious Entity Investigation
**Methodology:** Production priority scoring framework (rules + ML v2 + hard-alert bonuses)

---

## 1. SUSPECT COHORT

Ten entities flagged by composite risk profile — ranked by **operational escalation priority** combining rules-based detection, ML confidence (v2: XGBoost regression on behavioral risk score, isotonic calibration), hard-alert triggers (R08 sanctions, R05_TOR anonymization, R21 network-link), and typology family diversity:

| Rank | ID | Occupation | Income | Outflow | Ratio | Key Indicators | Priority |
|---|---|---|---|---|---|---|---|
| #1 | **C100091** | Store Owner | R$10k | R$91k | 108× | 898% passthrough, R08 sanctions screening, R21 wire-link (→C100236), KYC=66 | 73.19 |
| #2 | **C101208** | Chef | R$13k | R$150k | 138× | 822% passthrough, R08 sanctions screening, VPN, 29 counterparties (R15), 6 geo-risk events | 70.12 |
| #3 | **C100837** | Accountant | R$8k | R$139k | 220× | PEP + 4,367% passthrough (extreme), Tor anonymization, R09 EDD, 30 counterparties, Myanmar geo | 67.40 |
| #4 | **C102290** | Driver | R$11k | R$134k | 144× | **PRIMARY SAR CASE** — PEP, KYC=98, Tor + VPN×2, 2,013% passthrough, velocity burst (4 txs, R$42.6k), 7 typologies | 66.00 |
| #5 | **C101028** | Designer | R$47k | R$71k | 18× | PEP + confirmed sanctions match (R08), KYC=64, R10 KYC-inconsistency, multi-rail | 65.72 |
| #6 | **C102093** | Chef | R$8k | R$192k | 297× | PEP, 1,130% passthrough, Tor, 30 counterparties (highest fan-out), Myanmar + Yemen geo, KYC=63 | 62.60 |
| #7 | **C101582** | Nurse | R$11k | R$89k | 98× | 1,467% passthrough, R08 sanctions screening (Iraq cross-border), Tor ×2, KYC=73 | 59.69 |
| #8 | **C101542** | Freelancer | R$4k | R$103k | 336× | 303% passthrough, Tor ×2, R21 wire-link (→C100375), 28 counterparties, 7 typologies | 57.42 |
| #9 | **C100208** | Dentist | R$9k | R$144k | 198× | 3,675% passthrough, Tor, R21 wire-link (→C102252), KYC=89, Myanmar cross-border (R$51k) | 56.95 |
| #10 | **C101445** | Designer | R$21k | R$68k | 38× | R08 confirmed sanctions match (hard alert), 328% passthrough, VPN + Proxy, merchant convergence | 52.94 |

---

## 2. PRIMARY ENTITIES — EVIDENCE

### C100091 — Store Owner (R$10,173/yr) · Highest Priority
- R$91,350 outflow / 108× monthly income; 2,917% PIX passthrough (R$57.1k out / R$1.9k in)
- **R08 SANCTIONS SCREENING EVENT:** Wire TJRKHTP81JROK dated 2025-08-07, R$11,672.88 to M200363 in Iran (IR)
- R21 NETWORK LINK: Direct wire to C100236 (tx TMGHPD5XFHXCJ, R$1,255.77, 18-Jul — single transaction on that date)
- 10 triggered rules across 7 typology families; KYC risk=66, tier L2

### C100837 — Accountant (R$7,577/yr) · PEP + Extreme Passthrough
- PEP status — hard-alert trigger (R09 EDD)
- R$139,084 outflow / 220× monthly income; **4,367% passthrough** (extreme — R$104.9k out / R$2.4k in)
- Cross-border Card to Syria (SY) on 2025-09-12, R$3,457.10 (TVEJBJ314AYK1 — high-risk jurisdiction, R06 trigger)
- Cross-border Card to Myanmar (MM) on 2025-07-22, R$1,361.82 (TT94KQ67Q0Q92 — high-risk jurisdiction, R06 trigger)
- Tor anonymization event; 12 triggered rules; KYC risk=59, tier L2

### C101208 — Chef (R$13,047/yr) · Highest Transaction Volume
- R$150,178 outflow / 138× monthly income; 822% passthrough; R08 sanctions screening (Syria wire, 2025-08-12, R$2,166.18)
- 29 distinct counterparties (R15 fan-out); mixed-rail (PIX R$77.6k + Wire + Card); 6 cross-border events
- VPN anonymization; KYC risk=51, tier L1; 9 triggered rules across 6 typology families

### C102290 — Driver (R$11,177/yr) · PRIMARY SAR SHOWCASE
- **PEP + KYC=98** (highest risk score in cohort); 144× monthly income mismatch (R$134.3k outflow)
- Tor + 2× VPN anonymization; 2,013% passthrough (R$108.0k out / R$5.4k strict cash-in per R04)
- **Single-day velocity burst:** 2025-08-01, 4 txs totaling R$42.6k (R$20.5k + R$11.7k high-value pair)
- 11 triggered rules; 7 typology families; strongest investigative convergence in cohort

### C102093 — Chef (R$7,766/yr) · Highest Outflow Volume + Fan-Out
- R$192,075 total outflow / 297× monthly income; **1,130% passthrough**
- **30 distinct counterparties** (R15 maximum fan-out); PEP status; Tor anonymization
- Cross-border to Myanmar (R$3,088, 2025-07-17) and Yemen; 11 triggered rules

---

## 3. SANCTIONS SCREENING EVENTS

| Customer | Event | Date | Amount | Counterparty | Jurisdiction | Context |
|---|---|---|---|---|---|---|
| **C100091** | Wire to M200363 | 2025-08-07 | R$11,673 | M200363 | Iran (IR) | R08 trigger; only confirmed inter-subject Wire in cohort |
| **C101208** | Wire to M200815 | 2025-08-12 | R$2,166 | M200815 | Syria (SY) | R08 trigger; MCC 5999; high-risk jurisdiction |
| **C101028** | KYC-level match | — | — | — | Confirmed | R08/R09 hard alert; mandatory EDD |
| **C101582** | Wire to Iraq | 2025-08-21 | R$3,295 | M200390 | Iraq (IQ) | R08 trigger; MCC 6051 quasi-cash |
| **C101445** | KYC-level match | — | — | — | Confirmed | R08 hard alert; sanctions-driven priority |

---

## 4. EXTREME PASSTHROUGH PATTERNS

| Customer | PIX In | PIX Out | Ratio | Pattern Indicators |
|---|---|---|---|---|
| **C100837** | R$2,403 | R$104,966 | **4,367%** | Extreme passthrough; likely conduit account; 12 rules |
| **C100208** | R$1,513 | R$55,600 | **3,675%** | Extreme conduit behavior; Tor; network link |
| **C100091** | R$1,958 | R$57,117 | **2,917%** | Sanctions screening + network link + passthrough convergence |
| **C101582** | R$3,174 | R$46,574 | **1,467%** | Tor ×2, sanctions screening, quasi-cash merchants |
| **C102093** | R$10,046 | R$113,519 | **1,130%** | PEP, highest outflow, fan-out to 30 counterparties |
| **C102290** | R$5,367¹ | R$108,041 | **2,013%** | PEP, Tor+VPN, velocity burst, primary showcase |
| **C101208** | R$9,448 | R$77,635 | **822%** | Sanctions screening, high counterparty count |
| **C101445** | R$11,223 | R$36,834 | **328%** | Confirmed sanctions match; designer profile inconsistent |
| **C101542** | R$24,379 | R$73,949 | **303%** | Tor ×2, network link, 336× monthly income |
| **C101028** | R$23,591 | R$46,554 | **197%** | Only cohort member below 300%; PEP + confirmed sanctions match override |

¹ C102290 PIX In uses R04 strict cash-in denominator (R$5,367); all PIX received including other inflows totals R$10,299. Ratio of 2,013% reflects R04 rule definition.

Observation: All 10 cohort members show material passthrough patterns (197%–4,367%), indicating funds whose source is not visible within the monitored platform. Layering/flow-through hypothesis applies across entire cohort.

---

## 5. NETWORK OBSERVATIONS

| Linkage | Customer(s) | Detail | Context |
|---|---|---|---|
| **C100091 → C100236** | C100091, C100236 | Wire TMGHPD5XFHXCJ, R$1,255.77, 18-Jul | R21 hard alert; only confirmed inter-top10 Wire from this cohort |
| **C100208 → C102252** | C100208, C102252 | Wire TSM9Q0FWI3AUT, R$1,665.40, 14-Jul | R21 hard alert; C100208 directional link |
| **C101542 → C100375** | C101542, C100375 | Wire T8XYRVKV8AGM2, R$1,423.60, 27-Jul | R21 hard alert; low-value network signal |
| **Shared merchants (multi-counterparty)** | C101028, C101208, C102093 | 28–30 distinct receiver addresses | Merchant convergence; fan-out pattern (R15) |
| **Upstream funding** | C100091, C101582, C100208 | Multiple incoming wires from non-top10 flagged customers | Secondary network penetration |

Three confirmed inter-customer wires form the core network topology. Broad fan-out (25–30 counterparties per subject) suggests layering or rapid distribution rather than traditional network coordination.

---

## 6. TYPOLOGIES INDICATED

| # | Typology Family | Entities | Rules Fired | Characteristic |
|---|---|---|---|---|
| T1 | **Sanctions / PEP** | C101028, C100837, C101445, others | R08, R09, R10 | KYC-level or transactional sanctions hits; PEP status; mandatory EDD |
| T2 | **Income Mismatch** | All 10 | R03_HIGH, R03_LOW | 18×–336× monthly income disparity; declared occupation inconsistent with volumes |
| T3 | **Passthrough / Layering** | All 10 | R04 | 197%–4,367% passthrough; off-platform funding origin |
| T4 | **Anonymization** | C102290, C100837, C102093, C100208, C101542, C101582 | R05_TOR, R05_VPN | Tor ×1–2 per subject; VPN/Proxy use; intent to obscure origin |
| T5 | **Fan-Out / Structuring** | C102093, C101208, C101542 | R15 | 25–30 distinct receiving counterparties; dispersion pattern |
| T6 | **Multi-Rail** | All 10 | R17 | PIX + Card + Wire combinations; channel diversification |
| T7 | **High-Risk Merchant** | All 10 | R11 | MCC 6011 (financial), 7995 (gambling), 6051 (quasi-cash), 4829 (wire services) |
| T8 | **Network Linkage** | C100091, C100208, C101542 | R21 | Direct Wire to other flagged subjects (hard alert) |
| T9 | **Cross-Border / Geo-Risk** | C100837, C101208, C102093, C100208, C101582 | R06, R07 | High-risk jurisdictions (Iran, Syria, Iraq, Myanmar, Yemen) |
| T10 | **KYC Inconsistency** | C101028, C100837, C102290 | R09, R10 | PEP status + low risk ratings; occupation inconsistency |
| T11 | **Device / IP Anomaly** | C102290, others | R14 | Rooted device detected; IP anomalies |

---

## 7. ESCALATION SHORTLIST

### TIER 1 — SAR FILING RECOMMENDED IMMEDIATELY

**Hard-Alert Category (Sanctions / PEP / Network-Link):**

| ID | Priority | Basis |
|---|---|---|
| **C100091** | 73.19 | R08 sanctions screening (Iran Wire) + R21 network-link (→C100236) + 2,917% passthrough + income mismatch. Immediate filing. |
| **C101208** | 70.12 | R08 sanctions screening (Syria Wire, R$2.1k) + 822% passthrough + 29 counterparties (R15) + cross-border multi-event. |
| **C100837** | 67.40 | **PEP** (R09 EDD hard alert) + **4,367% extreme passthrough** + Tor + Syria/Myanmar geo-risk (R06). PRIORITY escalation. |
| **C102290** | 66.00 | **PRIMARY SAR SHOWCASE.** PEP + KYC=98 + Tor+VPN + 2,013% passthrough + velocity burst (4 txs, R$42.6k) + 7 typology families. Strongest investigative case. Mandatory EDD. |
| **C101028** | 65.72 | **CONFIRMED KYC-level SANCTIONS MATCH** + PEP status + R10 KYC-inconsistency + card not-present (R18). Mandatory EDD + immediate escalation. |
| **C102093** | 62.60 | PEP + 1,130% passthrough + **highest fan-out (30 counterparties)** + Tor + Myanmar/Yemen geo + 11 rules. Rapid distribution pattern. |
| **C101582** | 59.69 | R08 sanctions screening (Iraq) + 1,467% passthrough + Tor ×2 + quasi-cash MCC. Sanctions-driven priority. |
| **C101542** | 57.42 | 303% passthrough + Tor ×2 + R21 network-link (→C100375) + 336× monthly income (extreme) + 7 typologies. |
| **C100208** | 56.95 | 3,675% passthrough + Tor + R21 network-link (→C102252) + Myanmar cross-border (R$51k) + KYC risk=89. |
| **C101445** | 52.94 | **CONFIRMED SANCTIONS MATCH** (hard alert) + 328% passthrough + VPN + Proxy + merchant convergence. Behavioral ML score=0 (no soft rule fires); hard alert preserves mandatory escalation. |

**All 10 entities warrant immediate SAR filing** under Circular BACEN 3.978/2020 and COAF Normative Instruction 1/2014. No Tier 2 / Tier 3 deferral applies to this cohort.

### SECONDARY REVIEW

- **Upstream funding sources:** Conduct network penetration on incoming wires to all 10 subjects
- **Merchant risk review:** Cross-reference high-MCC merchants (6011, 6051, 7995, 4829) for convergence across top-10
- **KYC refresh:** All 10 require Enhanced Due Diligence; prioritize C101028, C101445 (confirmed sanctions matches) and C100837 (PEP + extreme passthrough)
- **Sanctions verification:** Cross-check transactional screening events (C100091, C101208, C101582) against OFAC, BACEN, EU consolidated lists

---

**End of Phase 1.** All 10 entities recommended for immediate SAR filing. Primary showcase SAR drafted on C102290 (investigative richness despite rank #6 operationally). Network SAR drafted on C100091 (sanctions screening + network hub). Tier 1 cases retained in case file for concurrent compliance officer review.
