"""API router – AI Study Planner"""
from fastapi import APIRouter, HTTPException
from models import StudyPlannerRequest, StudyPlannerResponse
from services.study_service import generate_study_plan

router = APIRouter()


@router.post("/plan", response_model=StudyPlannerResponse, summary="Generate optimized study plan")
def create_study_plan(request: StudyPlannerRequest):
    """
    Submit your exams, projects, and available daily hours.
    Receive an optimized study schedule with AI recommendations.
    """
    if not request.exams and not request.projects:
        raise HTTPException(status_code=400, detail="Provide at least one exam or project.")
    try:
        return generate_study_plan(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/sample", summary="Get sample study planner input for demo")
def get_sample_input():
    """Returns a pre-filled sample request body for hackathon demos."""
    return {
        "exams": [
            {"subject": "Mathematics", "exam_date": "2026-03-15", "difficulty": 4},
            {"subject": "Computer Networks", "exam_date": "2026-03-12", "difficulty": 3},
            {"subject": "Database Systems", "exam_date": "2026-03-20", "difficulty": 3},
        ],
        "projects": [
            {"name": "ML Research Paper", "deadline": "2026-03-10", "estimated_hours": 12},
            {"name": "Web App Project", "deadline": "2026-03-18", "estimated_hours": 8},
        ],
        "available_hours_per_day": 4.0,
        "start_date": "2026-02-27",
    }
