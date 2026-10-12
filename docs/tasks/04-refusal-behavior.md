# Outcome 4: Refusal behavior

## Task

Verify that unsupported questions trigger refusal instead of unsupported answers, and explain why the evidence is insufficient.

## Repository behavior

`src/rag.py` refuses when retrieval is empty, the highest score is below `0.02`, or none of the retrieved chunks matches any question token after common grammatical/question words are removed. The retrieval stage normally filters at `0.01`. Refusal uses `REFUSAL_MESSAGE`, an empty citations list, and `refused=True`.

These thresholds measure lexical overlap. They do not establish whether the context supports a claim. An unsupported question containing common corpus words may still be accepted. Record such failures honestly and fix them if needed; one successful refusal does not prove general refusal reliability.

## Procedure

Use a question with no expected lexical matches for a basic empty-retrieval check:

```powershell
python -m src.cli --corpus-profile default --question "Zanzibar population 2025?" --chunk-size 140 --overlap 30 --top-k 2
```

Also test the starter's suggested unsupported question, which may share common words with the corpus:

```powershell
python -m src.cli --question "Who won the world cup in 1958?" --chunk-size 140 --overlap 30 --top-k 2
python -m pytest -q
```

Use [Outcome 2's retrieval procedure](02-top-k-retrieval.md) for each question. Preserve any returned chunks and explain why they fail to establish the requested fact. If a question is accepted incorrectly, document it as a failure, review retrieval/refusal logic, and record the before-and-after behavior for any fix.

## Completed evidence (2026-10-12)

- Unsupported queries: `Who won the world cup in 1958?` and `Zanzibar population 2025?`.
- Corpus and configuration: default; chunk size 140; overlap 30; top-k 2.
- Retrieved context: World Cup returns `doc-1-chunk-0` (0.055556) and `doc-3-chunk-0` (0.045455), matching only `the`. Zanzibar returns an empty list. [Full retrieval, commands, before/after outputs, and tests](../evidence/task-04-refusal-behavior.md).
- Refusal output for both: `I do not have enough grounded evidence in the provided corpus to answer that question.`
- Both return `refused=True` and `citations=[]`; CLI prints `Refused: True` and `Citations: None`.
- Insufficient evidence: corpus passages describe RAG and refusal, not football winners or Zanzibar population.
- Failure and fix: World Cup initially returned `refused=False` with irrelevant RAG text. Added a common-word exclusion check in the answer stage to reject retrieval with no content-word matches. Raw retrieval and rankings are unchanged.
- Limitation: a content-word match is still not proof of support. Unsupported questions sharing topic words with the corpus can still be accepted; paraphrases with no shared content words may be refused. No general semantic-entailment guarantee is claimed.
- Tests: `python -m pytest -q` — `28 passed in 0.13s`; added unsupported/empty/common-word cases, nonempty retrieval regression, low-score topic-match regression, and CLI refusal validation.

## Acceptance checks

- [x] Selected unsupported evidence case refuses and contains no factual answer.
- [x] Refusal is clear and citations are empty.
- [x] Retrieval evidence is preserved, including empty retrieval.
- [x] Any false acceptance is disclosed and investigated.
