"""
AI Study Planner – core logic (rule-based scheduling + LLM recommendations).
"""
from datetime import date, timedelta, datetime
from typing import List, Tuple
import math

from models import (
    StudyPlannerRequest,
    StudyPlannerResponse,
    DailyStudyBlock,
    PriorityItem,
    Exam,
    Project,
)
from llm_client import get_study_recommendations
from scoring import compute_study_score, compute_efficiency_score


# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

DIFFICULTY_HOURS_MAP = {1: 1.0, 2: 1.5, 3: 2.5, 4: 3.5, 5: 5.0}


def _parse_date(s: str) -> date:
    return datetime.strptime(s, "%Y-%m-%d").date()


def _urgency_score(days_remaining: int, difficulty: int) -> float:
    """
    Higher score = higher priority.
    urgency = (difficulty * 10) / max(days_remaining, 1)
    Capped at 50.
    """
    return min(50.0, (difficulty * 10) / max(days_remaining, 1))


def _load_label(actual: float, available: float) -> str:
    ratio = actual / max(available, 0.1)
    if ratio <= 0.6:
        return "light"
    if ratio <= 0.9:
        return "moderate"
    return "heavy"


# ─────────────────────────────────────────────
# PRIORITY RANKING
# ─────────────────────────────────────────────

def build_priority_list(
    exams: List[Exam],
    projects: List[Project],
    today: date,
) -> List[PriorityItem]:
    items: List[PriorityItem] = []

    for exam in exams:
        due = _parse_date(exam.exam_date)
        days_left = max((due - today).days, 0)
        total_hours_needed = DIFFICULTY_HOURS_MAP.get(exam.difficulty, 2.5) * max(days_left, 1)
        daily_rec = round(total_hours_needed / max(days_left, 1), 1)
        items.append(
            PriorityItem(
                name=exam.subject,
                type="exam",
                due_date=exam.exam_date,
                days_remaining=days_left,
                urgency_score=_urgency_score(days_left, exam.difficulty),
                recommended_daily_hours=min(daily_rec, 4.0),
            )
        )

    for proj in projects:
        due = _parse_date(proj.deadline)
        days_left = max((due - today).days, 0)
        daily_rec = round(proj.estimated_hours / max(days_left, 1), 1)
        items.append(
            PriorityItem(
                name=proj.name,
                type="project",
                due_date=proj.deadline,
                days_remaining=days_left,
                urgency_score=_urgency_score(days_left, 3),   # projects default difficulty=3
                recommended_daily_hours=min(daily_rec, 3.0),
            )
        )

    # Sort descending by urgency
    items.sort(key=lambda x: x.urgency_score, reverse=True)
    return items


# ─────────────────────────────────────────────
# SCHEDULE BUILDER
# ─────────────────────────────────────────────

def build_schedule(
    priority_items: List[PriorityItem],
    available_hours: float,
    today: date,
    plan_days: int = 30,
) -> Tuple[List[DailyStudyBlock], int]:
    """
    Greedy allocation:
      - For each day, fill slots with the highest-priority task that still has
        remaining work to do.
    Returns (schedule, overloaded_days_count).
    """
    # Build a work-bank: {name -> hours_remaining}
    work_bank: dict = {}
    for item in priority_items:
        needed = item.recommended_daily_hours * item.days_remaining
        work_bank[item.name] = round(min(needed, item.days_remaining * item.recommended_daily_hours), 1)

    schedule: List[DailyStudyBlock] = []
    overloaded = 0

    for day_offset in range(plan_days):
        current_day = today + timedelta(days=day_offset)
        dow = DAYS[current_day.weekday()]

        # Filter tasks still due in the future
        active = [
            it for it in priority_items
            if _parse_date(it.due_date) >= current_day and work_bank.get(it.name, 0) > 0
        ]

        if not active:
            break  # no more work to schedule

        tasks_today: List[str] = []
        hours_used = 0.0
        remaining_capacity = available_hours

        for item in active:
            if remaining_capacity <= 0:
                break
            bank = work_bank.get(item.name, 0)
            if bank <= 0:
                continue
            # Allocate proportionally but cap at 2 hours per task per day
            alloc = round(min(item.recommended_daily_hours, remaining_capacity, bank, 2.0), 1)
            if alloc <= 0:
                continue
            tasks_today.append(f"{item.name} ({alloc}h) [{item.type}]")
            hours_used += alloc
            remaining_capacity -= alloc
            work_bank[item.name] = max(0.0, bank - alloc)

        if not tasks_today:
            continue

        load = _load_label(hours_used, available_hours)
        if load == "heavy":
            overloaded += 1

        schedule.append(
            DailyStudyBlock(
                date=str(current_day),
                day_of_week=dow,
                tasks=tasks_today,
                total_hours=round(hours_used, 1),
                load_level=load,
            )
        )

    return schedule, overloaded


# ─────────────────────────────────────────────
# MAIN SERVICE FUNCTION
# ─────────────────────────────────────────────

def generate_study_plan(req: StudyPlannerRequest) -> StudyPlannerResponse:
    today = _parse_date(req.start_date) if req.start_date else date.today()

    priority_items = build_priority_list(req.exams, req.projects, today)
    schedule, overloaded_days = build_schedule(priority_items, req.available_hours_per_day, today)

    # Build LLM context string
    exam_lines = "\n".join(
        f"  - {e.subject} on {e.exam_date} (difficulty {e.difficulty}/5)"
        for e in req.exams
    )
    proj_lines = "\n".join(
        f"  - {p.name} due {p.deadline} (~{p.estimated_hours}h of work)"
        for p in req.projects
    )
    llm_context = (
        f"Student has {req.available_hours_per_day} study hours per day.\n"
        f"Exams:\n{exam_lines}\n"
        f"Projects:\n{proj_lines}\n"
        f"Top priority: {priority_items[0].name if priority_items else 'None'}\n"
        f"Plan spans {len(schedule)} days. "
        f"{overloaded_days} day(s) are considered heavy load."
    )

    ai_recommendations = get_study_recommendations(llm_context)

    study_score = compute_study_score(overloaded_days, len(schedule))
    ses = compute_efficiency_score(study_score=study_score, budget_score=0.5)

    return StudyPlannerResponse(
        schedule=schedule[:14],          # Return 2-week view for demo clarity
        priority_ranking=priority_items,
        total_tasks=len(req.exams) + len(req.projects),
        ai_recommendations=ai_recommendations,
        student_efficiency_score=ses,
    )
