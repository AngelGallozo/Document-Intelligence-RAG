import fitz


def extract_text(pdf_path: str) -> str:

    doc = fitz.open(pdf_path)

    text = ""

    for page in doc:
        text += page.get_text()

    return text


def extract_pages(pdf_path):

    doc = fitz.open(pdf_path)

    pages = []

    for page_number, page in enumerate(
        doc,
        start=1
    ):

        pages.append(
            {
                "page": page_number,
                "text": page.get_text()
            }
        )

    return pages

def is_scanned_document(
    pages
):

    total_chars = sum(
        len(page["text"])
        for page in pages
    )

    return total_chars < 100