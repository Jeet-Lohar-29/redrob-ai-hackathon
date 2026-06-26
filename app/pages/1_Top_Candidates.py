import streamlit as st
import json
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "dashboard_reports.json"

st.set_page_config(
    page_title="Top Candidates",
    page_icon="🏆",
    layout="wide"
)

st.title("🏆 Top Candidates Leaderboard")

# Load reports
with open(DATA_PATH, "r", encoding="utf-8") as f:
    candidates = json.load(f)

####################################################
# TOP 3 CARDS
####################################################

top3=sorted(candidates,key=lambda x:x["match_percentage"],reverse=True)[:3]

col1,col2,col3=st.columns(3)

with col1:
    st.success(
        f"""
🥇 Rank #1

Candidate:
{top3[0]['candidate_id']}

Match:
{top3[0]['match_percentage']}%

Recommendation:
{top3[0]['hiring_recommendation']}
"""
    )

with col2:
    st.info(
        f"""
🥈 Rank #2

Candidate:
{top3[1]['candidate_id']}

Match:
{top3[1]['match_percentage']}%

Recommendation:
{top3[1]['hiring_recommendation']}
"""
    )

with col3:
    st.warning(
        f"""
🥉 Rank #3

Candidate:
{top3[2]['candidate_id']}

Match:
{top3[2]['match_percentage']}%

Recommendation:
{top3[2]['hiring_recommendation']}
"""
    )

st.divider()

####################################################
# SEARCH BOX
####################################################

search=st.text_input(
    "🔍 Search Candidate ID"
)

recommendation_filter = st.selectbox(
    "Recommendation Filter",
    [
        "All",
        "Strong Hire",
        "Hire",
        "Consider"
    ]
)

####################################################
# DATAFRAME
####################################################

rows=[]

for c in candidates:

    rows.append(
        {
            "Candidate ID":c["candidate_id"],
            "Match %":c["match_percentage"],
            "Recommendation":c["hiring_recommendation"],
            "Confidence":c["confidence_level"],
            "Technical Fit":c["technical_fit"],
            "Behavioral Fit":c["behavioral_fit"],
            "Availability Fit":c["availability_fit"]
        }
    )

df=pd.DataFrame(rows)

if search:
    df=df[
        df["Candidate ID"]
        .str.contains(search.upper())
    ]

if recommendation_filter != "All":
    df = df[
        df["Recommendation"] == recommendation_filter
    ]

df=df.sort_values(
    "Match %",
    ascending=False
)

styled_df = (
    df.style
    .background_gradient(
        subset=["Match %"],
        cmap="Greens"
    )
)

st.dataframe(
    styled_df,
    use_container_width=True,
    hide_index=True
)