import streamlit as st
import pandas as pd
import json
from pathlib import Path
import plotly.express as px

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "dashboard_reports.json"

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="Analytics Dashboard",
    layout="wide"
)

# ---------------- LOAD DATA ----------------

with open(DATA_PATH, "r", encoding="utf-8") as f:
    reports = json.load(f)

df = pd.DataFrame(reports)

# ---------------- SIDEBAR FILTERS ----------------

st.sidebar.header("Filters")

recommendation_filter = st.sidebar.multiselect(
    "Hiring Recommendation",
    options=df["hiring_recommendation"].unique(),
    default=df["hiring_recommendation"].unique()
)

confidence_filter = st.sidebar.multiselect(
    "Confidence Level",
    options=df["confidence_level"].unique(),
    default=df["confidence_level"].unique()
)

filtered_df = df[
    (df["hiring_recommendation"].isin(recommendation_filter))
    &
    (df["confidence_level"].isin(confidence_filter))
]

# ---------------- TITLE ----------------

st.title("📊 Recruiter Analytics Dashboard")

# ---------------- METRICS ----------------

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Candidates",
        len(filtered_df)
    )

with col2:
    st.metric(
        "Average Match %",
        round(filtered_df["match_percentage"].mean(), 1),
        delta="Healthy"
    )

with col3:
    strong_hires = len(
        filtered_df[
            filtered_df["hiring_recommendation"] == "Strong Hire"
        ]
    )

    percentage = round(
        (strong_hires / len(filtered_df)) * 100,
        1
    )

    st.metric(
        "Strong Hires",
        strong_hires,
        delta=f"{percentage}%"
    )

with col4:
    st.metric(
        "Average Technical Fit",
        round(filtered_df["technical_fit"].mean(), 1)
    )

# ---------------- TABS ----------------

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "📈 Distribution",
        "🥧 Recommendations",
        "🎯 Fit Analysis",
        "🏆 Top Candidates"
    ]
)

# =====================================================
# TAB 1
# =====================================================

with tab1:

    st.subheader("📈 Match Percentage Distribution")

    fig = px.histogram(
        filtered_df,
        x="match_percentage",
        nbins=20
    )

    fig.update_layout(template="plotly_dark")

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader("📉 Confidence Level Distribution")

    fig = px.histogram(
        filtered_df,
        x="confidence_level"
    )

    fig.update_layout(template="plotly_dark")

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# =====================================================
# TAB 2
# =====================================================

with tab2:

    st.subheader("🥧 Hiring Recommendation Distribution")

    fig = px.pie(
        filtered_df,
        names="hiring_recommendation"
    )

    fig.update_layout(template="plotly_dark")

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# =====================================================
# TAB 3
# =====================================================

with tab3:

    st.subheader("🎯 Technical vs Behavioral Fit")

    fig = px.scatter(
        filtered_df,
        x="technical_fit",
        y="behavioral_fit",
        color="match_percentage",
        hover_data=["candidate_id"]
    )

    fig.update_layout(template="plotly_dark")

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# =====================================================
# TAB 4
# =====================================================

with tab4:

    st.subheader("🏆 Top 10 Candidates")

    top10 = filtered_df.sort_values(
        "match_percentage",
        ascending=False
    ).head(10)

    st.dataframe(
        top10[
            [
                "candidate_id",
                "match_percentage",
                "hiring_recommendation",
                "technical_fit",
                "behavioral_fit"
            ]
        ],
        use_container_width=True
    )

