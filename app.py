from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from rag import ask_rag


app = FastAPI()


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://python-rag-chatbot-zei1.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# Request model
# ============================================================

class ChatRequest(BaseModel):
    message: str


# ============================================================
# Home
# ============================================================

@app.get("/")
def home():
    return {
        "message": "Python RAG API is running!"
    }


# ============================================================
# Health
# ============================================================

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


# ============================================================
# Chat
# ============================================================

@app.post("/chat")
def chat(request: ChatRequest):

    try:

        answer = ask_rag(request.message)

        return {
            "answer": answer
        }

    except Exception as e:

        return {
            "answer": "Sorry, something went wrong while processing your question.",
            "error": str(e)
        }