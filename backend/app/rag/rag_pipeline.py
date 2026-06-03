from app.services.reranking_service import (
    rerank_chunks
)

from app.rag.prompt_builder import (
    build_prompt
)

from app.rag.generator import (
    generate_answer
)

from app.rag.retriever import (
    get_context_data
)

def ask_question(
    question: str,
    documents=None
):

    chunks, metadata = (
        get_context_data(
            question=question,
            documents=documents
        )
    )

    chunks, metadata = (
        rerank_chunks(
            question,
            chunks,
            metadata,
            top_k=5
        )
    )

    context_chunks = []

    for chunk, meta in zip(chunks, metadata):

        context_chunks.append(
            {
                "text": chunk,
                "type": meta["type"],
                "page": meta["page"],
                "score": meta.get("score")
            }
        )

    prompt = build_prompt(question, context_chunks)

    answer = generate_answer(
        prompt
    )

    sources = []
    seen = set()

    source_id = 1

    for item in metadata:

        key = (
            item["document"],
            item["page"]
        )

        if key in seen:
            continue

        seen.add(key)

        sources.append(
            {
                "id": source_id,
                "document": item["document"],
                "page": item["page"],
                "type": item["type"],
                "rerank_score": round(
                    item["rerank_score"],
                    4
                )
            }
        )

        source_id += 1

    return {
        "question": question,
        "answer": answer,
        "sources": sources
    }