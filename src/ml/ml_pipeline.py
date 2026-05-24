"""
ML prioritization pipeline — Phase 3.

Builds customer-level features from a temporal window, derives weak-supervision
labels by re-running the Phase 2 rules engine on a forward window, trains an
XGBoost classifier, evaluates with imbalance-aware metrics, runs SHAP for
explainability, and writes a ranked output CSV.

This is a prioritization layer that complements the Phase 2 rules engine;
it never suppresses a rule-driven alert.
"""

import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src" / "rules"))

import numpy as np
import pandas as pd
import xgboost as xgb
import shap
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import average_precision_score, roc_auc_score
from scipy.stats import spearmanr

import alerts_engine as ae

FIGURES_DIR = ROOT / "outputs" / "figures"
RANKINGS_DIR = ROOT / "outputs" / "rankings"

RANDOM_STATE = 42
TOP_K = 50

# Risk-profile classification: full period for both features and labels.
# A temporal split was attempted (features Jul-Aug, labels Sep-Oct) but
# Phase 2 thresholds were calibrated for 4-month windows and yielded only
# 64 positives on a 2-month label slice — insufficient for stable training.
# The current setup treats the task as risk-profile classification, which
# the small dataset and stable customer behavior actually support.
FEAT_START  = pd.Timestamp("2025-07-01")
FEAT_END    = pd.Timestamp("2025-11-01")   # exclusive
LABEL_START = FEAT_START
LABEL_END   = FEAT_END

PHASE1_SUBJECTS = [
    "C100091", "C101208", "C101028", "C100837", "C101582",
    "C102290", "C102093", "C100208", "C101445", "C101542",
]


# ─────────────────────────────────────────────────────────────────────────────
# Feature engineering
# ─────────────────────────────────────────────────────────────────────────────

def build_features(txs_window, kyc, mer):
    """Customer-level aggregates from a transaction window."""
    cust = txs_window[txs_window.sender_entity_type == "customer"].copy()
    cust["timestamp"] = pd.to_datetime(cust.timestamp)
    cust["day"] = cust.timestamp.dt.date
    cust["hour"] = cust.timestamp.dt.hour
    cust["dow"] = cust.timestamp.dt.dayofweek

    # Behavioral aggregates
    agg = cust.groupby("sender_id").agg(
        tx_count=("transaction_id", "size"),
        distinct_active_days=("day", "nunique"),
        log_total_outflow=("amount_brl", lambda s: np.log1p(s.sum())),
        mean_tx_amount=("amount_brl", "mean"),
        std_tx_amount=("amount_brl", "std"),
        max_tx_amount=("amount_brl", "max"),
        distinct_geo_countries=("geo_country", "nunique"),
        distinct_merchants=("receiver_id", "nunique"),
        distinct_devices=("device_fingerprint", "nunique"),
        distinct_ip_addresses=("ip_address", "nunique"),
        distinct_mccs=("mcc", "nunique"),
    )

    max_daily = (cust.groupby(["sender_id", "day"]).size()
                     .groupby("sender_id").max().rename("max_txs_per_day"))

    # Rail-specific log outflows
    rails = (cust.groupby(["sender_id", "transaction_type"])["amount_brl"]
                 .sum().unstack(fill_value=0))
    rails.columns = [f"log_{c.lower()}_outflow" for c in rails.columns]
    rails = np.log1p(rails)

    # PIX cash_in (as receiver) vs cash_out (as sender)
    pix_out = (txs_window[(txs_window.pix_flow == "cash_out") &
                          (txs_window.sender_entity_type == "customer")]
                  .groupby("sender_id")["amount_brl"].sum())
    pix_in = (txs_window[txs_window.pix_flow == "cash_in"]
                 .groupby("receiver_id")["amount_brl"].sum())
    pix_feat = pd.DataFrame({
        "log_pix_out": np.log1p(pix_out),
        "log_pix_in":  np.log1p(pix_in.reindex(pix_out.index, fill_value=0)),
    })

    # Geo
    geo_hr = (cust[cust.country_risk_geo == "High"]
                 .groupby("sender_id").size().rename("count_high_risk_geo"))
    cb_frac = (cust.assign(_cb=(cust.cross_border == "Yes").astype(int))
                   .groupby("sender_id")["_cb"].mean().rename("fraction_cross_border"))
    ip_mm = cust[cust.ip_country.notna() & cust.sender_country.notna() &
                 (cust.ip_country != cust.sender_country)]
    ip_mm_ct = ip_mm.groupby("sender_id").size().rename("count_ip_mismatch")

    # Merchant
    mer_idx = mer.set_index("merchant_id")
    cust["_mer_cb"]      = cust.receiver_id.map(mer_idx["merchant_chargeback_ratio_90d"])
    cust["_mer_high_mcc"] = (cust.receiver_id.map(mer_idx["mcc_risk"]) == "High").astype(int)
    mer_feat = cust.groupby("sender_id").agg(
        mean_merchant_chargeback=("_mer_cb", "mean"),
        fraction_high_mcc=("_mer_high_mcc", "mean"),
    )

    # Network
    c2c = cust[cust.receiver_entity_type == "customer"]
    c2c_feat = c2c.groupby("sender_id").agg(
        count_c2c_tx=("transaction_id", "size"),
        distinct_c2c_counterparties=("receiver_id", "nunique"),
    )
    wire_sent = (cust[cust.transaction_type == "Wire"]
                    .groupby("sender_id").size().rename("count_wire_sent"))

    # Anonymization / device
    anon = cust[cust.ip_proxy_vpn_tor.isin(["Tor", "VPN", "Proxy"])]
    anon_ct = anon.groupby("sender_id").size().rename("count_anon_events")
    tor_ct  = (anon[anon.ip_proxy_vpn_tor == "Tor"]
                   .groupby("sender_id").size().rename("count_tor_events"))
    rooted_ct = (cust[cust.device_rooted == "Yes"]
                     .groupby("sender_id").size().rename("count_rooted_tx"))

    # Card / e-com
    cnp_ct = (cust[(cust.transaction_type == "Card") & (cust.card_present == "No")]
                  .groupby("sender_id").size().rename("count_cnp"))
    no_3ds_ct = (cust[cust.auth_3ds == "No"]
                     .groupby("sender_id").size().rename("count_no_3ds"))
    cb_status = (cust[cust.status == "Chargeback"]
                     .groupby("sender_id").size().rename("count_chargeback_status"))

    # Temporal
    night = (cust.assign(_n=((cust.hour < 6) | (cust.hour >= 22)).astype(int))
                 .groupby("sender_id")["_n"].mean().rename("fraction_night_activity"))
    weekend = (cust.assign(_w=(cust.dow >= 5).astype(int))
                   .groupby("sender_id")["_w"].mean().rename("fraction_weekend_activity"))

    # KYC static
    kyc_s = kyc.set_index("customer_id").copy()
    kyc_s["log_annual_income"] = np.log1p(kyc_s["annual_income_brl"])
    kyc_s["pep_flag"]          = (kyc_s.pep == "Yes").astype(int)
    kyc_s["risk_rating_ord"]   = kyc_s.risk_rating.map({"Low": 1, "Medium": 2, "High": 3})
    kyc_s["kyc_tier_ord"]      = kyc_s.kyc_tier.map({"L1": 1, "L2": 2, "L3": 3})
    kyc_s["age"] = ((FEAT_START - pd.to_datetime(kyc_s.date_of_birth))
                        .dt.days / 365.25)
    kyc_static = kyc_s[["log_annual_income", "pep_flag", "risk_rating_ord",
                        "kyc_tier_ord", "kyc_risk_score", "age"]]

    feats = pd.concat([agg, rails, max_daily, pix_feat,
                       geo_hr, cb_frac, ip_mm_ct,
                       mer_feat, c2c_feat, wire_sent,
                       anon_ct, tor_ct, rooted_ct,
                       cnp_ct, no_3ds_ct, cb_status,
                       night, weekend], axis=1)

    # Reindex to full customer base; zero-fill behavioral, join static
    feats = feats.reindex(kyc.customer_id)
    behavioral_cols = [c for c in feats.columns]
    feats[behavioral_cols] = feats[behavioral_cols].fillna(0)
    feats = feats.join(kyc_static, how="left")

    return feats


# ─────────────────────────────────────────────────────────────────────────────
# Labeling
# ─────────────────────────────────────────────────────────────────────────────

def build_labels(txs_window, kyc, mer):
    """Re-run Phase 2 engine on label window, derive binary labels."""
    fires = ae.run_rules(txs_window, kyc, mer)
    per = ae.score(fires)

    rows = []
    for cid in kyc.customer_id:
        e = per.get(cid, {"score": 0, "hard": False, "rules": []})
        rows.append({"customer_id": cid,
                     "composite_score": e["score"],
                     "hard_alert": e["hard"]})
    df = pd.DataFrame(rows).set_index("customer_id")

    # Tighter labeling: top vs bottom of the score distribution.
    # Using "Tier 1 vs Routine" yields ~96% prevalence in the labeled set —
    # metrics become trivially high (model learns active vs inactive, not
    # risk-vs-no-risk). Score >= 13 captures genuine top-risk profiles;
    # score <= 4 isolates customers with minimal/incidental rule fires.
    def to_y(r):
        if r.hard_alert or r.composite_score >= 13:
            return 1
        if r.composite_score <= 4:
            return 0
        return np.nan
    df["y"] = df.apply(to_y, axis=1)
    return df


# ─────────────────────────────────────────────────────────────────────────────
# Model + evaluation
# ─────────────────────────────────────────────────────────────────────────────

def train_xgb(X_dev, y_dev):
    X_tr, X_val, y_tr, y_val = train_test_split(
        X_dev, y_dev, test_size=0.25, stratify=y_dev, random_state=RANDOM_STATE
    )
    pos, neg = int(y_tr.sum()), int((y_tr == 0).sum())
    spw = neg / max(pos, 1)

    model = xgb.XGBClassifier(
        max_depth=4,
        learning_rate=0.1,
        n_estimators=500,
        subsample=0.8,
        colsample_bytree=0.8,
        scale_pos_weight=spw,
        random_state=RANDOM_STATE,
        objective="binary:logistic",
        eval_metric="aucpr",
        early_stopping_rounds=30,
        n_jobs=-1,
        verbosity=0,
    )
    model.fit(X_tr, y_tr, eval_set=[(X_val, y_val)], verbose=False)
    return model


def topk_metrics(y_true, probs, k=50):
    y_true = np.asarray(y_true)
    order = np.argsort(probs)[::-1][:k]
    hits = y_true[order].sum()
    return hits / k, hits / max(y_true.sum(), 1)


def percentile_bands(probs):
    """Percentile-based cutoffs sized to analyst review capacity:
    top 1% = ML Tier 1, top 5% = Tier 2, top 20% = Tier 3.
    Fixed-probability thresholds (e.g. p>=0.75) push >50% of the population
    into Tier 1 on this dataset and are operationally meaningless.
    """
    return {
        "tier1": np.percentile(probs, 99),
        "tier2": np.percentile(probs, 95),
        "tier3": np.percentile(probs, 80),
    }


def assign_band(p, cuts):
    if p >= cuts["tier1"]: return "ML Tier 1"
    if p >= cuts["tier2"]: return "ML Tier 2"
    if p >= cuts["tier3"]: return "ML Tier 3"
    return "Routine"


# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────

def main():
    print("Loading data...")
    txs, kyc, mer = ae.load_data()
    txs["timestamp"] = pd.to_datetime(txs.timestamp)

    print(f"\nFeature window: {FEAT_START.date()} → {(FEAT_END - pd.Timedelta(days=1)).date()}")
    print(f"Label window:   {LABEL_START.date()} → {(LABEL_END - pd.Timedelta(days=1)).date()}")

    txs_feat = txs[(txs.timestamp >= FEAT_START)  & (txs.timestamp < FEAT_END)]
    txs_lbl  = txs[(txs.timestamp >= LABEL_START) & (txs.timestamp < LABEL_END)]
    print(f"  feature-window txs: {len(txs_feat):>6}")
    print(f"  label-window txs:   {len(txs_lbl):>6}")

    X_all = build_features(txs_feat, kyc, mer)
    lbl   = build_labels(txs_lbl, kyc, mer)
    print(f"\nFeatures: {X_all.shape[0]} customers × {X_all.shape[1]} features")
    print(f"Labels:  pos={int(lbl.y.eq(1).sum())}  neg={int(lbl.y.eq(0).sum())}  excluded={int(lbl.y.isna().sum())}")

    # Confined cohort for training
    labeled = lbl.dropna(subset=["y"]).index
    X = X_all.loc[labeled].astype(float)
    y = lbl.loc[labeled, "y"].astype(int)

    X_dev, X_test, y_dev, y_test = train_test_split(
        X, y, test_size=0.30, stratify=y, random_state=RANDOM_STATE
    )
    print(f"\nTrain+val: n={len(X_dev)}  pos={int(y_dev.sum())}")
    print(f"Test:      n={len(X_test)}  pos={int(y_test.sum())}")

    model = train_xgb(X_dev, y_dev)

    # ── Evaluation ────────────────────────────────────────────────────────
    test_probs = model.predict_proba(X_test)[:, 1]
    pr_auc = average_precision_score(y_test, test_probs)
    roc    = roc_auc_score(y_test, test_probs)
    prec50, rec50 = topk_metrics(y_test, test_probs, k=TOP_K)
    print(f"\nTest metrics:")
    print(f"  PR-AUC          {pr_auc:.4f}")
    print(f"  ROC-AUC         {roc:.4f}")
    print(f"  Precision@Top{TOP_K} {prec50:.4f}")
    print(f"  Recall@Top{TOP_K}    {rec50:.4f}")

    # ── SHAP global + local ───────────────────────────────────────────────
    print("\nRunning SHAP (TreeExplainer)...")
    X_full = X_all.astype(float)
    explainer = shap.TreeExplainer(model)
    shap_vals = explainer.shap_values(X_full)
    probs_full = model.predict_proba(X_full)[:, 1]

    # Ranking-quality check: does ML probability rank customers similarly
    # to the Phase 2 composite score? Spearman on full population.
    full_scores = lbl.composite_score.reindex(X_full.index).fillna(0).values
    rho, _ = spearmanr(probs_full, full_scores)
    print(f"\nSpearman(ML prob, Phase 2 composite score) on all 2500 customers: {rho:.4f}")

    # Global summary plot
    plt.figure()
    shap.summary_plot(shap_vals, X_full, show=False, max_display=15)
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "ml_shap_summary.png", dpi=120, bbox_inches="tight")
    plt.close()
    print(f"  saved {FIGURES_DIR / 'ml_shap_summary.png'}")

    # Local: print top features for Phase 1 subjects
    print("\nSHAP local explanations (Phase 1 subjects):")
    feat_names = X_full.columns.tolist()
    for cid in PHASE1_SUBJECTS:
        if cid not in X_full.index:
            continue
        i = X_full.index.get_loc(cid)
        sv = shap_vals[i]
        order = np.argsort(-np.abs(sv))[:5]
        print(f"\n  {cid}  prob={probs_full[i]:.3f}  actual_y={lbl.loc[cid, 'y']}")
        for j in order:
            print(f"    {feat_names[j]:32s} shap={sv[j]:+7.3f}  value={X_full.iloc[i, j]:>10.2f}")

    # ── Ranked output for ALL customers ────────────────────────────────────
    print("\nWriting ml_ranked_output.csv...")
    cuts = percentile_bands(probs_full)
    print(f"  band cutoffs: T1>={cuts['tier1']:.4f}  T2>={cuts['tier2']:.4f}  T3>={cuts['tier3']:.4f}")
    rows = []
    for i, cid in enumerate(X_full.index):
        sv = shap_vals[i]
        order = np.argsort(-np.abs(sv))[:3]
        ay = lbl.loc[cid, "y"] if cid in lbl.index else np.nan
        rows.append({
            "customer_id": cid,
            "predicted_probability": round(float(probs_full[i]), 4),
            "predicted_band": assign_band(probs_full[i], cuts),
            "actual_label": int(ay) if pd.notna(ay) else -1,
            "top_shap_driver_1": feat_names[order[0]],
            "top_shap_driver_2": feat_names[order[1]],
            "top_shap_driver_3": feat_names[order[2]],
        })
    out = (pd.DataFrame(rows)
             .sort_values("predicted_probability", ascending=False)
             .reset_index(drop=True))
    out.to_csv(RANKINGS_DIR / "ml_ranked_output.csv", index=False)
    print(f"  {len(out)} rows written -> {RANKINGS_DIR / 'ml_ranked_output.csv'}")

    # Feature importance (gain)
    imp = pd.DataFrame({
        "feature": feat_names,
        "gain":    model.feature_importances_,
    }).sort_values("gain", ascending=False)
    imp.to_csv(RANKINGS_DIR / "ml_feature_importance.csv", index=False)
    print(f"\nTop 10 by gain:")
    print(imp.head(10).to_string(index=False))

    return {
        "metrics": {"PR-AUC": pr_auc, "ROC-AUC": roc,
                    f"Precision@Top{TOP_K}": prec50,
                    f"Recall@Top{TOP_K}": rec50},
        "feature_count": X_full.shape[1],
        "n_train": len(X_dev), "n_test": len(X_test),
        "pos_train": int(y_dev.sum()), "pos_test": int(y_test.sum()),
    }


if __name__ == "__main__":
    main()
