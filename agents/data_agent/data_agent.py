"""
Data agent — deterministic ingestion + optional LLM quality assessment.

Ingests the source xlsx, validates schema and rail coherence, writes
parquet artifacts plus a data-quality report. When use_llm=True, an LLM
reviews the quality report and adds risk-concentration observations.
"""

import sys
import json
from pathlib import Path
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from shared import RunContext, save_json, now_iso, llm_available, call_anthropic

PROMPT_FILE = Path(__file__).parent / "prompt.md"

DATA_FILE = Path(__file__).resolve().parents[2] / "data" / "AML Case Cloudwalk INC (2).xlsx"

REQUIRED_TXS_COLS = [
    "transaction_id", "timestamp", "transaction_type", "sender_id",
    "sender_entity_type", "receiver_id", "receiver_entity_type",
    "amount_brl", "status", "pix_flow", "card_present", "auth_3ds",
    "mcc", "geo_country", "country_risk_geo", "ip_proxy_vpn_tor",
    "device_fingerprint", "ip_address", "device_rooted", "cross_border",
    "sanctions_screening_hit",
]
REQUIRED_KYC_COLS = [
    "customer_id", "annual_income_brl", "declared_occupation",
    "risk_rating", "pep", "kyc_tier", "kyc_risk_score",
    "sanctions_list_hit", "date_of_birth",
]
REQUIRED_MER_COLS = [
    "merchant_id", "mcc", "owner_customer_id",
    "merchant_chargeback_ratio_90d", "mcc_risk",
]


def _validate_columns(df, required, sheet):
    missing = [c for c in required if c not in df.columns]
    return {"sheet": sheet, "missing_columns": missing,
            "row_count": len(df), "column_count": df.shape[1]}


def _rail_coherence(txs):
    """Check rail-specific fields are populated where expected."""
    pix = txs[txs.transaction_type == "PIX"]
    card = txs[txs.transaction_type == "Card"]
    return {
        "pix_total": len(pix),
        "pix_with_flow": int(pix.pix_flow.notna().sum()),
        "pix_flow_coverage_pct": round(100 * pix.pix_flow.notna().mean(), 2) if len(pix) else 0,
        "card_total": len(card),
        "card_with_present_flag": int(card.card_present.notna().sum()),
        "card_present_coverage_pct": round(100 * card.card_present.notna().mean(), 2) if len(card) else 0,
    }


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


def _llm_assessment(quality, summary, run_id):
    """LLM reviews quality report and adds risk-concentration observations."""
    prompt = PROMPT_FILE.read_text()
    parts = prompt.split("## User", 1)
    system = parts[0].replace("## System", "").strip()
    user = parts[1].strip() if len(parts) > 1 else ""
    # Pass only the summary (not the full quality report) to keep tokens manageable
    user = (user.replace("{run_id}", run_id)
                .replace("{quality_json}", json.dumps({
                    "validation": quality["validation"],
                    "rail_coherence": quality["rail_coherence"],
                    "distinct_counts": quality["distinct_counts"],
                }, indent=2, default=str))
                .replace("{summary_json}", json.dumps(summary, indent=2, default=str)))
    raw = call_anthropic(system, user, max_tokens=1200)
    return _parse_llm_json(raw)


def run(ctx: RunContext, data_file=DATA_FILE, use_llm=False):
    ctx.log("data_agent", "start", source=str(data_file), use_llm=use_llm)

    xl = pd.ExcelFile(data_file)
    txs = xl.parse("Transactions")
    kyc = xl.parse("KYC_Profiles")
    mer = xl.parse("Merchants")

    quality = {
        "run_id": ctx.run_id,
        "generated_at": now_iso(),
        "source_file": str(data_file),
        "validation": {
            "transactions": _validate_columns(txs, REQUIRED_TXS_COLS, "Transactions"),
            "kyc":          _validate_columns(kyc, REQUIRED_KYC_COLS, "KYC_Profiles"),
            "merchants":    _validate_columns(mer, REQUIRED_MER_COLS, "Merchants"),
        },
        "rail_coherence": _rail_coherence(txs),
        "missing_summary": {
            "transactions_null_per_col": {c: int(txs[c].isna().sum())
                                          for c in REQUIRED_TXS_COLS if c in txs.columns
                                          and txs[c].isna().any()},
        },
        "distinct_counts": {
            "customers": int(kyc.customer_id.nunique()),
            "merchants": int(mer.merchant_id.nunique()),
            "transactions": int(txs.transaction_id.nunique()),
        },
    }

    # Light enrichment — flag transactions touching high-risk geo / anonymization
    txs = txs.copy()
    txs["enrich_high_risk_geo"] = (txs.country_risk_geo == "High").astype(int)
    txs["enrich_anonymized"]    = txs.ip_proxy_vpn_tor.isin(["Tor", "VPN", "Proxy"]).astype(int)

    # Write parquet artifacts
    txs_path = ctx.artifact("processed_transactions.parquet")
    kyc_path = ctx.artifact("processed_customers.parquet")
    txs.to_parquet(txs_path, index=False)
    kyc.to_parquet(kyc_path, index=False)

    save_json(ctx.artifact("data_quality_report.json"), quality)

    # LLM assessment — enriches quality report with risk-concentration observations
    backend = "anthropic" if (use_llm and llm_available()) else "template"
    ctx.log("data_agent", "backend_selected", backend=backend)

    summary = {
        "pep_count": int((kyc.pep == "Yes").sum()),
        "pep_pct": round(100 * (kyc.pep == "Yes").mean(), 2),
        "sanctions_list_hits": int((kyc.sanctions_list_hit == "Yes").sum()),
        "tx_sanctions_hits": int((txs.sanctions_screening_hit == "Yes").sum()),
        "anonymized_tx_count": int(txs.ip_proxy_vpn_tor.isin(["Tor", "VPN", "Proxy"]).sum()),
        "anonymized_tx_pct": round(100 * txs.ip_proxy_vpn_tor.isin(["Tor", "VPN", "Proxy"]).mean(), 2),
        "high_risk_geo_tx_count": int((txs.country_risk_geo == "High").sum()),
        "cross_border_tx_count": int((txs.cross_border == "Yes").sum()),
        "kyc_risk_score_p90": float(kyc.kyc_risk_score.quantile(0.9)),
        "kyc_risk_score_mean": float(kyc.kyc_risk_score.mean().round(1)),
        "distinct_device_fingerprints": int(txs.device_fingerprint.nunique()),
        "rooted_device_tx_count": int((txs.device_rooted == "Yes").sum()),
    }

    if backend == "anthropic":
        llm_assessment = _llm_assessment(quality, summary, ctx.run_id)
        llm_assessment["_backend"] = "anthropic"
    else:
        llm_assessment = {
            "data_readiness": "ready",
            "schema_findings": [f"missing columns: {v['missing_columns']}" for v in quality["validation"].values() if v["missing_columns"]],
            "risk_concentration_observations": [
                f"{summary['pep_pct']}% of customers flagged PEP ({summary['pep_count']} total)",
                f"{summary['anonymized_tx_pct']}% of transactions use anonymization (Tor/VPN/Proxy)",
                f"{summary['tx_sanctions_hits']} transactions with sanctions screening hits",
            ],
            "rail_coherence_findings": [
                f"PIX pix_flow coverage: {quality['rail_coherence']['pix_flow_coverage_pct']}%",
                f"Card card_present coverage: {quality['rail_coherence']['card_present_coverage_pct']}%",
            ],
            "enrichment_applied": [
                "enrich_high_risk_geo added (country_risk_geo == High)",
                "enrich_anonymized added (Tor/VPN/Proxy ip_proxy_vpn_tor)",
            ],
            "recommendations": [],
            "_backend": "template",
        }

    quality["llm_assessment"] = llm_assessment
    save_json(ctx.artifact("data_quality_report.json"), quality)

    ctx.log("data_agent", "complete",
            transactions=len(txs), customers=len(kyc), merchants=len(mer),
            backend=backend,
            artifacts=["processed_transactions.parquet",
                       "processed_customers.parquet",
                       "data_quality_report.json"])

    return {"txs_path": str(txs_path), "kyc_path": str(kyc_path),
            "quality": quality}


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-id", default=None)
    ap.add_argument("--use-llm", action="store_true")
    args = ap.parse_args()
    ctx = RunContext(run_id=args.run_id)
    out = run(ctx, use_llm=args.use_llm)
    print(f"OK — {out['quality']['distinct_counts']}")
