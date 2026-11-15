# About this English edition

- Original (Spanish): https://github.com/DeconstructorGnostico/Sistema_Perfeccionado. It was not modified.
- Version: 1.1.0. Behavior is meant to match the Spanish version exactly.
- Tests: Spanish original unittest: 113 OK; English edition unittest: 113 OK (2 adapter tests skip unless the Pure Agent v3 sibling folder is present).
- Checked for equivalence: same pass/fail on every test, plus identical demo and benchmark/evaluation results case by case where the project has them.

## Stays in Spanish (by design)

`source.txt` (the architect's source text; tests check its SHA-256 and quote it), evaluation case banks (`eval/cases*.py`), Spanish fact base, lexicons and normalization tables, integrity citations of the source text, demo input sentences.

These are inputs the system is evaluated on, or bilingual detection data. Translating them would change the published numbers.

## Not included

generated PDF/PNG architecture diagrams (regenerate with `python docs/build_architecture.py`).

## Freeze hashes (English edition)

SHA-256 over the package's `*.py` files concatenated in alphabetical order:

- `gnostic_axioms/*.py`: `40ba3ee6e67f4368ad69d3cc45282bc8c90ad4ab0e335370600e322dbe9a7d47`
