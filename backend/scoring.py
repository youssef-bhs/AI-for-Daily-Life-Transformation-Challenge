"""
Student Efficiency Score (SES) – shared scoring utility.

Formula
-------
SES = (W_study * study_score + W_budget * budget_score) * 100

Where:
  study_score  = clamp(1 - overload_ratio, 0, 1)
                 overload_ratio = days where hours > available / total_plan_days

  budget_score = clamp(savings_rate / 0.20, 0, 1)
                 Assumes 20 % savings rate = perfect score

Both are normalised to [0, 100].
For single-module calls, the other score is assumed 0.5 (neutral).

Interpretation bands
---------------------
  90-100 → Excellent   🟢
  70-89  → Good        🟡
  50-69  → Fair        🟠
  <50    → Needs Work  🔴
"""


def compute_study_score(overloaded_days: int, total_days: int) -> float:
    """Returns a 0-1 float for study plan balance."""
    if total_days == 0:
        return 0.5
    ratio = overloaded_days / total_days
    return max(0.0, min(1.0, 1.0 - ratio))


def compute_budget_score(savings_rate: float) -> float:
    """Returns a 0-1 float; 20 % savings rate = 1.0."""
    return max(0.0, min(1.0, savings_rate / 0.20))


def compute_efficiency_score(
    study_score: float = 0.5,
    budget_score: float = 0.5,
    w_study: float = 0.5,
    w_budget: float = 0.5,
) -> float:
    raw = w_study * study_score + w_budget * budget_score
    return round(raw * 100, 1)


def score_label(score: float) -> str:
    if score >= 90:
        return "Excellent 🟢"
    if score >= 70:
        return "Good 🟡"
    if score >= 50:
        return "Fair 🟠"
    return "Needs Work 🔴"
