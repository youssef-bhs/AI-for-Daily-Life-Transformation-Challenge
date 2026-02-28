"""API router – AI Budget Optimizer"""
from fastapi import APIRouter, HTTPException
from models import BudgetOptimizerRequest, BudgetOptimizerResponse
from services.budget_service import analyze_budget

router = APIRouter()


@router.post("/analyze", response_model=BudgetOptimizerResponse, summary="Analyze and optimize student budget")
def analyze_student_budget(request: BudgetOptimizerRequest):
    """
    Submit your monthly income and expenses.
    Receive categorized analysis, waste detection, and AI-powered savings suggestions.
    """
    if request.monthly_income <= 0:
        raise HTTPException(status_code=400, detail="Monthly income must be greater than 0.")
    if not request.expenses:
        raise HTTPException(status_code=400, detail="Provide at least one expense.")
    try:
        return analyze_budget(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/sample", summary="Get sample budget input for demo")
def get_sample_input():
    """Returns a pre-filled sample request body for hackathon demos."""
    return {
        "monthly_income": 1500.0,
        "currency": "USD",
        "expenses": [
            {"category": "Rent", "amount": 500.0, "description": "Student apartment"},
            {"category": "Food", "amount": 320.0, "description": "Restaurants and groceries"},
            {"category": "Transport", "amount": 90.0, "description": "Bus pass + Uber"},
            {"category": "Entertainment", "amount": 150.0, "description": "Nights out, cinema"},
            {"category": "Subscriptions", "amount": 65.0, "description": "Netflix, Spotify, gym app"},
            {"category": "Coffee", "amount": 55.0, "description": "Daily café visits"},
            {"category": "Clothing", "amount": 80.0, "description": "Shopping"},
            {"category": "Education", "amount": 60.0, "description": "Books, courses"},
        ],
    }
