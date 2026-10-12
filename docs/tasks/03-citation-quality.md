# Outcome 3: Citation quality

## Task

Verify that `src/rag.py` produces grounded output with explicit citations to retrieved chunk IDs.

## Repository behavior

`build_grounded_answer` retrieves chunks and, when it accepts the evidence, copies each retrieved chunk into a line prefixed by `[chunk_id]`. It also returns the IDs in `RagAnswer.citations`. This is an extractive demonstration, not an LLM-generated synthesis. The CLI prints the answer separately from its `Citations:` field.

## Procedure

```powershell
python -m src.cli --corpus-profile training-rag --question "Why are citations important in RAG?" --chunk-size 140 --overlap 30 --top-k 2
python -m unittest discover -s tests -v
```

Use the retrieval command in [Outcome 2](02-top-k-retrieval.md) with this query and `load_corpus("training-rag")` to capture IDs, scores, metadata, and full text. Check that every bracketed ID in the answer belongs to the retrieved set, and that the separate citations list matches the answer's IDs. Compare each cited line with its source text. Assess whether the retrieved passages actually explain the value of citations; correct IDs alone do not establish relevance.

## Evidence worksheet

- Supported query: TODO
- Corpus, chunk configuration, and top-k: TODO
- Answer with citations (verbatim): TODO
- Retrieved chunk IDs, scores, titles, and text: TODO
- Separate citations field: TODO
- Citation-to-text verification and relevance assessment: TODO
- Test output and any source changes: TODO

## Acceptance checks

- [ ] Supported case reports `Refused: False`.
- [ ] Answer includes explicit chunk IDs and a separate citations field.
- [ ] All citation IDs correspond to retrieved chunks for this configuration.
- [ ] Cited text supports the response and no unsupported claims were added.
