from pydantic import BaseModel


class ChatRequest(BaseModel):

    question: str

    documents: list[str] | None = None