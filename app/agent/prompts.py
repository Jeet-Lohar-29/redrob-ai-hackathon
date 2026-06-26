def executive_summary_prompt(candidate_data):

    return f"""
You are a senior AI recruiter.

Candidate Information:

{candidate_data}

Generate:

1. Executive Summary

2. Strengths

3. Risks

4. Recommended Interview Areas

Keep response professional and concise.
"""


def comparison_prompt(candidate1, candidate2):

    return f"""
You are an expert recruiter.

Candidate A:

{candidate1}

Candidate B:

{candidate2}

Compare both candidates.

Explain:

- Strengths
- Risks
- Who is better overall
- Hiring recommendation
"""