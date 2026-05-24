"""
Orchestrator — sequential DAG runner for the AML multi-agent pipeline.

Stages run in fixed order. Each stage writes its artifacts to the run directory
and emits audit-log entries. Failures abort the run with a clear error trace.

Production migration path: the same DAG is defined in n8n_workflow.json with
identical artifact contracts. The Python orchestrator is for local repro/demo.
"""

import sys
import argparse
import traceback
from pathlib import Path

AGENTS_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(AGENTS_DIR))
for sub in ("data_agent", "detection_agent", "investigation_agent",
            "sar_agent", "compliance_agent"):
    sys.path.insert(0, str(AGENTS_DIR / sub))

from shared import RunContext, now_iso  # noqa: E402
import data_agent            # noqa: E402
import detection_agent       # noqa: E402
import investigation_agent   # noqa: E402
import sar_agent             # noqa: E402
import compliance_agent      # noqa: E402

# Each stage is (name, function). Functions accept (ctx, **kwargs).
PIPELINE = [
    ("data_agent",          lambda ctx, **kw: data_agent.run(ctx, use_llm=kw.get("use_llm", False))),
    ("detection_agent",     lambda ctx, **kw: detection_agent.run(ctx, top_n=kw.get("top_n", 5), use_llm=kw.get("use_llm", False))),
    ("investigation_agent", lambda ctx, **kw: investigation_agent.run(ctx, use_llm=kw.get("use_llm", False))),
    ("sar_agent",           lambda ctx, **kw: sar_agent.run(ctx, use_llm=kw.get("use_llm", False))),
    ("compliance_agent",    lambda ctx, **kw: compliance_agent.run(ctx, use_llm=kw.get("use_llm", False))),
]


def execute(top_n=5, use_llm=False, run_id=None):
    ctx = RunContext(run_id=run_id)
    ctx.log("orchestrator", "run_started",
            top_n=top_n, use_llm=use_llm, llm_available_now=False)
    print(f"\n========= RUN {ctx.run_id} =========")
    print(f"  artifacts dir: {ctx.dir}")
    print(f"  top_n={top_n}, use_llm={use_llm}\n")

    for name, fn in PIPELINE:
        print(f"[{now_iso()}] ▶ {name} ...")
        try:
            fn(ctx, top_n=top_n, use_llm=use_llm)
            print(f"[{now_iso()}] ✓ {name} complete")
        except Exception as exc:
            ctx.log("orchestrator", "stage_failed", stage=name,
                    error=str(exc), trace=traceback.format_exc())
            print(f"[{now_iso()}] ✗ {name} FAILED — {exc}")
            raise

    ctx.log("orchestrator", "run_complete")
    print(f"\n========= RUN COMPLETE =========")
    print(f"  artifacts: {ctx.dir}")
    print(f"  audit log: {ctx.audit_path}")
    return ctx


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Run the AML multi-agent pipeline end-to-end.")
    ap.add_argument("--top-n", type=int, default=5,
                    help="Number of customers to investigate (top by priority key).")
    ap.add_argument("--use-llm", action="store_true",
                    help="Use Anthropic API for LLM-augmented agents (requires ANTHROPIC_API_KEY).")
    ap.add_argument("--run-id", default=None,
                    help="Reuse an existing run_id (resumes / re-runs from cached artifacts).")
    args = ap.parse_args()
    execute(top_n=args.top_n, use_llm=args.use_llm, run_id=args.run_id)
