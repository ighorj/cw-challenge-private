"""
Isolation Forest anomaly detector — Phase 3 supplementary model.

Trained exclusively on raw transaction features; no labels, no scores,
no output from the rules engine. Provides an independent unsupervised
signal to cross-validate XGBoost priority rankings.

Features (transaction-level, aggregated per customer):
    amount_brl              — transaction amount
    tx_hour                 — hour of day (0–23)
    mcc_risk_enc            — MCC risk: Low=0, Medium=1, High=2
    country_risk_geo_enc    — geo risk: Low=0, Medium=1, High=2
    device_rooted_enc       — device_rooted: No=0, Yes=1
    anon_enc                — ip_proxy_vpn_tor: None=0, VPN/Proxy=1, Tor=2
    tx_type_enc             — transaction_type: PIX=0, Card=1, Wire=2
    card_present_enc        — card_present: Yes=0, No=1 (NaN→0)
    auth_3ds_enc            — auth_3ds: Yes=0, No=1 (NaN→0)

Aggregation: mean per customer (captures typical behaviour profile).
Anomaly score is inverted so higher → more anomalous.
Output saved to outputs/rankings/isolation_forest_scores.csv.
"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src" / "rules"))

import alerts_engine as ae

RANDOM_STATE = 42
OUTPUT_FILE  = ROOT / "outputs" / "rankings" / "isolation_forest_scores.csv"


def build_tx_features(txs: pd.DataFrame, mer: pd.DataFrame) -> pd.DataFrame:
    """Encode raw transaction features; return transaction-level DataFrame."""
    cust = txs[txs.sender_entity_type == "customer"].copy()
    cust["timestamp"] = pd.to_datetime(cust.timestamp)

    # amount and hour
    cust["tx_hour"] = cust.timestamp.dt.hour

    # MCC risk from merchant table
    mer_idx = mer.set_index("merchant_id")["mcc_risk"]
    mcc_risk_map = {"Low": 0, "Medium": 1, "High": 2}
    cust["mcc_risk_enc"] = cust.receiver_id.map(mer_idx).map(mcc_risk_map).fillna(0)

    # Geo country risk
    geo_map = {"Low": 0, "Medium": 1, "High": 2}
    cust["country_risk_geo_enc"] = cust.country_risk_geo.map(geo_map).fillna(0)

    # Device rooted
    cust["device_rooted_enc"] = (cust.device_rooted == "Yes").astype(int)

    # Anonymization (None=0, VPN/Proxy=1, Tor=2)
    anon_map = {"VPN": 1, "Proxy": 1, "Tor": 2}
    cust["anon_enc"] = cust.ip_proxy_vpn_tor.map(anon_map).fillna(0)

    # Transaction type
    tx_type_map = {"PIX": 0, "Card": 1, "Wire": 2}
    cust["tx_type_enc"] = cust.transaction_type.map(tx_type_map).fillna(0)

    # Card present (NaN → 0)
    cust["card_present_enc"] = cust.card_present.map({"Yes": 0, "No": 1}).fillna(0)

    # 3DS (NaN → 0)
    cust["auth_3ds_enc"] = cust.auth_3ds.map({"Yes": 0, "No": 1}).fillna(0)

    return cust[
        ["sender_id", "amount_brl", "tx_hour",
         "mcc_risk_enc", "country_risk_geo_enc", "device_rooted_enc",
         "anon_enc", "tx_type_enc", "card_present_enc", "auth_3ds_enc"]
    ]


def build_customer_features(tx_feat: pd.DataFrame) -> pd.DataFrame:
    """Aggregate transaction-level features to customer means."""
    return tx_feat.groupby("sender_id").mean()


def run(txs: pd.DataFrame, mer: pd.DataFrame) -> pd.DataFrame:
    """Fit Isolation Forest and return per-customer anomaly scores."""
    tx_feat   = build_tx_features(txs, mer)
    X         = build_customer_features(tx_feat).astype(float)

    clf = IsolationForest(
        n_estimators=200,
        max_samples="auto",
        contamination=0.05,
        random_state=RANDOM_STATE,
        n_jobs=-1,
    )
    clf.fit(X)

    # score_samples returns negative average depth: more negative = more anomalous.
    # Invert sign so higher score = more anomalous.
    raw_scores = clf.score_samples(X)
    anomaly_score = -raw_scores        # higher → more anomalous
    is_anomaly    = clf.predict(X)     # -1 = anomaly, 1 = normal

    out = pd.DataFrame({
        "customer_id":    X.index,
        "anomaly_score":  anomaly_score.round(6),
        "is_anomaly":     (is_anomaly == -1),
    }).sort_values("anomaly_score", ascending=False).reset_index(drop=True)

    out["rank"] = range(1, len(out) + 1)
    return out, X


def main():
    print("Loading data…")
    txs, kyc, mer = ae.load_data()

    print("Building features and fitting Isolation Forest…")
    scores, X = run(txs, mer)

    scores.to_csv(OUTPUT_FILE, index=False)
    print(f"Saved {len(scores)} rows → {OUTPUT_FILE}")
    print(f"\nTop 20 most anomalous customers:")
    print(scores.head(20).to_string(index=False))


if __name__ == "__main__":
    main()
