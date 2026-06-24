import pandas as pd

def top_candidates(df, n=10):
    return df.sort_values(
        "match_percentage",
        ascending=False
    ).head(n)


def strong_hires(df):
    return df[
        df["hiring_recommendation"]=="Strong Hire"
    ]


def low_risk(df):
    return df[
        df["risk_score"]<=20
    ]


def high_technical_fit(df):
    return df[
        df["technical_fit"]>=90
    ]

def get_candidate(candidate_id, df):

    result = df[
        df["candidate_id"] == candidate_id
    ]

    if len(result) == 0:
        return None

    return result.iloc[0]

def candidate_summary(candidate_id, df):

    candidate = get_candidate(
        candidate_id,
        df
    )

    if candidate is None:
        return "Candidate not found"

    return f"""
Candidate {candidate_id}

Match Percentage: {candidate['match_percentage']}
Recommendation: {candidate['hiring_recommendation']}
Technical Fit: {candidate['technical_fit']}
Behavioral Fit: {candidate['behavioral_fit']}
Risk Score: {candidate['risk_score']}
"""

def explain_candidate(candidate_id, df):

    candidate = get_candidate(
        candidate_id,
        df
    )

    if candidate is None:
        return "Candidate not found"

    explanation = []

    if candidate["technical_fit"] >= 90:
        explanation.append(
            "Strong technical fit."
        )

    if candidate["risk_score"] <= 20:
        explanation.append(
            "Low risk profile."
        )

    if candidate["availability_fit"] >= 80:
        explanation.append(
            "Good availability."
        )

    return "\n".join(explanation)

def compare_candidates(
        cand1,
        cand2,
        df
):

    c1 = get_candidate(cand1, df)
    c2 = get_candidate(cand2, df)

    if c1 is None or c2 is None:
        return None

    return {
        "candidate_1": cand1,
        "match_1": c1["match_percentage"],

        "candidate_2": cand2,
        "match_2": c2["match_percentage"]
    }