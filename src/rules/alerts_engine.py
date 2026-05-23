"""
AML alerts engine — Phase 2 artifact.

Loads the CloudWalk dataset, applies 21 calibrated AML rules,
computes composite scores per customer, assigns escalation bands,
and writes results to alerts_output.csv.

Architecture:
    Tier A  — Hard alerts (immediate SAR, bypass scoring)
    Tier B  — Score contributors (HIGH=3, MEDIUM=2, LOW=1)
    Tier C  — Amplifiers (+1, only count if >=1 Tier-B fires)
"""

import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA_FILE = ROOT / "data" / "AML Case Cloudwalk INC (2).xlsx"
OUTPUT_FILE = ROOT / "outputs" / "rankings" / "alerts_output.csv"


def load_data(path=DATA_FILE):
    xl = pd.ExcelFile(path)
    txs = xl.parse("Transactions")
    kyc = xl.parse("KYC_Profiles")
    mer = xl.parse("Merchants")
    return txs, kyc, mer


def run_rules(txs, kyc, mer):
    """Apply all rules and return list of (rule_id, tier, weight, customers)."""
    cust = txs[txs.sender_entity_type == "customer"].copy()
    cust["day"] = pd.to_datetime(cust.timestamp).dt.date

    fires = []

    # ── Tier A — Hard alerts ──────────────────────────────────────────────

    # R08 SANCTIONS-HIT
    sanc = set(kyc.loc[kyc.sanctions_list_hit == "Yes", "customer_id"])
    sanc |= set(txs.loc[txs.sanctions_screening_hit == "Yes", "sender_id"])
    sanc &= set(cust.sender_id)
    fires.append(("R08", "A", 0, sanc))

    # R16 SELF-MERCHANT
    owners = mer.set_index("merchant_id")["owner_customer_id"].dropna()
    c2m = cust[cust.receiver_entity_type == "merchant"].copy()
    c2m["owner"] = c2m.receiver_id.map(owners)
    self_mer = set(c2m.loc[c2m.sender_id == c2m.owner, "sender_id"])
    fires.append(("R16", "A", 0, self_mer))

    # ── Tier B — Score contributors ───────────────────────────────────────

    # R01 VEL-BURST
    daily = cust.groupby(["sender_id", "day"]).size()
    fires.append(("R01", "B", 3,
                  set(daily[daily >= 4].index.get_level_values(0).unique())))

    # R02 STRUCT-BAND
    band = cust[(cust.amount_brl >= 9000) & (cust.amount_brl < 10000)]
    s = band.groupby("sender_id").size()
    fires.append(("R02_HIGH", "B", 3, set(s[s >= 3].index)))
    fires.append(("R02_LOW",  "B", 1, set(s[(s >= 1) & (s < 3)].index)))

    # R03 INCOME-MISMATCH
    outflow = cust.groupby("sender_id")["amount_brl"].sum()
    monthly = kyc.set_index("customer_id")["annual_income_brl"] / 12
    ratio = (outflow / monthly).dropna()
    fires.append(("R03_HIGH", "B", 3, set(ratio[ratio >= 100].index)))
    fires.append(("R03_LOW",  "B", 1, set(ratio[(ratio >= 50) & (ratio < 100)].index)))

    # R04 PASSTHRU
    pix_out = (txs[(txs.pix_flow == "cash_out") &
                   (txs.sender_entity_type == "customer")]
                  .groupby("sender_id")["amount_brl"].sum())
    pix_in = (txs[txs.pix_flow == "cash_in"]
                 .groupby("receiver_id")["amount_brl"].sum())
    pass_ratio = (pix_out / pix_in.reindex(pix_out.index)).replace([float("inf")], 1e9)
    fires.append(("R04", "B", 3,
                  set(pix_out[(pass_ratio > 2.0) & (pix_out >= 20_000)].index)))

    # R05 ANON-IP (Tor takes precedence over VPN/Proxy for weight purposes)
    anon = cust[cust.ip_proxy_vpn_tor.isin(["Tor", "VPN", "Proxy"])]
    tor_users = set(anon.loc[anon.ip_proxy_vpn_tor == "Tor", "sender_id"])
    vpn = anon[anon.ip_proxy_vpn_tor.isin(["VPN", "Proxy"])].groupby("sender_id").size()
    vpn_users = set(vpn[vpn >= 2].index) - tor_users
    fires.append(("R05_TOR", "B", 3, tor_users))
    fires.append(("R05_VPN", "B", 2, vpn_users))

    # R06 GEO-HIGH-RISK
    hr_geo = cust[cust.country_risk_geo == "High"]
    geo_vol = set(hr_geo.loc[hr_geo.amount_brl >= 5000, "sender_id"])
    geo_rec = hr_geo.groupby("sender_id").size()
    fires.append(("R06", "B", 2, geo_vol | set(geo_rec[geo_rec >= 2].index)))

    # R07 GEO-IP-MISMATCH
    mm = cust[cust.ip_country.notna() & cust.sender_country.notna() &
              (cust.ip_country != cust.sender_country)]
    mmc = mm.groupby("sender_id").size()
    fires.append(("R07", "B", 2, set(mmc[mmc >= 2].index)))

    # R09 PEP-EDD
    fires.append(("R09", "B", 3, set(kyc.loc[kyc.pep == "Yes", "customer_id"])))

    # R11 MCC-HIGH-RISK
    hr_mer = set(mer.loc[mer.mcc_risk == "High", "merchant_id"])
    mcc_c = cust[cust.receiver_id.isin(hr_mer)].groupby("sender_id").size()
    fires.append(("R11", "B", 2, set(mcc_c[mcc_c >= 3].index)))

    # R14 ROOTED-DEVICE
    root_c = cust[cust.device_rooted == "Yes"].groupby("sender_id").size()
    fires.append(("R14", "B", 2, set(root_c[root_c >= 3].index)))

    # R15 FAN-OUT
    fan = cust.groupby("sender_id")["receiver_id"].nunique()
    fires.append(("R15", "B", 2, set(fan[fan >= 25].index)))

    # R18 CARD-NO-3DS
    cnp = cust[(cust.transaction_type == "Card") &
               (cust.card_present == "No") &
               (cust.auth_3ds != "Yes") &
               (cust.amount_brl >= 2000)]
    cnp_c = cnp.groupby("sender_id").size()
    fires.append(("R18", "B", 1, set(cnp_c[cnp_c >= 3].index)))

    # R19 CHARGEBACK-MERCHANT
    hr_cb = set(mer.loc[mer.merchant_chargeback_ratio_90d >= 0.10, "merchant_id"])
    cb_c = cust[cust.receiver_id.isin(hr_cb)].groupby("sender_id").size()
    cb_rec = set(cb_c[cb_c >= 3].index)
    own_cb = set(cust.loc[cust.status == "Chargeback", "sender_id"])
    fires.append(("R19", "B", 2, cb_rec | own_cb))

    # ── Tier C — Amplifiers ───────────────────────────────────────────────

    # R10 KYC-INCONSISTENCY
    i1 = (kyc.pep == "Yes") & (kyc.risk_rating.isin(["Low", "Medium"]))
    i2 = (kyc.kyc_risk_score >= 80) & (kyc.risk_rating == "Low")
    i3 = (kyc.pep == "Yes") & (kyc.kyc_tier == "L1")
    fires.append(("R10", "C", 1, set(kyc.loc[i1 | i2 | i3, "customer_id"])))

    # R17 MULTI-RAIL
    rails = cust.groupby("sender_id")["transaction_type"].nunique()
    fires.append(("R17", "C", 1, set(rails[rails >= 3].index)))

    # R12 DEVICE-REUSE (expected empty on this dataset)
    dev = cust.dropna(subset=["device_fingerprint"]).groupby("device_fingerprint")["sender_id"].nunique()
    shared_dev = dev[dev >= 2].index
    fires.append(("R12", "C", 1,
                  set(cust.loc[cust.device_fingerprint.isin(shared_dev), "sender_id"])))

    # R13 IP-REUSE (expected empty on this dataset)
    ip = cust.dropna(subset=["ip_address"]).groupby("ip_address")["sender_id"].nunique()
    shared_ip = ip[ip >= 2].index
    fires.append(("R13", "C", 1,
                  set(cust.loc[cust.ip_address.isin(shared_ip), "sender_id"])))

    # ── Cohort-dependent rules ────────────────────────────────────────────
    # Two cohort tiers — wider one for merchant convergence, tighter for
    # network linkage. Loose cohorts cascade across the population given
    # this dataset's structurally elevated income-to-volume baseline.

    interim = {}
    for rid, tier, w, cids in fires:
        for cid in cids:
            e = interim.setdefault(cid, {"score": 0, "hard": False})
            if tier == "A":
                e["hard"] = True
            elif tier in ("B", "C"):
                e["score"] += w
    cohort_t2 = {cid for cid, e in interim.items() if e["hard"] or e["score"] >= 6}
    cohort_t1 = {cid for cid, e in interim.items() if e["hard"] or e["score"] >= 10}

    # R20 MERCHANT-CONVERGENCE — uses wider cohort (Tier 2+)
    flagged_tx = cust[cust.sender_id.isin(cohort_t2) &
                      (cust.receiver_entity_type == "merchant")]
    conv = flagged_tx.groupby("receiver_id")["sender_id"].nunique()
    conv_mers = set(conv[conv >= 2].index)
    conv_senders = set(flagged_tx.loc[flagged_tx.receiver_id.isin(conv_mers), "sender_id"])
    fires.append(("R20", "C", 1, conv_senders))

    # R21 NETWORK-LINK — Wire transfers only, both ends in Tier 1 cohort.
    # Restricting to the Wire rail matches Phase 1's confirmed finding
    # (C101848 → C102360) and avoids cascading across high-volume PIX C2C.
    c2c_wire = txs[(txs.sender_entity_type == "customer") &
                   (txs.receiver_entity_type == "customer") &
                   (txs.transaction_type == "Wire")]
    links = c2c_wire[c2c_wire.sender_id.isin(cohort_t1) &
                     c2c_wire.receiver_id.isin(cohort_t1)]
    fires.append(("R21", "A", 0, set(links.sender_id) | set(links.receiver_id)))

    return fires


def score(fires):
    """Aggregate fires into per-customer scores and rule lists."""
    base = set()
    for _, tier, _, cids in fires:
        if tier in ("A", "B"):
            base |= cids

    per = {}
    for rid, tier, w, cids in fires:
        for cid in cids:
            entry = per.setdefault(cid, {"rules": [], "score": 0, "hard": False})
            entry["rules"].append(rid)
            if tier == "A":
                entry["hard"] = True
            elif tier == "B":
                entry["score"] += w
            elif tier == "C" and cid in base:
                entry["score"] += w
    return per


def assign_band(entry):
    if entry["hard"]:
        return "Tier 1 — Hard alert"
    s = entry["score"]
    if s >= 10:
        return "Tier 1 — SAR immediate"
    if s >= 6:
        return "Tier 2 — SAR standard window"
    if s >= 3:
        return "Tier 3 — Enhanced monitoring"
    return "Routine"


def main():
    txs, kyc, mer = load_data()
    fires = run_rules(txs, kyc, mer)
    per = score(fires)

    rows = [{
        "customer_id": cid,
        "triggered_rules": "|".join(sorted(set(e["rules"]))),
        "total_score": e["score"],
        "escalation_band": assign_band(e),
        "hard_alert_flag": e["hard"],
    } for cid, e in per.items()]

    df = (pd.DataFrame(rows)
            .sort_values(by=["total_score", "hard_alert_flag"],
                         ascending=[False, False])
            .reset_index(drop=True))

    df.to_csv(OUTPUT_FILE, index=False)
    print(f"Wrote {len(df)} alerts -> {OUTPUT_FILE}\n")

    print("Escalation band counts:")
    print(df["escalation_band"].value_counts().to_string(), "\n")

    print("Top 15 by score:")
    print(df.head(15).to_string(index=False))


if __name__ == "__main__":
    main()
