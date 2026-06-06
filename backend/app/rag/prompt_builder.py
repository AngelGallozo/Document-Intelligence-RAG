def build_prompt(
    question: str,
    context_chunks: list[dict]
):

    formatted_context = []

    for chunk in context_chunks:

        chunk_type = chunk.get("type", "text")
        page = chunk.get("page", "unknown")
        text = chunk.get("text", "")

        if chunk_type == "table":
            formatted_context.append(
                f"[TABLE | page {page}]\n{text}"
            )
        else:
            formatted_context.append(
                f"[TEXT | page {page}]\n{text}"
            )

    context = "\n\n".join(formatted_context)

    prompt = f"""
Eres un asistente especializado en responder
preguntas utilizando exclusivamente la información
proporcionada.

Si la respuesta no aparece en el contexto,
indica claramente que no se encontró información.

Contexto:
{context}

Pregunta:
{question}

Respuesta:
""".strip()

    return prompt