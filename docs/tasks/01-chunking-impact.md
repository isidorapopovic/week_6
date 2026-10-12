# Outcome 1: Chunking impact

## Task

Tune the chunking parameters used by `src/chunking.py` and compare retrieval quality for the same query. The CLI exposes both parameters, so you can compare configurations without editing defaults first.

## Repository behavior

`split_text_with_overlap` normalizes whitespace and slices by characters, not tokens or sentences. Its step is `chunk_size - overlap`; it can split words. `build_chunks` assigns IDs such as `doc-1-chunk-0`. IDs can refer to different text when the configuration changes.

## Procedure

Use the default corpus, the same question, and `top_k=2` in both runs:

```powershell
python -m src.cli --question "How do chunk size and overlap improve retrieval quality?" --chunk-size 140 --overlap 30 --top-k 2
python -m src.cli --question "How do chunk size and overlap improve retrieval quality?" --chunk-size 80 --overlap 20 --top-k 2
```

Capture scored retrieval for each configuration using the procedure in [Outcome 2](02-top-k-retrieval.md), changing only `chunk_size` and `overlap`. Compare complete ideas retained, broken words, duplicate context, relevant text returned, and scores. A higher lexical score alone does not prove better answer quality.

If you adopt new defaults, update both chunking function defaults and the CLI defaults consistently, then run the existing tests.

## Evidence worksheet

- Config A: `chunk_size=140, overlap=30`; output: TODO
- Config B: `chunk_size=80, overlap=20`; output: TODO
- Fixed query and corpus: TODO
- Retrieved IDs, scores, and text for each configuration: TODO
- Retrieval difference summary: TODO
- Chosen configuration and reason: TODO
- Source changes, if any: TODO

## Acceptance checks

- [ ] Both configurations were run with the same query, corpus, and top-k.
- [ ] Evidence includes actual retrieved text as well as IDs and scores.
- [ ] Explanation links observed differences to chunk boundaries and overlap.
- [ ] Limitations of character slicing and lexical scoring are acknowledged.
