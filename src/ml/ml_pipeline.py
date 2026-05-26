"""
ML prioritization pipeline — Phase 3 (v2).

Regression-based behavioral risk ranker:
  • Target: behavioral_risk_score, the sum of weights for the **soft
    behavioral** core rules (R02 structuring, R03 income mismatch,
    R09 PEP). Hard regulatory alerts (R08 sanctions, R16 self-merchant,
    R21 network linkage) are deliberately excluded from the target —
    those are binary regulatory facts owned by the rules engine, not
    things ML should be expected to predict from transactional behavior.
    The remaining rules (R01, R04–R07, R10–R15, R17–R20) are held out
    and survive only as raw behavioral aggregates the model must learn
    to combine. This breaks the trivial circularity of the v1 binary
    classifier (which used composite_score as both target and feature
    proxy).
  • Training set: ALL 2,500 customers. v1 excluded 1,726 customers in
    the score-4-to-12 band; here the regression target is defined for
    everyone, so the model sees the full distribution.
  • Features: behavioral aggregates + Isolation Forest anomaly score
    + network-exposure features (counterparty composite scores,
    high-chargeback merchant exposure).
  • Calibration: isotonic regression maps the raw regression score to
    a [0,1] probability anchored on P(composite_score is in top decile),
    so downstream agents that consume `predicted_probability` get a
    meaningful probability rather than a min-max'd score.

Outputs:
  outputs/rankings/ml_ranked_output.csv        — per-customer rank + SHAP drivers
  outputs/rankings/ml_feature_importance.csv   — XGBoost gain
  outputs/figures/ml_shap_summary.png          — SHAP global summary
"""

import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src" / "rules"))
sys.path.insert(0, str(ROOT / "src" / "ml"))

import numpy as np
import pandas as pd
import xgboost as xgb
import shap
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    average_precision_score, roc_auc_score,
    mean_squared_error, mean_absolute_error, r2_score,
)
from sklearn.isotonic import IsotonicRegression
from scipy.stats import spearmanr

import alerts_engine as ae
import isolation_forest as iso_mod

FIGURES_DIR  = ROOT / "outputs" / "figures"
RANKINGS_DIR = ROOT / "outputs" / "rankings"

RANDOM_STATE = 42
TOP_K = 50

# Window. Full review period; rule thresholds are calibrated for this span,
# and a 2-month label window collapses positive density (see v1 notes).
FEAT_START = pd.Timestamp("2025-07-01")
FEAT_END   = pd.Timestamp("2025-11-01")

# Behavioral core rules: soft, score-contributor rules that map to
# patterns the model can learn from transaction aggregates. The
# remaining rules (R01, R04–R07, R10–R15, R17–R20) are deliberately
# held out — the model must rediscover them from raw aggregates.
# Hard regulatory alerts (R08, R16, R21) are owned by the rules engine
# and excluded from the ML target: they are binary regulatory facts,
# not behavioral patterns ML should be asked to predict.
BEHAVIORAL_CORE_RULE_IDS = {
    "R02_HIGH", "R02_LOW",       # structuring
    "R03_HIGH", "R03_LOW",       # income mismatch
    "R09",                       # PEP transactional
}

PHASE1_SUBJECTS = [
    "C100091", "C101208", "C101028", "C100837", "C101582",
    "C102290", "C102093", "C100208", "C101445", "C101542",
]

HIGH_SCORE_COUNTERPARTY_CUTOFF = 10        # composite_score threshold for "risky counterparty"
HIGH_CHARGEBACK_MERCHANT_CUTOFF = 0.10     # mirrors R19 in alerts_engine


# ─────────────────────────────────────────────────────────────────────────────
# Targets — core_risk_score (label) and composite_score (comparison only)
# ─────────────────────────────────────────────────────────────────────────────

def build_targets(txs_window, kyc, mer):
    """Compute behavioral_risk_score (regression target) and full
    composite_score (kept only for comparison + counterparty features)."""
    fires = ae.run_rules(txs_window, kyc, mer)

    behav_score = {cid: 0 for cid in kyc.customer_id}
    full_score  = {cid: 0 for cid in kyc.customer_id}
    hard_full   = {cid: False for cid in kyc.customer_id}

    for rid, tier, w, cids in fires:
        for cid in cids:
            if cid not in full_score:
                continue
            # full composite (replicates Phase 2 scoring) — comparison only
            if tier in ("B", "C"):
                full_score[cid] += w
            if tier == "A":
                hard_full[cid] = True

            # behavioral target (soft rules only; hard alerts excluded)
            if rid in BEHAVIORAL_CORE_RULE_IDS:
                behav_score[cid] += w

    df = pd.DataFrame({
        "customer_id":           list(kyc.customer_id),
        "behavioral_risk_score": [behav_score[c] for c in kyc.customer_id],
        "composite_score":       [full_score[c]  for c in kyc.customer_id],
        "hard_alert":            [hard_full[c]   for c in kyc.customer_id],
    }).set_index("customer_id")
    return df


# ─────────────────────────────────────────────────────────────────────────────
# Feature engineering
# ─────────────────────────────────────────────────────────────────────────────

def build_behavioral_features(txs_window, kyc, mer):
    """Customer-level aggregates from a transaction window.
    Identical signal coverage to v1 minus `pep_flag` (1:1 with R09 label)."""
    cust = txs_window[txs_window.sender_entity_type == "customer"].copy()
    cust["timestamp"] = pd.to_datetime(cust.timestamp)
    cust["day"]  = cust.timestamp.dt.date
    cust["hour"] = cust.timestamp.dt.hour
    cust["dow"]  = cust.timestamp.dt.dayofweek

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

    rails = (cust.groupby(["sender_id", "transaction_type"])["amount_brl"]
                 .sum().unstack(fill_value=0))
    rails.columns = [f"log_{c.lower()}_outflow" for c in rails.columns]
    rails = np.log1p(rails)

    pix_out = (txs_window[(txs_window.pix_flow == "cash_out") &
                          (txs_window.sender_entity_type == "customer")]
                  .groupby("sender_id")["amount_brl"].sum())
    pix_in = (txs_window[txs_window.pix_flow == "cash_in"]
                 .groupby("receiver_id")["amount_brl"].sum())
    pix_feat = pd.DataFrame({
        "log_pix_out": np.log1p(pix_out),
        "log_pix_in":  np.log1p(pix_in.reindex(pix_out.index, fill_value=0)),
    })

    geo_hr = (cust[cust.country_risk_geo == "High"]
                 .groupby("sender_id").size().rename("count_high_risk_geo"))
    cb_frac = (cust.assign(_cb=(cust.cross_border == "Yes").astype(int))
                   .groupby("sender_id")["_cb"].mean().rename("fraction_cross_border"))
    ip_mm = cust[cust.ip_country.notna() & cust.sender_country.notna() &
                 (cust.ip_country != cust.sender_country)]
    ip_mm_ct = ip_mm.groupby("sender_id").size().rename("count_ip_mismatch")

    mer_idx = mer.set_index("merchant_id")
    cust["_mer_cb"]      = cust.receiver_id.map(mer_idx["merchant_chargeback_ratio_90d"])
    cust["_mer_high_mcc"] = (cust.receiver_id.map(mer_idx["mcc_risk"]) == "High").astype(int)
    mer_feat = cust.groupby("sender_id").agg(
        mean_merchant_chargeback=("_mer_cb", "mean"),
        fraction_high_mcc=("_mer_high_mcc", "mean"),
    )

    c2c = cust[cust.receiver_entity_type == "customer"]
    c2c_feat = c2c.groupby("sender_id").agg(
        count_c2c_tx=("transaction_id", "size"),
        distinct_c2c_counterparties=("receiver_id", "nunique"),
    )
    wire_sent = (cust[cust.transaction_type == "Wire"]
                    .groupby("sender_id").size().rename("count_wire_sent"))

    anon = cust[cust.ip_proxy_vpn_tor.isin(["Tor", "VPN", "Proxy"])]
    anon_ct = anon.groupby("sender_id").size().rename("count_anon_events")
    tor_ct  = (anon[anon.ip_proxy_vpn_tor == "Tor"]
                   .groupby("sender_id").size().rename("count_tor_events"))
    rooted_ct = (cust[cust.device_rooted == "Yes"]
                     .groupby("sender_id").size().rename("count_rooted_tx"))

    cnp_ct = (cust[(cust.transaction_type == "Card") & (cust.card_present == "No")]
                  .groupby("sender_id").size().rename("count_cnp"))
    no_3ds_ct = (cust[cust.auth_3ds == "No"]
                     .groupby("sender_id").size().rename("count_no_3ds"))
    cb_status = (cust[cust.status == "Chargeback"]
                     .groupby("sender_id").size().rename("count_chargeback_status"))

    night = (cust.assign(_n=((cust.hour < 6) | (cust.hour >= 22)).astype(int))
                 .groupby("sender_id")["_n"].mean().rename("fraction_night_activity"))
    weekend = (cust.assign(_w=(cust.dow >= 5).astype(int))
                   .groupby("sender_id")["_w"].mean().rename("fraction_weekend_activity"))

    # KYC static. pep_flag intentionally dropped: it is the 1:1 trigger
    # for R09, which is in the label set. log_annual_income stays —
    # R03 uses the income/outflow ratio, not income alone.
    kyc_s = kyc.set_index("customer_id").copy()
    kyc_s["log_annual_income"] = np.log1p(kyc_s["annual_income_brl"])
    kyc_s["risk_rating_ord"]   = kyc_s.risk_rating.map({"Low": 1, "Medium": 2, "High": 3})
    kyc_s["kyc_tier_ord"]      = kyc_s.kyc_tier.map({"L1": 1, "L2": 2, "L3": 3})
    kyc_s["age"] = ((FEAT_START - pd.to_datetime(kyc_s.date_of_birth))
                        .dt.days / 365.25)
    kyc_static = kyc_s[["log_annual_income", "risk_rating_ord",
                        "kyc_tier_ord", "kyc_risk_score", "age"]]

    feats = pd.concat([agg, rails, max_daily, pix_feat,
                       geo_hr, cb_frac, ip_mm_ct,
                       mer_feat, c2c_feat, wire_sent,
                       anon_ct, tor_ct, rooted_ct,
                       cnp_ct, no_3ds_ct, cb_status,
                       night, weekend], axis=1)

    feats = feats.reindex(kyc.customer_id)
    feats[feats.columns] = feats[feats.columns].fillna(0)
    feats = feats.join(kyc_static, how="left")
    return feats


def build_network_features(txs_window, kyc, mer, targets):
    """Counterparty- and merchant-exposure features.

    Uses the Phase 2 composite_score of each receiver as the
    counterparty risk signal. This is rules-engine output, not model
    prediction, so it does not create a model-feedback loop.
    """
    cust = txs_window[txs_window.sender_entity_type == "customer"].copy()
    score_map = targets["composite_score"].to_dict()

    # ── counterparty exposure (customer → customer) ──
    c2c = cust[cust.receiver_entity_type == "customer"].copy()
    c2c["_recv_score"] = c2c.receiver_id.map(score_map).fillna(0)
    c2c["_high"]       = (c2c._recv_score >= HIGH_SCORE_COUNTERPARTY_CUTOFF).astype(int)

    high_cp = (c2c[c2c._high == 1].groupby("sender_id")["receiver_id"]
                  .nunique().rename("count_high_score_counterparties"))
    max_cp  = c2c.groupby("sender_id")["_recv_score"].max().rename("max_counterparty_score")

    c2c_out = c2c.groupby("sender_id")["amount_brl"].sum()
    c2c_high_out = c2c[c2c._high == 1].groupby("sender_id")["amount_brl"].sum()
    frac_high_out = (c2c_high_out / c2c_out).rename("fraction_outflow_to_high_score")

    # ── merchant exposure ──
    mer_idx = mer.set_index("merchant_id")
    c2m = cust[cust.receiver_entity_type == "merchant"].copy()
    c2m["_cb"] = c2m.receiver_id.map(mer_idx["merchant_chargeback_ratio_90d"])
    high_cb = (c2m[c2m._cb >= HIGH_CHARGEBACK_MERCHANT_CUTOFF]
                  .groupby("sender_id")["receiver_id"]
                  .nunique().rename("count_high_chargeback_merchants"))

    net = pd.concat([high_cp, max_cp, frac_high_out, high_cb], axis=1)
    net = net.reindex(kyc.customer_id).fillna(0)
    return net


def build_isolation_forest_feature(txs_window, mer, kyc):
    """Fit Isolation Forest standalone and return per-customer anomaly score."""
    if_df, _ = iso_mod.run(txs_window, mer)
    if_feat = (if_df.set_index("customer_id")["anomaly_score"]
                    .rename("iforest_anomaly_score"))
    if_feat = if_feat.reindex(kyc.customer_id).fillna(if_feat.mean())
    return if_feat.to_frame()


def build_features(txs_window, kyc, mer, targets):
    behavioral = build_behavioral_features(txs_window, kyc, mer)
    network    = build_network_features(txs_window, kyc, mer, targets)
    iforest    = build_isolation_forest_feature(txs_window, mer, kyc)
    X = behavioral.join(network, how="left").join(iforest, how="left")
    return X


# ─────────────────────────────────────────────────────────────────────────────
# Model
# ─────────────────────────────────────────────────────────────────────────────

def train_regressor(X_dev, y_dev):
    X_tr, X_val, y_tr, y_val = train_test_split(
        X_dev, y_dev, test_size=0.25, random_state=RANDOM_STATE
    )
    model = xgb.XGBRegressor(
        max_depth=4,
        learning_rate=0.08,
        n_estimators=800,
        subsample=0.85,
        colsample_bytree=0.85,
        reg_lambda=1.0,
        random_state=RANDOM_STATE,
        objective="reg:squarederror",
        eval_metric="rmse",
        early_stopping_rounds=40,
        n_jobs=-1,
        verbosity=0,
    )
    model.fit(X_tr, y_tr, eval_set=[(X_val, y_val)], verbose=False)
    return model


# ─────────────────────────────────────────────────────────────────────────────
# Calibration: regression score → probability
# ─────────────────────────────────────────────────────────────────────────────

def fit_calibrator(scores, binary_target):
    """Isotonic regression from raw regression score to P(top-decile)."""
    iso = IsotonicRegression(out_of_bounds="clip", y_min=0.0, y_max=1.0)
    iso.fit(scores, binary_target.astype(float))
    return iso


# ─────────────────────────────────────────────────────────────────────────────
# Bands + metrics
# ─────────────────────────────────────────────────────────────────────────────

def percentile_bands(probs):
    """Percentile cutoffs sized to analyst review capacity."""
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


def topk_overlap(true_scores, pred_scores, k=50):
    """How many of the model's top-k are in the true top-k?"""
    true_top = set(pd.Series(true_scores).sort_values(ascending=False).head(k).index)
    pred_top = set(pd.Series(pred_scores).sort_values(ascending=False).head(k).index)
    return len(true_top & pred_top) / k


def topk_binary(y_true, probs, k=50):
    y_true = np.asarray(y_true)
    order = np.argsort(probs)[::-1][:k]
    hits = y_true[order].sum()
    return hits / k, hits / max(y_true.sum(), 1)


# ─────────────────────────────────────────────────────────────────────────────
# Public scoring entrypoint — used by both `main()` and `detection_agent`
# ─────────────────────────────────────────────────────────────────────────────

def score_population(txs, kyc, mer, *, verbose=False, with_shap=True):
    """Train v2 pipeline on the supplied data and return the ranked DataFrame
    + band cutoffs + fitted model + SHAP values + feature matrix.

    The detection_agent uses this to avoid duplicating training logic.
    """
    txs = txs.copy()
    txs["timestamp"] = pd.to_datetime(txs.timestamp)
    txs_window = txs[(txs.timestamp >= FEAT_START) & (txs.timestamp < FEAT_END)]

    targets = build_targets(txs_window, kyc, mer)
    y_behav = targets["behavioral_risk_score"].astype(float)
    X = build_features(txs_window, kyc, mer, targets).astype(float)

    X_dev, X_test, y_dev, y_test = train_test_split(
        X, y_behav, test_size=0.30, random_state=RANDOM_STATE
    )
    model = train_regressor(X_dev, y_dev)
    pred_full = pd.Series(model.predict(X), index=X.index, name="predicted_score")

    composite = targets["composite_score"].reindex(X.index).astype(float)
    decile_cutoff = composite.quantile(0.90)
    y_top = (composite >= decile_cutoff) | targets["hard_alert"].reindex(X.index)
    calibrator = fit_calibrator(pred_full.loc[X_dev.index].values,
                                y_top.loc[X_dev.index].values)
    prob_full = pd.Series(calibrator.predict(pred_full.values), index=X.index,
                          name="predicted_probability")

    cuts = percentile_bands(prob_full.values)

    if with_shap:
        explainer = shap.TreeExplainer(model)
        shap_vals = explainer.shap_values(X)
    else:
        shap_vals = None

    feat_names = X.columns.tolist()
    rows = []
    for i, cid in enumerate(X.index):
        if shap_vals is not None:
            sv = shap_vals[i]
            order = np.argsort(-np.abs(sv))[:3]
            d1, d2, d3 = feat_names[order[0]], feat_names[order[1]], feat_names[order[2]]
        else:
            d1 = d2 = d3 = ""
        rows.append({
            "customer_id": cid,
            "predicted_probability": round(float(prob_full.iloc[i]), 4),
            "predicted_band": assign_band(prob_full.iloc[i], cuts),
            "predicted_score": round(float(pred_full.iloc[i]), 4),
            "behavioral_risk_score": int(y_behav.iloc[i]),
            "composite_score": int(composite.iloc[i]),
            "hard_alert": bool(targets.loc[cid, "hard_alert"]),
            "iforest_anomaly_score": round(float(X.loc[cid, "iforest_anomaly_score"]), 6),
            "top_shap_driver_1": d1,
            "top_shap_driver_2": d2,
            "top_shap_driver_3": d3,
        })
    ranked = (pd.DataFrame(rows)
                .sort_values("predicted_probability", ascending=False)
                .reset_index(drop=True))

    return {
        "ranked": ranked,
        "cuts": cuts,
        "model": model,
        "feature_matrix": X,
        "shap_values": shap_vals,
        "targets": targets,
        "X_test": X_test, "y_test": y_test,
    }


# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────

def main():
    print("Loading data...")
    txs, kyc, mer = ae.load_data()

    # Run the full v2 pipeline via the public entrypoint
    result = score_population(txs, kyc, mer, with_shap=True)

    ranked      = result["ranked"]
    cuts        = result["cuts"]
    model       = result["model"]
    X           = result["feature_matrix"]
    shap_vals   = result["shap_values"]
    targets     = result["targets"]
    X_test      = result["X_test"]
    y_test      = result["y_test"]

    y_behav   = targets["behavioral_risk_score"].astype(float).reindex(X.index)
    composite = targets["composite_score"].astype(float).reindex(X.index)
    feat_names = X.columns.tolist()

    print(f"\nFeatures: {X.shape[0]} customers × {X.shape[1]} features")
    print(f"behavioral_risk_score  mean={y_behav.mean():.2f}  std={y_behav.std():.2f}  "
          f"max={int(y_behav.max())}  nonzero={(y_behav > 0).sum()}/{len(y_behav)}")

    # ── Regression metrics on test ────────────────────────────────────────
    test_pred = model.predict(X_test)
    rmse = float(np.sqrt(mean_squared_error(y_test, test_pred)))
    mae  = float(mean_absolute_error(y_test, test_pred))
    r2   = float(r2_score(y_test, test_pred))
    rho_test, _ = spearmanr(test_pred, y_test)
    print(f"\nRegression metrics (test set, n={len(y_test)}):")
    print(f"  RMSE      {rmse:.4f}")
    print(f"  MAE       {mae:.4f}")
    print(f"  R²        {r2:.4f}")
    print(f"  Spearman  {rho_test:.4f}")

    # ── Binary-classification metrics (apples-to-apples vs v1) ────────────
    prob_full = ranked.set_index("customer_id")["predicted_probability"]
    y_v1 = composite.apply(lambda s: 1 if s >= 13 else (0 if s <= 4 else np.nan))
    y_v1[targets["hard_alert"].reindex(X.index)] = 1
    test_v1 = y_v1.reindex(X_test.index).dropna()
    if len(test_v1) > 0 and test_v1.nunique() == 2:
        prob_test = prob_full.reindex(test_v1.index)
        pr_auc = average_precision_score(test_v1, prob_test)
        roc    = roc_auc_score(test_v1, prob_test)
        prec50, rec50 = topk_binary(test_v1.values, prob_test.values, k=TOP_K)
        print(f"\nBinary metrics on v1-labeled test subset "
              f"(n={len(test_v1)}, pos={int(test_v1.sum())}):")
        print(f"  PR-AUC          {pr_auc:.4f}")
        print(f"  ROC-AUC         {roc:.4f}")
        print(f"  Precision@Top{TOP_K} {prec50:.4f}")
        print(f"  Recall@Top{TOP_K}    {rec50:.4f}")

    # ── Full-population ranking quality ───────────────────────────────────
    pred_full = pd.Series(model.predict(X), index=X.index)
    rho_full_behav, _ = spearmanr(pred_full.values, y_behav.values)
    rho_full_comp,  _ = spearmanr(pred_full.values, composite.values)
    top50_overlap  = topk_overlap(composite, pred_full, k=50)
    top100_overlap = topk_overlap(composite, pred_full, k=100)
    print(f"\nFull-population (n=2500) ranking quality:")
    print(f"  Spearman(pred, behavioral_risk_score) : {rho_full_behav:.4f}")
    print(f"  Spearman(pred, composite_score)       : {rho_full_comp:.4f}")
    print(f"  Top-50  overlap vs true top-50        : {top50_overlap:.4f}")
    print(f"  Top-100 overlap vs true top-100       : {top100_overlap:.4f}")

    # ── SHAP global summary plot ──────────────────────────────────────────
    print("\nWriting SHAP global summary plot...")
    plt.figure()
    shap.summary_plot(shap_vals, X, show=False, max_display=15)
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "ml_shap_summary.png", dpi=120, bbox_inches="tight")
    plt.close()
    print(f"  saved {FIGURES_DIR / 'ml_shap_summary.png'}")

    # ── Local SHAP for Phase 1 cohort ─────────────────────────────────────
    print("\nSHAP local explanations (Phase 1 cohort subjects):")
    for cid in PHASE1_SUBJECTS:
        if cid not in X.index:
            continue
        i = X.index.get_loc(cid)
        sv = shap_vals[i]
        order = np.argsort(-np.abs(sv))[:5]
        print(f"\n  {cid}  pred_score={pred_full.iloc[i]:6.2f}  "
              f"prob={prob_full.loc[cid]:.3f}  "
              f"behav={int(y_behav.iloc[i])}  "
              f"composite={int(composite.iloc[i])}  "
              f"hard={bool(targets.loc[cid, 'hard_alert'])}")
        for j in order:
            print(f"    {feat_names[j]:34s} shap={sv[j]:+7.3f}  value={X.iloc[i, j]:>10.2f}")

    # ── Write output CSV (+ actual_label for backward compat) ─────────────
    print(f"\nBand cutoffs: T1>={cuts['tier1']:.4f}  T2>={cuts['tier2']:.4f}  T3>={cuts['tier3']:.4f}")
    ranked = ranked.copy()
    ranked["actual_label"] = ranked.customer_id.map(
        lambda c: int(y_v1.loc[c]) if c in y_v1.index and pd.notna(y_v1.loc[c]) else -1
    )
    ranked.to_csv(RANKINGS_DIR / "ml_ranked_output.csv", index=False)
    print(f"  {len(ranked)} rows written -> {RANKINGS_DIR / 'ml_ranked_output.csv'}")

    # ── Feature importance ────────────────────────────────────────────────
    imp = pd.DataFrame({
        "feature": feat_names,
        "gain":    model.feature_importances_,
    }).sort_values("gain", ascending=False)
    imp.to_csv(RANKINGS_DIR / "ml_feature_importance.csv", index=False)
    print(f"\nTop 12 by gain:")
    print(imp.head(12).to_string(index=False))

    return {
        "regression": {"RMSE": rmse, "MAE": mae, "R2": r2, "Spearman_test": rho_test},
        "ranking_full": {
            "Spearman_behavioral": rho_full_behav,
            "Spearman_composite":  rho_full_comp,
            "Top50_overlap":       top50_overlap,
            "Top100_overlap":      top100_overlap,
        },
        "feature_count": X.shape[1],
        "n_train": 2500 - len(X_test), "n_test": len(X_test),
    }


if __name__ == "__main__":
    main()
