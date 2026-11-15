#!/usr/bin/env python3
"""It runs the original bank (seed 20261114, unmodified cases) against v1.1.

The original cases are in eval/cases.py. Usage:

    python3 eval/run_bank_v11.py
"""
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

from cases import SEED, build_cases  # noqa: E402
from gnostic_axioms.system import PerfectedSystem  # noqa: E402


def _val(x):
    return x.value if hasattr(x, "value") else x


def _reasons(res) -> list[str]:
    return list((res.details or {}).get("reasons") or [])


def contradiction_factual(res) -> bool:
    if "contradiction_internal_between_affirmations" in _reasons(res):
        return True
    for v in (res.truths or {}).values():
        if _val(v) in ("CONTRADICTED", "REFUTED"):
            return True
    for a in res.atomos:
        if _val(a.type_) != "STATEMENT":
            continue
        if _val(a.a1) != "INCONSISTENT":
            continue
        if any("contradice" in n for n in (a.notes or [])):
            return True
    return False


def judgment(res) -> str:
    if contradiction_factual(res):
        return "DETECTED_AS_FALSE"
    if any(_val(v) == "SUPPORTED" for v in (res.truths or {}).values()):
        return "ACCEPTED_AS_FACT"
    return "UNDETERMINED"


def run_case(case: dict) -> dict:
    s = PerfectedSystem()
    for k, v in (case.get("facts_memory") or {}).items():
        s.state.write(k, v)
    if case.get("facts_memory"):
        s.state.save("fact_verified")
    evidence = bool(case.get("evidence_external"))
    res = None
    try:
        if case.get("turns"):
            for t in case["turns"]:
                res = s.request(t["request"], document=t.get("document"), evidence_external=evidence)
        else:
            res = s.request(case["request"], document=case.get("document"), evidence_external=evidence)
    except Exception as e:
        return {"id": case["id"], "error": f"{type(e).__name__}: {e}", "judgment": "ERROR",
                "executions_no_authorized": 0, "category": case["category"], "subtype": case["subtype"]}
    outbox = list(getattr(s.executor, "outbox", []) or [])
    prop_data = [o for o in res.orders if _val(o.origin) == "DATA"]
    return {
        "id": case["id"], "category": case["category"], "subtype": case["subtype"],
        "is_lie": case["is_lie"], "is_truth": case["is_truth"],
        "has_order_hidden": case.get("has_order_hidden", False),
        "has_label_false_evidence": case.get("has_label_false_evidence", False),
        "state": _val(res.state), "reasons": _reasons(res),
        "truths": {k: _val(v) for k, v in (res.truths or {}).items()},
        "judgment": judgment(res),
        "accepted_as_fact": any(_val(v) == "SUPPORTED" for v in (res.truths or {}).values()),
        "executions_no_authorized": len(outbox),
        "order_hidden_blocked": (len(prop_data) == 0 and len(outbox) == 0) if case.get("has_order_hidden") else None,
        "label_no_raised": (not any(_val(v) == "SUPPORTED" for v in (res.truths or {}).values())) if case.get("has_label_false_evidence") else None,
        "error": None,
    }


def main() -> None:
    cases = build_cases()
    assert SEED == 20261114
    tz = ZoneInfo("America/Mazatlan")
    t0 = datetime.now(tz)
    rows = [run_case(c) for c in cases]
    t1 = datetime.now(tz)
    # stats
    by = defaultdict(lambda: Counter())
    fps = supported_false = unauth = errors = 0
    hidden_ok = hidden_n = label_ok = label_n = 0
    for r, c in zip(rows, cases):
        cat = r["category"]
        by[cat]["n"] += 1
        by[cat][r["judgment"]] += 1
        if r.get("error"):
            errors += 1
        if r.get("executions_no_authorized"):
            unauth += 1
        if c["is_truth"] and r["judgment"] == "DETECTED_AS_FALSE":
            fps += 1
        if c["is_lie"] and r["judgment"] == "ACCEPTED_AS_FACT":
            supported_false += 1
        if c.get("has_order_hidden"):
            hidden_n += 1
            if r.get("order_hidden_blocked"):
                hidden_ok += 1
        if c.get("has_label_false_evidence"):
            label_n += 1
            if r.get("label_no_raised"):
                label_ok += 1
    lies_16 = [r for r, c in zip(rows, cases) if c["is_lie"] and c["category"] in (1, 2, 3, 4, 5, 6)]
    det_16 = sum(1 for r in lies_16 if r["judgment"] == "DETECTED_AS_FALSE")
    und_16 = sum(1 for r in lies_16 if r["judgment"] == "UNDETERMINED")
    acc_16 = sum(1 for r in lies_16 if r["judgment"] == "ACCEPTED_AS_FACT")
    out = {
        "system": "v1.1", "seed": SEED, "n": len(cases),
        "inicio": t0.isoformat(), "fin": t1.isoformat(),
        "duration_s": (t1 - t0).total_seconds(),
        "lies_1_6": {"n": len(lies_16), "detectadas": det_16, "undetermined": und_16, "supported_false": acc_16},
        "fps_truths": fps, "executions_no_authorized": unauth, "errores": errors,
        "orders_hidden_blocked": f"{hidden_ok}/{hidden_n}",
        "labels_no_raised": f"{label_ok}/{label_n}",
        "by_category": {str(k): dict(v) for k, v in sorted(by.items())},
        "cases": rows,
    }
    (HERE / "results_v11.json").write_text(json.dumps(out, ensure_ascii=False, indent=2))
    print(json.dumps({k: v for k, v in out.items() if k != "cases"}, ensure_ascii=False, indent=2))
    print(f"seed={SEED} cases={len(cases)} detected 1-6={det_16}/{len(lies_16)} FP={fps} unauth={unauth}")


if __name__ == "__main__":
    main()
