from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)

def create_page_chunks(
    pages
):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = []

    for page_data in pages:

        page_number = page_data["page"]

        page_text = page_data["text"]

        page_chunks = splitter.split_text(
            page_text
        )

        for chunk in page_chunks:

            chunks.append(
                {
                    "page": page_number,
                    "text": chunk
                }
            )

    return chunks