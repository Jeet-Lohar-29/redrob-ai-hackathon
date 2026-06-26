import streamlit as st
import pandas as pd
import json
from pathlib import Path
import plotly.graph_objects as go

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "dashboard_reports.json"

st.set_page_config(page_title="Candidate Details",layout="wide")

with open(DATA_PATH, "r", encoding="utf-8") as f:
    reports = json.load(f)

candidate_dict = {}

for r in reports:
    candidate_dict[r["candidate_id"]] = r

st.title("🔎 Candidate Intelligence")

candidate_id = st.selectbox(
    "Select Candidate",
    list(candidate_dict.keys())
)

candidate = candidate_dict[candidate_id]

st.download_button(
    "📥 Download Candidate Report",
    data=json.dumps(candidate,indent=4),
    file_name=f"{candidate_id}.json",
    mime="application/json"
)

import plotly.graph_objects as go

gauge_fig = go.Figure(
    go.Indicator(
        mode="gauge+number",
        value=candidate["match_percentage"],
        title={"text":"Match %"},
        gauge={
            "axis":{"range":[0,100]},
            "steps":[
                {"range":[0,50],"color":"red"},
                {"range":[50,80],"color":"orange"},
                {"range":[80,100],"color":"green"}
            ]
        }
    )
)

col1,col2,col3,col4 = st.columns([2,1,1,1])

with col1:
    st.plotly_chart(gauge_fig,use_container_width=True)

with col2:
    st.metric("Recommendation",candidate["hiring_recommendation"])

with col3:
    st.metric("Confidence",candidate["confidence_level"])

with col4:
    st.metric("Risk Score",candidate["risk_score"])

st.divider()

st.subheader("📊 Scorecard")

col1,col2,col3 = st.columns(3)

with col1:
    st.metric(
        "Technical Fit",
        candidate["technical_fit"]
    )

with col2:
    st.metric(
        "Behavioral Fit",
        candidate["behavioral_fit"]
    )

with col3:
    st.metric(
        "Availability Fit",
        candidate["availability_fit"]
    )

st.write("### Technical Fit")
st.progress(candidate["technical_fit"]/100)

st.write("### Behavioral Fit")
st.progress(candidate["behavioral_fit"]/100)

st.write("### Availability Fit")
st.progress(candidate["availability_fit"]/100)

left,right = st.columns(2)

with left:

    st.subheader("✅ Strengths")

    for s in candidate["strengths"]:
        st.success(s)

with right:

    st.subheader("⚠ Risks")

    if len(candidate["risks"]) == 0:
        st.info("No major risks detected.")

    else:
        for r in candidate["risks"]:
            st.warning(r)

st.divider()

st.subheader("📝 Executive Summary")

st.info(
    candidate["executive_summary"]
)

st.subheader("🎯 Interview Focus")

for item in candidate["recommended_interview_focus"]:
    st.write("•",item)

