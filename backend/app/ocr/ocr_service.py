import pytesseract
from app.models.ocr_models import OCRProfile
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)
from PIL import Image
import cv2
import tempfile

from app.ocr.preprocessing import (
    preprocess_image
)

from app.ocr.image_utils import (
    pdf_to_images
)



def image_to_text(
    image_path: str,
    page_number: int,
    profile: OCRProfile
):

    processed = preprocess_image(
        image_path,
        profile
    )

    with tempfile.NamedTemporaryFile(
        suffix=".png",
        delete=False
    ) as tmp:

        temp_path = tmp.name

    cv2.imwrite(
        temp_path,
        processed
    )

    if page_number is not None:

        cv2.imwrite(
            f"data/debug_ocr/page_{page_number}.png",
            processed
        )

    config = (
        "--oem 3 "
        "--psm 6"
    )

    text = pytesseract.image_to_string(
        Image.open(temp_path),
        lang="spa",
        config=config
    )

    return text

def extract_pdf_ocr(
    pdf_path: str,
    profile: OCRProfile = OCRProfile.STANDARD
):

    image_paths = pdf_to_images(
        pdf_path,
        "data/temp_images"
    )

    pages = []

    for page_number, image_path in enumerate(
        image_paths,
        start=1
    ):

        text = image_to_text(
            image_path,
            page_number,
            profile
        )

        pages.append(
            {
                "page": page_number,
                "text": text
            }
        )

    return pages