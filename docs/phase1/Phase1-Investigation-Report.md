# AML/FT INVESTIGATION — PHASE 1 REPORT (EXECUTIVE)
**Dataset:** CloudWalk INC — 52,000 transactions · 2,500 customers · Jul–Oct 2025
**Phase:** 1 — Suspicious Entity Investigation
**Investigator:** Senior AML/FT

---

## 1. SUSPECT COHORT

Nine entities flagged by composite risk profile (structuring · velocity · income-to-volume · passthrough · network · geo/IP):

> The final investigative cohort below reflects the refined production-oriented scoring and orchestration framework developed during later phases of the project. Ranking now accounts for hard-alert rule bonuses (R08 sanctions, R05_TOR anonymization, R21 network-link), typology family diversity, and dangerous-combination multipliers in addition to raw transaction volume.

| Rank | ID | Occupation | Income | Outflow | Ratio | Key Indicators |
|---|---|---|---|---|---|---|
| 🔴 1 | **C102290** | Driver | R$11k | R$134k | 144× | PEP, KYC=98, VPN×2+Tor, 2,013% passthrough, burst · 7 typology families · priority 66.0 |
| 🔴 2 | **C100880** | Entrepreneur | R$9k | R$106k | 141× | Tor, 3 structuring, chargeback on structuring tx, R21 network-link (C101647→) · priority 41.6 |
| 🔴 3 | **C101848** | Accountant | R$10k | R$97k | 117× | Wire → C102360 (only inter-subject Wire), AF geo, same-day burst, KYC=30 · priority 37.9 |
| 🔴 4 | **C102360** | Consultant | R$3k | R$74k | 299× | 3 structuring, Wire-linked to C101848, 276% passthrough, R21 · priority 37.6 |
| 🟠 5 | C101854 | Trader | R$12k | R$103k | 105× | 4 structuring (cohort high), VPN · priority 29.8 |
| 🟠 6 | C101534 | Entrepreneur | R$8k | R$99k | 142× | AF+UAE geo, Proxy, 3 structuring, shared merchant · priority 27.9 |
| 🟠 7 | C101328 | Entrepreneur | R$23k | R$153k | 78× | Highest absolute volume, Belarus+AF geo, 4-tx burst · priority 23.8 |
| 🟠 8 | C100740 | Nurse | R$14k | R$80k | 69× | 834% passthrough, Proxy, R$26k single PIX · priority 23.6 |
| 🟡 9 | C101162 | Teacher | R$11k | R$96k | 103× | Two velocity bursts, Proxy+VPN · priority 20.8 |

---

## 2. PRIMARY ENTITIES — EVIDENCE

### C102290 — Driver (PEP, KYC=98) · Highest Priority
- PEP + KYC=98; declared occupation atypical for PEP profile — clarify under EDD
- R$134k outflow / 144× monthly income; Tor + 2× VPN; 2,013% passthrough (R$5k in / R$108k out)
- Aug 1 burst: 4 PIX txs / R$42.6k incl. R$20.5k + R$11.7k high-value pair

### C102360 — Consultant (R$2,971/yr) · Income-Volume Disparity
- Lowest declared income in cohort; R$74k outflow = 299× monthly income
- 3 structuring-band hits; 276% passthrough
- Wire-linked to C101848 (tx TAAUIOJCM76S3, R$2,857, 23-Sep) — only confirmed inter-subject Wire

### C101328 — Entrepreneur · Highest Absolute Volume
- R$153k outflow — top of cohort
- Geo-tagged to Belarus (FATF grey) + Afghanistan (FATF high-risk)
- 4-tx burst on 21-Aug (R$37k); shared merchant M200964 with C101848, C101534

### C101848 — Accountant · Network Hub
- **Only confirmed direct Wire to another flagged subject (→ C102360, 23-Sep)**
- 4-tx burst R$39k on **same day** as the Wire
- AF geo-tag; shared merchant M200964 with C101328 + C101534; KYC=30 (monitoring gap)

### C100880 — Entrepreneur · Tor + Structuring + Chargeback
- 3 structuring-band hits; Tor usage; **chargeback on a structuring-band tx**
- Shared merchants M200460, M200186 with C102290
- 141× monthly income

---

## 3. STRUCTURING

**Screening threshold:** R$9,000–R$9,999 band (investigative criterion, not a finding by itself).

| Entity | Hits | Context |
|---|---|---|
| C101854 | 4 | VPN |
| C102360 | 3 | Wire to C101848 |
| C101534 | 3 | AF geo, Proxy |
| C100880 | 3 | Tor; chargeback on band tx |

Cohort-wide: 988 band-transactions across the dataset; 151 customers with ≥2 hits. Recurrence across low-income subjects with concurrent anonymization/geo signals raises suspicion of threshold-conscious behavior.

---

## 4. VELOCITY

| Entity | Day | Txs | Outflow | Context |
|---|---|---|---|---|
| C102290 | 1-Aug | 4 | R$42.6k | R$20.5k + R$11.7k pair |
| C101328 | 21-Aug | 4 | R$37.2k | Belarus + AF geo |
| C101848 | 23-Sep | 4 | R$39.3k | **Same-day Wire to C102360** |
| C100740 | 13-Aug | 3 | R$38.3k | R$26k single PIX; Proxy |
| C101162 | 26-Sep / 4-Oct | 3 / 3 | R$24.7k / R$16.1k | Proxy+VPN |

4 txs/day is the cohort maximum — a low-frequency dataset overall, making these bursts notable. C101848's same-day burst + Wire to C102360 is the strongest coordination signal in the cohort.

---

## 5. CASH-IN / CASH-OUT (PASSTHROUGH)

| Entity | Cash-IN | Cash-OUT | Ratio |
|---|---|---|---|
| C102290 | R$5.4k | R$108k | **2,013%** |
| C100740 | R$6.1k | R$51k | 834% |
| C101534 | R$7.1k | R$47k | 660% |
| C101328 | R$13.7k | R$74k | 537% |
| C101848 | R$9.3k | R$42k | 451% |
| C101854 | R$16.3k | R$52k | 317% |
| C102360 | R$15.4k | R$42k | 276% |

Outflows materially exceed observed platform inflows across all primary subjects, indicating funds whose origin is not visible within the monitored platform. Source-of-funds documentation required under EDD.

Secondary screening identified **100 entities** showing receive-few/distribute-many behavior (≤3 senders → ≥8 receivers, ≥R$20k inflow) — intermediary/mule-pattern population for follow-up.

---

## 6. NETWORK OBSERVATIONS

| Linkage | Detail |
|---|---|
| **C101848 → C102360** | Wire TAAUIOJCM76S3, R$2,857, 23-Sep — only confirmed inter-subject Wire |
| **M200964** | Shared receiver: C101534, C101328, C101848 |
| **M200460 / M200186** | Shared receivers: C100880 + C102290 |
| **M200894** | Shared receiver: C102360 + C100740 |
| **Upstream Wires** | C100543 → C100740; C101647 → C100880; C100331 → C101534 |
| **Device / IP** | No shared identifiers across the nine subjects |

The confirmed Wire and four shared-merchant convergence points support a network-level review of the cohort, beyond individual-entity SARs.

---

## 7. TYPOLOGIES INDICATED

| # | Typology | Entities |
|---|---|---|
| T1 | **Structuring / threshold-conscious behavior** (R$9k–R$10k band recurrence) | C101854, C102360, C101534, C100880 |
| T2 | **Intermediary / mule pattern** (receive-few / distribute-many) | 100-entity secondary population; C101278, C101505 notable |
| T3 | **Multi-rail layering** (PIX + Card + Wire combinations) | All 9 primary subjects |
| T4 | **Off-platform funding** (passthrough 276%–2,013%) | All 7 entities in §5 |
| T5 | **Anonymization tools** (Proxy / VPN / Tor) | C102290, C100880, C101162, C100740, C101534 |
| T6 | **High-risk jurisdiction exposure** (AF, BY) | C101534, C101328, C101848 |
| T7 | **PEP with inconsistent profile** | C102290 (mandatory EDD under FATF Rec. 12) |
| T8 | **Potential multi-account coordination** (Wire + shared merchants) | C101848 ↔ C102360 ↔ C101328 ↔ C101534 |

---

## 8. ESCALATION SHORTLIST

### TIER 1 — SAR FILING RECOMMENDED IMMEDIATELY

| ID | Basis |
|---|---|
| **C102290** | PEP + KYC=98; activity materially inconsistent with profile (Tor+VPN, R$134k, 2,013% passthrough, burst). Mandatory EDD applies. Highest investigative priority in cohort. |
| **C100880** | Tor anonymization + R21 hard alert (Wire received from flagged C101647) + 3 structuring hits + chargeback on structuring tx; shared merchants with C102290. |
| **C101848** | Only confirmed inter-subject Wire (→ C102360); AF geo; same-day burst; KYC=30 monitoring gap; shared-merchant convergence node; R21 hard alert. |
| **C102360** | 299× income disparity; 3 structuring hits; Wire counterparty to C101848; R21 hard alert. |

### TIER 2 — SAR RECOMMENDED (STANDARD WINDOW)

| ID | Basis |
|---|---|
| C101854 | 4 structuring hits (cohort high); VPN. |
| C101534 | AF+UAE geo; 3 structuring hits; Proxy; shared merchant M200964. |
| C101328 | R$153k highest outflow; Belarus+AF geo; velocity burst. |

### TIER 3 — ENHANCED MONITORING

| ID | Basis |
|---|---|
| C100740 | 834% passthrough; Proxy; upstream Wire from C100543. |
| C101162 | Two velocity-burst dates; Proxy+VPN. |

### SECONDARY REVIEW

- **Upstream funding sources:** C100543, C101647, C100331 — pull profiles
- **Shared merchants:** M200964 (3-subject convergence), M200460, M200186 — initiate merchant risk review

---

**End of Phase 1.** Primary SAR drafted on C102290; network SAR drafted on C101848. Tier 2 and Tier 3 cases retained in case file for follow-on action.
