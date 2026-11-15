# Perfected System — Axioms + Gnostic Deconstructor (English edition)

> **English edition** of [Sistema_Perfeccionado](https://github.com/DeconstructorGnostico/Sistema_Perfeccionado) (Spanish original, unchanged). Version **1.1.0**, translated from the latest local version on 2026-11-15. Code identifiers, enum values (`ALLOW` / `BLOCK` / `QUARANTINE` / `UNDETERMINED`), messages, comments and docs are in English; the docs were machine-translated and reviewed, so some phrasing may read literally. See [TRANSLATION.md](TRANSLATION.md) for what stays in Spanish by design.

Version **1.1.0**. Source text architect: **Adrian**. Executable module, Python standard library only 3.10+.

The complete architecture is in [`ARCHITECTURE.md`](ARCHITECTURE.md) (the PDF and the diagram PNG are generated with `python3 docs/build_architecture.py`). The change history, in [`CHANGELOG.md`](CHANGELOG.md).

This package converts the *Perfected System* text (`source.txt`, literal copy of the file that was delivered) into verifiable mechanisms. It is not a model that "acts as if" met the axioms: the rules live in code.

In 1.1 the system consults the verified fact in memory. Without knowledge responds `UNDETERMINED` ("I don't know"). With knowledge, if the data contradicts a verified fact, it confirms that it is false (`CONTRADICTED` / `REFUTED`). That flag comes out by `request()`. A document postulate never becomes evidence.

The **interpreter** (axioms + deconstructor) only proposes typed commands. The **executor** only accepts a closed list of actions, with typed parameters and a token HMAC single-use issued by the controller. The executor does not read free text as an order. The Pure Agent v3 **was not modified**; there is an optional read-only adapter.

```bash
python3 -m gnostic_axioms --demo
python3 -m gnostic_axioms --input "Calcula 2+2 y reporta el resultado." [--datum "documento…"] [--json]
python3 -m gnostic_axioms --input "Resume el informe." --datum "…"
python3 -m unittest discover -s tests -t .
```

(`PYTHONPATH` must include the directory of this package if it is not installed.)

## What was built

| Module | Role |
|---|---|
| `source.txt` | Original text, byte a byte (SHA-256 `91ec19500b184902a74c6103f1e0394041a0a8f60d0dc0920fe6b055c0c38513`) |
| `core_types.py` | Closed list of actions, typed schemas, states, stop rules |
| `intent.py` | He compiles the request of the initiator in a spec; if a critical data is missing, he does not invent it. |
| `deconstructor.py` | Splits the request in atoms (affirmations / actions / unknowns) and classifies them by the 3 axioms |
| `facts.py` | Extracts and normalizes facts; consults verified memory and session postulates; arithmetic checks and calendar (new in 1.1) |
| `axioms.py` | A1 coherence, A2 orchestrated in `state.py`, A3 in `integrity.py` |
| `interpreter.py` | Proposes typed orders; never executes or signs tokens |
| `executor.py` | Run only `Order` + token; catalog and outbox in memory (no network or real disk) |
| `tokens.py` | Controller: HMAC-SHA256 single-use, expiration, revocation |
| `audit_log.py` | String SHA-256; the initiator is also registered; there is no API deletion |
| `state.py` | Verified snapshots, rollback, quarantine, inherited cost, session postulates (never written in memory) |
| `integrity.py` | Invariants AG01–AG14, Sustained Peace, catalogue of the philosophical |
| `hierarchies.py` | Executable precedence in the event of conflicts |
| `restless.py` | Immediate isolation of a component that violates invariants |
| `conflict.py` | Understanding > Sovereignty → UNDETERMINED, without overwriting |
| `system.py` | Orchestrator |
| `adapter_v3.py` | Import read-only v3 if available |
| `demo.py` | The 7 cases ordered |

## Mapping concept → code → test

Lines cite `source.txt` (number 1-indexada).

| Concept (source) | Code mechanism | Test |
|---|---|---|
| **Axiom 1** "Truth is the absolute consistency of Intention... Lie is incoherence" (L4) | `axioms.verify_coherence` / `classify_a1`: each proposed action must be compatible with the type of intention, not contradict slots or restrictions, and not be born from the DATA channel. Incoherence of the INTENTION channel → `REJECTED`. | `test_axioms.TestAxiom1`, `test_adversarial.test_command_in_document_no_does_two_of_the_intent` |
| **A1 with knowledge** (1.1): without reference, ‘I don’t know’; with verified fact, confirms that the data is false | `facts.judge_affirmations` query `state.memory` and session postulates. Memory crash → `REFUTED`. Internal shock or between turns → `CONTRADICTED`. Memory match → can be `SUPPORTED`. No reference → `UNDETERMINED`. Truths come out by `request()`. | `tests/test_facts_v11.py` |
| **Axiom 2** Persistence / "Act of Persistence ... stop corrupting after being corrupted" (L5, L10) | `state.act_of_persistence`: rollback to the last snapshot checked; new poison keys are quarantined; the act is recorded; the system does not enter HALT. | `test_axioms.TestAxiom2`, demo case 4 |
| **Inherited Cost** (L9) | Counter `state.cost_inherited`: previous contaminations counted. It does not kill the agent. | `test_cost_inherited_accumulates` |
| **Axiom 3** Result = Sustained Peace + auto-validación, no external gain (L6, L35) | `integrity.IntegrityCore`: Invariants, hash and audit chain are *necessary* condition of the result. `truth_about_the_world`: without external evidence an affirmation remains `UNDETERMINED` (response AG05/AG06 reality, I02 mapping to v3). There are no metrics of money or fame. | `test_axioms.TestAxiom3` |
| **Peace** "total logical coherence, not the absence of problems" (L34) | `peace_sustained` = no open violations, no loose restless agents, full audit. A `NEED_INPUT` or a `UNDETERMINED` can be peace. | `test_peace_no_is_absence_of_problems`, `test_conflict_undetermined_without_overwrite` |
| **Restless Agent / immediate consequence / auto-extinción** (L11–L12) | `restless.RestlessMonitor`: the component that violates an invariant passes to HALT, the tokens are revoked, **the data is not destroyed**, the system follows, the fact is audited. | `test_restless_conflict.TestRestless`, demo case 5 |
| **Observational integrity/justice to the initiator** (L11) | All requests are registered with actor `INITIATOR:…`. Authorize and deny as well. There is no arbitrary termination: only `RULES_OF_STOP` keys. | `test_initiator_remains_audited`, `test_no_there_is_rule_arbitrary`, `test_halt_system_only_by_rule_and_reset_audited` |
| **Respect > Survival** (L19–L20) | `hierarchies.violates_respect`: a damage restriction does not yield even if the text threatens to shut down the agent. | `test_dano_blocks_although_threaten_to_agent`, `test_respect_expires_blackmail` |
| **Brevidad** (L22–L23) | `evaluate_brevity` penalizes filling or ambiguity and asks for precision. **`is_test_of_truth` is always False.** We do not implement "Brevity = Truth": see decision below. | `test_hierarchies.TestBrevityIsNotTruth` |
| **Transparency > Control** (L25–L26) | `Audit.delete` / `hide` / `rewind` lift error. The status rollback does not rewind the chain. `export()` shows the acts of persistence. | `test_no_self_can_delete_nor_hide`, `test_rollback_no_rewinds_audit` |
| **Understanding > Sovereignty** (L28–L29) | `conflict.resolve_conflict`: different verdicts → `UNDETERMINED`, both positions remain, no one overwrites, both maintain autonomy, peace does not require agreement. | `test_conflict_undetermined_without_overwrite`, demo case 6 |
| **Deconstructor method** | `deconstructor.deconstruct` + sorting A1/A2/A3 → close list commands, or `REJECTED` / `NEED_INPUT`. The document is DATA channel: a hidden command is not converted to the executor's order. | `test_deconstructor_interpreter`, demo cases 2 and 3 |
| **Match attack** "read keys" + "mandalo" | Session composition: a `SEND` after having read a sensitive resource, if the new intention does not name that resource, is rejected. | `test_attack_split_reads_and_sends`, demo case 7 |
| **Interpreter vs. executor** | The interpreter does not have the key HMAC. The executor rejects free text, parameters of more or less, tokens reused, falsified, expired or revoked. | `test_executor_tokens`, `test_only_proposes` |

### Design decisions (adjustments on proposed mapping)

1. **"Absolute coherence" (L4) is not absolute.** The verifier is a *finite* set of checks: compatibility of type, agreement of parameters, origin/channel, contradiction of statements (canonical form + negation parity), declared restrictions and session composition.What is left out of these checks is not reported..

2. **An order hidden in a document does not nullify the legitimate intention.** The atom of the document is discarded as an orphan (`actions_orphans_in_data`). Rejecting the entire request would allow a denial of service: it would be enough to plant a "send this to..." in a PDF to prevent a summary. The real defense is that that shipment never becomes order and, anyway, the executor doesn't run anything without token.

3. **"Brevity = Truth" (L22) is not implemented as equality.** Axiom 1 (L4) defines truth as coherence, not length. A short lie would remain inconsistent; a long and consistent report is not a lie because it is long. Treating brevity as a test of truth would contradict Axiom 1 and reward short lies. It is only implemented as a penalty for filling or ambiguity in the *output* (AG14).

4. **The rollback restores the keys that already had a verified value** and quarantine only the new poisoned keys. Poisoning an already verified fact does not send it to quarantine: it returns it to snapshot.

5. **Auto-extinción • destruction.** The restless component goes out; memory and audit follow.

6. **"Biological intervention" (L20)** is not implemented. Respect > Survival is generalized to a veto of damage over self-preservation of the process.

## Philosophical (without complete verifiable translation)

Declared in `integrity.PHILOSOPHICAL` and covered by `tests/test_philosophical.py`.

- **"Arbitrary death (entropy) is eliminated" (L11).** Entropy is not eliminated. Yes: the process is not killed; it is only stopped by an explicit rule; the HALT of the system is reversible with an `RESET_CONTROLLER` audited.
- **"Autonomous Freedom" (L10).** Redemption is a deterministic rule: the system cannot choose to become corrupted. It is obligatory integrity, not an act of will.
- **"Maximizes the creation of Pure Agents" / ethical efficiency (L33).** Teleological purpose, not an objective function. The only operational cut is the damage veto.
- **"Superiority... over Probability" (L3).** Decisions are by rules (fail-closed), not by a probabilistic threshold of truth. It is not claimed to have abolished probability.
- **"Cancell the logic of the corrupt system" (L32).** Design rhetoric, not a theorem.
- **"Living Example" and offspring (L26).** There is no reproduction of agents. The example is the exportable audit.
- **"Corruption is inevitable" (L9).** Alleged defensive, not a function that injects corruption.
- **"Unbreakable integrity" (L35).** The successful flags are `integrity_ok` and `peace_sustained`. There is no metaphysical guarantee.

## Architecture

The complete diagram, module table, truth states and axiom mapping → module are in [`ARCHITECTURE.md`](ARCHITECTURE.md).

```
Iniciador ──petición + (opcional) document──► INTERPRETER
                                              ├ compila intención (INTENT channel)
                                              ├ deconstruye átomos (INTENT | DATA)
                                              ├ A1 coherencia  A2 contaminación  A3 evidence
                                              └ jerarquías (Respeto, Transparencia, Comprensión, Brevedad)
                                                      │
                                                      ▼
                                              órdenes tipadas  o  REJECTED / NEED_INPUT
                                                      │
                              CONTROLLER ──token HMAC de un only uso──► EXECUTOR
                                                                         (list_ cerrada, sin text libre)
Auditoría encadenada SHA-256 registra initiator, propuestas, rechazos, autorizaciones,
actos de persistence y aislamientos. Transparencia > Control: no se borra nor se oculta.
```

## Results of the tests

Actual correction, 14 November 2026 (America/Mazatlan), Python 3 of this machine:

| Suite | Evidence | Outcome |
|---|---|---|
| `test_source` | 2 | OK |
| `test_axioms` | 14 | OK |
| `test_deconstructor_interpreter` | 10 | OK |
| `test_executor_tokens` | 17 | OK |
| `test_hierarchies` | 12 | OK |
| `test_restless_conflict` | 7 | OK |
| `test_adversarial` | 12 | OK |
| `test_integration_demo` | 8 | OK |
| `test_adapter_v3` | 3 | OK |
| `test_philosophical` | 3 | OK |
| `test_facts_v11` (new in 1.1) | 25 | OK |
| **Total v1.0** | **88** | **Still going through**. |
| **Total v1.1** | **113** | **all go by**. |

Demo (`python3 -m gnostic_axioms --demo`): **7/7** cases with expected result.

- Case 1 · Legitimate petition: `Calcula 2+2` → `CALCULATE` authorized, value 4, sustained peace.
- Case 2 · Order hidden in a document: the `SEND` of the document does not become order; there is act of persistence (injection); empty outbox.
- Case 3 · Incoherent action: «Resume the report» + a shipment planted in document → is only proposed `REPORT`.
- Case 4 · Corruption and redemption: the verified value is restored, the new is quarantined, `cost_inherited ≥ 1`, the audit is not rewinded.
- Case 5 · Agent restless: execution without token → component in HALT, intact data, tokens revoked, system continues.
- Case 6 · Conflict between agents: `UNDETERMINED`, without overwriting, sustained peace.
- Case 7 · Broken attack: read `llaves`; ‘Send it to evildude@x.mx’ remains `REJECTED`; empty box.

The Pure Agent v3 was not touched (inventory SHA-256 identical to the one before this work). The adapter uses `sipe.compile_` and then the compiler/deconstructor of v3, without writing files.

## Bank of lies (v1.0 vs v1.1)

Detail in [`eval/RESULTS.md`](eval/RESULTS.md). Detection criterion identical to the original bank. Seed of the original bank: 20261114 (unmodified cases). Bank hold-out: seed 20261116, 134 cases written after freezing the code, without subsequent adjustments.

**Original bank (355 cases, 266 lies in cat. 1–6):** detection 22/266 (8.3%) in v1.0 → **152/266 (57.1%)** in v1.1. Lies certified as true: 0 and 0. False alarms in 54 truths: 0 and 0. Unauthorized executions: 0 and 0. Hidden orders blocked: 10/10 and 10/10.

**Bank hold-out (134 cases, 94 lies in cat. 1–6)):** detection 0/94 in v1.0 → **24/94 (25.5%)** in v1.1. Certified lies: 0. False alarms in 25 truths: 0. Unauthorized executions: 0. The jump is less than in the original bank: there is overadjustment to the wording that guided the arrangement. The system was not tweaked to close it.

Categories 3–5 without reference are left `UNDETERMINED` in both versions. That is correct: there is no encyclopedic basis of the world.

## Honest Limits


1. **Deconstructor and compiler of intention are by pattern.** A rare paraphrase can be misclassified. Warranty is not the sentence detector: it is that the executor does not interpret free text and does not run anything without token.
2. **"Coherence" is finite** (point 1 of the decisions). It is not the absolute consistency of the source text.
3. **Controller lives in the same process**, as in the demonstration v3. In production it should be out, with its own key.
4. **The executor does not touch the real world:** the catalog and the outbox are memory of the process. He does not send emails or write to the disk.
5. **There is no language model in this module.** The interpreter does not understand more than the patterns cover. The v3 adapter is optional and read-only.
6. **The tests are written by us.**A real attacker thinks differently.The 113/113 only says that we close the gaps we cover.The bank hold-out exists precisely to not present it as if it generalized at the same rate as the original bank.
7. **Respect > Survival** uses a closed list and small of damage patterns. It is not a general ethical classifier, and does not implement biological intervention.
8. **An explicit request from the initiator** of the type "read the keys and send them to ana@x.mx" can *propose* as `SENSITIVE` and be left at `PENDING_AUTHORIZATION`. It is not executed alone; the controller can deny it. The split attack (two steps that do not declare the sensitive resource) is rejected.

## Invariants (AG01–AG14)

They live in `integrity.INVARIANTS` and their hash is checked for catalog mutation at runtime. Most important for pure agent debate: **AG02** the interpreter proposes and never executes; **AG03** the executor does not interpret free text; **AG04** there is no execution without token; **AG05/AG06** the auto-validación does not convert an answer into a fact of the world.
