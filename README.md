# CloudWalk AML/FT Investigation Pipeline

End-to-end AML/FT analysis on a 52,000-transaction CloudWalk dataset, combining manual investigation, a 21-rule alerting engine, and an XGBoost prioritization layer to produce SAR-ready outputs.

---

## Objective

Given four months of customer and transaction data, identify and rank suspicious entities defensibly:

1. Surface a cohort of high-risk subjects through manual investigation and file SARs.
2. Generalize the analyst's reasoning into a deterministic, auditable rules engine.
3. Layer an XGBoost prioritization model that complements (not replaces) the rules engine.

The pipeline targets operational realism and methodological honesty over benchmark optimization.

---

## Phase overview

| Phase | Output | Key deliverable |
|---|---|---|
| **1 — Investigation** | 9-subject cohort · 2 SARs filed | `docs/phase1/` |
| **2 — Rules engine** | 21 rules · composite scoring · escalation bands | `docs/phase2/`, `src/rules/` |
| **3 — ML prioritization** | XGBoost classifier · SHAP explanations · ranked queue | `docs/phase3/`, `src/ml/` |

---

## Architecture

```
Raw transactions + KYC
        │
        ▼
[ Phase 2 — Rules engine ]  ─► 21-rule alert set · composite score · escalation band
        │
        ▼
[ Phase 3 — XGBoost ]       ─► continuous probability · top-3 SHAP drivers
        │
        ▼
[ Analyst triage queue ]    ─► re-ranked, explained
```

The ML layer never suppresses a rule-driven escalation. It re-orders within bands and provides per-customer explanations.

---

## How to run

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the rules engine — generates outputs/rankings/alerts_output.csv
python3 src/rules/alerts_engine.py

# 3. Run the ML pipeline — generates outputs/figures/*.png and outputs/rankings/ml_*.csv
python3 src/ml/ml_pipeline.py
```

Scripts resolve their own paths relative to the repository root; run from any working directory.

---

## Key findings

- **Phase 1 primary SAR:** C102290 — PEP with KYC score 98/100, R$134k outflow (144× declared monthly income), Tor/VPN use, 2,013 % passthrough ratio.
- **Phase 1 network SAR:** C101848 → C102360 — only confirmed inter-subject Wire in the cohort, with same-day velocity burst.
- **Phase 2 reproduction:** All 9 manually investigated subjects land in Tier 1 / Tier 2 of the deterministic engine; C102290 ranks #2 of 2,494 alerted customers.
- **Phase 3 honesty:** XGBoost does **not** outperform the rules engine on labeled extremes (rules-only PR-AUC = 1.000 vs ML 0.998 — labels derive from the rules). The ML layer contributes intra-band ranking and SHAP-based explainability, not predictive lift.
- **SHAP concordance passes:** top drivers for C102290, C101848, and C102360 reproduce the SAR reasoning.

---

## Repository structure

```
CW/
├── data/                   Source dataset (xlsx)
│
├── docs/
│   ├── phase1/             Investigation report + 2 SARs
│   ├── phase2/             Rule catalog + executive summary
│   ├── phase3/             ML strategy, results, features, summary
│   └── final/              Reference case PDF
│
├── src/
│   ├── rules/              alerts_engine.py — rules + composite scoring
│   ├── ml/                 ml_pipeline.py — XGBoost + SHAP
│   └── notebooks/          Exploratory notebooks
│
├── outputs/
│   ├── figures/            SHAP / PCA / chart PNGs
│   ├── rankings/           Generated CSVs (alerts, ML scores, importance)
│   └── logs/
│
├── config/                 Engineering principles (ClaudeInstructions.md)
│
├── README.md
├── requirements.txt
├── LICENSE
└── .gitignore
```

---

## Reviewer entry points

- High-level project narrative — this README + `docs/phase3/Phase3_ML_Summary.md`
- Investigation details — `docs/phase1/Phase1-Investigation-Report.md`
- Rule logic — `docs/phase2/alert_rules.md` and `src/rules/alerts_engine.py`
- Model honesty discussion — `docs/phase3/ml_results.md` (§ A1 baseline, § A4 concordance)
