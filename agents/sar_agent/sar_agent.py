"""
SAR agent — drafts SAR from investigation case + evidence bundle.

LLM-augmented with deterministic template fallback (same JSON contract).
The template renders the institution's standard SAR structure deterministically.
"""

import sys
import re
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from shared import RunContext, load_json, save_json, llm_available, call_anthropic, now_iso, soften_language, ml_confidence_band
from aml_constants import RULE_DESCRIPTIONS, sanctions_status

PROMPT_FILE = Path(__file__).parent / "prompt.md"


def _template_sar(case, bundle, run_id):
    """Deterministic SAR draft from the structured case + evidence."""
    cid = case["customer_id"]
    kyc = bundle["kyc"]
    agg = bundle["aggregate_behavior"]
    rules = bundle["detection_signals"]["triggered_rules"]
    monthly_income = kyc["annual_income_brl"] / 12 if kyc["annual_income_brl"] else None
    income_mult = round(agg["total_outflow_brl"] / monthly_income) if monthly_income else None

    sar_ref = f"SAR-{run_id}-{cid}-01"

    triggered_alerts = []
    for r in rules:
        if r not in RULE_DESCRIPTIONS:
            continue
        code, _, logic = RULE_DESCRIPTIONS[r]
        triggered_alerts.append({
            "alert_code": code,
            "detection_logic": logic,
            "date_or_aggregate": "review-period aggregate",
            "relevance": "Contributes to composite risk indicator",
        })

    structured = {
        "customer_id": cid,
        "sar_reference": sar_ref,
        "prepared_at": now_iso(),
        "severity": case.get("severity", bundle.get("severity", "unknown")),
        "executive_summary": case["summary"],
        "triggered_alerts": triggered_alerts,
        "detailed_findings": case["key_facts"],
        "regulatory_basis": [
            "FATF Recommendation 12 — PEP customers require Enhanced Due Diligence" if kyc.get("pep") == "Yes" else "FATF Recommendation 10 — CDD applies",
            "FATF Recommendation 19 — Cross-border monitoring (where applicable)",
            "Circular BACEN 3.978/2020 — Activity materially inconsistent with declared profile is a reportable indicator",
            "COAF — Suspicious Activity Report filing obligation",
        ],
        "recommended_actions": [
            f"Submit SAR to COAF following institutional policy ({case['recommended_next_step']}).",
            "Initiate Enhanced Due Diligence: source-of-funds and source-of-wealth documentation.",
            "Elevate to enhanced monitoring tier; reduce thresholds for ongoing alerting.",
            "Initiate merchant-level review for any shared receiving merchants.",
            "Compliance Officer to assess transactional restrictions pending EDD outcome.",
        ],
        "key_metrics": {
            "total_outflow_brl": agg["total_outflow_brl"],
            "declared_annual_income_brl": kyc["annual_income_brl"],
            "income_disparity_multiple": income_mult,
            "passthrough_pct": agg.get("passthrough_ratio_pct"),
            "distinct_counterparties": agg["distinct_counterparties"],
            "anonymization_events_total": sum(agg["anonymization_events"].values()) if agg["anonymization_events"] else 0,
            "kyc_risk_score": kyc["kyc_risk_score"],
            "pep": kyc.get("pep"),
            "ml_confidence_band": ml_confidence_band(bundle.get("detection_signals", {}).get("ml_probability", 0.0)),
        },
        "sanctions_status": sanctions_status(
            kyc.get("sanctions_list_hit"),
            sum(1 for tx in bundle.get("key_transactions", [])
                if tx.get("sanctions_screening_hit") == "Yes"),
        ),
        "linked_entities": [
            {"entity_id": e["entity_id"], "relationship": e["relationship"], "status": "Identified during this investigation"}
            for e in case["entity_links"]
        ],
        "_backend": "template",
    }
    structured["executive_summary"] = soften_language(structured["executive_summary"])

    # Render markdown SAR using the structured payload
    md = _render_markdown(structured, case, bundle)
    return structured, md


def _render_markdown(s, case, bundle):
    """Render markdown SAR mirroring the docs/phase1/SAR-2025-C102290-01.md structure."""
    kyc = bundle["kyc"]
    lines = [
        f"# SUSPICIOUS ACTIVITY REPORT (SAR)",
        f"**Internal Reference:** {s['sar_reference']}",
        f"**Filing Institution:** CloudWalk INC — AML/FT Compliance Unit",
        f"**Prepared at:** {s['prepared_at']}",
        f"**Classification:** Internal — Compliance Restricted",
        "",
        "---",
        "",
        "## 1. CASE IDENTIFICATION",
        "",
        "| Field | Value |",
        "|---|---|",
        f"| Primary Subject | {s['customer_id']} |",
        f"| Declared Occupation | {kyc.get('declared_occupation') or '—'} |",
        f"| Declared Annual Income | R${kyc['annual_income_brl']:,.0f} |",
        f"| PEP Status | {kyc.get('pep')} |",
        f"| KYC Risk Score | {kyc['kyc_risk_score']} / 100 |",
        f"| Risk Rating | {kyc.get('risk_rating')} |",
        f"| KYC Tier | {kyc.get('kyc_tier')} |",
        f"| Total Outflow (review period) | R${s['key_metrics']['total_outflow_brl']:,.0f} |",
        f"| Sanctions Status | {s.get('sanctions_status', {}).get('label', '—')} |",
        f"| ML Confidence | {s['key_metrics'].get('ml_confidence_band', '—')} |",
        "",
        "---",
        "",
        "## 2. EXECUTIVE SUMMARY",
        "",
        s["executive_summary"],
        "",
        "---",
        "",
        "## 3. TRIGGERED ALERTS",
        "",
        "| Alert | Detection logic | Relevance |",
        "|---|---|---|",
    ]
    for a in s["triggered_alerts"]:
        lines.append(f"| {a['alert_code']} | {a['detection_logic']} | {a['relevance']} |")

    lines += ["", "---", "", "## 4. DETAILED FINDINGS", ""]
    for f in s["detailed_findings"]:
        lines.append(f"- {f}")

    lines += ["", "---", "", "## 5. REGULATORY BASIS", ""]
    for r in s["regulatory_basis"]:
        lines.append(f"- {r}")

    lines += ["", "---", "", "## 6. RECOMMENDED ACTIONS", ""]
    for i, a in enumerate(s["recommended_actions"], 1):
        lines.append(f"{i}. {a}")

    lines += ["", "---", "", "## 7. LINKED ENTITIES", ""]
    if s["linked_entities"]:
        lines += ["| Entity | Relationship | Status |", "|---|---|---|"]
        for e in s["linked_entities"]:
            lines.append(f"| {e['entity_id']} | {e['relationship']} | {e['status']} |")
    else:
        lines.append("None identified.")

    lines += ["", "---", "",
              "_This report constitutes an internal compliance escalation. Conclusions are based on transactional and KYC data available at preparation time. Final SAR filing determination is subject to Compliance Officer and MLRO review._"]
    return "\n".join(lines)


def _llm_sar(case, bundle, run_id):
    """LLM-backed SAR generation. Same schema output."""
    prompt = PROMPT_FILE.read_text()
    parts = prompt.split("## User", 1)
    system = parts[0].replace("## System", "").strip()
    user = parts[1].strip() if len(parts) > 1 else ""
    user = (user.replace("{run_id}", run_id)
                .replace("{investigation_case_json}", json.dumps(case, indent=2, default=str))
                .replace("{evidence_bundle_json}", json.dumps(bundle, indent=2, default=str)))
    raw = call_anthropic(system, user, max_tokens=4000)
    # Parse <<<JSON>>>...<<<MARKDOWN>>>...
    m = re.search(r"<<<JSON>>>(.+?)<<<MARKDOWN>>>(.+)", raw, re.DOTALL)
    if not m:
        raise ValueError("LLM response missing required JSON / MARKDOWN delimiters")
    json_text = m.group(1).strip()
    # Strip markdown code fences if present around JSON
    if json_text.startswith("```"):
        json_text = re.sub(r'^```(?:json)?\s*', '', json_text)
        json_text = re.sub(r'\s*```$', '', json_text)
    structured = json.loads(json_text)
    structured["_backend"] = "anthropic"
    md = m.group(2).strip()
    return structured, md


def run(ctx: RunContext, use_llm=False):
    ctx.log("sar_agent", "start", use_llm=use_llm)
    inv = load_json(ctx.artifact("investigation_case.json"))
    ev  = load_json(ctx.artifact("evidence_bundle.json"))

    backend = "anthropic" if (use_llm and llm_available()) else "template"
    ctx.log("sar_agent", "backend_selected", backend=backend)

    # Process all cases recommended for SAR filing
    structured_list = []
    md_parts = []
    for case, bundle in zip(inv["cases"], ev["bundles"]):
        if case["recommended_next_step"] not in ("file_sar_immediate", "file_sar_standard_window"):
            ctx.log("sar_agent", "skipped",
                    customer=case["customer_id"],
                    reason=f"recommendation={case['recommended_next_step']}")
            continue
        if backend == "anthropic":
            s, md = _llm_sar(case, bundle, ctx.run_id)
        else:
            s, md = _template_sar(case, bundle, ctx.run_id)
        structured_list.append(s)
        md_parts.append(md)
        ctx.log("sar_agent", "sar_drafted",
                customer=case["customer_id"],
                sar_reference=s["sar_reference"])

    out = {
        "run_id": ctx.run_id,
        "generated_at": now_iso(),
        "backend": backend,
        "sars": structured_list,
    }
    save_json(ctx.artifact("sar_structured.json"), out)
    ctx.artifact("sar_draft.md").write_text("\n\n---\n\n".join(md_parts))

    ctx.log("sar_agent", "complete", sar_count=len(structured_list), backend=backend)
    return out


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--use-llm", action="store_true")
    args = ap.parse_args()
    ctx = RunContext(run_id=args.run_id)
    run(ctx, use_llm=args.use_llm)
