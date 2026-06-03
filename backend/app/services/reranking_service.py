from copy import deepcopy
from sentence_transformers import (
    CrossEncoder
)

model = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)

MIN_RERANK_SCORE = 0.0

def rerank_chunks(
    question,
    chunks,
    metadata,
    top_k=5
):

    pairs = [
        (question, chunk)
        for chunk in chunks
    ]

    scores = model.predict(
        pairs
    )

    ranked = sorted(
        zip(
            chunks,
            metadata,
            scores
        ),
        key=lambda x: x[2],
        reverse=True
    )

    ranked = [
        item
        for item in ranked
        if item[2] >= MIN_RERANK_SCORE
    ]
    
    ranked = ranked[:top_k]

    reranked_chunks = []
    reranked_metadata = []

    for chunk, meta, score in ranked:

        meta_copy = deepcopy(meta)

        meta_copy["rerank_score"] = round(
            float(score),
            4
        )

        reranked_chunks.append(chunk)
        reranked_metadata.append(meta_copy)

    return (
        reranked_chunks,
        reranked_metadata
    )