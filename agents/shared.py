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
