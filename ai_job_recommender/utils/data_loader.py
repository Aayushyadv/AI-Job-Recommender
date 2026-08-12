"""Data loading utilities with flexible column mapping and caching."""
import pandas as pd
import streamlit as st

DATA_PATH = "data/jobs.csv"

# Map common alternate column names -> canonical names used across the app
COLUMN_ALIASES = {
    "title": ["title", "job_title", "position", "role"],
    "company": ["company", "company_name", "employer"],
    "location": ["location", "job_location", "city"],
    "work_type": ["work_type", "employment_type", "job_type"],
    "experience": ["experience", "experience_level", "seniority"],
    "skills": ["skills", "required_skills", "skill_set"],
    "description": ["description", "job_description", "summary"],
    "salary_min": ["salary_min", "min_salary"],
    "salary_max": ["salary_max", "max_salary"],
    "posted_days_ago": ["posted_days_ago", "days_ago", "posted"],
}


def _canonicalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    lower_map = {c.lower().strip(): c for c in df.columns}
    rename = {}
    for canonical, aliases in COLUMN_ALIASES.items():
        for alias in aliases:
            if alias in lower_map:
                rename[lower_map[alias]] = canonical
                break
    return df.rename(columns=rename)


@st.cache_data(show_spinner="Loading job dataset...")
def load_jobs(path: str = DATA_PATH) -> pd.DataFrame:
    df = pd.read_csv(path)
    df = _canonicalize_columns(df)

    required = ["title", "company", "location", "work_type", "experience", "skills"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(
            f"Dataset is missing required columns: {missing}. "
            f"Found columns: {list(df.columns)}"
        )

    df["skills"] = df["skills"].fillna("").astype(str)
    df["description"] = df.get("description", pd.Series([""] * len(df))).fillna("")
    df["skills_list"] = df["skills"].apply(
        lambda s: [x.strip() for x in s.split(",") if x.strip()]
    )
    # Combined text field used by the TF-IDF recommender
    df["combined_text"] = (
        df["title"].fillna("") + " " +
        df["skills"].fillna("") + " " +
        df["description"].fillna("")
    ).str.lower()

    if "job_id" not in df.columns:
        df["job_id"] = range(1, len(df) + 1)

    return df


def get_filter_options(df: pd.DataFrame) -> dict:
    return {
        "locations": sorted(df["location"].dropna().unique().tolist()),
        "work_types": sorted(df["work_type"].dropna().unique().tolist()),
        "experience": sorted(df["experience"].dropna().unique().tolist()),
    }


def get_all_skills(df: pd.DataFrame) -> list:
    skills = set()
    for lst in df["skills_list"]:
        skills.update(lst)
    return sorted(skills)


def apply_filters(df: pd.DataFrame, location=None, work_type=None, experience=None) -> pd.DataFrame:
    filtered = df
    if location and location != "All":
        filtered = filtered[filtered["location"] == location]
    if work_type and work_type != "All":
        filtered = filtered[filtered["work_type"] == work_type]
    if experience and experience != "All":
        filtered = filtered[filtered["experience"] == experience]
    return filtered
