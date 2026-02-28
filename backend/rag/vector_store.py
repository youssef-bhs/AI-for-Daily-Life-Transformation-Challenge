"""
SmartStudent AI – Vector Store
Embeds knowledge base documents using OpenAI embeddings (text-embedding-3-small).
Falls back to TF-IDF + cosine similarity when no API key is configured.
"""
import os
import math
import re
from pathlib import Path
from typing import List, Dict, Tuple
from dotenv import load_dotenv

# Always load .env from backend/ regardless of CWD
_ENV_FILE = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=_ENV_FILE, override=True)

_OPENAI_KEY = os.getenv("OPENAI_API_KEY", "")
_EMBED_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")

# In-memory index: list of (doc, embedding_vector)
_index: List[Tuple[Dict, List[float]]] = []
_tfidf_index: List[Tuple[Dict, Dict[str, float]]] = []   # fallback
_use_openai_embed = bool(_OPENAI_KEY and not _OPENAI_KEY.startswith("sk-your"))


# ──────────────────────────────────────────────────────────────────────────────
# Utility – cosine similarity
# ──────────────────────────────────────────────────────────────────────────────

def _cosine(a: List[float], b: List[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


# ──────────────────────────────────────────────────────────────────────────────
# OpenAI embedding
# ──────────────────────────────────────────────────────────────────────────────

def _openai_embed(text: str) -> List[float]:
    from openai import OpenAI
    client = OpenAI(api_key=_OPENAI_KEY)
    response = client.embeddings.create(model=_EMBED_MODEL, input=text)
    return response.data[0].embedding


# ──────────────────────────────────────────────────────────────────────────────
# TF-IDF fallback
# ──────────────────────────────────────────────────────────────────────────────

def _tokenize(text: str) -> List[str]:
    return re.findall(r"[a-z]+", text.lower())


def _tfidf_vector(tokens: List[str], idf: Dict[str, float]) -> Dict[str, float]:
    tf: Dict[str, float] = {}
    for t in tokens:
        tf[t] = tf.get(t, 0) + 1
    total = max(len(tokens), 1)
    return {t: (count / total) * idf.get(t, 0.0) for t, count in tf.items()}


def _build_idf(corpus: List[List[str]]) -> Dict[str, float]:
    n = len(corpus)
    df: Dict[str, int] = {}
    for doc_tokens in corpus:
        for t in set(doc_tokens):
            df[t] = df.get(t, 0) + 1
    return {t: math.log((n + 1) / (freq + 1)) + 1 for t, freq in df.items()}


def _tfidf_cosine(vec_a: Dict[str, float], vec_b: Dict[str, float]) -> float:
    keys = set(vec_a) & set(vec_b)
    dot = sum(vec_a[k] * vec_b[k] for k in keys)
    norm_a = math.sqrt(sum(v * v for v in vec_a.values()))
    norm_b = math.sqrt(sum(v * v for v in vec_b.values()))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


# ──────────────────────────────────────────────────────────────────────────────
# Public API
# ──────────────────────────────────────────────────────────────────────────────

def build_index(documents: List[Dict]) -> None:
    """Embed all documents and store in the in-memory index."""
    global _index, _tfidf_index, _use_openai_embed

    if _use_openai_embed:
        try:
            print(f"[VectorStore] Building OpenAI embedding index ({_EMBED_MODEL})…")
            for doc in documents:
                text = f"{doc['title']}\n{doc['content']}"
                vec = _openai_embed(text)
                _index.append((doc, vec))
            print(f"[VectorStore] Indexed {len(_index)} documents with OpenAI embeddings.")
            return
        except Exception as e:
            print(f"[VectorStore] OpenAI embedding failed: {e}. Falling back to TF-IDF.")
            _index.clear()
            _use_openai_embed = False

    # TF-IDF fallback
    print("[VectorStore] Building TF-IDF index (no API key / fallback)…")
    corpus_tokens = [_tokenize(f"{d['title']} {d['content']}") for d in documents]
    idf = _build_idf(corpus_tokens)
    for doc, tokens in zip(documents, corpus_tokens):
        vec = _tfidf_vector(tokens, idf)
        _tfidf_index.append((doc, vec, tokens, idf))
    print(f"[VectorStore] Indexed {len(_tfidf_index)} documents with TF-IDF.")


def retrieve(query: str, top_k: int = 3) -> List[Dict]:
    """Return top_k most relevant documents for a query."""
    if not _index and not _tfidf_index:
        return []

    if _use_openai_embed and _index:
        try:
            q_vec = _openai_embed(query)
            scored = [(doc, _cosine(q_vec, vec)) for doc, vec in _index]
        except Exception:
            scored = []
    else:
        if not _tfidf_index:
            return []
        _, _, _, idf = _tfidf_index[0]
        q_tokens = _tokenize(query)
        q_vec = _tfidf_vector(q_tokens, idf)
        scored = [(doc, _tfidf_cosine(q_vec, vec)) for doc, vec, _, _ in _tfidf_index]

    scored.sort(key=lambda x: x[1], reverse=True)
    return [doc for doc, score in scored[:top_k] if score > 0]
