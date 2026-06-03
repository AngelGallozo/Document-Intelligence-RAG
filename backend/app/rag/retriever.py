from app.services.embedding_service import (
    generate_embeddings
)

from app.services.vector_store_service import (
    search
)


def retrieve_context(
    question: str,
    top_k: int = 5,
    documents=None
):

    query_embedding = generate_embeddings(
        [question]
    )[0]

    results = search(
        query_embedding=query_embedding,
        n_results=top_k,
        document_filters=documents
    )

    return results

def get_context_chunks(
    question,
    top_k=5,
    documents=None
):

    results = retrieve_context(
        question=question,
        top_k=top_k,
        documents=documents
    )

    return results["documents"][0]

def get_context_data(
    question,
    top_k=20,
    documents=None
):

    results = retrieve_context(
        question,
        top_k,
        documents
    )

    return (
        results["documents"][0],
        results["metadatas"][0]
    )