"""
LLM client - multi-provider wrapper (OpenAI / Groq / Gemini) with RAG support.
Falls back to canned responses if no API key is configured (demo-safe).

Supported providers (set LLM_PROVIDER in .env):
  - gemini  ->  uses GEMINI_API_KEY   +  MODEL_NAME (default: gemini-2.0-flash)
  - openai  ->  uses OPENAI_API_KEY   +  MODEL_NAME (default: gpt-3.5-turbo)
  - groq    ->  uses GROQ_API_KEY     +  MODEL_NAME (default: llama3-70b-8192)

Gemini uses its OpenAI-compatible REST endpoint so no extra SDK is needed.
"""
import os
from pathlib import Path
from typing import List, Dict, Optional
from dotenv import load_dotenv

# Always load .env from the backend/ directory regardless of CWD
_ENV_FILE = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=_ENV_FILE, override=True)

_PROVIDER    = os.getenv("LLM_PROVIDER", "gemini").lower()
_MODEL       = os.getenv("MODEL_NAME", "gemini-2.0-flash")
_OPENAI_KEY  = os.getenv("OPENAI_API_KEY", "")
_GROQ_KEY    = os.getenv("GROQ_API_KEY", "")
_GEMINI_KEY  = os.getenv("GEMINI_API_KEY", "")


# ---------------------------------------------------------------------------
# Provider helpers
# ---------------------------------------------------------------------------

def _has_key() -> bool:
    if _PROVIDER == "gemini":
        return bool(_GEMINI_KEY and not _GEMINI_KEY.startswith("your-"))
    if _PROVIDER == "groq":
        return bool(_GROQ_KEY and not _GROQ_KEY.startswith("gsk_your"))
    return bool(_OPENAI_KEY and not _OPENAI_KEY.startswith("sk-your"))


def get_provider_name() -> str:
    """Return a human-readable provider label for the API response."""
    if not _has_key():
        return "demo"
    return _PROVIDER


def _build_client():
    """Return (OpenAI client, model_name) tuple for the configured provider."""
    from openai import OpenAI

    if _PROVIDER == "gemini":
        client = OpenAI(
            api_key=_GEMINI_KEY,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
        )
        model = _MODEL if _MODEL else "gemini-2.0-flash"
        return client, model

    if _PROVIDER == "groq":
        client = OpenAI(
            api_key=_GROQ_KEY,
            base_url="https://api.groq.com/openai/v1",
        )
        model = _MODEL if _MODEL != "gpt-3.5-turbo" else "llama3-70b-8192"
        return client, model

    # Default: openai
    client = OpenAI(api_key=_OPENAI_KEY)
    return client, _MODEL


def _chat_completion(
    messages: List[Dict],
    max_tokens: int = 400,
    temperature: float = 0.7,
) -> str:
    """Send a chat completion request to the configured provider."""
    client, model = _build_client()

    # Gemma models don't support the 'system' role – fold it into the first user message
    if "gemma" in model.lower():
        adjusted: List[Dict] = []
        system_text = ""
        for msg in messages:
            if msg["role"] == "system":
                system_text = msg["content"]
            else:
                adjusted.append(msg)
        if system_text and adjusted:
            adjusted[0] = {
                "role": "user",
                "content": f"{system_text}\n\n{adjusted[0]['content']}",
            }
        messages = adjusted

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=max_tokens,
        temperature=temperature,
    )
    return response.choices[0].message.content.strip()


# ---------------------------------------------------------------------------
# Fallbacks (demo mode)
# ---------------------------------------------------------------------------

def _fallback_study(_: str) -> str:
    return (
        "Based on your schedule, start with the most urgent exams first. "
        "Break study sessions into 25-minute Pomodoro blocks with 5-minute breaks. "
        "Review notes the night before each exam. Tackle projects early to avoid last-minute stress. "
        "Keep Sundays lighter for recovery and reflection."
    )


def _fallback_budget(_: str) -> str:
    return (
        "Your biggest savings opportunity is in discretionary spending. "
        "Consider meal prepping to cut food costs by ~30%. "
        "Audit subscriptions monthly - cancel unused ones. "
        "Set a weekly cash-envelope budget for entertainment. "
        "Even saving an extra 50 TND/month compounds to 600 TND/year."
    )


def _fallback_chat(question: str, error: str = "") -> str:
    if error:
        # Surface real API errors (rate limit, auth, etc.)
        if "429" in error or "quota" in error.lower() or "rate" in error.lower():
            return (
                "⚠️ Limite de quota Gemini atteinte (free tier).\n"
                "Patiente quelques minutes ou change le modele dans .env :\n"
                "MODEL_NAME=gemini-1.5-flash  ou  gemini-1.0-pro\n\n"
                f"Erreur: {error[:200]}"
            )
        if "401" in error or "api_key" in error.lower() or ("invalid" in error.lower() and "argument" not in error.lower()):
            return (
                "🔑 Cle API invalide.\n"
                "Verifie GEMINI_API_KEY dans backend/.env\n"
                f"Erreur: {error[:200]}"
            )
        return f"❌ Erreur API ({_PROVIDER}):\n{error[:300]}"
    return (
        "Je suis en mode demo (aucune cle LLM configuree). "
        "Ajoute GEMINI_API_KEY dans backend/.env et redemarres le serveur."
    )


# ---------------------------------------------------------------------------
# Public functions
# ---------------------------------------------------------------------------

def get_study_recommendations(context: str) -> str:
    """Call LLM for study plan recommendations."""
    if not _has_key():
        return _fallback_study(context)
    try:
        return _chat_completion(
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert academic coach for university students. "
                        "Give concise, actionable, motivating study recommendations "
                        "in 3-5 bullet points. Be specific to the student's situation."
                    ),
                },
                {"role": "user", "content": context},
            ],
            max_tokens=300,
        )
    except Exception as e:
        print(f"[LLM] study recommendations error: {e}")
        return _fallback_study(context)


def get_budget_suggestions(context: str) -> str:
    """Call LLM for budget optimisation suggestions."""
    if not _has_key():
        return _fallback_budget(context)
    try:
        return _chat_completion(
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a personal finance advisor specialising in student budgets. "
                        "Provide 3-5 practical, specific money-saving tips based on the student's "
                        "actual spending. Be encouraging and realistic."
                    ),
                },
                {"role": "user", "content": context},
            ],
            max_tokens=300,
        )
    except Exception as e:
        print(f"[LLM] budget suggestions error: {e}")
        return _fallback_budget(context)


def chat_with_rag(
    question: str,
    rag_context: str = "",
    conversation_history: Optional[List[Dict]] = None,
) -> str:
    """
    RAG-augmented chat for the SmartStudent AI assistant.

    Parameters
    ----------
    question            : The student current question.
    rag_context         : Pre-retrieved context from the vector store.
    conversation_history: List of previous {"role": ..., "content": ...} dicts.
    """
    if not _has_key():
        return _fallback_chat("")

    system_prompt = (
        "You are SmartStudent AI, a friendly and knowledgeable assistant helping "
        "Tunisian university students with study strategies, time management, budgeting "
        "(in Tunisian Dinar - TND), and academic performance.\n"
        "Be concise, practical, and encouraging. Use bullet points when listing steps.\n"
        "When discussing money, use TND as the currency unless the user specifies otherwise.\n"
        "Always tailor advice to the student context provided."
    )

    if rag_context:
        system_prompt += f"\n\n{rag_context}"

    messages: List[Dict] = [{"role": "system", "content": system_prompt}]

    if conversation_history:
        messages.extend(conversation_history[-6:])

    messages.append({"role": "user", "content": question})

    try:
        return _chat_completion(messages, max_tokens=500, temperature=0.7)
    except Exception as e:
        print(f"[LLM] chat_with_rag error: {e}")
        return _fallback_chat(question, error=str(e))
