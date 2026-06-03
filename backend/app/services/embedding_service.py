from sentence_transformers import SentenceTransformer

model = SentenceTransformer(
    "intfloat/multilingual-e5-base"
)


def generate_embeddings(texts: list[str]):

    embeddings = model.encode(
        texts,
        convert_to_numpy=True
    )

    return embeddings.tolist()