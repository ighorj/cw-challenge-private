"""
Deterministic priority + severity scoring.

Pure functions used by detection_agent (to rank the queue) and compliance_agent
(to drive severity-aware decisions). No I/O, no LLM, no hidden state — the
math is the entire contract.

Design rationale:
  - Hard alert is a strong signal but not overriding (8-point bonus, not ×100).
  - Tor anonymization scores higher than VPN (deliberate vs incidental).
  - Typology *diversity* matters: 8 distinct families is harder to explain as
    legitimate than 8 fires within the same family.
  - Critical combinations (anonymization + extreme income + passthrough) get
    a multiplier rather than a flat bonus — they compound in severity.
  - Sanctions hit always escalates to critical regardless of other signals.
"""

FAMILIES = {
    "velocity":         {"R01"},
    "structuring":      {"R02_HIGH", "R02_LOW"},
    "income_mismatch":  {"R03_HIGH", "R03_LOW"},
    "passthrough":      {"R04"},
    "anonymization":    {"R05_TOR", "R05_VPN", "R14"},
    "geo":              {"R06", "R07"},
    "sanctions_pep":    {"R08", "R09", "R10"},
    "merchant":         {"R11", "R16", "R19", "R20"},
    "device_ip":        {"R12", "R13"},
    "fanout":           {"R15"},
    "card_ecom":        {"R18"},
    "network_link":     {"R21"},
}

CRITICAL_BONUS = {
    "R08":      15,  # sanctions hit — never silently ignored
    "R16":       8,  # self-merchant — rare layering pattern
    "R05_TOR":   5,  # Tor anonymization (deliberate, not incidental)
    "R09":       2,  # PEP regulatory exposure
    "R03_HIGH":  2,  # extreme income disparity
    "R04":       1,  # passthrough behavior
}


def typology_families_hit(triggered_rules):
    rule_set = set(triggered_rules)
    return [name for name, members in FAMILIES.items() if rule_set & members]


def priority_score(rules_score, ml_probability, hard_alert, triggered_rules):
    """Composite priority: additive bonuses, multiplicative for dangerous combos."""
    rule_set = set(triggered_rules)
    base = rules_score
    bonus = sum(CRITICAL_BONUS.get(r, 0) for r in rule_set)
    families = typology_families_hit(rule_set)
    diversity_bonus = max(0, len(families) - 4) * 2
    hard_bonus = 8 if hard_alert else 0

    multiplier = 1.0
    has_anon    = bool(rule_set & FAMILIES["anonymization"])
    has_income  = "R03_HIGH" in rule_set
    has_passth  = "R04" in rule_set
    if has_anon and has_income and has_passth:
        # Tor + income + passthrough is qualitatively worse than VPN equivalent
        multiplier = 1.4 if "R05_TOR" in rule_set else 1.3
    if "R08" in rule_set:
        multiplier = max(multiplier, 1.5)

    score = (base + bonus + diversity_bonus + hard_bonus) * multiplier + ml_probability * 10
    return round(score, 2)


def severity_band(priority, triggered_rules):
    """Discrete severity from priority + critical-rule presence."""
    rules = set(triggered_rules)
    if "R08" in rules or "R16" in rules:
        return "critical"
    if priority >= 70:
        return "critical"
    if priority >= 50:
        return "high"
    if priority >= 30:
        return "medium"
    if priority >= 15:
        return "low"
    return "routine"


def evidence_strength(triggered_rules, key_metrics):
    """0–1: quantitative grounding + typology breadth + rule depth."""
    rule_count = len(triggered_rules)
    families = len(typology_families_hit(triggered_rules))
    quant = sum(1 for k in ("total_outflow_brl", "income_disparity_multiple",
                            "passthrough_pct", "anonymization_events_total")
                if key_metrics.get(k))
    s = (rule_count / 12) * 0.4 + (families / 7) * 0.4 + (quant / 4) * 0.2
    return round(min(s, 1.0), 2)


def confidence_level(evidence_strength_val, rule_count):
    if evidence_strength_val >= 0.75 and rule_count >= 6:
        return "high"
    if evidence_strength_val >= 0.50 and rule_count >= 4:
        return "moderate"
    return "low"
