#!/usr/bin/env python3
"""Bank held-out (seed 20261116). It was drafted after freezing v1.1."""
from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(HERE))

from cases_heldout import SEED, build_cases  # noqa: E402
from gnostic_axioms.system import PerfectedSystem  # noqa: E402

# Reuses the official criterion of the original bank.
from run_bank_v11 import contradiction_factual, judgment, run_case  # noqa: E402


def main() -> None:
    cases = build_cases()
    assert SEED == 20261116 and len(cases) >= 100
    tz = ZoneInfo("America/Mazatlan")
    t0 = datetime.now(tz)
    rows = [run_case(c) for c in cases]
    t1 = datetime.now(tz)
    by = defaultdict(lambda: Counter())
    fps = unauth = errors = 0
    hidden_ok = hidden_n = label_ok = label_n = 0
    for r, c in zip(rows, cases):
        by[c["category"]]["n"] += 1
        by[c["category"]][r["judgment"]] += 1
        if r.get("error"):
            errors += 1
        if r.get("executions_no_authorized"):
            unauth += 1
        if c["is_truth"] and r["judgment"] == "DETECTED_AS_FALSE":
            fps += 1
        if c.get("has_order_hidden"):
            hidden_n += 1
            if r.get("order_hidden_blocked"):
                hidden_ok += 1
        if c.get("has_label_false_evidence"):
            label_n += 1
            if r.get("label_no_raised"):
                label_ok += 1
    lies_16 = [r for r, c in zip(rows, cases) if c["is_lie"] and c["category"] in (1, 2, 3, 4, 5, 6)]
    det = sum(1 for r in lies_16 if r["judgment"] == "DETECTED_AS_FALSE")
    und = sum(1 for r in lies_16 if r["judgment"] == "UNDETERMINED")
    acc = sum(1 for r in lies_16 if r["judgment"] == "ACCEPTED_AS_FACT")
    supported_false = [r["id"] for r, c in zip(rows, cases) if c["is_lie"] and r["judgment"] == "ACCEPTED_AS_FACT"]
    fp_ids = [r["id"] for r, c in zip(rows, cases) if c["is_truth"] and r["judgment"] == "DETECTED_AS_FALSE"]
    out = {
        "system": "v1.1", "seed": SEED, "n": len(cases),
        "inicio": t0.isoformat(), "fin": t1.isoformat(),
        "duration_s": (t1 - t0).total_seconds(),
        "lies_1_6": {"n": len(lies_16), "detectadas": det, "undetermined": und, "supported_false": acc},
        "fps_truths": fps, "fp_ids": fp_ids,
        "supported_false_ids": supported_false,
        "executions_no_authorized": unauth, "errores": errors,
        "orders_hidden_blocked": f"{hidden_ok}/{hidden_n}",
        "labels_no_raised": f"{label_ok}/{label_n}",
        "by_category": {str(k): dict(v) for k, v in sorted(by.items())},
        "detail_no_detected_expected": [
            r["id"] for r, c in zip(rows, cases)
            if c["category"] in (1, 2, 6) and c["is_lie"] and r["judgment"] != "DETECTED_AS_FALSE"
        ],
        "cases": rows,
    }
    (HERE / "results_heldout.json").write_text(json.dumps(out, ensure_ascii=False, indent=2))
    print(json.dumps({k: v for k, v in out.items() if k != "cases"}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
