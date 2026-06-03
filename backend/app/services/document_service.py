from pathlib import Path
import json
from contextlib import suppress
from app.services.vector_store_service import (
    delete_document_chunks
)
from app.services.ingestion_service import (
    process_document
)

PDF_FOLDER = Path("data/pdfs")
PROCESSED_FOLDER = Path("data/processed")
CHUNKS_FOLDER = Path("data/chunks")


def get_document_paths(
    filename: str
):

    pdf_path = (
        PDF_FOLDER /
        filename
    )

    txt_path = (
        PROCESSED_FOLDER /
        f"{Path(filename).stem}.txt"
    )

    chunks_path = (
        CHUNKS_FOLDER /
        f"{Path(filename).stem}.json"
    )

    metadata_path = (
        PROCESSED_FOLDER /
        f"{Path(filename).stem}.metadata.json"
    )

    return (
        pdf_path,
        txt_path,
        chunks_path,
        metadata_path
    )

def delete_document(
    filename: str
):

    (
        pdf_path,
        txt_path,
        chunks_path,
        metadata_path
    ) = get_document_paths(
        filename
    )

    if not pdf_path.exists():
        return False

    delete_document_chunks(
        filename
    )

    for path in [
        txt_path,
        chunks_path,
        metadata_path,
        pdf_path
    ]:

        with suppress(FileNotFoundError):
            path.unlink()

    return True

def reindex_document(
    filename: str
):

    (
        pdf_path,
        txt_path,
        chunks_path,
        metadata_path
    ) = get_document_paths(
        filename
    )

    if not pdf_path.exists():

        return None

    delete_document_chunks(
        filename
    )

    if txt_path.exists():
        txt_path.unlink()

    if chunks_path.exists():
        chunks_path.unlink()
    
    if metadata_path.exists():
        metadata_path.unlink()

    return process_document(
        pdf_path,
        None
    )

def get_document_status(
    filename: str
):

    pdf_path = PDF_FOLDER / filename

    if not pdf_path.exists():

        return None

    metadata_path = (
        PROCESSED_FOLDER /
        f"{pdf_path.stem}.metadata.json"
    )

    if not metadata_path.exists():

        return {
            "filename": filename,
            "indexed": False
        }

    with open(
        metadata_path,
        "r",
        encoding="utf-8"
    ) as f:

        metadata = json.load(f)

    metadata["indexed"] = True

    return metadata