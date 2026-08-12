"""TF-IDF + Linear Kernel based job recommendation engine."""
import numpy as np
import pandas as pd
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel


@st.cache_resource(show_spinner="Building recommendation engine...")
def build_vectorizer(corpus: tuple):
    """Cache the fitted vectorizer + matrix keyed off the corpus tuple (hashable)."""
    vectorizer = TfidfVectorizer(
        stop_words="english",
        max_features=5000,
        ngram_range=(1, 2),
    )
    matrix = vectorizer.fit_transform(corpus)
    return vectorizer, matrix


def _get_engine(df: pd.DataFrame):
    corpus = tuple(df["combined_text"].tolist())
    return build_vectorizer(corpus)


def recommend_by_text(df: pd.DataFrame, query: str, top_n: int = 15) -> pd.DataFrame:
    """Recommend jobs given a free-text query (job title search or skills search)."""
    if df.empty or not query.strip():
        return df.head(0).assign(match_score=[])

    vectorizer, matrix = _get_engine(df)
    query_vec = vectorizer.transform([query.lower()])
    scores = linear_kernel(query_vec, matrix).flatten()

    result = df.copy()
    result["match_score"] = scores
    result = result[result["match_score"] > 0].sort_values("match_score", ascending=False)
    result["match_pct"] = (result["match_score"] / (result["match_score"].max() or 1) * 100).round(1)
    return result.head(top_n)


def recommend_by_resume(df: pd.DataFrame, resume_text: str, top_n: int = 15) -> pd.DataFrame:
    """Same engine, driven by extracted resume text instead of a short query."""
    return recommend_by_text(df, resume_text, top_n=top_n)


def why_recommended(job_row: pd.Series, query_skills: list) -> list:
    """Return the overlapping skills/keywords that drove the match, for the 'Why Recommended' box."""
    job_skills_lower = [s.lower() for s in job_row.get("skills_list", [])]
    query_lower = [s.lower().strip() for s in query_skills if s.strip()]
    overlap = [s for s in job_row.get("skills_list", []) if s.lower() in query_lower]
    if not overlap:
        # fall back to substring matches against title/description
        text = (job_row.get("title", "") + " " + job_row.get("description", "")).lower()
        overlap = [s for s in query_lower if s in text]
    return overlap


def skill_gap(job_row: pd.Series, user_skills: list) -> dict:
    """Compare the user's skills to a job's required skills."""
    job_skills = set(s.lower() for s in job_row.get("skills_list", []))
    user_skills_lower = set(s.lower().strip() for s in user_skills if s.strip())

    matched = job_skills & user_skills_lower
    missing = job_skills - user_skills_lower
    match_pct = round(len(matched) / len(job_skills) * 100, 1) if job_skills else 0.0

    return {
        "matched": sorted(matched),
        "missing": sorted(missing),
        "match_pct": match_pct,
    }
