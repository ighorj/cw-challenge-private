"""
Detection agent — wraps the Phase 2 rules engine and Phase 3 ML pipeline.

Does NOT reimplement either. Calls into src/rules and src/ml directly,
then merges their outputs into a single prioritized alert queue.
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(ROOT / "src" / "rules"))
sys.path.insert(0, str(ROOT / "src" / "ml"))

from shared import RunContext, save_json, load_json, now_iso  # noqa: E402
from priority import priority_score, severity_band, typology_families_hit  # noqa: E402
import alerts_engine as ae  # noqa: E402
import ml_pipeline as mp    # noqa: E402
from sklearn.model_selection import train_test_split  # noqa: E402


def run(ctx: RunContext, top_n=10):
    ctx.log("detection_agent", "start")

    # Load processed datasets from data agent's output
    txs = pd.read_parquet(ctx.artifact("processed_transactions.parquet"))
    kyc = pd.read_parquet(ctx.artifact("processed_customers.parquet"))
    # Merchants are needed by rules — load directly from data dir
    mer = pd.read_excel(ROOT / "data" / "AML Case Cloudwalk INC (2).xlsx",
                        sheet_name="Merchants")
    txs["timestamp"] = pd.to_datetime(txs.timestamp)

    # ── Phase 2 rules ─────────────────────────────────────────────────────
    fires = ae.run_rules(txs, kyc, mer)
    per = ae.score(fires)
    rows = [{"customer_id": cid,
             "triggered_rules": "|".join(sorted(set(e["rules"]))),
             "total_score": e["score"],
             "escalation_band": ae.assign_band(e),
             "hard_alert_flag": e["hard"]}
            for cid, e in per.items()]
    alerts = (pd.DataFrame(rows)
                .sort_values(["total_score", "hard_alert_flag"], ascending=[False, False])
                .reset_index(drop=True))
    alerts.to_csv(ctx.artifact("alerts_output.csv"), index=False)
    ctx.log("detection_agent", "rules_complete",
            alerted_customers=len(alerts),
            hard_alerts=int(alerts.hard_alert_flag.sum()))

    # ── Phase 3 ML ────────────────────────────────────────────────────────
    X_all = mp.build_features(txs, kyc, mer)
    lbl   = mp.build_labels(txs, kyc, mer)
    labeled = lbl.dropna(subset=["y"]).index
    X = X_all.loc[labeled].astype(float)
    y = lbl.loc[labeled, "y"].astype(int)
    X_dev, X_test, y_dev, y_test = train_test_split(
        X, y, test_size=0.30, stratify=y, random_state=42)
    model = mp.train_xgb(X_dev, y_dev)
    X_full = X_all.astype(float)
    probs = model.predict_proba(X_full)[:, 1]
    cuts = mp.percentile_bands(probs)
    ml_df = pd.DataFrame({
        "customer_id": X_full.index,
        "predicted_probability": probs.round(4),
        "predicted_band": [mp.assign_band(p, cuts) for p in probs],
    }).sort_values("predicted_probability", ascending=False).reset_index(drop=True)
    ml_df.to_csv(ctx.artifact("ml_ranked_output.csv"), index=False)
    ctx.log("detection_agent", "ml_complete",
            ml_tier1_count=int((ml_df.predicted_band == "ML Tier 1").sum()))

    # ── Merge into prioritized queue ──────────────────────────────────────
    merged = (alerts.merge(ml_df, on="customer_id", how="left")
                    .fillna({"predicted_probability": 0.0,
                             "predicted_band": "Routine"}))

    # Compute deterministic priority + severity per customer (see priority.py)
    merged["triggered_rules_list"] = merged.triggered_rules.fillna("").apply(
        lambda s: s.split("|") if s else [])
    merged["priority_score"] = merged.apply(
        lambda r: priority_score(int(r.total_score), float(r.predicted_probability),
                                 bool(r.hard_alert_flag), r.triggered_rules_list),
        axis=1)
    merged["severity"] = merged.apply(
        lambda r: severity_band(r.priority_score, r.triggered_rules_list), axis=1)

    queue = (merged.sort_values("priority_score", ascending=False)
                   .head(top_n)
                   .reset_index(drop=True))

    queue_obj = {
        "run_id": ctx.run_id,
        "generated_at": now_iso(),
        "top_n": top_n,
        "customers": [
            {"rank": i + 1,
             "customer_id": r.customer_id,
             "rules_score": int(r.total_score),
             "ml_probability": float(r.predicted_probability),
             "priority_score": float(r.priority_score),
             "severity": r.severity,
             "typology_families": typology_families_hit(r.triggered_rules_list),
             "escalation_band": r.escalation_band,
             "ml_band": r.predicted_band,
             "hard_alert": bool(r.hard_alert_flag),
             "triggered_rules": r.triggered_rules_list}
            for i, r in queue.iterrows()
        ],
    }
    save_json(ctx.artifact("prioritized_alert_queue.json"), queue_obj)

    ctx.log("detection_agent", "complete",
            queue_size=len(queue_obj["customers"]),
            top_customer=queue_obj["customers"][0]["customer_id"])
    return queue_obj


if __name__ == "__main__":
    ctx = RunContext()
    out = run(ctx)
    print(f"Top: {out['customers'][0]['customer_id']}  "
          f"score={out['customers'][0]['rules_score']}  "
          f"ml={out['customers'][0]['ml_probability']}")
