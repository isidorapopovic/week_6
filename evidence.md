# Week 6 RAG evidence

Status: Technical evidence for Outcomes 1–5 completed on 2026-10-12. Pair contributions and demo lead await learner input; see [Task 05 report notes](docs/tasks/05-final-evidence-pair.md).

1. **Outcome 1: Chunking impact**
   - Config A: `chunk_size=140, overlap=30`; 6 chunks; top results `doc-2-chunk-0` (0.400000), `doc-2-chunk-1` (0.200000).
   - Config B: `chunk_size=80, overlap=20`; 9 chunks; top results `doc-2-chunk-1` (0.500000), `doc-2-chunk-0` (0.333333).
   - Retrieval difference summary: same query, default corpus, and top-k 2. A preserves the complete sentence about chunk size and overlap in its first result; B splits it and ranks a mid-word continuation first despite a higher lexical score. Retain A's defaults. Both exhibit word splits and duplicate context. [Full commands, retrieval text, CLI output, analysis, and passing test snapshot](docs/evidence/task-01-chunking-impact.md).
2. **Outcome 2: Top-k retrieval**
   - Query: `How do chunk size and overlap improve retrieval quality?`; default corpus; chunk size 140; overlap 30; minimum score 0.01.
   - Top-k output: k=2 returns `doc-2-chunk-0` (0.4), `doc-2-chunk-1` (0.2); k=3 additionally returns `doc-3-chunk-1` (0.2). [Full retrieval text, score calculations, reproducible command, and test evidence](docs/evidence/task-02-top-k-retrieval.md).
   - Why ranking is correct: scores decrease as 8/20, 1/5, 1/5, 2/18, 2/22 across the full eligible ranking. Equal scores retain input order. Top-2 and top-3 are prefixes of that ranking. Matches to `and` produce semantically weak results; this verifies lexical ranking, not universal relevance.
3. **Outcome 3: Citation quality**
   - Supported query: `Why are citations important in RAG?`; training-rag corpus; chunk size 220; overlap 30; top-k 1.
   - Answer with citations: `[tr-doc-1-chunk-0] RAG with citations should retrieve relevant documents with source metadata and include references in the answer. Citations improve transparency and trust because users can verify evidence.` [Full answer, CLI output, baseline comparison, and passing tests](docs/evidence/task-03-citation-quality.md).
   - Retrieved chunk IDs: `tr-doc-1-chunk-0` (score 0.153846). Inline ID, separate citations list, and complete source text agree; `Refused: False`.
4. **Outcome 4: Refusal behavior**
   - Unsupported query: `Who won the world cup in 1958?`; default corpus; chunk size 140; overlap 30; top-k 2. Also tested `Zanzibar population 2025?` with the same settings.
   - Retrieved context: World Cup returns `doc-1-chunk-0` (0.055556), `doc-3-chunk-0` (0.045455), matching only `the`; Zanzibar returns no chunks. [Full context, before/after evidence, commands, and tests](docs/evidence/task-04-refusal-behavior.md).
   - Refusal output: `I do not have enough grounded evidence in the provided corpus to answer that question.` Both cases return `Refused: True` and no citations after the common-word-only support check was added. This lexical guard does not prove semantic support for every accepted question.
5. **Outcome 5: Final evidence pair**
   - Supported case command + output:

     ```powershell
     python -m src.cli --corpus-profile training-rag --question "Why are citations important in RAG?" --chunk-size 220 --overlap 30 --top-k 1
     ```

     Full retrieval from the same configuration:

     ```text
     Retrieved count: 1
     Rank 1: tr-doc-1-chunk-0; score=0.153846
     Document: tr-doc-1; title: RAG with Citations
     Text: RAG with citations should retrieve relevant documents with source metadata and include references in the answer. Citations improve transparency and trust because users can verify evidence.
     ```

     CLI stdout:

     ```text
     Question:
     Why are citations important in RAG?

     Answer:
     Grounded response based on retrieved context:
     [tr-doc-1-chunk-0] RAG with citations should retrieve relevant documents with source metadata and include references in the answer. Citations improve transparency and trust because users can verify evidence.

     Corpus profile: training-rag

     Refused: False
     Citations: tr-doc-1-chunk-0
     ```

     Inline citation and separate list match the sole retrieved source exactly. The passage explicitly supports transparency, trust, and evidence verification. The 220/30, top-k 1 settings preserve the full explanation, as established in Task 03.

   - Unsupported case command + output:

     ```powershell
     python -m src.cli --corpus-profile default --question "Who won the world cup in 1958?" --chunk-size 140 --overlap 30 --top-k 2
     ```

     Full retrieval from the same configuration:

     ```text
     Retrieved count: 2
     Rank 1: doc-1-chunk-0; score=0.055556
     Document: doc-1; title: RAG Fundamentals
     Text: Retrieval augmented generation combines retrieval with text generation. The model should answer using retrieved evidence rather than unsuppo
     Rank 2: doc-3-chunk-0; score=0.045455
     Document: doc-3; title: Refusal Behavior
     Text: If retrieved context does not support a claim, the system should refuse and ask for better evidence. This reduces hallucinations and increas
     ```

     CLI stdout:

     ```text
     Question:
     Who won the world cup in 1958?

     Answer:
     I do not have enough grounded evidence in the provided corpus to answer that question.

     Corpus profile: default

     Refused: True
     Citations: None
     ```

     Neither RAG passage establishes a football winner. Matches are only to `the`, so the answer-stage content-word guard refuses even though raw retrieval is nonempty. Task 04 also records the empty-retrieval Zanzibar example and the initial World Cup failure.

## Final reproduction and test snapshot

Run from the repository root with the project Python environment active:

```powershell
python -m scripts.final_evidence
python -m pytest -q
```

The evidence runner prints both commands, complete retrieval metadata/text, and real CLI stdout. It exits with an error if expected refusal behavior, citation mapping, copied passages, or CLI/direct-output consistency fails. Both cases returned `Verification: PASS` on 2026-10-12 with Python 3.13.3.

Recorded complete-suite output:

```text
............................                                             [100%]
28 passed in 0.07s
```

Task 05 originally specified `python -m unittest discover -s tests -v`. That command was executed but reported `Ran 0 tests in 0.000s` and `NO TESTS RAN`, because this repository uses pytest functions. It is not evidence of passing tests; the pytest result above is the actual validation.

## Submission review

All five technical outcomes have recorded evidence, both case commands are explicit, and the test snapshot is preserved. [The original checklist](docs/homework-checklist.md) remains the submission guidance. Installation was not repeated: the existing Python environment successfully runs the app and tests. Learner understanding and personal contributions cannot be inferred from automated runs.

Known limits: character chunking can split words and duplicate context; lexical rankings can reward common words; cited text is copied rather than synthesized; the refusal guard checks content-word overlap rather than semantic entailment. Historical failure and correction are preserved in Task 04. Pair accountability and demo lead remain awaiting learner input.
