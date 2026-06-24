<div align="center">

# 🚀 Intelligent Candidate Discovery
### AI Recruiter Powered by Retrieval + Explainable AI

An end-to-end candidate ranking platform built for the **Redrob AI Hackathon**.

Combining:

🔎 BM25 Retrieval • 🧠 Dense Embeddings • ⚡ Cross Encoder Re-ranking • 📊 Explainable AI

---

![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly)
![Pandas](https://img.shields.io/badge/Pandas-black?style=for-the-badge&logo=pandas)
![SentenceTransformers](https://img.shields.io/badge/SentenceTransformers-orange?style=for-the-badge)
![BM25](https://img.shields.io/badge/BM25-Retrieval-success?style=for-the-badge)
![CrossEncoder](https://img.shields.io/badge/Cross_Encoder-ReRanking-red?style=for-the-badge)

</div>

---

# 📌 Problem Statement

Recruiters struggle to discover the best candidates from massive profile datasets.

Traditional keyword search often misses:

- Hidden talent
- Contextual relevance
- Behavioral signals
- Availability constraints
- Explainability

This project solves that by building an **AI-powered Candidate Intelligence Platform** that combines retrieval systems and explainable scoring.

---

# 🏗 Architecture

```text
100,000 Candidates
        ↓
BM25 Retrieval
        ↓
Top 5,000
        ↓
Dense Embeddings
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
Hiring Recommendation
```

---

# ✨ Features

## 🔎 Candidate Ranking

- BM25 Retrieval
- Dense Embedding Search
- Cross Encoder Re-ranking
- Match Percentage Scoring

---

## 📊 Candidate Intelligence

- Technical Fit
- Behavioral Fit
- Availability Fit
- Risk Score
- Confidence Level
- Hiring Recommendation

---

## 🧠 Explainable AI

Each candidate receives:

✅ Strengths

⚠ Risks

📄 Executive Summary

🎯 Interview Focus Areas

---

## ⚔ Candidate Comparison

Compare candidates side-by-side using:

- Radar Charts
- Score Comparison
- Strength Analysis
- Better Match Recommendation

---

## 📈 Analytics Dashboard

Interactive dashboard with:

### Match Distribution

### Recommendation Distribution

### Technical vs Behavioral Fit

### Confidence Analysis

### Top Candidates Leaderboard

---

# 🖥 Screenshots

---

## Home Page

![Home](screenshots/home1.png)

---

## Pipeline Architecture

![Pipeline](screenshots/home2.png)

---

## Top Candidates

![Leaderboard](screenshots/top1.png)

---

## Candidate Intelligence

![Candidate](screenshots/candidate1.png)

---

## Explainable AI Report

![Explainability](screenshots/candidate2.png)

---

## Candidate Comparison

![Comparison](screenshots/compare1.png)

---

## Radar Analysis

![Radar](screenshots/compare2.png)

---

## Analytics Dashboard

![Analytics](screenshots/analytics1.png)

---

## Recommendation Distribution

![Recommendation](screenshots/analytics3.png)

---

## Technical vs Behavioral Fit

![Fit Analysis](screenshots/analytics4.png)

---

# 📂 Project Structure

```text
redrob-ai-hackathon
│
├── app
│     ├── Home.py
│     ├── pages
│     │      ├── 1_Top_Candidates.py
│     │      ├── 2_Candidate_Details.py
│     │      ├── 3_Candidate_Comparison.py
│     │      └── 4_Analytics.py
│
├── data
├── reports
├── models
├── screenshots
├── notebooks
├── requirements.txt
└── README.md
```

---

# 📈 Scale

| Stage | Candidates |
|---------|------------|
| Initial Corpus | 100,000 |
| BM25 Retrieval | 5,000 |
| Dense Retrieval | 1,000 |
| Cross Encoder | 300 |
| Final Recommendation | Top Candidates |

---

# 🛠 Tech Stack

### Backend

- Python

### Data Processing

- Pandas
- NumPy

### Retrieval

- BM25
- BGE Embeddings
- Cross Encoder

### Visualization

- Plotly
- Streamlit

### Machine Learning

- Sentence Transformers
- Scikit-Learn

---

# 🚀 Installation

Clone repository:

```bash
git clone https://github.com/Jeet-Lohar-29/redrob-ai-hackathon.git
```

Move inside:

```bash
cd redrob-ai-hackathon
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# ▶ Run Application

```bash
streamlit run app/Home.py
```

---

# 📊 Outputs

The system generates:

- Candidate Reports
- Match Scores
- Explainability Insights
- Risk Analysis
- Executive Summary
- Interview Focus Areas
- Analytics Dashboard

---

# 🔮 Future Improvements

- Resume PDF Parsing
- Multi-job Support
- RAG-powered Recruiter Assistant
- LLM Chat Interface
- Real-time ATS Integration
- Candidate Q&A
- Semantic Resume Search

---

# 👨‍💻 Author

### Jeet Lohar

B.Tech CSE | Data Science Minor

AI • Retrieval Systems • Explainable AI • ML

GitHub:

https://github.com/Jeet-Lohar-29

---

# 🏆 Built For

## Redrob AI – India Runs Hackathon

### Intelligent Candidate Discovery

---

<div align="center">

⭐ If you like this project, give it a star!

</div>
