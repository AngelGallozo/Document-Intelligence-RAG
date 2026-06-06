from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.documents import router as documents_router

app = FastAPI(
    title="Document Chatbot API"
)

app.include_router(
    documents_router,
    prefix="/api",
    tags=["Documents"]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)