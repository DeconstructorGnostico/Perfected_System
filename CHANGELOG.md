# Changelog

## 1.1.0-en — 2026-11-15 (English edition)

- Full English translation of code identifiers, enum values, messages, comments, docstrings and docs (from the Spanish Sistema_Perfeccionado 1.1.0).
- Behavior unchanged: tests (unittest: 113 OK (2 adapter tests skip unless the Pure Agent v3 sibling folder is present)) and benchmarks/evaluations match the Spanish version case by case.
- Hardcoded `/workspace` paths replaced with relative paths (the v3 adapter uses the sibling folder `pure_agent_v3` or the `AGENT_PURE_V3_ROOT` variable).
- New freeze SHA-256 (alphabetical concatenation of `*.py`):
- `gnostic_axioms/*.py`: `40ba3ee6e67f4368ad69d3cc45282bc8c90ad4ab0e335370600e322dbe9a7d47`

## 1.1.0 — 14 November 2026 (America/Mazatlan)

The system consults the verified fact in memory when processing a request or document. Without knowledge responds `UNDETERMINED`. With knowledge, if the data contradicts a verified fact, it confirms that it is false (`CONTRADICTED` / `REFUTED`). That flag comes out by `request()`.

### Added

- Module `facts.py`: fact extraction, magnitude normalization (3 / "three" / 3.0, Romans, scientific notation, units, dates), verified memory query, session postulates, arithmetic checks and calendar.
- Session posts in `state.py` (`register_postulates`, `register_texts_session`). A document postulate is never written in memory or raised to `SUPPORTED`.
- Partition of clauses joined by "y" / "and" / "e" / "but" / comma, only when both sides seem to be preached.
- Domain checks: amounts that do not fit, percentages, averages, Debe/Haber, impossible dates (April 31, February 29th, not leap) and inverted chronology.
- 25 new tests in `tests/test_facts_v11.py`.
- `ARCHITECTURE.md`, PDF architecture and bank hold-out (`eval/`).

### Changed

- The interpreter receives memory, postulates and session texts, and calls `judge_affirmations`. Every branch of return, including `REJECTED`, carries `truths` (`_with_truths`).
- `system.py` does not degrade a `SUPPORTED` born of verified memory.
- The deconstructor no longer treats "report" / "open" within a statement as order, nor a bare equation (`2+2=5`) as `CALCULATE`.
- Antonimia amplified (Spanish and English, pairs of status).

### Guarantees not touched

- The document remains unverified, false evidence labels do not lift, hidden orders are blocked, the executor only runs with token, there is no encyclopedic basis for the invented world.

### Evidence

- 88 original tests: continue passing.
- 25 new tests: pass.
- Total: 113/113, plus demo 7/7.

## 1.0.0 — 14 November 2026

First public version: axioms, deconstructor, interpreter that only proposes, close list executor with token HMAC single-use, 88 tests and demo of 7 cases.
