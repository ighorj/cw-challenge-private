# Investigation Summary — run 20260526-120114-87e097
_Backend: template · Generated: 2026-05-26T15:01:32+00:00_
_ML confidence labels are calibrated relative to the investigated escalation cohort, not the full customer population._

## C100091
**Recommendation:** file_sar_immediate
**Confidence:** high — 10 concurrent rule fires; all facts traceable to transaction records
ML confidence: **Moderate** (cohort rank #3)

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
ML confidence: **Moderate-High** (cohort rank #2)

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
ML confidence: **High** (cohort rank #1)

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
