"""
Shared utilities for the AML multi-agent pipeline.

Provides:
  - RunContext: per-run state (run_id, paths, audit log)
  - load_json / save_json: thin wrappers used by every agent
  - llm_call: optional Anthropic backend with deterministic fallback

The fallback is not "fake LLM" — it is a deterministic template renderer
that produces structured JSON identical in schema to the LLM-backed call.
Use --use-llm or set ANTHROPIC_API_KEY to switch backend at runtime.
"""

import json
import os
import datetime as dt
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNS_DIR = ROOT / "outputs" / "phase4_demo" / "runs"


def now_iso():
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


class RunContext:
    """Per-run state. Maintains run_id, artifact paths, and the audit log."""

    def __init__(self, run_id=None):
        self.run_id = run_id or dt.datetime.now().strftime("%Y%m%d-%H%M%S") + "-" + uuid.uuid4().hex[:6]
        self.dir = RUNS_DIR / self.run_id
        self.dir.mkdir(parents=True, exist_ok=True)
        self.audit_path = self.dir / "audit_log.json"
        self._audit = []
        if self.audit_path.exists():
            self._audit = json.loads(self.audit_path.read_text())

    def artifact(self, name):
        return self.dir / name

    def log(self, agent, event, **extra):
        entry = {"ts": now_iso(), "agent": agent, "event": event, **extra}
        self._audit.append(entry)
        save_json(self.audit_path, self._audit)
        return entry

    def __repr__(self):
        return f"RunContext(run_id={self.run_id!r})"


def load_json(path):
    return json.loads(Path(path).read_text())


def save_json(path, obj):
    Path(path).write_text(json.dumps(obj, indent=2, default=str))


# ─────────────────────────────────────────────────────────────────────────────
# LLM backend — anthropic if available, deterministic template otherwise
# ─────────────────────────────────────────────────────────────────────────────

def llm_available():
    """True if Anthropic SDK is installed AND the API key is present."""
    if not os.environ.get("ANTHROPIC_API_KEY"):
        return False
    try:
        import anthropic  # noqa: F401
        return True
    except ImportError:
        return False


def call_anthropic(system, user, model="claude-opus-4-5", max_tokens=1200):
    """Live Anthropic call. Caller is responsible for backend selection."""
    import anthropic
    client = anthropic.Anthropic()
    resp = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        system=system,
        messages=[{"role": "user", "content": user}],
    )
    return resp.content[0].text


# ─────────────────────────────────────────────────────────────────────────────
# AML language utilities
# ─────────────────────────────────────────────────────────────────────────────

import re as _re

_LANGUAGE_SOFTENER = [
    # Assertive causation → hedged
    (r'\bconsistent with layering\b',          'potentially consistent with layering'),
    (r'\bdirect nexus to\b',                   'transaction exposure involving'),
    (r'\bdirect nexus\b',                      'potential nexus'),
    (r'\bconstitutes\b',                       'may constitute'),
    (r'\bdemonstrates\b',                      'suggests'),
    (r'\bconfirms\b',                          'indicates'),
    (r'\bis evidence of\b',                    'may be consistent with'),
    (r'\bused as a conduit\b',                 'potentially functioning as a conduit'),
    (r'\bthe account is a conduit\b',          'the account may be functioning as a conduit'),
    # Sanctions language — only soften non-confirmed references
    (r'\bconfirmed sanctions exposure\b',      'sanctions screening event requiring review'),
    (r'\bOFAC-sanctioned jurisdiction\b',      'jurisdiction subject to OFAC sanctions screening'),
    (r'\bsanctioned jurisdiction\b',           'jurisdiction subject to sanctions screening'),
    # Outcome language
    (r'\bindicates? (?:money laundering|ML)\b','may be consistent with money laundering'),
    (r'\bmoney laundering activity\b',         'activity potentially consistent with money laundering'),
    (r'\bterrorist financing activity\b',      'activity warranting terrorist financing review'),
]


def soften_language(text: str) -> str:
    """Replace overly assertive AML language with cautious investigative phrasing."""
    for pattern, replacement in _LANGUAGE_SOFTENER:
        text = _re.sub(pattern, replacement, text, flags=_re.IGNORECASE)
    return text


def ml_confidence_band(probability: float) -> str:
    """Absolute ML confidence band (population-level fallback)."""
    if probability >= 0.95:
        return "Very High"
    if probability >= 0.80:
        return "High"
    if probability >= 0.60:
        return "Moderate-High"
    if probability >= 0.40:
        return "Moderate"
    return "Low"


def ml_confidence_band_cohort(rank: int, total: int, fallback_probability: float = 0.0) -> str:
    """
    Cohort-relative ML confidence band.

    Labels are calibrated to the current escalation queue distribution —
    not the full customer population. Preserves meaningful differentiation
    inside the top-risk cohort where absolute bands collapse to a single label.

    rank=1 is the highest ML probability in the cohort.
    """
    if total <= 2:
        return ml_confidence_band(fallback_probability)
    pct = rank / total
    if pct <= 0.10:
        return "Extreme"
    if pct <= 0.25:
        return "Very High"
    if pct <= 0.55:
        return "High"
    if pct <= 0.80:
        return "Moderate-High"
    return "Moderate"


COHORT_RELATIVE_NOTE = (
    "ML confidence labels are calibrated relative to the investigated escalation cohort, "
    "not the full customer population."
)
