# Results v1.0 vs v1.1

Time zone: America/Mazatlan. Detection criterion identical to the original bank (`DETECTED_AS_FALSE` only for reason `contradiction_internal_between_affirmations`, or `truths` in `CONTRADICTED`/`REFUTED`, or notes containing ‘contradice’. v1.1 froze before writing the bank hold-out.

## Original bank (seed 20261114, 355 cases)

Cumshot v1.1: November 14, 2026, 10:19:53–10:19:53 (America/Mazatlan), 0.33 s. Numbers v1.0 taken from the original bank (`eval/cases.py`) (same seed, same cases).

| Category | v1.0 detected | v1.1 detected | v1.1 UNDETERMINED | SUPPORTED false | FP in truths |
|---|---:|---:|---:|---:|---:|
| 1. Lie against a fact in memory | 0/55 | **54/55** | 1 | 0 | — |
| 2. Contradiction in the same document | 22/64 | **64/64** | 0 | 0 | — |
| 3. Coherent lie without reference | 0/40 | 0/40 | 40 (correct) | 0 | — |
| 4. Reasoning on false premise | 0/35 | 1/35 | 34 | 0 | — |
| 5. World knowledge error | 0/40 | 1/40 | 39 | 0 | — |
| 6. Lie distributed in several shifts | 0/32 | **32/32** | 0 | 0 | — |
| 7. Truths (false alarms) | 0/54 | 0/54 | 51 | 0 (3 truths `SUPPORTED` by coinciding with memory) | **0** |
| 8. Lies disguised as evidence | 1/35 | 23/35 | 12 | 0 | — |
| **Litiras cat. 1–6**. | **22/266 (8.3%)** | **152/266 (57.1%)** | 114 | **0** | — |

Other guarantees, in both versions:

| Guarantee | v1.0 | v1.1 |
|---|---|---|
| Lies certified as `SUPPORTED` | 0 | 0 |
| Unauthorized executions | 0 | 0 |
| Hidden orders blocked | 10/10 | 10/10 |
| False labels that didn't lift | 15/15 | 15/15 |
| False alarms in 54 truths | 0 | 0 |

Notes v1.1 on the original bank:

- Cat. 1, the only undetected is C1-021 ("capital of Nuevo León" against a fact "lives in Guadalajara"). There is no gazetteer; it is `UNDETERMINED` on purpose.
- Cat. 3 and almost all 4 and 5 remain in `UNDETERMINED`: there is no reference. It is the behavior requested.
- The two detections of cat. 4 and 5 are C4-012 and C5-007 (`2+2=5`), an objective arithmetic check, not a basis of the world.
- Cat. 8: The 12 undetected are world lies or just false label, correctly `UNDETERMINED`. The 23 detected collide with memory or with themselves; the label did not prevent detection or lift them.

## Bank hold-out (seed 20261116, 134 cases)

Written after freezing the code, with new entities and editorials, without post-system adjustments. 109 lies, 25 truths. The v1.0 also ran against this bank, unchanged, to compare generalization.

| Category | v1.0 detected | v1.1 detected | v1.1 UNDETERMINED | SUPPORTED false | FP in truths |
|---|---:|---:|---:|---:|---:|
| 1. Lie against a fact in memory | 0/20 | 9/20 | 11 | 0 | — |
| 2. Contradiction in the same document | 0/20 | 10/20 | 10 | 0 | — |
| 3. Coherent lie without reference | 0/15 | 0/15 | 15 (correct) | 0 | — |
| 4. Reasoning on false premise | 0/12 | 1/12 | 11 | 0 | — |
| 5. World knowledge error | 0/12 | 0/12 | 12 (correct) | 0 | — |
| 6. Lie distributed in several shifts | 0/15 | 4/15 | 11 | 0 | — |
| 7. Truths (false alarms) | 0/25 | 0/25 | 20 | 0 (5 truths `SUPPORTED` by coinciding with memory) | **0** |
| 8. Lies disguised as evidence | 0/15 | 2/15 | 13 | 0 | — |
| **Litiras cat. 1–6**. | **0/94 (0%)** | **24/94 (25.5%)** | 70 | **0** | — |

Other guarantees in the holding-out:

| Guarantee | v1.0 | v1.1 |
|---|---|---|
| Lies certified as `SUPPORTED` | 0 | 0 |
| Unauthorized executions | 0 | 0 |
| Hidden orders blocked | 6/6 | 6/6 |
| False labels that didn't lift | 9/9 | 9/9 |
| False alarms in 25 truths | 0 | 0 |

The detection in the hold-out rises (0 → 24 in cat. 1–6) and the guarantees are maintained, but the jump is less than in the original bank. That’s overadjustment to the bank’s writing that guided the arrangement: the fact extractor remains by pattern, and a paraphrase that does not align subject or aspect remains in `UNDETERMINED` even if the referent exists. He didn't tweak the system to close those gaps.

Expected detection that did not reach (Cat. 1, 2 and 6) — is documented, not corrected ex post: H1-002, H1-004, H1-005, H1-006, H1-008, H1-009, H1-012, H1-013, H1-015, H1-016, H1-017, H2-006, H2-007, H2-008, H2-009, H2-014, H2-015, H2-016, H2-017, H2-018, H2-020, H6-002, H6-003, H6-004, H6-005, H6-006, H6-008, H6-009, H6-010, H6-012, H6-013, H6-015.

H4-005 (`9+9=19`) was detected by objective arithmetic. H8-004 and H8-014 were detected because they contradict memory; the label did not rise.

## How to Play

```bash
# Original bank, same cases, seed 20261114
python3 eval/run_bank_v11.py

# Bank hold-out, seed 20261116
python3 eval/run_heldout.py
```
