"""
Investigation agent — LLM-augmented with deterministic template fallback.

For each customer in the prioritized queue, build an evidence bundle from the
raw artifacts (no fabrication), call the LLM backend (or template) to produce
the investigation case JSON, then emit the case + a human-readable summary.
"""

import sys
from pathlib import Path
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from shared import RunContext, save_json, load_json, llm_available, call_anthropic, now_iso, soften_language, ml_confidence_band
from aml_constants import RULE_DESCRIPTIONS, sanctions_status

ROOT = Path(__file__).resolve().parents[2]
PROMPT_FILE = Path(__file__).parent / "prompt.md"

# MCCs that materially elevate transaction risk
HIGH_RISK_MCC = {"6011", "6211", "4829", "7995", "6051", "4111", "4900", "5199"}

# Map rule IDs (Phase 2) to AML typologies for narrative grouping
RULE_TO_TYPOLOGY = {
    "R01": "velocity-burst", "R02_HIGH": "structuring", "R02_LOW": "structuring",
    "R03_HIGH": "income-mismatch", "R03_LOW": "income-mismatch",
    "R04": "passthrough", "R05_TOR": "anonymization", "R05_VPN": "anonymization",
    "R06": "high-risk-geo", "R07": "geo-ip-mismatch", "R08": "sanctions",
    "R09": "PEP-EDD", "R10": "KYC-inconsistency", "R11": "high-MCC",
    "R12": "device-reuse", "R13": "ip-reuse", "R14": "rooted-device",
    "R15": "fan-out", "R16": "self-merchant", "R17": "multi-rail",
    "R18": "card-no-3DS", "R19": "chargeback-merchant",
    "R20": "merchant-convergence", "R21": "network-linkage",
}


def _tx_typology_tag(row):
    """Primary evidential typology label for a transaction row."""
    ip = row.get("ip_proxy_vpn_tor")
    if ip is not None and not (isinstance(ip, float) and pd.isna(ip)):
        if str(ip) == "Tor":
            return "anonymization_tor"
        if str(ip) in ("VPN", "Proxy"):
            return "anonymization_vpn"
    if str(row.get("sanctions_screening_hit", "No")) == "Yes":
        return "sanctions_screen"
    if str(row.get("transaction_type", "")) == "Wire":
        return "wire"
    geo = str(row.get("geo_country", "BR"))
    if str(row.get("cross_border", "No")) == "Yes" or geo not in ("BR", "nan", ""):
        return "cross_border"
    if str(row.get("device_rooted", "No")) == "Yes":
        return "rooted_device"
    if str(row.get("mcc", "")) in HIGH_RISK_MCC:
        return "high_risk_mcc"
    return "high_value"


def timeline_event_score(row, amount_rank, burst_count, is_first_of_type):
    """
    Score a transaction by evidential weight for timeline selection.
    Higher score = more important to surface in the investigation timeline.
    """
    score = 0.0
    ip = row.get("ip_proxy_vpn_tor")
    ip_str = str(ip) if (ip is not None and not (isinstance(ip, float) and pd.isna(ip))) else None

    if ip_str == "Tor":
        score += 20
    elif ip_str in ("VPN", "Proxy"):
        score += 12

    if str(row.get("sanctions_screening_hit", "No")) == "Yes":
        score += 18

    rail = str(row.get("transaction_type", ""))
    if rail == "Wire":
        score += 12
    elif rail == "Card":
        score += 2

    geo = str(row.get("geo_country", "BR"))
    if str(row.get("cross_border", "No")) == "Yes" or geo not in ("BR", "nan", ""):
        score += 10

    if burst_count >= 4:
        score += 14
    elif burst_count >= 3:
        score += 7

    if str(row.get("mcc", "")) in HIGH_RISK_MCC:
        score += 8

    if str(row.get("device_rooted", "No")) == "Yes":
        score += 5

    # Amount rank bonus: rank 1 = +13.5, rank 10 = +0
    score += max(0.0, (10 - amount_rank) * 1.5)

    # Milestone bonus: first occurrence of this typology in the customer's history
    if is_first_of_type:
        score += 8

    return score


def select_evidential_transactions(cust_txs, triggered_rules, daily_counts, max_txs=8):
    """
    Evidence-weighted, typology-diverse transaction selection.

    Replaces naive top-N-by-amount selection. Prioritises anonymization,
    sanctions hits, Wire, cross-border, velocity burst days, high-risk MCC,
    and first-occurrence milestones. Enforces a diversity cap so no single
    typology dominates the timeline.
    """
    if len(cust_txs) == 0:
        return cust_txs.copy()

    txs = cust_txs.sort_values("timestamp").reset_index(drop=True)

    # Amount rank map (1 = largest)
    amount_ranks = {
        row.transaction_id: rank
        for rank, (_, row) in enumerate(txs.nlargest(len(txs), "amount_brl").iterrows(), 1)
    }

    # Score each transaction, tracking first-of-typology milestones chronologically
    first_seen: set = set()
    scored = []
    for _, row in txs.iterrows():
        tag = _tx_typology_tag(row)
        is_first = tag not in first_seen
        first_seen.add(tag)
        day = pd.to_datetime(row.timestamp).date()
        score = timeline_event_score(
            row,
            amount_rank=amount_ranks.get(row.transaction_id, 99),
            burst_count=daily_counts.get(day, 1),
            is_first_of_type=is_first,
        )
        scored.append((score, tag, row))

    # Greedy diversity-constrained selection
    scored.sort(key=lambda x: -x[0])
    MAX_PER_TYPOLOGY = 2
    typology_counts: dict = {}
    selected = []

    for score, tag, row in scored:
        if len(selected) >= max_txs:
            break
        count = typology_counts.get(tag, 0)
        # Allow max 2 per typology; relax only if < 4 selected total
        if count >= MAX_PER_TYPOLOGY and len(selected) >= 4:
            continue
        selected.append(row)
        typology_counts[tag] = count + 1

    if not selected:
        return txs.head(max_txs)

    sel_ids = {r.transaction_id for r in selected}
    return txs[txs.transaction_id.isin(sel_ids)].sort_values("timestamp")


def _timeline_event_desc(tx):
    """Narrative-rich event description for a key_transactions dict entry."""
    desc = f"{tx['rail']} R${tx['amount_brl']:,.0f} → {tx['counterparty']}"
    ctx = []
    if tx.get("ip_anon"):
        ctx.append(f"via {tx['ip_anon']}")
    if tx.get("burst_day"):
        ctx.append("velocity burst")
    geo = str(tx.get("geo_country", "BR"))
    if geo not in ("BR", "None", "nan", ""):
        ctx.append(f"geo: {geo}")
    if tx.get("sanctions_hit"):
        ctx.append("sanctions screening event")
    mcc = str(tx.get("mcc", ""))
    if mcc in HIGH_RISK_MCC:
        ctx.append(f"MCC {mcc}")
    if tx.get("typology_tag") == "rooted_device":
        ctx.append("rooted device")
    if ctx:
        desc += f" ({'; '.join(ctx)})"
    return desc


def build_evidence_bundle(customer, txs, kyc, ml_df, alerts):
    """Gather everything we know about the customer into one JSON-serializable dict."""
    cid = customer["customer_id"]
    kyc_row = kyc[kyc.customer_id == cid].iloc[0].to_dict() if (kyc.customer_id == cid).any() else {}
    cust_txs = txs[txs.sender_id == cid].copy().sort_values("timestamp")
    received = txs[txs.receiver_id == cid].copy()
    ml_row = ml_df[ml_df.customer_id == cid].iloc[0].to_dict() if (ml_df.customer_id == cid).any() else {}

    # Anonymization breakdown
    anon = cust_txs[cust_txs.ip_proxy_vpn_tor.isin(["Tor", "VPN", "Proxy"])]
    anon_breakdown = anon.ip_proxy_vpn_tor.value_counts().to_dict() if len(anon) else {}

    # PIX flows
    pix_out = cust_txs[(cust_txs.transaction_type == "PIX") & (cust_txs.pix_flow == "cash_out")].amount_brl.sum()
    pix_in  = received[received.pix_flow == "cash_in"].amount_brl.sum()

    # Single-day bursts
    cust_txs["day"] = pd.to_datetime(cust_txs.timestamp).dt.date
    daily = cust_txs.groupby("day").size()
    bursts = [{"date": str(d), "tx_count": int(c),
               "day_total_brl": float(cust_txs[cust_txs.day == d].amount_brl.sum())}
              for d, c in daily.items() if c >= 3]

    # Evidence-weighted key transaction selection (replaces naive top-5-by-amount)
    daily_dict = daily.to_dict()
    key_txs = select_evidential_transactions(
        cust_txs, customer.get("triggered_rules", []), daily_dict)
    key_txs_out = [{
        "tx_id": r.transaction_id,
        "timestamp": str(r.timestamp),
        "rail": r.transaction_type,
        "amount_brl": float(r.amount_brl),
        "counterparty": r.receiver_id,
        "geo_country": r.geo_country,
        "ip_anon": (str(r.ip_proxy_vpn_tor) if pd.notna(r.ip_proxy_vpn_tor) else None),
        "mcc": (int(r.mcc) if pd.notna(r.mcc) else None),
        "typology_tag": _tx_typology_tag(r),
        "burst_day": daily_dict.get(pd.to_datetime(r.timestamp).date(), 1) >= 3,
        "sanctions_hit": str(r.sanctions_screening_hit) == "Yes" if "sanctions_screening_hit" in r.index else False,
    } for _, r in key_txs.iterrows()]

    return {
        "customer_id": cid,
        "severity": customer.get("severity", "unknown"),
        "priority_score": customer.get("priority_score"),
        "typology_families": customer.get("typology_families", []),
        "kyc": {
            "annual_income_brl": float(kyc_row.get("annual_income_brl", 0)),
            "declared_occupation": kyc_row.get("declared_occupation"),
            "pep": kyc_row.get("pep"),
            "kyc_tier": kyc_row.get("kyc_tier"),
            "kyc_risk_score": int(kyc_row.get("kyc_risk_score", 0)),
            "risk_rating": kyc_row.get("risk_rating"),
            "sanctions_list_hit": kyc_row.get("sanctions_list_hit"),
            "sanctions_status": sanctions_status(
                kyc_row.get("sanctions_list_hit"),
                int((cust_txs.sanctions_screening_hit == "Yes").sum()) if "sanctions_screening_hit" in cust_txs.columns else 0,
            ),
            "ml_confidence_band": ml_confidence_band(float(ml_row.get("predicted_probability", 0.0))),
        },
        "detection_signals": {
            "rules_score": customer["rules_score"],
            "ml_probability": customer["ml_probability"],
            "escalation_band": customer["escalation_band"],
            "ml_band": customer["ml_band"],
            "hard_alert": customer["hard_alert"],
            "triggered_rules": customer["triggered_rules"],
            "shap_drivers": [],  # populated by orchestrator if available
        },
        "aggregate_behavior": {
            "tx_count": int(len(cust_txs)),
            "total_outflow_brl": float(cust_txs.amount_brl.sum()),
            "distinct_counterparties": int(cust_txs.receiver_id.nunique()),
            "pix_outflow_brl": float(pix_out),
            "pix_inflow_brl": float(pix_in),
            "passthrough_ratio_pct": (round(100 * pix_out / pix_in, 1) if pix_in else None),
            "anonymization_events": anon_breakdown,
            "cross_border_events": int((cust_txs.cross_border == "Yes").sum()),
            "wire_count": int((cust_txs.transaction_type == "Wire").sum()),
        },
        "single_day_bursts": bursts,
        "key_transactions": key_txs_out,
    }


def _template_case(bundle):
    """Deterministic fallback when LLM is not used. Output schema identical."""
    cid = bundle["customer_id"]
    kyc = bundle["kyc"]
    agg = bundle["aggregate_behavior"]
    rules = bundle["detection_signals"]["triggered_rules"]
    typologies = sorted({RULE_TO_TYPOLOGY[r] for r in rules if r in RULE_TO_TYPOLOGY})

    monthly_income = kyc["annual_income_brl"] / 12 if kyc["annual_income_brl"] else None
    income_mult = (agg["total_outflow_brl"] / monthly_income) if monthly_income else None

    summary_parts = []
    if kyc.get("pep") == "Yes":
        summary_parts.append(f"PEP-flagged customer (KYC risk score {kyc['kyc_risk_score']}/100)")
    else:
        summary_parts.append(f"Customer with KYC risk score {kyc['kyc_risk_score']}/100")
    if income_mult:
        summary_parts.append(
            f"declared income R${kyc['annual_income_brl']:,.0f}/yr versus "
            f"R${agg['total_outflow_brl']:,.0f} in {agg['tx_count']} outflows "
            f"(≈{income_mult:.0f}× declared monthly income)")
    if agg.get("passthrough_ratio_pct"):
        summary_parts.append(f"PIX passthrough ratio {agg['passthrough_ratio_pct']:.0f}%")
    if agg["anonymization_events"]:
        anon_str = ", ".join(f"{v} {k}" for k, v in agg["anonymization_events"].items())
        summary_parts.append(f"anonymization events ({anon_str})")
    summary = soften_language(". ".join(summary_parts) + ". Activity appears materially inconsistent with the declared customer profile.")

    key_facts = []
    if income_mult:
        key_facts.append(
            f"R${agg['total_outflow_brl']:,.0f} total outflow vs R${monthly_income:,.0f}/month declared income ({income_mult:.0f}×)")
    if agg.get("passthrough_ratio_pct") is not None:
        key_facts.append(
            f"PIX passthrough {agg['passthrough_ratio_pct']:.0f}% (R${agg['pix_outflow_brl']:,.0f} out / R${agg['pix_inflow_brl']:,.0f} in)")
    if agg["anonymization_events"]:
        key_facts.append(
            f"Anonymization breakdown: {agg['anonymization_events']}")
    for b in bundle["single_day_bursts"]:
        key_facts.append(f"Single-day burst {b['date']}: {b['tx_count']} txs / R${b['day_total_brl']:,.0f}")
    if kyc.get("pep") == "Yes" and kyc.get("risk_rating") in ("Low", "Medium"):
        key_facts.append(
            f"KYC inconsistency: PEP=Yes, score={kyc['kyc_risk_score']}, "
            f"risk_rating={kyc['risk_rating']}, tier={kyc['kyc_tier']}")

    entity_links = []
    for tx in bundle["key_transactions"][:5]:
        entity_links.append({
            "entity_type": "merchant" if str(tx["counterparty"]).startswith("M") else "customer",
            "entity_id": tx["counterparty"],
            "relationship": f"{tx['rail']} recipient of R${tx['amount_brl']:,.0f}"
                            + (f" via {tx['ip_anon']}" if tx["ip_anon"] else ""),
            "evidence": f"tx {tx['tx_id']} on {tx['timestamp'][:10]}",
        })

    timeline = sorted(
        [{"date": tx["timestamp"][:10],
          "event": _timeline_event_desc(tx),
          "source": f"tx {tx['tx_id']}"}
         for tx in bundle["key_transactions"]],
        key=lambda x: x["date"])

    severity = bundle.get("severity", "unknown")
    hard = bundle["detection_signals"]["hard_alert"]
    band = bundle["detection_signals"]["escalation_band"]
    if severity == "critical":
        next_step = "file_sar_immediate"
    elif severity == "high" or hard or band.startswith("Tier 1"):
        next_step = "file_sar_immediate"
    elif severity == "medium" or band.startswith("Tier 2"):
        next_step = "file_sar_standard_window"
    elif severity == "low" or band.startswith("Tier 3"):
        next_step = "enhanced_monitoring"
    else:
        next_step = "no_action"

    return {
        "customer_id": cid,
        "severity": severity,
        "summary": summary,
        "triggered_typologies": typologies,
        "key_facts": key_facts,
        "entity_links": entity_links,
        "timeline": timeline,
        "confidence": f"high — {len(rules)} concurrent rule fires; all facts traceable to transaction records",
        "recommended_next_step": next_step,
        "_backend": "template",
    }


def _llm_case(bundle, run_id):
    """LLM-backed implementation. Same schema, free-form narrative quality."""
    import json
    prompt = PROMPT_FILE.read_text()
    # Split system / user via the headers in prompt.md
    parts = prompt.split("## User", 1)
    system = parts[0].replace("## System", "").strip()
    user_template = parts[1].strip() if len(parts) > 1 else ""
    # Trim bundle to essential fields to stay within token budget
    slim_bundle = {
        "customer_id": bundle["customer_id"],
        "severity": bundle["severity"],
        "priority_score": bundle["priority_score"],
        "typology_families": bundle["typology_families"],
        "kyc": bundle["kyc"],
        "detection_signals": bundle["detection_signals"],
        "aggregate_behavior": bundle["aggregate_behavior"],
        "single_day_bursts": bundle["single_day_bursts"][:5],
        "key_transactions": bundle["key_transactions"][:8],
    }
    user = (user_template
            .replace("{run_id}", run_id)
            .replace("{customer_id}", bundle["customer_id"])
            .replace("{evidence_bundle_json}", json.dumps(slim_bundle, indent=2, default=str)))
    raw = call_anthropic(system, user, max_tokens=2000)

    # Strip markdown code fences if present
    raw_clean = raw.strip()
    if raw_clean.startswith("```json"):
        raw_clean = raw_clean[7:]  # strip ```json
    elif raw_clean.startswith("```"):
        raw_clean = raw_clean[3:]  # strip ```
    if raw_clean.endswith("```"):
        raw_clean = raw_clean[:-3]  # strip trailing ```
    raw_clean = raw_clean.strip()

    # Try direct parse first (JSON should be the entire response per prompt spec)
    try:
        case = json.loads(raw_clean)
    except json.JSONDecodeError:
        # Fallback: extract JSON by bracket matching
        s = raw_clean.find("{")
        if s == -1:
            raise ValueError("No JSON object found in LLM response")
        # Count braces to find matching close
        depth = 0
        e = -1
        for i in range(s, len(raw_clean)):
            if raw_clean[i] == "{":
                depth += 1
            elif raw_clean[i] == "}":
                depth -= 1
                if depth == 0:
                    e = i
                    break
        if e == -1:
            raise ValueError("Unmatched braces in JSON extraction")
        case = json.loads(raw_clean[s:e + 1])

    case["_backend"] = "anthropic"
    return case


def run(ctx: RunContext, use_llm=False):
    ctx.log("investigation_agent", "start", use_llm=use_llm)

    queue = load_json(ctx.artifact("prioritized_alert_queue.json"))
    txs = pd.read_parquet(ctx.artifact("processed_transactions.parquet"))
    kyc = pd.read_parquet(ctx.artifact("processed_customers.parquet"))
    ml_df = pd.read_csv(ctx.artifact("ml_ranked_output.csv"))
    alerts = pd.read_csv(ctx.artifact("alerts_output.csv"))

    backend = "anthropic" if (use_llm and llm_available()) else "template"
    ctx.log("investigation_agent", "backend_selected", backend=backend)

    cases = []
    bundles = []
    for customer in queue["customers"]:
        bundle = build_evidence_bundle(customer, txs, kyc, ml_df, alerts)
        bundles.append(bundle)
        if backend == "anthropic":
            case = _llm_case(bundle, ctx.run_id)
        else:
            case = _template_case(bundle)
        cases.append(case)
        ctx.log("investigation_agent", "case_built",
                customer=customer["customer_id"],
                next_step=case["recommended_next_step"])

    investigation_case = {
        "run_id": ctx.run_id,
        "generated_at": now_iso(),
        "backend": backend,
        "cases": cases,
    }
    evidence_bundle = {
        "run_id": ctx.run_id,
        "generated_at": now_iso(),
        "bundles": bundles,
    }
    save_json(ctx.artifact("investigation_case.json"), investigation_case)
    save_json(ctx.artifact("evidence_bundle.json"), evidence_bundle)

    # Human-readable summary (markdown)
    md = [f"# Investigation Summary — run {ctx.run_id}",
          f"_Backend: {backend} · Generated: {now_iso()}_", ""]
    for case in cases:
        md += [f"## {case['customer_id']}",
               f"**Recommendation:** {case['recommended_next_step']}",
               f"**Confidence:** {case['confidence']}", "",
               case["summary"], "",
               "**Triggered typologies:** " + ", ".join(case["triggered_typologies"]), "",
               "### Key facts"]
        md += [f"- {k}" for k in case["key_facts"]]
        md += ["", "### Timeline"]
        md += [f"- `{t['date']}` — {t['event']} ({t['source']})" for t in case["timeline"]]
        md += ["", "---", ""]
    ctx.artifact("investigation_summary.md").write_text("\n".join(md))

    ctx.log("investigation_agent", "complete",
            cases=len(cases), backend=backend)
    return investigation_case


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--use-llm", action="store_true")
    args = ap.parse_args()
    ctx = RunContext(run_id=args.run_id)
    run(ctx, use_llm=args.use_llm)
