# Investigation Summary — run 20260526-041414-4aa919
_Backend: template · Generated: 2026-05-26T04:14:37+00:00_
_ML confidence labels are calibrated relative to the investigated escalation cohort, not the full customer population._

## C100091
**Recommendation:** file_sar_immediate
**Confidence:** high — 10 concurrent rule fires; all facts traceable to transaction records
ML confidence: **Moderate-High** (cohort rank #8)

Customer with KYC risk score 66/100. declared income R$10,173/yr versus R$91,350 in 18 outflows (≈108× declared monthly income). PIX passthrough ratio 4008%. Activity appears materially inconsistent with the declared customer profile.

**Triggered typologies:** chargeback-merchant, high-MCC, high-risk-geo, income-mismatch, merchant-convergence, multi-rail, network-linkage, passthrough, sanctions, structuring

### Key facts
- R$91,350 total outflow vs R$848/month declared income (108×)
- PIX passthrough 4008% (R$57,117 out / R$1,425 in)

### Timeline
- `2025-07-09` — PIX R$7,680 → C100179 (MCC 7995) (tx T1RBG8O7Y6NC6)
- `2025-07-15` — PIX R$9,732 → M200985 (tx TLF007IGRTEAB)
- `2025-07-18` — Wire R$1,256 → C100236 (tx TMGHPD5XFHXCJ)
- `2025-08-07` — Wire R$11,673 → M200363 (geo: IR; sanctions screening event) (tx TJRKHTP81JROK)
- `2025-08-20` — PIX R$18,508 → M200796 (tx TRD52BHJTAJLQ)
- `2025-08-22` — PIX R$541 → M200527 (geo: DE; MCC 7995) (tx TQWXFJ3VKTJO0)
- `2025-10-03` — Card R$11,591 → M200233 (MCC 6011) (tx TJZQI83ROKQ81)
- `2025-10-04` — PIX R$4,988 → M200800 (geo: ES) (tx TGWER3C1MRCSR)

---

## C101208
**Recommendation:** file_sar_immediate
**Confidence:** high — 9 concurrent rule fires; all facts traceable to transaction records
ML confidence: **High** (cohort rank #5)

Customer with KYC risk score 51/100. declared income R$13,047/yr versus R$150,178 in 29 outflows (≈138× declared monthly income). anonymization events (2 VPN). Activity appears materially inconsistent with the declared customer profile.

**Triggered typologies:** anonymization, card-no-3DS, chargeback-merchant, fan-out, high-MCC, income-mismatch, merchant-convergence, multi-rail, sanctions

### Key facts
- R$150,178 total outflow vs R$1,087/month declared income (138×)
- Anonymization breakdown: {'VPN': 2}

### Timeline
- `2025-07-22` — PIX R$1,241 → M200526 (via VPN; geo: PT) (tx TJZRYWR88WZHJ)
- `2025-08-12` — Wire R$2,166 → M200815 (geo: SY; sanctions screening event) (tx TNHZDN7D6LYK6)
- `2025-08-18` — Wire R$2,234 → M200524 (geo: GB) (tx TTY9XRY0X3DFN)
- `2025-08-29` — Card R$1,089 → M200972 (via VPN; geo: RU) (tx TQSBX6QW4LBWX)
- `2025-09-08` — Card R$6,889 → M200212 (geo: YE; MCC 7995) (tx TOHDJ4A6OYGZA)
- `2025-09-17` — Wire R$17,044 → M200962 (geo: PT) (tx T01OIP42LWSQO)
- `2025-09-23` — Card R$14,012 → M200637 (MCC 7995) (tx TIQS2U9KT1J0U)
- `2025-09-23` — PIX R$7,719 → M200331 (geo: RU; MCC 6011) (tx TF9EJQVFQTQJM)

---

## C100837
**Recommendation:** file_sar_immediate
**Confidence:** high — 12 concurrent rule fires; all facts traceable to transaction records
ML confidence: **Extreme** (cohort rank #1)

PEP-flagged customer (KYC risk score 59/100). declared income R$7,577/yr versus R$139,084 in 29 outflows (≈220× declared monthly income). PIX passthrough ratio 4367%. anonymization events (1 Tor). Activity appears materially inconsistent with the declared customer profile.

**Triggered typologies:** KYC-inconsistency, PEP-EDD, anonymization, chargeback-merchant, fan-out, high-MCC, high-risk-geo, income-mismatch, merchant-convergence, multi-rail, passthrough, rooted-device

### Key facts
- R$139,084 total outflow vs R$631/month declared income (220×)
- PIX passthrough 4367% (R$104,966 out / R$2,403 in)
- Anonymization breakdown: {'Tor': 1}
- KYC inconsistency: PEP=Yes, score=59, risk_rating=Medium, tier=L2

### Timeline
- `2025-07-08` — Wire R$1,703 → M200513 (geo: US) (tx TPCPL90MU9SRF)
- `2025-07-22` — Card R$1,362 → M200684 (geo: MM; MCC 4900) (tx TT94KQ67Q0Q92)
- `2025-08-01` — Wire R$12,957 → M200053 (geo: GB; MCC 4829) (tx T4MHTBYMYYY0C)
- `2025-08-04` — PIX R$2,783 → M200806 (via Tor) (tx T4VUTEFNQBUQH)
- `2025-08-07` — Wire R$1,746 → M200849 (geo: DE; MCC 4111) (tx TDU1GAYIB8X9S)
- `2025-08-16` — PIX R$8,639 → M200237 (geo: GB; MCC 4900) (tx TJ7QJ1RGK5KXZ)
- `2025-08-18` — Card R$1,142 → M200004 (MCC 6051; rooted device) (tx TPTMR0FBGXQOB)
- `2025-08-20` — PIX R$27,305 → M200309 (MCC 4829) (tx TTP6ORO2Q3V22)

---

## C102290
**Recommendation:** file_sar_immediate
**Confidence:** high — 11 concurrent rule fires; all facts traceable to transaction records
ML confidence: **Very High** (cohort rank #2)

PEP-flagged customer (KYC risk score 98/100). declared income R$11,177/yr versus R$134,319 in 27 outflows (≈144× declared monthly income). PIX passthrough ratio 2013%. anonymization events (2 VPN, 1 Tor). Activity appears materially inconsistent with the declared customer profile.

**Triggered typologies:** KYC-inconsistency, PEP-EDD, anonymization, chargeback-merchant, fan-out, high-MCC, income-mismatch, merchant-convergence, multi-rail, passthrough, velocity-burst

### Key facts
- R$134,319 total outflow vs R$931/month declared income (144×)
- PIX passthrough 2013% (R$108,041 out / R$5,367 in)
- Anonymization breakdown: {'VPN': 2, 'Tor': 1}
- Single-day burst 2025-08-01: 4 txs / R$42,590
- KYC inconsistency: PEP=Yes, score=98, risk_rating=Medium, tier=L1

### Timeline
- `2025-07-10` — Card R$3,196 → M200283 (geo: AE; MCC 6051) (tx TLRPWM2IMAYPY)
- `2025-07-29` — Card R$3,296 → M200004 (MCC 6051; rooted device) (tx T4FZR2CAYR4SR)
- `2025-08-01` — PIX R$20,509 → M200888 (velocity burst) (tx TJQAMN5JTWDXB)
- `2025-08-01` — PIX R$11,742 → M200489 (velocity burst; MCC 6211; rooted device) (tx TVK4KFT22QPUH)
- `2025-08-01` — PIX R$8,225 → M200845 (velocity burst; MCC 4111) (tx TS1NXL736G19W)
- `2025-08-12` — Wire R$1,364 → M200662 (via VPN) (tx TB24ZK5RW3PP8)
- `2025-09-28` — PIX R$8,506 → M200393 (via VPN; MCC 4900) (tx TZ76800M19NE3)
- `2025-10-03` — Card R$3,835 → M200122 (via Tor; MCC 6011) (tx TNUU7IUG3D1A2)

---

## C101028
**Recommendation:** file_sar_immediate
**Confidence:** high — 9 concurrent rule fires; all facts traceable to transaction records
ML confidence: **Moderate** (cohort rank #10)

PEP-flagged customer (KYC risk score 64/100). declared income R$47,312/yr versus R$71,406 in 18 outflows (≈18× declared monthly income). PIX passthrough ratio 587%. anonymization events (1 Proxy, 1 VPN). Activity appears materially inconsistent with the declared customer profile.

**Triggered typologies:** KYC-inconsistency, PEP-EDD, anonymization, card-no-3DS, chargeback-merchant, high-MCC, merchant-convergence, passthrough, sanctions

### Key facts
- R$71,406 total outflow vs R$3,943/month declared income (18×)
- PIX passthrough 587% (R$46,554 out / R$7,927 in)
- Anonymization breakdown: {'Proxy': 1, 'VPN': 1}
- KYC inconsistency: PEP=Yes, score=64, risk_rating=Low, tier=L3

### Timeline
- `2025-07-01` — Card R$4,390 → M200105 (geo: KP) (tx TFNO8A1FBZUMA)
- `2025-07-01` — PIX R$10,558 → M200161 (tx T4ZAVV478VX1Q)
- `2025-07-03` — PIX R$3,376 → M200538 (via Proxy; MCC 6011) (tx TCTY4DMIEFHUU)
- `2025-07-05` — Card R$1,381 → M200818 (MCC 6211) (tx THYRFBT3SQ4RJ)
- `2025-07-08` — Card R$6,975 → M200118 (via VPN; MCC 6011) (tx TQXICCVPO421G)
- `2025-07-17` — Card R$3,969 → C100265 (rooted device) (tx T4DASTQ56M2QJ)
- `2025-08-11` — Card R$4,318 → M200980 (MCC 4111) (tx TKFJIS94Y7C0I)
- `2025-09-12` — Card R$1,135 → M200386 (geo: DE; MCC 4829) (tx THCF7RXE8PSWC)

---

## C102093
**Recommendation:** file_sar_immediate
**Confidence:** high — 11 concurrent rule fires; all facts traceable to transaction records
ML confidence: **High** (cohort rank #4)

PEP-flagged customer (KYC risk score 63/100). declared income R$7,766/yr versus R$192,075 in 30 outflows (≈297× declared monthly income). PIX passthrough ratio 2944%. anonymization events (2 VPN, 1 Tor, 1 Proxy). Activity appears materially inconsistent with the declared customer profile.

**Triggered typologies:** KYC-inconsistency, PEP-EDD, anonymization, chargeback-merchant, fan-out, geo-ip-mismatch, high-MCC, income-mismatch, merchant-convergence, multi-rail, passthrough

### Key facts
- R$192,075 total outflow vs R$647/month declared income (297×)
- PIX passthrough 2944% (R$113,519 out / R$3,856 in)
- Anonymization breakdown: {'VPN': 2, 'Tor': 1, 'Proxy': 1}
- KYC inconsistency: PEP=Yes, score=63, risk_rating=Low, tier=L2

### Timeline
- `2025-07-08` — Card R$15,825 → M200243 (via Tor; MCC 6051) (tx T14MV5I9E7I9F)
- `2025-07-17` — Card R$3,088 → M200684 (geo: MM; MCC 4900) (tx TOOKNC1OPBY00)
- `2025-07-18` — PIX R$28,584 → M200989 (MCC 4900) (tx T16QYYM1VN5DG)
- `2025-08-03` — PIX R$12,386 → M200067 (geo: US) (tx TGKT5KP09AYYH)
- `2025-08-14` — Card R$8,709 → M200446 (rooted device) (tx T1Y075FPNVJEF)
- `2025-09-09` — PIX R$4,579 → M200879 (via VPN; MCC 4900) (tx TOE917V7W7073)
- `2025-09-10` — Wire R$1,268 → M200402 (tx TX718NJNNFBJJ)
- `2025-10-04` — PIX R$7,372 → M200450 (via Proxy; MCC 4900) (tx TW909K20R5G5S)

---

## C102040
**Recommendation:** file_sar_immediate
**Confidence:** high — 11 concurrent rule fires; all facts traceable to transaction records
ML confidence: **High** (cohort rank #3)

PEP-flagged customer (KYC risk score 60/100). declared income R$7,288/yr versus R$61,862 in 17 outflows (≈102× declared monthly income). PIX passthrough ratio 5044%. anonymization events (1 Tor, 1 Proxy). Activity appears materially inconsistent with the declared customer profile.

**Triggered typologies:** KYC-inconsistency, PEP-EDD, anonymization, chargeback-merchant, high-MCC, income-mismatch, merchant-convergence, multi-rail, passthrough, rooted-device, structuring

### Key facts
- R$61,862 total outflow vs R$607/month declared income (102×)
- PIX passthrough 5044% (R$43,385 out / R$860 in)
- Anonymization breakdown: {'Tor': 1, 'Proxy': 1}
- KYC inconsistency: PEP=Yes, score=60, risk_rating=Low, tier=L3

### Timeline
- `2025-07-05` — Card R$3,343 → M200567 (MCC 7995; rooted device) (tx TH7HAGZQMLJR6)
- `2025-07-06` — Wire R$3,474 → M200302 (geo: GB) (tx T530L3I6DS1KC)
- `2025-07-10` — PIX R$9,292 → C100517 (MCC 6051) (tx TK8A8ZYQPY4JC)
- `2025-07-12` — Wire R$6,349 → M200049 (geo: GB; MCC 4111) (tx TQMR8H4QYFJDJ)
- `2025-07-20` — PIX R$7,031 → M200695 (via Tor) (tx T4NVTFMTAET7V)
- `2025-07-25` — Wire R$2,132 → M200913 (via Proxy; geo: CN) (tx TC1Y2A8SSWDQC)
- `2025-08-16` — Card R$881 → M200595 (geo: DE) (tx T7PBESY3I5111)
- `2025-09-13` — PIX R$15,332 → M200953 (MCC 6011) (tx T568LVLWC47D3)

---

## C101582
**Recommendation:** file_sar_immediate
**Confidence:** high — 7 concurrent rule fires; all facts traceable to transaction records
ML confidence: **Moderate** (cohort rank #9)

Customer with KYC risk score 73/100. declared income R$10,907/yr versus R$89,473 in 23 outflows (≈98× declared monthly income). anonymization events (2 Tor). Activity appears materially inconsistent with the declared customer profile.

**Triggered typologies:** anonymization, chargeback-merchant, high-MCC, income-mismatch, merchant-convergence, multi-rail, sanctions

### Key facts
- R$89,473 total outflow vs R$909/month declared income (98×)
- Anonymization breakdown: {'Tor': 2}

### Timeline
- `2025-07-05` — PIX R$506 → M200966 (MCC 4900) (tx TF8F0668QXDKJ)
- `2025-07-15` — PIX R$13,310 → M200696 (via Tor; MCC 4111) (tx T1UADPDDHFJPA)
- `2025-07-23` — Card R$454 → M200449 (geo: FR) (tx TG9WZU12O72OV)
- `2025-08-21` — Card R$3,295 → M200390 (geo: IQ; MCC 6051) (tx T1XY2A460O51H)
- `2025-08-25` — Card R$7,454 → C101819 (MCC 4900) (tx TOYX9MA23Q8NW)
- `2025-09-08` — PIX R$3,329 → M200797 (via Tor; MCC 4829) (tx T4P4Q65XC570F)
- `2025-09-21` — Wire R$24,230 → M200508 (MCC 4111) (tx TMBR17QPP9GD3)
- `2025-10-01` — PIX R$4,003 → M200282 (tx TARPIXB23P87B)

---

## C101542
**Recommendation:** file_sar_immediate
**Confidence:** high — 9 concurrent rule fires; all facts traceable to transaction records
ML confidence: **Moderate-High** (cohort rank #6)

Customer with KYC risk score 59/100. declared income R$3,687/yr versus R$103,287 in 28 outflows (≈336× declared monthly income). PIX passthrough ratio 751%. anonymization events (1 Tor, 1 Proxy, 1 VPN). Activity appears materially inconsistent with the declared customer profile.

**Triggered typologies:** anonymization, chargeback-merchant, fan-out, high-MCC, income-mismatch, merchant-convergence, multi-rail, network-linkage, passthrough

### Key facts
- R$103,287 total outflow vs R$307/month declared income (336×)
- PIX passthrough 751% (R$73,949 out / R$9,844 in)
- Anonymization breakdown: {'Tor': 1, 'Proxy': 1, 'VPN': 1}

### Timeline
- `2025-07-09` — PIX R$3,104 → M200841 (geo: AE; MCC 4829) (tx TRK1KEG424MBN)
- `2025-07-14` — PIX R$5,761 → M200971 (via Tor; MCC 7995) (tx T991C2EOAP061)
- `2025-07-20` — Card R$6,530 → M200260 (geo: US) (tx TTFTKZBP4CFMG)
- `2025-07-27` — Wire R$1,424 → C100375 (MCC 6051) (tx T8XYRVKV8AGM2)
- `2025-08-04` — PIX R$25,849 → M200966 (MCC 4900) (tx TSWFX3XIHOF2R)
- `2025-08-17` — PIX R$11,121 → M200616 (MCC 4829) (tx TCIOVP5V3QUJF)
- `2025-09-24` — PIX R$779 → M200196 (via Proxy; geo: US) (tx TUI6B5CHKXRA8)
- `2025-10-04` — Wire R$6,257 → M200776 (geo: LY) (tx TESLWHQ8LG92B)

---

## C100208
**Recommendation:** file_sar_immediate
**Confidence:** high — 9 concurrent rule fires; all facts traceable to transaction records
ML confidence: **Moderate-High** (cohort rank #7)

Customer with KYC risk score 89/100. declared income R$8,756/yr versus R$144,242 in 22 outflows (≈198× declared monthly income). PIX passthrough ratio 3675%. anonymization events (1 Tor, 1 Proxy, 1 VPN). Activity appears materially inconsistent with the declared customer profile.

**Triggered typologies:** KYC-inconsistency, anonymization, high-MCC, high-risk-geo, income-mismatch, merchant-convergence, multi-rail, network-linkage, passthrough

### Key facts
- R$144,242 total outflow vs R$730/month declared income (198×)
- PIX passthrough 3675% (R$55,600 out / R$1,513 in)
- Anonymization breakdown: {'Tor': 1, 'Proxy': 1, 'VPN': 1}

### Timeline
- `2025-07-03` — PIX R$18,916 → M200392 (MCC 4111) (tx TDL35CEBX1UUB)
- `2025-07-11` — Card R$51,589 → M200535 (geo: MM) (tx T7ILZTP10SBFN)
- `2025-07-14` — Wire R$1,665 → C102252 (tx TSM9Q0FWI3AUT)
- `2025-08-16` — Card R$22,284 → M200042 (MCC 4829) (tx T5EHA9CPQOOVG)
- `2025-08-19` — PIX R$3,411 → C100814 (via Tor) (tx TES9D9NM8CEMC)
- `2025-08-30` — Wire R$1,176 → M200620 (via Proxy) (tx TMMMDIC9EH6NQ)
- `2025-09-05` — Card R$1,964 → M200234 (geo: DE; MCC 4900) (tx TIYS64RBC1N8I)
- `2025-09-22` — PIX R$277 → M200779 (via VPN; MCC 7995) (tx TP549PR319CUY)

---
