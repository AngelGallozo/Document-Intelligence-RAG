import chromadb

client = chromadb.PersistentClient(
    path="data/vectordb"
)

collection = client.get_or_create_collection(
    name="documents"
)

def add_chunks(
    ids,
    chunks,
    embeddings,
    metadata
):

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadata
    )

def search(
    query_embedding,
    n_results=5,
    document_filters=None
):

    query_params = {
        "query_embeddings": [query_embedding],
        "n_results": n_results
    }

    if document_filters:

        if len(document_filters) == 1:

            query_params["where"] = {
                "document": document_filters[0]
            }

        else:

            query_params["where"] = {
                "$or": [
                    {"document": doc}
                    for doc in document_filters
                ]
            }

    return collection.query(
        **query_params
    )

def delete_document_chunks(
    document_name: str
):

    collection.delete(
        where={
            "document": document_name
        }
    )