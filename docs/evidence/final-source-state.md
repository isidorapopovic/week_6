# Final tested source state

- Technical evidence/source commit: `d0432a34023055be4ec0e72f921e244a0e71cde5` (`Complete task 05 reproducible final evidence pair`). Recorded with `git rev-parse HEAD` after committing the completed technical work.
- Application behavior: includes Task 04's content-word refusal guard; Task 05 adds an evidence runner and documentation only.
- Validation date: 2026-10-12; Python 3.13.3.
- Evidence runner: `python -m scripts.final_evidence` — both cases returned `Verification: PASS`.
- Complete test suite: `python -m pytest -q` — `28 passed in 0.07s`.
- Full evidence and stdout: [root evidence.md](../../evidence.md).

This source-state note is added in a subsequent documentation-only commit so the technical revision can be recorded without a self-referential commit hash. The tested application, tests, and evidence runner are identical to the recorded revision.

Pair-member names, contributions, and demo lead remain awaiting learner input. The technical submission evidence is complete; the personal report-accountability fields are not yet complete.
