from pathlib import Path
import pandas as pd
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "jobs.csv"

COLUMN_ALIASES = {
    "title": ["title", "job_title", "position", "role"],
    "company": ["company", "company_name", "employer", "name"],
    "location": ["location", "job_location", "city"],
    "work_type": [
        "work_type",
        "employment_type",
        "job_type",
        "formatted_work_type",
    ],
    "experience": [
        "experience",
        "experience_level",
        "seniority",
        "formatted_experience_level",
    ],
    "skills": [
        "skills",
        "required_skills",
        "skill_set",
        "skill_abr",
    ],
    "description": [
        "description",
        "job_description",
        "summary",
        "description_x",
    ],
    "salary_min": ["salary_min", "min_salary"],
    "salary_max": ["salary_max", "max_salary"],
    "posted_days_ago": [
        "posted_days_ago",
        "days_ago",
        "posted",
    ],
}


def _canonicalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    lower_map = {
        str(c).lower().strip(): c
        for c in df.columns
    }

    rename = {}

    for canonical, aliases in COLUMN_ALIASES.items():
        for alias in aliases:
            alias_lower = alias.lower().strip()

            if alias_lower in lower_map:
                rename[lower_map[alias_lower]] = canonical
                break

    return df.rename(columns=rename)


@st.cache_data(show_spinner="Loading job dataset...")
def load_jobs(path=None) -> pd.DataFrame:

    if path is None:
        path = DATA_PATH

    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(
            f"Dataset not found: {path}"
        )

    df = pd.read_csv(path)
    df = _canonicalize_columns(df)

    required = [
        "title",
        "company",
        "location",
        "work_type",
        "experience",
        "skills",
    ]

    missing = [
        column
        for column in required
        if column not in df.columns
    ]

    if missing:
        raise ValueError(
            f"Dataset is missing required columns: {missing}. "
            f"Found columns: {list(df.columns)}"
        )

    text_columns = [
        "title",
        "company",
        "location",
        "work_type",
        "experience",
        "skills",
    ]

    for column in text_columns:
        df[column] = (
            df[column]
            .fillna("")
            .astype(str)
            .str.strip()
        )

    if "description" not in df.columns:
        df["description"] = ""
    else:
        df["description"] = (
            df["description"]
            .fillna("")
            .astype(str)
        )

    df["skills_list"] = df["skills"].apply(
        lambda s: [
            x.strip()
            for x in str(s).replace("|", ",").split(",")
            if x.strip()
        ]
    )

    df["combined_text"] = (
        df["title"].fillna("")
        + " "
        + df["skills"].fillna("")
        + " "
        + df["description"].fillna("")
    ).str.lower()

    if "job_id" not in df.columns:
        df["job_id"] = range(1, len(df) + 1)

    return df


def get_filter_options(df: pd.DataFrame) -> dict:
    return {
        "locations": sorted(
            df["location"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        ),
        "work_types": sorted(
            df["work_type"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        ),
        "experience": sorted(
            df["experience"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        ),
    }


def get_all_skills(df: pd.DataFrame) -> list:
    skills = set()

    for skill_list in df["skills_list"]:
        skills.update(skill_list)

    return sorted(skills)


def apply_filters(
    df: pd.DataFrame,
    location=None,
    work_type=None,
    experience=None,
) -> pd.DataFrame:

    filtered = df.copy()

    if location and location != "All":
        filtered = filtered[
            filtered["location"] == location
        ]

    if work_type and work_type != "All":
        filtered = filtered[
            filtered["work_type"] == work_type
        ]

    if experience and experience != "All":
        filtered = filtered[
            filtered["experience"] == experience
        ]

    return filtered
