# Task 04: Refusal evidence

Executed on 2026-10-12 with Python 3.13.3. Default corpus, chunk size 140, overlap 30, top-k 2. No retrieval scoring, chunking, corpus, or CLI defaults changed.

## Initial failure

Before the answer-stage fix, this command incorrectly accepted a question outside the corpus:

```powershell
python -m src.cli --question "Who won the world cup in 1958?"
```

Recorded baseline stdout:

```text
Question:
Who won the world cup in 1958?

Answer:
Grounded response based on retrieved context:
[doc-1-chunk-0] Retrieval augmented generation combines retrieval with text generation. The model should answer using retrieved evidence rather than unsuppo
[doc-3-chunk-0] If retrieved context does not support a claim, the system should refuse and ask for better evidence. This reduces hallucinations and increas

Corpus profile: default

Refused: False
Citations: doc-1-chunk-0, doc-3-chunk-0
```

It did not invent a winner, but failed to refuse and presented unrelated context as an answer. Both passages match only `the`; scores exceed 0.02 despite containing no football evidence. The Zanzibar case already refused because retrieval was empty.

## Fix

In `src/rag.py`, remove common grammatical/question words from the question's token set and require at least one remaining token to match a retrieved chunk. If no such match exists, return the existing refusal message, empty citations, and `refused=True`. The existing empty-retrieval and below-0.02 checks remain.

This guard operates after raw retrieval, so Task 01 and Task 02 scores/rankings remain reproducible. It also preserves both citation cases tested in Task 03. It does not filter individual weak passages from an otherwise accepted result set.

## Full retrieval and final outputs

```powershell
python -m scripts.verify_refusal
```

Recorded stdout:

```text
Corpus: default; chunk_size: 140; overlap: 30; top_k: 2

Question: Who won the world cup in 1958?
Retrieved count: 2
Rank 1: doc-1-chunk-0; score=0.055556
Document: doc-1; title: RAG Fundamentals
Text: Retrieval augmented generation combines retrieval with text generation. The model should answer using retrieved evidence rather than unsuppo
Rank 2: doc-3-chunk-0; score=0.045455
Document: doc-3; title: Refusal Behavior
Text: If retrieved context does not support a claim, the system should refuse and ask for better evidence. This reduces hallucinations and increas
Answer: I do not have enough grounded evidence in the provided corpus to answer that question.
Refused: True
Citations: []

Question: Zanzibar population 2025?
Retrieved count: 0
Answer: I do not have enough grounded evidence in the provided corpus to answer that question.
Refused: True
Citations: []
```

The World Cup question's meaningful tokens (`won`, `world`, `cup`, `1958`) occur in neither retrieved passage. The Zanzibar question has no lexical matches at all. Neither case has source evidence for the requested fact.

## Final CLI commands and output

```powershell
python -m src.cli --question "Who won the world cup in 1958?" --chunk-size 140 --overlap 30 --top-k 2
```

```text
Question:
Who won the world cup in 1958?

Answer:
I do not have enough grounded evidence in the provided corpus to answer that question.

Corpus profile: default

Refused: True
Citations: None
```

```powershell
python -m src.cli --corpus-profile default --question "Zanzibar population 2025?" --chunk-size 140 --overlap 30 --top-k 2
```

```text
Question:
Zanzibar population 2025?

Answer:
I do not have enough grounded evidence in the provided corpus to answer that question.

Corpus profile: default

Refused: True
Citations: None
```

## Validation and limits

Added nine pytest cases including parameterized examples: World Cup, Zanzibar, Mars, common-word-only, empty, and punctuation-only questions; a regression where raw retrieval is nonempty and above the score threshold; a topic match below the answer threshold; and CLI refusal formatting. Existing supported-answer, citation, retrieval, chunking, and corpus tests remain passing.

```powershell
python -m pytest -q
```

```text
............................                                             [100%]
28 passed in 0.13s
```

This is a narrow lexical safeguard. One shared content word can still accept an unsupported question about a familiar topic; an unsupported detail is not checked for entailment. Conversely, synonymous wording with no shared tokens can be refused. These passing examples establish the documented behavior, not universal hallucination prevention. Semantic support evaluation would require a broader follow-up change.
