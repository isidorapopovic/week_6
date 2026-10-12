from dataclasses import dataclass

from .chunking import Chunk
from .retrieval import retrieve_top_k, tokenize


REFUSAL_MESSAGE = "I do not have enough grounded evidence in the provided corpus to answer that question."

# Ignore common grammatical/question words when checking topic overlap.
# This is a lexical guard, not proof that a passage entails an answer.
COMMON_WORDS = frozenset(
    "a an the and or but if in on at to of for from with by as is are was were "
    "be been being do does did have has had should would could can may might "
    "will shall what which who whom whose when where why how it its this that "
    "these those i you we they he she them our your their".split()
)


@dataclass(frozen=True)
class RagAnswer:
    answer: str
    citations: list[str]
    refused: bool


def build_grounded_answer(question: str, chunks: list[Chunk], top_k: int = 2) -> RagAnswer:
    results = retrieve_top_k(question, chunks, k=top_k)
    if not results:
        return RagAnswer(answer=REFUSAL_MESSAGE, citations=[], refused=True)

    best = results[0]
    if best.score < 0.02:
        return RagAnswer(answer=REFUSAL_MESSAGE, citations=[], refused=True)

    topic_tokens = set(tokenize(question)) - COMMON_WORDS
    if not any(topic_tokens.intersection(tokenize(item.chunk.text)) for item in results):
        return RagAnswer(answer=REFUSAL_MESSAGE, citations=[], refused=True)

    supporting_points = []
    citations = []
    for item in results:
        citations.append(item.chunk.chunk_id)
        supporting_points.append(f"[{item.chunk.chunk_id}] {item.chunk.text}")

    answer = "Grounded response based on retrieved context:\n" + "\n".join(supporting_points)
    return RagAnswer(answer=answer, citations=citations, refused=False)
