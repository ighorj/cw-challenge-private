"""
Detection agent — wraps the Phase 2 rules engine and Phase 3 ML pipeline.

Does NOT reimplement either. Calls into src/rules and src/ml directly,
then merges their outputs into a single prioritized alert queue.
When use_llm=True, an LLM adds qualitative triage rationale to the queue.
"""

import sys
import json
from pathlib import Path
import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(ROOT / "src" / "rules"))
sys.path.insert(0, str(ROOT / "src" / "ml"))

from shared import RunContext, save_json, load_json, now_iso, llm_available, call_anthropic  # noqa: E402
from priority import priority_score, severity_band, typology_families_hit  # noqa: E402
import alerts_engine as ae  # noqa: E402
import ml_pipeline as mp    # noqa: E402
from sklearn.model_selection import train_test_split  # noqa: E402

PROMPT_FILE = Path(__file__).parent / "prompt.md"


def _parse_llm_json(raw):
    """Strip code fences and extract first balanced JSON object from LLM response."""
    clean = raw.strip()
    if clean.startswith("```json"):
        clean = clean[7:]
    elif clean.startswith("```"):
        clean = clean[3:]
    if clean.endswith("```"):
        clean = clean[:-3]
    clean = clean.strip()
    try:
        return json.loads(clean)
    except json.JSONDecodeError:
        s = clean.find("{")
        if s == -1:
            raise ValueError(f"No JSON object in LLM response. Raw (first 300 chars): {raw[:300]!r}")
        depth, e = 0, -1
        for i in range(s, len(clean)):
            if clean[i] == "{": depth += 1
            elif clean[i] == "}":
                depth -= 1
                if depth == 0: e = i; break
        if e == -1:
            raise ValueError(f"Unmatched braces in LLM response. Raw (first 300 chars): {raw[:300]!r}")
        return json.loads(clean[s:e + 1])


def _llm_triage(queue_obj, run_id):
    """LLM adds qualitative triage rationale to the prioritized queue."""
    prompt = PROMPT_FILE.read_text()
    parts = prompt.split("## User", 1)
    system = parts[0].replace("## System", "").strip()
    user = parts[1].strip() if len(parts) > 1 else ""
    user = (user.replace("{run_id}", run_id)
                .replace("{queue_json}", json.dumps(queue_obj, indent=2, default=str)))
    raw = call_anthropic(system, user, max_tokens=2000)
    return _parse_llm_json(raw)


def run(ctx: RunContext, top_n=10, use_llm=False):
    ctx.log("detection_agent", "start", use_llm=use_llm)

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
    # LLM triage — adds qualitative rationale per alert and cross-customer patterns
    backend = "anthropic" if (use_llm and llm_available()) else "template"
    ctx.log("detection_agent", "backend_selected", backend=backend)

    if backend == "anthropic":
        triage = _llm_triage(queue_obj, ctx.run_id)
        triage["_backend"] = "anthropic"
    else:
        triage = {
            "triage_summary": (
                f"Queue of {len(queue_obj['customers'])} customers. "
                f"Top customer {queue_obj['customers'][0]['customer_id']} scored "
                f"{queue_obj['customers'][0]['priority_score']} with severity "
                f"{queue_obj['customers'][0]['severity']}."
            ),
            "alert_rationale": [
                {
                    "customer_id": c["customer_id"],
                    "rank": c["rank"],
                    "severity": c["severity"],
                    "primary_typology": c["typology_families"][0] if c["typology_families"] else "unknown",
                    "rationale": f"{len(c['triggered_rules'])} rules fired across {len(c['typology_families'])} typology families; priority={c['priority_score']}.",
                    "investigation_priority": "immediate" if c["severity"] in ("critical",) else ("urgent" if c["severity"] == "high" else "standard"),
                }
                for c in queue_obj["customers"]
            ],
            "cross_customer_patterns": [],
            "recommended_investigation_order": [c["customer_id"] for c in queue_obj["customers"]],
            "_backend": "template",
        }

    queue_obj["triage"] = triage
    save_json(ctx.artifact("prioritized_alert_queue.json"), queue_obj)

    ctx.log("detection_agent", "complete",
            queue_size=len(queue_obj["customers"]),
            top_customer=queue_obj["customers"][0]["customer_id"],
            backend=backend)
    return queue_obj


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--top-n", type=int, default=10)
    ap.add_argument("--use-llm", action="store_true")
    args = ap.parse_args()
    ctx = RunContext(run_id=args.run_id)
    out = run(ctx, top_n=args.top_n, use_llm=args.use_llm)
    print(f"Top: {out['customers'][0]['customer_id']}  "
          f"score={out['customers'][0]['rules_score']}  "
          f"ml={out['customers'][0]['ml_probability']}")
