from pathlib import Path
import json
from app.models.ocr_models import OCRProfile
from fastapi import (
    APIRouter,
    UploadFile,
    HTTPException,
    Form
)

from app.models.chat_models import (
    ChatRequest
)
from app.rag.retriever import (
    retrieve_context
)

from app.rag.rag_pipeline import (
    ask_question
)

from app.services.table_service import (
    extract_tables
)

from app.services.ingestion_service import (
    process_document
)

from app.services.document_service import (
    delete_document
)

from app.services.document_service import (
    reindex_document
)
from app.services.document_service import (
    get_document_status
)

router = APIRouter()

PDF_FOLDER = Path("data/pdfs")
PROCESSED_FOLDER = Path("data/processed")

@router.post("/upload")
async def upload_pdf(
    file: UploadFile,
    ocr_profile: OCRProfile | None = Form(None)
):

    pdf_path = PDF_FOLDER / file.filename

    with open(pdf_path, "wb") as f:
        f.write(await file.read())

    result = process_document(
        pdf_path,
        ocr_profile
    )

    return result

    

@router.get("/documents")
def list_documents():

    documents = []

    for pdf_file in PDF_FOLDER.glob("*.pdf"):

        txt_file = PROCESSED_FOLDER / f"{pdf_file.stem}.txt"

        documents.append(
            {
                "filename": pdf_file.name,
                "processed": txt_file.exists(),
                "size_bytes": pdf_file.stat().st_size
            }
        )

    return documents


@router.get("/documents/{filename}")
def get_document(filename: str):

    pdf_path = PDF_FOLDER / filename

    if not pdf_path.exists():
        raise HTTPException(
            status_code=404,
            detail="Documento no encontrado"
        )

    txt_path = PROCESSED_FOLDER / f"{pdf_path.stem}.txt"

    extracted_text = ""

    if txt_path.exists():

        with open(
            txt_path,
            "r",
            encoding="utf-8"
        ) as f:

            extracted_text = f.read()

    return {
        "filename": pdf_path.name,
        "size_bytes": pdf_path.stat().st_size,
        "processed": txt_path.exists(),
        "characters": len(extracted_text),
        "preview": extracted_text[:1000]
    }

@router.get("/search")
def semantic_search(question: str):

    results = retrieve_context(
        question
    )

    return results

@router.post("/chat")
def chat(
    request: ChatRequest
):

    return ask_question(
        question=request.question,
        documents=request.documents
    )


@router.get(
    "/documents/{filename}/tables"
)
def get_document_tables(
    filename: str
):

    pdf_path = PDF_FOLDER / filename

    if not pdf_path.exists():

        raise HTTPException(
            status_code=404,
            detail="Documento no encontrado"
        )

    tables = extract_tables(
        str(pdf_path)
    )

    return {
        "document": filename,
        "tables_found": len(tables),
        "tables": tables
    }


@router.delete(
    "/documents/{filename}"
)
def remove_document(
    filename: str
):

    deleted = delete_document(
        filename
    )

    if not deleted:

        raise HTTPException(
            status_code=404,
            detail="Documento no encontrado"
        )

    return {
        "deleted": filename
    }


@router.post(
    "/documents/{filename}/reindex"
)
def reindex(
    filename: str
):

    result = reindex_document(
        filename
    )

    if result is None:

        raise HTTPException(
            status_code=404,
            detail="Documento no encontrado"
        )

    return result


@router.get(
    "/documents/{filename}/status"
)
def document_status(
    filename: str
):

    status = get_document_status(
        filename
    )

    if status is None:

        raise HTTPException(
            status_code=404,
            detail="Documento no encontrado"
        )

    return status