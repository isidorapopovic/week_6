# Outcome 5: Final evidence pair

## Task

Document one supported and one unsupported question with reproducible commands, complete retrieval evidence, and actual output. Consolidate all outcomes into root-level `evidence.md` using the exact structure required by the README.

## Procedure

1. Finish [Outcomes 1–4](README.md) and choose cases with verified behavior.
2. Run each case with explicit corpus, chunk size, overlap, and top-k. Capture stdout verbatim.
3. Capture retrieval IDs, scores, titles, and complete chunk text using Outcome 2's procedure with exactly the same case settings. The CLI alone does not print full retrieval diagnostics.
4. Run `python -m unittest discover -s tests -v` and preserve the output.
5. Fill `evidence.md` below, then check [the submission guidance](../homework-checklist.md).

Suggested case commands (verify results before using them as evidence):

```powershell
python -m src.cli --corpus-profile training-rag --question "Why are citations important in RAG?" --chunk-size 140 --overlap 30 --top-k 2
python -m src.cli --corpus-profile default --question "Zanzibar population 2025?" --chunk-size 140 --overlap 30 --top-k 2
```

## Required `evidence.md` structure

Copy this structure and replace TODOs with measured results. Include fenced code blocks for commands and outputs inside the relevant bullets.

1. **Outcome 1: Chunking impact**
   - Config A: TODO
   - Config B: TODO
   - Retrieval difference summary: TODO
2. **Outcome 2: Top-k retrieval**
   - Query: TODO
   - Top-k output: TODO (both k=2 and k=3, IDs, scores, and text)
   - Why ranking is correct: TODO
3. **Outcome 3: Citation quality**
   - Supported query: TODO
   - Answer with citations: TODO
   - Retrieved chunk IDs: TODO
4. **Outcome 4: Refusal behavior**
   - Unsupported query: TODO
   - Retrieved context: TODO
   - Refusal output: TODO
5. **Outcome 5: Final evidence pair**
   - Supported case command + output: TODO (include full retrieval evidence)
   - Unsupported case command + output: TODO (include full retrieval evidence)

## Report preparation notes

- Test command and output snapshot: TODO
- Final source commit (`git rev-parse HEAD` after committing completed work): TODO
- Member 1 contribution: TODO
- Member 2 contribution: TODO
- Designated demo lead: TODO
- What was learned about chunking, ranking, citations, and refusal: TODO
- Remaining limitations and failed cases: TODO

## Acceptance checks

- [ ] Both cases include question, exact configuration, full retrieval, and output.
- [ ] Supported case includes verified citations; unsupported case includes refusal.
- [ ] Commands reproduce the evidence from the recorded source state.
- [ ] `evidence.md` contains all five required sections without unfilled TODOs.
- [ ] Test snapshot, pair contributions, and demo lead are recorded.
