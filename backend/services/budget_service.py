"""
AI Budget Optimizer – core logic (rule-based analysis + LLM suggestions).
"""
from typing import List

from models import (
    BudgetOptimizerRequest,
    BudgetOptimizerResponse,
    CategoryBreakdown,
    WasteItem,
    AnnualProjection,
    Expense,
)
from llm_client import get_budget_suggestions
from scoring import compute_budget_score, compute_efficiency_score


# ─────────────────────────────────────────────
# BENCHMARK SPENDING PERCENTAGES
# Based on 50/30/20 rule adapted for students
# ─────────────────────────────────────────────

BENCHMARKS: dict = {
    # category_lower_keyword → (recommended_pct, status_thresholds)
    "rent":          {"pct": 0.30, "high": 0.35, "excessive": 0.45},
    "housing":       {"pct": 0.30, "high": 0.35, "excessive": 0.45},
    "food":          {"pct": 0.15, "high": 0.20, "excessive": 0.28},
    "groceries":     {"pct": 0.12, "high": 0.18, "excessive": 0.25},
    "transport":     {"pct": 0.10, "high": 0.15, "excessive": 0.20},
    "transportation":{"pct": 0.10, "high": 0.15, "excessive": 0.20},
    "entertainment": {"pct": 0.05, "high": 0.08, "excessive": 0.12},
    "subscriptions": {"pct": 0.03, "high": 0.05, "excessive": 0.08},
    "clothing":      {"pct": 0.04, "high": 0.07, "excessive": 0.10},
    "health":        {"pct": 0.05, "high": 0.08, "excessive": 0.12},
    "education":     {"pct": 0.08, "high": 0.15, "excessive": 0.25},
    "utilities":     {"pct": 0.05, "high": 0.08, "excessive": 0.12},
    "coffee":        {"pct": 0.02, "high": 0.03, "excessive": 0.05},
    "gym":           {"pct": 0.02, "high": 0.04, "excessive": 0.06},
    "default":       {"pct": 0.05, "high": 0.08, "excessive": 0.12},
}

WASTE_SUGGESTIONS: dict = {
    "food":           "Try meal prepping 3-4 days a week. Cook in bulk to save ~30%.",
    "entertainment":  "Set a weekly entertainment cash envelope. Use student discounts.",
    "subscriptions":  "Audit every subscription. Cancel any unused for 30+ days.",
    "coffee":         "Switch to brewing at home 4/5 days. Save $40-60/month.",
    "clothing":       "Try second-hand shops or swap events with friends.",
    "transport":      "Use student transit pass or cycle for short distances.",
    "default":        "Review this category and identify where you can cut 20-30%.",
}


def _get_benchmark(category: str) -> dict:
    key = category.lower()
    for k, v in BENCHMARKS.items():
        if k in key:
            return v
    return BENCHMARKS["default"]


def _get_waste_suggestion(category: str) -> str:
    key = category.lower()
    for k, v in WASTE_SUGGESTIONS.items():
        if k in key:
            return v
    return WASTE_SUGGESTIONS["default"]


def _status(actual_pct: float, bm: dict) -> str:
    if actual_pct > bm["excessive"]:
        return "excessive"
    if actual_pct > bm["high"]:
        return "high"
    return "optimal"


# ─────────────────────────────────────────────
# MAIN SERVICE FUNCTION
# ─────────────────────────────────────────────

def analyze_budget(req: BudgetOptimizerRequest) -> BudgetOptimizerResponse:
    income = req.monthly_income
    expenses = req.expenses

    total_expenses = round(sum(e.amount for e in expenses), 2)
    monthly_savings = round(income - total_expenses, 2)
    savings_rate = (monthly_savings / income) if income > 0 else 0.0

    # ── Category Breakdown ──
    breakdown: List[CategoryBreakdown] = []
    waste_items: List[WasteItem] = []

    for exp in expenses:
        bm = _get_benchmark(exp.category)
        actual_pct = (exp.amount / income) if income > 0 else 0.0
        status = _status(actual_pct, bm)

        breakdown.append(
            CategoryBreakdown(
                category=exp.category,
                amount=exp.amount,
                percentage=round(actual_pct * 100, 1),
                status=status,
                benchmark_pct=round(bm["pct"] * 100, 1),
            )
        )

        # Detect waste
        recommended_max = round(bm["high"] * income, 2)
        if exp.amount > recommended_max:
            excess = round(exp.amount - recommended_max, 2)
            waste_items.append(
                WasteItem(
                    category=exp.category,
                    current_amount=exp.amount,
                    recommended_max=recommended_max,
                    excess_amount=excess,
                    suggestion=_get_waste_suggestion(exp.category),
                )
            )

    # Sort breakdown by amount descending
    breakdown.sort(key=lambda x: x.amount, reverse=True)

    # ── Annual Projection ──
    potential_monthly_saving = round(sum(w.excess_amount for w in waste_items), 2)
    ann_projection = AnnualProjection(
        current_annual_expenses=round(total_expenses * 12, 2),
        projected_annual_savings=round(monthly_savings * 12, 2),
        optimized_annual_savings=round((monthly_savings + potential_monthly_saving) * 12, 2),
        delta=round(potential_monthly_saving * 12, 2),
    )

    # ── LLM Context ──
    expense_lines = "\n".join(
        f"  - {e.category}: {req.currency} {e.amount:.0f} ({round(e.amount/income*100,1)}% of income)"
        for e in sorted(expenses, key=lambda x: x.amount, reverse=True)
    )
    llm_context = (
        f"Monthly income: {req.currency} {income:.0f}\n"
        f"Total expenses: {req.currency} {total_expenses:.0f}\n"
        f"Monthly savings: {req.currency} {monthly_savings:.0f} ({round(savings_rate*100,1)}%)\n"
        f"Expense breakdown:\n{expense_lines}\n"
        f"Potential monthly saving if waste eliminated: {req.currency} {potential_monthly_saving:.0f}"
    )

    ai_suggestions = get_budget_suggestions(llm_context)

    budget_score = compute_budget_score(savings_rate)
    ses = compute_efficiency_score(study_score=0.5, budget_score=budget_score)

    return BudgetOptimizerResponse(
        total_expenses=total_expenses,
        monthly_savings=monthly_savings,
        savings_rate_pct=round(savings_rate * 100, 1),
        category_breakdown=breakdown,
        waste_detected=waste_items,
        annual_projection=ann_projection,
        ai_suggestions=ai_suggestions,
        student_efficiency_score=ses,
    )
