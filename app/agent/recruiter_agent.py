import re
from agent.tools import *


def recruiter_agent(query, df):

    q = query.lower()

    # Extract candidate IDs from query
    ids = re.findall(
        r"CAND_\d+",
        query.upper()
    )

    # WHY CANDIDATE RECOMMENDED
    if "why" in q and len(ids) == 1:

        explanation = explain_candidate(
            ids[0],
            df
        )

        return (
            explanation,
            None
        )

    # CANDIDATE SUMMARY
    elif (
        ("summary" in q or "summarize" in q)
        and len(ids) == 1
    ):

        summary = candidate_summary(
            ids[0],
            df
        )

        return (
            summary,
            None
        )

    # COMPARE TWO CANDIDATES
    elif (
        "compare" in q
        and len(ids) == 2
    ):

        comparison = compare_candidates(
            ids[0],
            ids[1],
            df
        )

        return (
            str(comparison),
            None
        )

    # STRONG HIRE + LOW RISK
    elif (
        "strong hire" in q
        and "low risk" in q
    ):

        result = df[
            (df["hiring_recommendation"] == "Strong Hire")
            &
            (df["risk_score"] <= 20)
        ]

        return (
            "Strong hires with low risk found.",
            result
        )

    # TOP CANDIDATES
    elif "top" in q:

        result = top_candidates(df)

        return (
            "Top candidates found.",
            result
        )

    # STRONG HIRES
    elif "strong hire" in q:

        result = strong_hires(df)

        return (
            "Strong hires found.",
            result
        )

    # LOW RISK
    elif "low risk" in q:

        result = low_risk(df)

        return (
            "Low risk candidates found.",
            result
        )

    # HIGH TECHNICAL FIT
    elif "technical" in q:

        result = high_technical_fit(df)

        return (
            "High technical fit candidates found.",
            result
        )

    else:

        return (
            """
                I couldn't understand the query.

                Try:

                • Show top candidates

                • Show strong hires

                • Show low risk candidates

                • Find candidates with technical fit above 90

                • Why is CAND_0018499 recommended?

                • Summarize CAND_0018499

                • Compare CAND_0018499 and CAND_0061265

                • Show strong hires with low risk
            """,
            None
        )