from app.models.ocr_models import OCRProfile
from app.services.preprocessing_service import clean_text
from app.ocr.ocr_service import extract_pdf_ocr
import json
from pathlib import Path

PROCESSED_FOLDER = Path(
    "data/processed"
)

from app.services.pdf_service import (
    extract_pages,
    is_scanned_document
)
from app.services.embedding_service import (
    generate_embeddings
)

from app.services.vector_store_service import (
    add_chunks
)

from app.services.pdf_service import (
    extract_pages
)
from app.services.chunking_service import (
    create_page_chunks
)
from app.services.table_service import (
    extract_tables,
    table_to_text
)

def process_document(
    pdf_path: Path,
    ocr_profile: OCRProfile | None = None
):
    ocr_used = False
    pages = extract_pages(
        str(pdf_path)
    )


    if is_scanned_document(
        pages
    ):

        ocr_used = True

        profile = (
            ocr_profile
            or OCRProfile.STANDARD
        )

        pages = extract_pdf_ocr(
            str(pdf_path),
            profile
        )

    for page in pages:
        page["text"] = clean_text(
            page["text"]
        )


    tables = extract_tables(
        str(pdf_path)
    )

    table_chunks = []

    for table in tables:

        text = table_to_text(
            table
        )

        if text.strip():

            table_chunks.append(
                {
                    "text": text,
                    "page": table["page"],
                    "type": "table",
                    "table_index": table["table_index"]
                }
            )
    
    full_text = "\n\n".join(
        page["text"]
        for page in pages
    )

    page_chunks = create_page_chunks(
        pages
    )

    for chunk in page_chunks:
        chunk["type"] = "text"

    
    all_chunks = (
        page_chunks +
        table_chunks
    )
    
    chunk_texts = [
        chunk["text"]
        for chunk in all_chunks
    ]

    embeddings = generate_embeddings(
        chunk_texts
    )

    metadata = []

    for i, chunk in enumerate(
        all_chunks
    ):

        metadata.append(
            {
                "document": pdf_path.name,
                "chunk_id": i,
                "page": chunk["page"],
                "type": chunk["type"],
                "chunk_preview": chunk["text"][:200]
            }
        )

    ids = [
        f"{pdf_path.stem}_{i}"
        for i in range(
            len(all_chunks)
        )
    ]

    documents = [
        chunk["text"]
        for chunk in all_chunks
    ]

    add_chunks(
        ids=ids,
        chunks=documents,
        embeddings=embeddings,
        metadata=metadata
    )

    txt_path = PROCESSED_FOLDER / f"{pdf_path.stem}.txt"

    with open(
        txt_path,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(full_text)

    metadata_file = (
        PROCESSED_FOLDER /
        f"{pdf_path.stem}.metadata.json"
    )

    document_metadata = {
        "filename": pdf_path.name,
        "pages": len(pages),
        "chunks": len(all_chunks),
        "tables_found": len(tables),
        "ocr_used": ocr_used,
        "ocr_profile": (
            profile.value
            if ocr_used
            else None
        )
    }

    with open(
        metadata_file,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            document_metadata,
            f,
            ensure_ascii=False,
            indent=2
        )

    return document_metadata
