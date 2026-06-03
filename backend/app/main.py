from fastapi import FastAPI

from app.api.documents import router as documents_router

app = FastAPI(
    title="Document Chatbot API"
)

app.include_router(
    documents_router,
    prefix="/api",
    tags=["Documents"]
)