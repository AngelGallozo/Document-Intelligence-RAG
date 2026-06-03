import pdfplumber


def extract_tables(pdf_path: str):

    tables = []

    with pdfplumber.open(pdf_path) as pdf:

        for page_number, page in enumerate(
            pdf.pages,
            start=1
        ):

            page_tables = page.extract_tables()

            for table_index, table in enumerate(
                page_tables,
                start=1
            ):

                tables.append(
                    {
                        "page": page_number,
                        "table_index": table_index,
                        "data": table
                    }
                )

    return tables


def table_to_text(table):

    rows = table["data"]

    if not rows:
        return ""

    headers = rows[0]

    text_rows = []

    for row in rows[1:]:

        values = []

        for header, value in zip(
            headers,
            row
        ):

            values.append(
                f"{header}: {value}"
            )

        text_rows.append(
            " | ".join(values)
        )

    return "\n".join(text_rows)