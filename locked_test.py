"""Locked Changed-Input Record runner (AI-closed execution).

Order of operations -- do not change it:
 1. YOU write your prediction in docs/locked-prediction.md (no AI help), then
        git add docs/locked-prediction.md
        git commit -m "Lock human prediction for changed-input test"
 2. Run:  python locked_test.py
    The script refuses to run if the prediction file is missing, still contains the
    blank template marker, or has uncommitted edits. It records the commit hash of the
    locked prediction, runs base vs. changed input, and writes output/locked_test_result.json/.md.
 3. Commit the result, then complete the reconciliation section by hand.

The changed input is revenue per flight hour (all forecast years), which is deliberately NOT
shown in any sensitivity table of the frozen output.
"""
from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from joby.model import load_inputs, value, with_changes

ROOT = Path(__file__).resolve().parent
PREDICTION = ROOT / "docs" / "locked-prediction.md"
BLANK_MARKER = "[WRITE HERE]"
CHANGED_INPUT = "revenue_per_hour_multiplier"
OLD, NEW = 1.0, 0.8  # $2,500 -> $2,000 per flight hour in 2027, same proportion every year


def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()


def main() -> int:
    if not PREDICTION.exists():
        print("Refusing to run: docs/locked-prediction.md does not exist.")
        return 1
    if BLANK_MARKER in PREDICTION.read_text(encoding="utf-8"):
        print("Refusing to run: the prediction still contains the blank template marker. Write your prediction first.")
        return 1
    if git("status", "--porcelain", "--", str(PREDICTION.relative_to(ROOT))):
        print("Refusing to run: commit docs/locked-prediction.md before execution.")
        return 1
    commit = git("log", "-1", "--format=%H", "--", str(PREDICTION.relative_to(ROOT)))
    commit_time = git("log", "-1", "--format=%cI", "--", str(PREDICTION.relative_to(ROOT)))

    inputs = load_inputs()
    before = value(inputs)
    after = value(with_changes(inputs, **{CHANGED_INPUT: NEW}))
    price = inputs["market"]["share_price"]["value"]

    def summary(v):
        rows = v["rows"]
        return {
            "value_per_share": v["value_per_share"],
            "enterprise_value": v["enterprise_value"],
            "revenue_2030": next(r["revenue"] for r in rows if r["year"] == 2030),
            "fcff_2030": next(r["fcff"] for r in rows if r["year"] == 2030),
            "cumulative_new_equity": sum(r["equity_raise"] for r in rows),
            "action": "Do not initiate" if v["value_per_share"] <= 0 else (
                "Initiate" if price <= 0.75 * v["value_per_share"] else "Watch / defer"),
        }

    result = {
        "prediction_commit": commit,
        "prediction_commit_time": commit_time,
        "run_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "changed_input": "Revenue per flight hour, all forecast years (USD per flight hour)",
        "old_value": "x1.0 ($2,500 in 2027, +2.5%/yr thereafter)",
        "new_value": "x0.8 ($2,000 in 2027, +2.5%/yr thereafter)",
        "before": summary(before),
        "after": summary(after),
    }
    out = ROOT / "output"
    out.mkdir(exist_ok=True)
    (out / "locked_test_result.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    b, a = result["before"], result["after"]
    md = [
        "# Locked changed-input test — preserved execution result", "",
        f"Prediction locked in commit `{commit}` at {commit_time}. Run at {result['run_utc']}.", "",
        f"Changed input: {result['changed_input']}: {result['old_value']} → {result['new_value']}. All other inputs unchanged.", "",
        "| Output | Before | After | Change |", "|---|---:|---:|---:|",
    ]
    for k in ("value_per_share", "enterprise_value", "revenue_2030", "fcff_2030", "cumulative_new_equity"):
        md.append(f"| {k} | {b[k]:,.2f} | {a[k]:,.2f} | {a[k] - b[k]:+,.2f} |")
    md += [f"| committee action | {b['action']} | {a['action']} | {'changed' if a['action'] != b['action'] else 'unchanged'} |", ""]
    (out / "locked_test_result.md").write_text("\n".join(md), encoding="utf-8")
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # same cp1252 console fix as analysis.py
    print("\n".join(md))
    return 0


if __name__ == "__main__":
    sys.exit(main())
