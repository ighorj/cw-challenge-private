"""
Canonical AML constants shared across all agents.

Single source of truth for rule descriptions, typology families,
and sanctions concept distinction. Import from here — never define
rule semantics in agent-specific code.
"""

# ─────────────────────────────────────────────────────────────────────────────
# Canonical rule descriptions
# (code, typology_family, detection_logic)
# ─────────────────────────────────────────────────────────────────────────────
RULE_DESCRIPTIONS = {
    "R01":      ("R01-VEL-BURST",        "velocity",         "≥4 transactions in a single calendar day"),
    "R02_HIGH": ("R02-STRUCT-BAND",      "structuring",      "≥3 transactions in R$9,000–R$10,000 band"),
    "R02_LOW":  ("R02-STRUCT-BAND",      "structuring",      "1–2 transactions in R$9,000–R$10,000 band"),
    "R03_HIGH": ("R03-INCOME-MISMATCH",  "income_mismatch",  "Total outflow >100× declared monthly income"),
    "R03_LOW":  ("R03-INCOME-MISMATCH",  "income_mismatch",  "Total outflow >50× declared monthly income"),
    "R04":      ("R04-PASSTHRU",         "passthrough",      "PIX outflow-to-inflow ratio >200%"),
    "R05_TOR":  ("R05-ANON-TOR",        "anonymization",    "Transaction executed via Tor anonymization network"),
    "R05_VPN":  ("R05-ANON-VPN",        "anonymization",    "≥2 transactions via VPN or proxy service"),
    "R06":      ("R06-GEO-HIGH-RISK",    "geo",              "Cross-border activity involving high-risk jurisdiction"),
    "R07":      ("R07-GEO-IP-MISMATCH", "geo",              "IP country differs from declared country (≥2 events)"),
    "R08":      ("R08-SANCTIONS-SCREEN", "sanctions_pep",    "Transactional sanctions screening event detected"),
    "R09":      ("R09-PEP-EDD",         "sanctions_pep",    "PEP status — Enhanced Due Diligence required (FATF Rec. 12)"),
    "R10":      ("R10-KYC-INCONSIST",   "sanctions_pep",    "Contradictory KYC field combination (e.g. PEP + Low risk rating)"),
    "R11":      ("R11-MCC-HIGH-RISK",   "merchant",         "≥3 transactions to high-risk MCC merchants"),
    "R12":      ("R12-DEVICE-REUSE",    "device_ip",        "Same device fingerprint linked to multiple accounts"),
    "R13":      ("R13-IP-REUSE",        "device_ip",        "Same IP address linked to multiple accounts"),
    "R14":      ("R14-ROOTED-DEVICE",   "anonymization",    "≥3 transactions from rooted or jailbroken device"),
    "R15":      ("R15-FAN-OUT",         "fanout",           "≥25 distinct receiving counterparties in review period"),
    "R16":      ("R16-SELF-MERCHANT",   "merchant",         "Customer is registered owner of receiving merchant"),
    "R17":      ("R17-MULTI-RAIL",      "merchant",         "Mixed-rail activity: PIX + Card + Wire within review window"),
    "R18":      ("R18-CARD-NO-3DS",     "card_ecom",        "≥3 card-not-present transactions without 3DS authentication"),
    "R19":      ("R19-CHARGEBACK",      "merchant",         "Chargeback history or repeat use of high-chargeback merchants"),
    "R20":      ("R20-MERCHANT-CONVERGE","merchant",        "Shared receiving merchant with another flagged subject"),
    "R21":      ("R21-NETWORK-LINK",    "network_link",     "Direct wire transfer to another flagged subject"),
}

# Compact reference block for injection into LLM prompts
RULE_REFERENCE_BLOCK = "\n".join(
    f"  {rid}: [{code}] {logic}"
    for rid, (code, _, logic) in RULE_DESCRIPTIONS.items()
)


# ─────────────────────────────────────────────────────────────────────────────
# Sanctions concept distinction
# ─────────────────────────────────────────────────────────────────────────────

def sanctions_status(kyc_sanctions_hit, tx_screening_count):
    """
    Distinguish confirmed entity-level sanctions match from transactional screening events.

    Returns a dict used in SAR and investigation outputs.
    """
    confirmed = str(kyc_sanctions_hit).strip().lower() == "yes"
    screening = int(tx_screening_count) > 0
    return {
        "confirmed_sanctions_match": confirmed,
        "screening_events": int(tx_screening_count),
        "label": (
            "Confirmed KYC-level sanctions list match"
            if confirmed
            else (
                f"{tx_screening_count} transactional screening event(s) — pending entity-level review"
                if screening
                else "No sanctions indicator"
            )
        ),
        "severity": "confirmed" if confirmed else ("screening_hit" if screening else "none"),
    }


# ─────────────────────────────────────────────────────────────────────────────
# Primary showcase case
# ─────────────────────────────────────────────────────────────────────────────

PRIMARY_SHOWCASE_CASE = "C102290"
PRIMARY_SHOWCASE_RATIONALE = (
    "C102290 is designated as the primary investigative showcase case. "
    "It presents the highest investigative richness in the dataset: PEP status, "
    "Tor anonymization, multi-typology convergence (income mismatch, passthrough, "
    "fan-out, merchant convergence, KYC inconsistency), and a strong evidence-backed "
    "timeline narrative. This designation is based on investigative depth and "
    "explainability — not on operational escalation score, which is driven by the "
    "sanctions-weighted priority engine."
)
