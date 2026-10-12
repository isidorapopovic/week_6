from dataclasses import dataclass

from .chunking import Chunk
from .retrieval import COMMON_WORDS, retrieve_top_k, tokenize


REFUSAL_MESSAGE = "I do not have enough grounded evidence in the provided corpus to answer that question."


@dataclass(frozen=True)
class RagAnswer:
    answer: str
    citations: list[str]
    refused: bool


def build_grounded_answer(question: str, chunks: list[Chunk], top_k: int = 2,
                          ignore_common_words: bool = False) -> RagAnswer:
    results = retrieve_top_k(question, chunks, k=top_k, ignore_common_words=ignore_common_words)
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
