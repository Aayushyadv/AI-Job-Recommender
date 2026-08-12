"""Reusable Plotly chart builders, styled for the dark theme."""
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

DARK_TEMPLATE = "plotly_dark"
ACCENT = "#FF4B4B"
PALETTE = ["#FF4B4B", "#4B8BFF", "#4BFF9F", "#FFC94B", "#B14BFF", "#4BFFF0"]


def top_skills_chart(df: pd.DataFrame, n: int = 10):
    all_skills = []
    for lst in df["skills_list"]:
        all_skills.extend(lst)
    counts = pd.Series(all_skills).value_counts().head(n).sort_values()
    fig = px.bar(
        x=counts.values, y=counts.index, orientation="h",
        labels={"x": "Job Postings", "y": "Skill"},
        title=f"Top {n} In-Demand Skills",
        color=counts.values, color_continuous_scale=["#2b2f3a", ACCENT],
    )
    fig.update_layout(template=DARK_TEMPLATE, coloraxis_showscale=False, height=420)
    return fig


def top_locations_chart(df: pd.DataFrame, n: int = 10):
    counts = df["location"].value_counts().head(n).sort_values()
    fig = px.bar(
        x=counts.values, y=counts.index, orientation="h",
        labels={"x": "Job Postings", "y": "Location"},
        title=f"Top {n} Hiring Locations",
        color=counts.values, color_continuous_scale=["#2b2f3a", "#4B8BFF"],
    )
    fig.update_layout(template=DARK_TEMPLATE, coloraxis_showscale=False, height=420)
    return fig


def experience_distribution_chart(df: pd.DataFrame):
    counts = df["experience"].value_counts()
    fig = px.pie(
        names=counts.index, values=counts.values,
        title="Experience Level Distribution",
        color_discrete_sequence=PALETTE, hole=0.45,
    )
    fig.update_layout(template=DARK_TEMPLATE, height=420)
    return fig


def work_type_chart(df: pd.DataFrame):
    counts = df["work_type"].value_counts()
    fig = px.bar(
        x=counts.index, y=counts.values,
        labels={"x": "Work Type", "y": "Job Postings"},
        title="Jobs by Work Type",
        color=counts.index, color_discrete_sequence=PALETTE,
    )
    fig.update_layout(template=DARK_TEMPLATE, showlegend=False, height=380)
    return fig


def match_gauge(match_pct: float):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=match_pct,
        number={"suffix": "%"},
        gauge={
            "axis": {"range": [0, 100]},
            "bar": {"color": ACCENT},
            "steps": [
                {"range": [0, 40], "color": "#3a2020"},
                {"range": [40, 70], "color": "#3a3520"},
                {"range": [70, 100], "color": "#203a28"},
            ],
        },
        title={"text": "Match Score"},
    ))
    fig.update_layout(template=DARK_TEMPLATE, height=250, margin=dict(t=40, b=10, l=20, r=20))
    return fig
