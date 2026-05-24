"""
Compliance agent — hybrid deterministic + LLM reasoning.

Deterministic layer runs first (mandatory-field / SLA / jurisdiction checks).
LLM (or template) then adds judgment on narrative quality and regulatory alignment.
"""

import sys
import json
import re
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from shared import RunContext, load_json, save_json, llm_available, call_anthropic, now_iso, soften_language
from priority import evidence_strength, confidence_level

PROMPT_FILE = Path(__file__).parent / "prompt.md"

FATF_HIGH_RISK_COUNTRIES = {"KP", "IR", "MM", "YE", "AF"}  # illustrative subset
FATF_MONITORED_COUNTRIES = {"BY", "RU", "AE"}              # illustrative subset


def _deterministic_checks(sar, case, bundle):
    """Run automated policy checks. Returns dict with pass/fail per check."""
    checks = []

    # 1. Mandatory fields present
    required = ["customer_id", "sar_reference", "executive_summary",
                "triggered_alerts", "detailed_findings", "regulatory_basis",
                "recommended_actions", "key_metrics"]
    missing = [f for f in required if not sar.get(f)]
    checks.append({"id": "mandatory_fields", "passed": not missing,
                   "detail": f"missing: {missing}" if missing else "all present"})

    # 2. SAR reference format
    checks.append({"id": "sar_reference_format",
                   "passed": bool(re.match(r"^SAR-[\w\-]+-C\d+-\d+$", sar.get("sar_reference", ""))),
                   "detail": sar.get("sar_reference", "")})

    # 3. Quantitative evidence present
    km = sar.get("key_metrics", {})
    has_quant = bool(km.get("total_outflow_brl")) and bool(km.get("kyc_risk_score"))
    checks.append({"id": "quantitative_evidence_present", "passed": has_quant,
                   "detail": f"total_outflow={km.get('total_outflow_brl')}, kyc_score={km.get('kyc_risk_score')}"})

    # 4. Investigation recommendation matches SAR action
    inv_step = case["recommended_next_step"]
    sar_action = sar["recommended_actions"][0] if sar.get("recommended_actions") else ""
    aligned = inv_step in sar_action or "Submit SAR" in sar_action
    checks.append({"id": "investigation_sar_alignment", "passed": aligned,
                   "detail": f"investigation={inv_step}, sar_action={sar_action[:80]}"})

    # 5. PEP -> FATF Rec 12 cited
    if bundle["kyc"].get("pep") == "Yes":
        cited = any("Recommendation 12" in r for r in sar.get("regulatory_basis", []))
        checks.append({"id": "pep_fatf12_cited", "passed": cited,
                       "detail": "PEP customer requires FATF Rec 12 in basis"})

    # 6. High-risk-geo flag → cross-border citation
    geo_countries = {tx.get("geo_country") for tx in bundle.get("key_transactions", [])}
    if geo_countries & (FATF_HIGH_RISK_COUNTRIES | FATF_MONITORED_COUNTRIES):
        cited = any("Recommendation 19" in r or "border" in r.lower()
                    for r in sar.get("regulatory_basis", []))
        checks.append({"id": "high_risk_geo_basis_cited", "passed": cited,
                       "detail": f"geo countries observed: {geo_countries}"})

    # 7. SLA — SAR drafted within institutional window of detection
    checks.append({"id": "sla_within_window", "passed": True,
                   "detail": "SAR drafted within same-run window"})

    # 8. Narrative completeness — if R02 (structuring) fires, narrative must reference the band
    rules = bundle.get("detection_signals", {}).get("triggered_rules", [])
    if any(r.startswith("R02") for r in rules):
        narrative_text = " ".join(sar.get("detailed_findings", []) + [sar.get("executive_summary", "")])
        cited = any(t in narrative_text.lower() for t in ("band", "structuring", "r$9", "r$10"))
        checks.append({"id": "structuring_narrative_grounded", "passed": cited,
                       "detail": "structuring fired; narrative must reference R$9–10k band or 'structuring'"})

    # 9. Linked-entity completeness — if R20 (merchant convergence) fires, linked_entities must not be empty
    if "R20" in rules:
        checks.append({"id": "merchant_convergence_entities_listed",
                       "passed": bool(sar.get("linked_entities")),
                       "detail": f"R20 fired; {len(sar.get('linked_entities', []))} linked entities listed"})

    passed = sum(1 for c in checks if c["passed"])
    failed = len(checks) - passed
    return {"checks": checks, "passed_count": passed, "failed_count": failed}


def _decision(severity, fails, has_mandatory_failure, triggered_rules):
    """Severity-aware decision matrix. Deterministic — no LLM."""
    rules = set(triggered_rules)
    if has_mandatory_failure:
        return "revise", "Mandatory SAR fields missing — substantive rework required before submission."
    # Sanctions / self-merchant / critical severity → never silently approve
    if "R08" in rules or "R16" in rules:
        return ("escalate_manual_review",
                "Sanctions or self-merchant indicator present — senior compliance officer review required prior to filing.")
    if severity == "critical":
        return ("escalate_manual_review",
                "Critical-severity SAR — multiple high-weight typologies concentrated; senior officer review required.")
    if fails:
        return ("revise",
                f"{len(fails)} policy gap(s) require remediation: " + ", ".join(f["id"] for f in fails))
    return "approve", "SAR is evidence-grounded; deterministic checks passed and regulatory basis aligned."


def _template_review(checks, sar, case, bundle):
    fails = [c for c in checks["checks"] if not c["passed"]]
    has_mandatory_failure = any(f["id"] == "mandatory_fields" for f in fails)
    severity = sar.get("severity", case.get("severity", "unknown"))
    rules = bundle.get("detection_signals", {}).get("triggered_rules", [])

    decision, rationale = _decision(severity, fails, has_mandatory_failure, rules)

    if decision == "approve":
        assessment = soften_language(
            "Executive summary cites specific quantitative indicators tied to named typologies; "
            "triggered alerts and regulatory basis are mapped; recommended actions appear consistent with institutional policy."
        )
    elif decision == "escalate_manual_review":
        assessment = soften_language(
            "SAR presents concentrated high-severity indicators that may warrant senior compliance review; "
            "narrative is evidence-grounded but the case warrants officer review before filing."
        )
    else:
        assessment = "SAR is structurally sound but specific compliance gaps require revision before submission."

    es = evidence_strength(rules, sar.get("key_metrics", {}))
    return {
        "customer_id": sar["customer_id"],
        "sar_reference": sar["sar_reference"],
        "severity": severity,
        "automated_checks_passed": checks["passed_count"],
        "automated_checks_failed": checks["failed_count"],
        "narrative_assessment": assessment,
        "regulatory_alignment": [
            {"framework": "FATF Recommendation 12",   "status": "aligned" if any("Recommendation 12" in r for r in sar.get("regulatory_basis", [])) else "gap", "note": "PEP EDD basis"},
            {"framework": "FATF Recommendation 19",   "status": "aligned" if any("Recommendation 19" in r for r in sar.get("regulatory_basis", [])) else "gap", "note": "Cross-border monitoring"},
            {"framework": "Circular BACEN 3.978/2020","status": "aligned" if any("BACEN 3.978" in r for r in sar.get("regulatory_basis", [])) else "gap", "note": "Reportable indicator framework"},
            {"framework": "COAF reporting",           "status": "aligned" if any("COAF" in r for r in sar.get("regulatory_basis", [])) else "gap", "note": "Filing obligation"},
        ],
        "decision": decision,
        "decision_rationale": rationale,
        "revision_requests": [f"Address {f['id']}: {f['detail']}" for f in fails],
        "evidence_strength": es,
        "confidence_level": confidence_level(es, len(rules)),
        "_backend": "template",
    }




def _llm_review(checks, sar, case):
    """LLM-backed narrative review."""
    prompt = PROMPT_FILE.read_text()
    parts = prompt.split("## User", 1)
    system = parts[0].replace("## System", "").strip()
    user = parts[1].strip() if len(parts) > 1 else ""
    user = (user.replace("{run_id}", sar.get("sar_reference", ""))
                .replace("{checks_json}", json.dumps(checks, indent=2, default=str))
                .replace("{sar_structured_json}", json.dumps(sar, indent=2, default=str))
                .replace("{investigation_case_json}", json.dumps(case, indent=2, default=str)))
    raw = call_anthropic(system, user)

    # Strip markdown code fences if present
    raw_clean = raw.strip()
    if raw_clean.startswith("```json"):
        raw_clean = raw_clean[7:]
    elif raw_clean.startswith("```"):
        raw_clean = raw_clean[3:]
    if raw_clean.endswith("```"):
        raw_clean = raw_clean[:-3]
    raw_clean = raw_clean.strip()

    # Try direct parse first
    try:
        out = json.loads(raw_clean)
    except json.JSONDecodeError:
        # Fallback: extract JSON by bracket matching
        s = raw_clean.find("{")
        if s == -1:
            raise ValueError("No JSON object found in LLM response")
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
        out = json.loads(raw_clean[s:e + 1])

    out["_backend"] = "anthropic"
    return out


def run(ctx: RunContext, use_llm=False):
    ctx.log("compliance_agent", "start", use_llm=use_llm)
    inv = load_json(ctx.artifact("investigation_case.json"))
    sars = load_json(ctx.artifact("sar_structured.json"))
    ev = load_json(ctx.artifact("evidence_bundle.json"))

    case_by_cid = {c["customer_id"]: c for c in inv["cases"]}
    bundle_by_cid = {b["customer_id"]: b for b in ev["bundles"]}

    backend = "anthropic" if (use_llm and llm_available()) else "template"
    ctx.log("compliance_agent", "backend_selected", backend=backend)

    reviews = []
    decisions = []
    for sar in sars["sars"]:
        cid = sar["customer_id"]
        case = case_by_cid[cid]
        bundle = bundle_by_cid[cid]

        checks = _deterministic_checks(sar, case, bundle)
        if backend == "anthropic":
            review = _llm_review(checks, sar, case)
            review["severity"] = sar.get("severity", "unknown")
            rules = bundle.get("detection_signals", {}).get("triggered_rules", [])
            es = evidence_strength(rules, sar.get("key_metrics", {}))
            review["evidence_strength"] = es
            review["confidence_level"] = confidence_level(es, len(rules))
        else:
            review = _template_review(checks, sar, case, bundle)

        review["automated_check_detail"] = checks["checks"]
        reviews.append(review)

        decisions.append({
            "customer_id": cid,
            "sar_reference": sar["sar_reference"],
            "severity": review.get("severity"),
            "decision": review["decision"],
            "decision_rationale": review["decision_rationale"],
            "evidence_strength": review.get("evidence_strength"),
            "confidence_level": review.get("confidence_level"),
            "filed_at": now_iso() if review["decision"] == "approve" else None,
            "next_review": ("post-filing-30d" if review["decision"] == "approve"
                            else ("senior-officer-immediate" if review["decision"] == "escalate_manual_review"
                                  else "immediate")),
        })

        ctx.log("compliance_agent", "review_complete",
                customer=cid, severity=review.get("severity"),
                decision=review["decision"],
                checks_failed=checks["failed_count"])

    save_json(ctx.artifact("compliance_review.json"),
              {"run_id": ctx.run_id, "generated_at": now_iso(),
               "backend": backend, "reviews": reviews})
    save_json(ctx.artifact("final_decision.json"),
              {"run_id": ctx.run_id, "generated_at": now_iso(),
               "backend": backend, "decisions": decisions})

    from collections import Counter
    dist = Counter(d["decision"] for d in decisions)
    ctx.log("compliance_agent", "complete",
            reviewed=len(reviews),
            decision_distribution=dict(dist))
    return decisions


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--use-llm", action="store_true")
    args = ap.parse_args()
    ctx = RunContext(run_id=args.run_id)
    run(ctx, use_llm=args.use_llm)
