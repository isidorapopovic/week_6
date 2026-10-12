# Week 6 Homework Checklist (RAG)

Use this checklist when preparing your submission.

Verified on 2026-10-12 against [the pinned-environment validation transcript](evidence/checklist-validation.txt). All 34 tests passed with pytest 8.3.3, all task evidence scripts ran successfully, and both final cases passed. Unchecked personal items require learner input.

## A. Baseline setup

- [x] Project installs and tests run locally.
- [x] You can run the CLI with a custom question.
- [ ] You understand where chunking, retrieval, and answer behavior are implemented.

Installation was verified in a new `.venv-checklist` environment using `requirements.txt`. Source locations: `src/chunking.py` (chunking), `src/retrieval.py` (retrieval), `src/rag.py` (answer/citation/refusal), and `src/cli.py` (command interface). Learner confirmation of understanding is pending.

## B. Outcome 1: Explain chunking effect on retrieval quality

- [x] You ran at least two chunking configurations (for example: `chunk_size=140, overlap=30` and one alternative).
- [x] You compared retrieval output for the same question under both configurations.
- [x] You wrote a short explanation of the observed difference in retrieval quality.

Evidence: [Task 01](evidence/task-01-chunking-impact.md).

## C. Outcome 2: Implement top-k retrieval pipeline

- [x] Retrieval returns top-k chunks sorted by relevance score.
- [x] You show one example output with `top_k=2` and one with `top_k=3`.
- [x] You explain how your scoring approach decides relevance.

Evidence: [Task 02](evidence/task-02-top-k-retrieval.md); relevance is the documented lexical score, with semantic limitations disclosed.

## D. Outcome 3: Return answers with explicit citations

- [x] Supported answer includes explicit citations to chunk IDs.
- [x] Citation IDs in answer correspond to retrieved chunks shown in evidence.
- [x] Answer format clearly separates answer body and citations/references.

Evidence: [Task 03](evidence/task-03-citation-quality.md).

## E. Outcome 4: Refuse unsupported questions

- [x] For an unsupported question, the system refuses instead of generating an unsupported claim.
- [x] Refusal message is clear and consistent with grounded RAG behavior.
- [x] You explain briefly why retrieved evidence was insufficient.

Evidence: [Task 04](evidence/task-04-refusal-behavior.md), including the original failure and fix.

## F. Outcome 5: Show supported and unsupported evidence

- [x] You provide one supported query with: question, retrieved chunks, answer, citations.
- [x] You provide one unsupported query with: question, retrieved chunks (or empty result), refusal output.
- [x] Evidence for both examples is reproducible from CLI commands or tests.

Evidence: [root evidence.md](../evidence.md); reproduce with `python -m scripts.final_evidence`.

## G. Pair accountability

- [ ] Pair report includes contribution of both members.
- [ ] The designated demo lead for this week is recorded.

Awaiting actual names, each member's contribution, and demo lead (or confirmation of individual work). These cannot be inferred from commits or generated on the learner's behalf.

## H. Suggested extension (optional)

- [x] Improve lexical scoring or citation formatting.
- [x] Add at least 3 tests for your extension.

Implemented optional `--ignore-common-words` lexical scoring and six tests in `tests/test_scoring_extension.py`. [Extension and installation evidence](evidence/checklist-completion.md).

## I. Submission bundle (recommended)

- [x] `evidence.md` with Outcome 1-5 sections.
- [x] CLI commands used for both example queries.
- [x] Test output snapshot.

