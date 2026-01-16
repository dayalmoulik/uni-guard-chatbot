"""
FastAPI Server for UniGuard Chatbot
"""

from fastapi import FastAPI
from pydantic import BaseModel
from app import handle_user_query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import pathlib

app = FastAPI(
    title="UniGuard Chatbot API",
    description="A compliant university admissions assistant",
    version="1.0.0"
)

# -----------------------------
# Load HTML manually (SAFE)
# -----------------------------
HTML_PATH = pathlib.Path(__file__).parent / "index.html"

@app.get("/", response_class=HTMLResponse)
def serve_ui():
    return HTML_PATH.read_text(encoding="utf-8")

# -----------------------------
# Request / Response Models
# -----------------------------
class ChatRequest(BaseModel):
    query: str


class ChatResponse(BaseModel):
    response: str


# -----------------------------
# Health Check
# -----------------------------
@app.get("/")
def health():
    return {"status": "UniGuard is running"}


# -----------------------------
# Chat Endpoint
# -----------------------------
@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    answer = handle_user_query(request.query)
    return ChatResponse(response=answer)

# -----------------------------
# Static Files Serving
# -----------------------------
#app.mount("/", StaticFiles(directory="static", html=True), name="static")