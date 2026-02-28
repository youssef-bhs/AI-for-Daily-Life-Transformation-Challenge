"""
Pydantic models (request/response schemas) for all modules.
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date


# ─────────────────────────────────────────────
# STUDY PLANNER SCHEMAS
# ─────────────────────────────────────────────

class Exam(BaseModel):
    subject: str = Field(..., example="Mathematics")
    exam_date: str = Field(..., example="2026-03-15")   # ISO format YYYY-MM-DD
    difficulty: int = Field(default=3, ge=1, le=5, description="1=easy … 5=very hard")

class Project(BaseModel):
    name: str = Field(..., example="Machine Learning Report")
    deadline: str = Field(..., example="2026-03-10")
    estimated_hours: float = Field(default=8.0, ge=1)

class StudyPlannerRequest(BaseModel):
    exams: List[Exam]
    projects: List[Project]
    available_hours_per_day: float = Field(..., ge=0.5, le=24, example=4.0)
    start_date: Optional[str] = Field(default=None, description="Defaults to today")

class DailyStudyBlock(BaseModel):
    date: str
    day_of_week: str
    tasks: List[str]
    total_hours: float
    load_level: str       # "light" | "moderate" | "heavy"

class PriorityItem(BaseModel):
    name: str
    type: str             # "exam" | "project"
    due_date: str
    days_remaining: int
    urgency_score: float
    recommended_daily_hours: float

class StudyPlannerResponse(BaseModel):
    schedule: List[DailyStudyBlock]
    priority_ranking: List[PriorityItem]
    total_tasks: int
    ai_recommendations: str
    student_efficiency_score: float


# ─────────────────────────────────────────────
# BUDGET OPTIMIZER SCHEMAS
# ─────────────────────────────────────────────

class Expense(BaseModel):
    category: str = Field(..., example="Food")
    amount: float = Field(..., ge=0, example=350.0)
    description: Optional[str] = Field(default="", example="Restaurants & groceries")

class BudgetOptimizerRequest(BaseModel):
    monthly_income: float = Field(..., ge=0, example=1500.0)
    expenses: List[Expense]
    currency: Optional[str] = Field(default="USD")

class CategoryBreakdown(BaseModel):
    category: str
    amount: float
    percentage: float
    status: str           # "optimal" | "high" | "excessive"
    benchmark_pct: float  # recommended % of income

class WasteItem(BaseModel):
    category: str
    current_amount: float
    recommended_max: float
    excess_amount: float
    suggestion: str

class AnnualProjection(BaseModel):
    current_annual_expenses: float
    projected_annual_savings: float
    optimized_annual_savings: float
    delta: float

class BudgetOptimizerResponse(BaseModel):
    total_expenses: float
    monthly_savings: float
    savings_rate_pct: float
    category_breakdown: List[CategoryBreakdown]
    waste_detected: List[WasteItem]
    annual_projection: AnnualProjection
    ai_suggestions: str
    student_efficiency_score: float


# ─────────────────────────────────────────────
# RAG CHAT SCHEMAS
# ─────────────────────────────────────────────

class ChatMessage(BaseModel):
    role: str = Field(..., example="user", description="'user' or 'assistant'")
    content: str = Field(..., example="How should I prepare for my math exam?")

class ChatRequest(BaseModel):
    question: str = Field(..., example="How can I reduce my food expenses as a student?")
    conversation_history: Optional[List[ChatMessage]] = Field(
        default=None,
        description="Previous turns in the conversation for multi-turn support.",
    )
    top_k_docs: int = Field(default=3, ge=1, le=6, description="Number of RAG documents to retrieve")

class ChatResponse(BaseModel):
    answer: str
    retrieved_docs: List[str] = Field(
        default_factory=list,
        description="Titles of the knowledge base documents used to ground the answer.",
    )
    provider: str = Field(default="", description="LLM provider used (openai / groq / demo)")
