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

if "messages" not in st.session_state:
    st.session_state.messages = []

st.sidebar.subheader("Example Queries")
st.sidebar.info(
    """
Show top candidates

Show strong hires

Show low risk candidates

Show strong hires with low risk

Why is CAND_0018499 recommended?

Summarize CAND_0018499

Compare CAND_0018499 and CAND_0061265

Generate interview questions for CAND_0018499

What are the strengths of CAND_0018499
"""
)

if st.sidebar.button("Clear Chat"):
    st.session_state.messages = []
    st.experimental_rerun()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

query = st.chat_input("Ask Recruiter AI...")


def _badge(text: str, color: str = "gray") -> str:
    return f"<span style='background-color:{color}; color:white; padding:4px 8px; border-radius:4px;'>{text}</span>"


def _render_candidate_card(candidate: dict) -> None:
    if not candidate:
        return
    primary, secondary = st.columns([3, 2])
    with primary:
        st.markdown(f"### {candidate.get('candidate_id', 'Unknown')}")
        st.markdown(candidate.get('executive_summary', ''))
        st.markdown(
            f"{_badge(candidate.get('recommendation', 'Unknown'), '#2f80ed')} "
            f"{_badge(candidate.get('confidence_level', 'Unknown'), '#17b978')}"
        , unsafe_allow_html=True)
    with secondary:
        st.metric("Match", candidate.get('match_percentage', 'N/A'))
        st.metric("Technical", candidate.get('technical_fit', 'N/A'))
        st.metric("Risk", candidate.get('risk_score', 'N/A'))
        st.metric("Availability", candidate.get('availability_fit', 'N/A'))
    st.markdown("**Strengths:**")
    for strength in candidate.get('strengths', []):
        st.markdown(f"- {strength}")
    if candidate.get('risks'):
        st.markdown("**Risks:**")
        for risk in candidate.get('risks', []):
            st.markdown(f"- {risk}")
    st.markdown("---")


def _render_tool_result(result: dict) -> None:
    result_type = result.get("type")
    if result_type == "dataframe":
        records = result.get("data", [])
        if records:
            data_frame = pd.DataFrame(records)
            with st.expander("Candidate results", expanded=True):
                st.dataframe(data_frame, use_container_width=True)
                for record in records[:5]:
                    with st.expander(record.get('candidate_id', 'Candidate')):
                        _render_candidate_card(record)
        else:
            st.info(result.get("message", "No candidates found."))
    elif result_type == "object":
        data = result.get("data", {})
        if data.get("error"):
            st.error(data.get("error"))
        elif data.get("candidate_id"):
            with st.expander("Candidate summary", expanded=True):
                _render_candidate_card(data)
                st.json(data)
        elif data.get("candidate_1") and data.get("candidate_2"):
            st.markdown("### Candidate comparison")
            compare_cols = st.columns(2)
            with compare_cols[0]:
                _render_candidate_card(data.get("candidate_1", {}))
            with compare_cols[1]:
                _render_candidate_card(data.get("candidate_2", {}))
            with st.expander("Raw comparison data"):
                st.json(data)
        else:
            st.json(data)
    else:
        st.info(result.get("data", {}).get("message", "No detailed result available."))

if query:
    st.session_state.messages.append({"role": "user", "content": query})

    with st.chat_message("user"):
        st.markdown(query)

    response, result, history = recruiter_agent(query, df, st.session_state.messages)

    with st.chat_message("assistant"):
        st.markdown(response)
        _render_tool_result(result)

    st.session_state.messages.append({"role": "assistant", "content": response})
