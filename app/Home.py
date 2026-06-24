import streamlit as st

st.set_page_config(
    page_title="Intelligent Candidate Discovery",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Intelligent Candidate Discovery")

st.markdown(
"""
### AI Recruiter Powered by Retrieval + Explainable AI

An end-to-end candidate ranking system that combines:

- 🔍 BM25 Retrieval
- 🧠 BGE Dense Embeddings
- ⚡ Cross Encoder Re-ranking
- 📊 Feature Engineering
- 🎯 Final Match Scoring
- 🧾 Explainable AI Reports

---
"""
)

col1,col2,col3,col4=st.columns(4)

with col1:
    st.metric(
        "Candidates",
        "100,000"
    )

with col2:
    st.metric(
        "BM25 Shortlist",
        "5,000"
    )

with col3:
    st.metric(
        "Dense Retrieval",
        "1,000"
    )

with col4:
    st.metric(
        "Final Candidates",
        "300"
    )

st.divider()

st.subheader("Pipeline Architecture")

st.subheader("⚙️ Pipeline Architecture")

st.code("""
100,000 Candidates
        ↓
BM25 Retrieval
        ↓
Top 5,000
        ↓
BGE Dense Embeddings
        ↓
Top 1,000
        ↓
Cross Encoder Re-ranking
        ↓
Top 300
        ↓
Recruiter Intelligence Layer
        ↓
Explainability Engine
        ↓
Executive Dashboard
        ↓
Final Hiring Recommendation
""")

st.divider()

st.subheader("Project Features")

c1,c2=st.columns(2)

with c1:
    st.success("""
✔ Semantic Search

✔ Explainable AI

✔ Candidate Ranking

✔ Hiring Recommendation

✔ Behavioral Signals

✔ Match Percentage
""")

with c2:
    st.info("""
✔ Technical Fit

✔ Availability Fit

✔ Risk Analysis

✔ Interview Focus Areas

✔ Recruiter Engagement

✔ Candidate Comparison
""")
    
st.markdown("---")

st.markdown(
"""
<center>

Built for Redrob AI Hackathon 🚀

BM25 • Dense Retrieval • Cross Encoder • Explainable AI

Created using Python + Streamlit + Plotly

</center>
""",
unsafe_allow_html=True
)