"""API router – Health check"""
from fastapi import APIRouter
from datetime import datetime

router = APIRouter()

@router.get("/health")
def health_check():
    return {
        "status": "ok",
        "app": "SmartStudent AI",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat(),
    }
