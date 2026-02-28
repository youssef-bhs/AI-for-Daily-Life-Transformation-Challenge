"""
SmartStudent AI – Main FastAPI Application Entry Point
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env first, before any module-level imports read env vars
load_dotenv(dotenv_path=Path(__file__).resolve().parent / ".env", override=True)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import study_planner, budget_optimizer, health, chat

app = FastAPI(
    title="SmartStudent AI",
    description="AI-powered daily life transformation for students",
    version="1.0.0",
)

# Allow React dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api", tags=["Health"])
app.include_router(study_planner.router, prefix="/api/study", tags=["Study Planner"])
app.include_router(budget_optimizer.router, prefix="/api/budget", tags=["Budget Optimizer"])
app.include_router(chat.router, prefix="/api/chat", tags=["AI Chat (RAG)"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
