# Outcome 5: Final evidence pair

## Task

Document one supported and one unsupported question with reproducible commands, complete retrieval evidence, and actual output. Consolidate all outcomes into root-level `evidence.md` using the exact structure required by the README.

## Procedure

1. Finish [Outcomes 1–4](README.md) and choose cases with verified behavior.
2. Run each case with explicit corpus, chunk size, overlap, and top-k. Capture stdout verbatim.
3. Capture retrieval IDs, scores, titles, and complete chunk text using Outcome 2's procedure with exactly the same case settings. The CLI alone does not print full retrieval diagnostics.
4. Run `python -m pytest -q` and preserve the output. The original unittest command discovers zero tests in this pytest-based repository.
5. Fill `evidence.md` below, then check [the submission guidance](../homework-checklist.md).

Suggested case commands (verify results before using them as evidence):

```powershell
python -m src.cli --corpus-profile training-rag --question "Why are citations important in RAG?" --chunk-size 220 --overlap 30 --top-k 1
python -m src.cli --corpus-profile default --question "Who won the world cup in 1958?" --chunk-size 140 --overlap 30 --top-k 2
```

## Completed final evidence

[Root evidence.md](../../evidence.md) now contains the exact five-outcome structure, completed evidence fields, and full final-pair command/output blocks. Detailed Outcomes 1–4 remain linked for their complete historical experiments.

Run `python -m scripts.final_evidence` from the repository root to reproduce the final pair's scored retrieval and actual CLI stdout. Both cases passed consistency checks. Supported settings preserve the complete citation explanation from Task 03; the unsupported case demonstrates refusal with nonempty but irrelevant retrieval from Task 04. The empty-retrieval Zanzibar case remains documented there.

## Report preparation notes

- Test command and output snapshot: `python -m pytest -q` — `28 passed in 0.07s`, recorded in root evidence. Original unittest command was also executed and reported zero tests; it is not treated as validation.
- Final source commit: recorded in `docs/evidence/final-source-state.md` after committing the evidence runner and completed technical work.
- Member 1 contribution: awaiting learner-provided name and contribution.
- Member 2 contribution: awaiting learner-provided name and contribution, or confirmation that this was individual work.
- Designated demo lead: awaiting learner input.
- What was learned: smaller chunks can increase lexical scores while losing sentence context; top-k is ordered by matching-token density with stable ties; citations must match actual retrieved text and IDs; raw overlap does not establish answer support, so common-word-only matches must refuse.
- Remaining limitations: broken words and duplicate context, weak lexical matches, extractive rather than synthesized answers, and refusal based on content-word matching rather than entailment. Task 04 records the original World Cup false acceptance and its fix. No personal reflections or contributions were inferred.

## Acceptance checks

- [x] Both cases include question, exact configuration, full retrieval, and output.
- [x] Supported case includes verified citations; unsupported case includes refusal.
- [x] Commands reproduce the evidence from the recorded source state.
- [x] `evidence.md` contains all five required sections without unfilled TODOs.
- [ ] Test snapshot, pair contributions, and demo lead are recorded.

Technical evidence and the test snapshot are complete. The final checkbox remains open only because pair contributions and the demo lead require learner input.
