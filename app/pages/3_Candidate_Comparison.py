import streamlit as st
import json
from pathlib import Path
import plotly.graph_objects as go

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "dashboard_reports.json"

st.set_page_config(
    page_title="Candidate Comparison",
    layout="wide"
)

with open(DATA_PATH, "r", encoding="utf-8") as f:
    reports = json.load(f)

candidate_dict = {
    r["candidate_id"]:r
    for r in reports
}

st.title("⚔ Candidate Comparison")

ids = list(candidate_dict.keys())

col1,col2 = st.columns(2)

with col1:
    candidate1 = st.selectbox(
        "Candidate A",
        ids,
        index=0
    )

with col2:
    candidate2 = st.selectbox(
        "Candidate B",
        ids,
        index=1
    )

c1 = candidate_dict[candidate1]
c2 = candidate_dict[candidate2]

st.divider()

left,right = st.columns(2)

with left:
    st.subheader(candidate1)
    st.metric(
        "Match %",
        c1["match_percentage"]
    )

with right:
    st.subheader(candidate2)
    st.metric(
        "Match %",
        c2["match_percentage"]
    )

import pandas as pd

df = pd.DataFrame({
    "Metric":[
        "Technical Fit",
        "Behavioral Fit",
        "Availability Fit",
        "Risk Score"
    ],
    candidate1:[
        c1["technical_fit"],
        c1["behavioral_fit"],
        c1["availability_fit"],
        c1["risk_score"]
    ],
    candidate2:[
        c2["technical_fit"],
        c2["behavioral_fit"],
        c2["availability_fit"],
        c2["risk_score"]
    ]
})

st.subheader("📊 Score Comparison")

st.dataframe(
    df,
    use_container_width=True
)

winner = candidate1

if c2["match_percentage"] > c1["match_percentage"]:
    winner = candidate2

st.success(
    f"🏆 Better Match : {winner}"
)

categories = [
    "Technical Fit",
    "Behavioral Fit",
    "Availability Fit",
    "Risk Score"
]

fig = go.Figure()

fig.add_trace(go.Scatterpolar(
    r=[
        c1["technical_fit"],
        c1["behavioral_fit"],
        c1["availability_fit"],
        c1["risk_score"]
    ],
    theta=categories,
    fill='toself',
    name=candidate1
))

fig.add_trace(go.Scatterpolar(
    r=[
        c2["technical_fit"],
        c2["behavioral_fit"],
        c2["availability_fit"],
        c2["risk_score"]
    ],
    theta=categories,
    fill='toself',
    name=candidate2
))

fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="#0E1117",
    polar=dict(
        bgcolor="#0E1117",
        radialaxis=dict(
            visible=True,
            range=[0,100]
        )
    ),
    height=500
)

st.plotly_chart(fig,use_container_width=True)

col1,col2 = st.columns(2)

with col1:

    st.subheader("Strengths A")

    for s in c1["strengths"]:
        st.success(s)

with col2:

    st.subheader("Strengths B")

    for s in c2["strengths"]:
        st.success(s)

