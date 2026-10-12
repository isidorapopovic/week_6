# Outcome 4: Refusal behavior

## Task

Verify that unsupported questions trigger refusal instead of unsupported answers, and explain why the evidence is insufficient.

## Repository behavior

`src/rag.py` refuses when retrieval is empty or the highest score is below `0.02`. The retrieval stage normally filters at `0.01`. Refusal uses `REFUSAL_MESSAGE`, an empty citations list, and `refused=True`.

These thresholds measure lexical overlap. They do not establish whether the context supports a claim. An unsupported question containing common corpus words may still be accepted. Record such failures honestly and fix them if needed; one successful refusal does not prove general refusal reliability.

## Procedure

Use a question with no expected lexical matches for a basic empty-retrieval check:

```powershell
python -m src.cli --corpus-profile default --question "Zanzibar population 2025?" --chunk-size 140 --overlap 30 --top-k 2
```

Also test the starter's suggested unsupported question, which may share common words with the corpus:

```powershell
python -m src.cli --question "Who won the world cup in 1958?" --chunk-size 140 --overlap 30 --top-k 2
python -m unittest discover -s tests -v
```

Use [Outcome 2's retrieval procedure](02-top-k-retrieval.md) for each question. Preserve any returned chunks and explain why they fail to establish the requested fact. If a question is accepted incorrectly, document it as a failure, review retrieval/refusal logic, and record the before-and-after behavior for any fix.

## Evidence worksheet

- Unsupported query: TODO
- Corpus and configuration: TODO
- Retrieved context (full IDs, scores, text, or explicit empty list): TODO
- Refusal output (verbatim): TODO
- `refused` value and citations: TODO
- Why evidence was insufficient: TODO
- Common-word unsupported case result and limitations: TODO
- Fixes and test output, if applicable: TODO

## Acceptance checks

- [ ] Selected unsupported evidence case refuses and contains no factual answer.
- [ ] Refusal is clear and citations are empty.
- [ ] Retrieval evidence is preserved, including empty retrieval.
- [ ] Any false acceptance is disclosed and investigated.
