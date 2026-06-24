import streamlit as st
import pandas as pd
import json
from pathlib import Path

from agent.recruiter_agent import recruiter_agent

DATA_PATH = Path(__file__).parent.parent / "data" / "dashboard_reports.json"

with open(DATA_PATH, "r") as f:
    reports = json.load(f)

df = pd.DataFrame(reports)

st.title("🤖 AI Recruiter Agent")

st.markdown("""
Ask things like:

- Show top candidates
- Show strong hires
- Show low risk candidates
- Find candidates with high technical fit
""")

query = st.chat_input(
    "Ask the AI recruiter..."
)

if query:

    message, result = recruiter_agent(
        query,
        df
    )

    st.success(message)

    if result is not None:

        st.dataframe(
            result,
            use_container_width=True
        )

