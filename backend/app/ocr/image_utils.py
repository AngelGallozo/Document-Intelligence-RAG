import fitz
from pathlib import Path

def pdf_to_images(
    pdf_path: str,
    output_dir: str
):

    output_path = Path(output_dir)

    output_path.mkdir(
        parents=True,
        exist_ok=True
    )

    doc = fitz.open(pdf_path)

    images = []

    for page_number, page in enumerate(
        doc,
        start=1
    ):

        pix = page.get_pixmap(
            matrix=fitz.Matrix(
                2,
                2
            )
        )

        image_file = (
            output_path /
            f"page_{page_number}.png"
        )

        pix.save(
            str(image_file)
        )

        images.append(
            str(image_file)
        )

    return images