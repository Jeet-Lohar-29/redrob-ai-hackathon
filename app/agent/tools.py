import re
from typing import Any, Dict, List, Optional

import pandas as pd

SEARCH_FIELDS = [
    "executive_summary",
    "strengths",
    "risks",
    "recommended_interview_focus",
    "hiring_recommendation",
    "confidence_level",
]

ROLE_SYNONYMS = {
    "backend engineer": ["backend", "api", "microservices", "python", "java"],
    "backend developer": ["backend", "api", "microservices", "python", "java"],
    "python engineer": ["python", "backend", "automation"],
    "java developer": ["java", "backend", "spring"],
    "ai engineer": ["ai", "machine learning", "ml", "llm", "nlp"],
    "machine learning engineer": ["machine learning", "ml", "ai", "data science"],
    "ml engineer": ["machine learning", "ml", "ai"],
    "llm engineer": ["llm", "large language model", "ai"],
    "nlp engineer": ["nlp", "natural language", "language model"],
    "data scientist": ["data science", "machine learning", "analytics"],
    "data analyst": ["data", "analytics", "business intelligence"],
    "software engineer": ["software engineer", "sde", "developer"],
    "sde": ["software engineer", "developer"],
    "platform engineer": ["platform", "cloud", "infrastructure"],
    "cloud engineer": ["cloud", "platform", "devops"],
}


def _normalize_text(value: Any) -> str:
    if isinstance(value, list):
        return " ".join(str(item) for item in value).lower()
    if pd.isna(value):
        return ""
    return str(value).lower()


def _aggregate_search_text(row: pd.Series) -> str:
    values = [_normalize_text(row.get(field, "")) for field in SEARCH_FIELDS]
    return " ".join(values)


def _term_tokens(query: str) -> List[str]:
    return [token for token in re.split(r"\W+", query.lower()) if token]


def _resolve_role_terms(query: str) -> str:
    if not query:
        return ""
    lower = query.strip().lower()
    for key, terms in ROLE_SYNONYMS.items():
        if key in lower:
            return " ".join(terms)
    return query


def _filter_by_text(df: pd.DataFrame, query: str, fields: Optional[List[str]] = None) -> pd.DataFrame:
    query_value = str(query).strip().lower()
    if not query_value:
        return df.iloc[0:0]

    tokens = _term_tokens(query_value)
    if not tokens:
        return df.iloc[0:0]

    fields_to_search = fields or SEARCH_FIELDS
    mask = pd.Series(False, index=df.index)
    for field in fields_to_search:
        if field not in df.columns:
            continue
        field_text = df[field].apply(_normalize_text)
        for token in tokens:
            mask = mask | field_text.str.contains(re.escape(token), na=False)

    return df[mask].sort_values("match_percentage", ascending=False)


def top_candidates(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    if df is None or df.empty:
        return pd.DataFrame([])
    if "match_percentage" in df.columns:
        return df.sort_values("match_percentage", ascending=False).head(n)
    return df.head(n)


def strong_hires(df: pd.DataFrame) -> pd.DataFrame:
    if df is None or df.empty:
        return pd.DataFrame([])
    if "hiring_recommendation" not in df.columns:
        return pd.DataFrame([])
    return df[df["hiring_recommendation"].astype(str).str.contains("strong hire", case=False, na=False)]


def low_risk(df: pd.DataFrame) -> pd.DataFrame:
    if df is None or df.empty:
        return pd.DataFrame([])
    if "risk_score" not in df.columns:
        return pd.DataFrame([])
    return df[df["risk_score"].fillna(100).astype(float) <= 20]


def high_technical_fit(df: pd.DataFrame) -> pd.DataFrame:
    if df is None or df.empty:
        return pd.DataFrame([])
    if "technical_fit" not in df.columns:
        return pd.DataFrame([])
    return df[df["technical_fit"].fillna(0).astype(float) >= 90]


def get_candidate(candidate_id: str, df: pd.DataFrame) -> Optional[pd.Series]:
    if not candidate_id or df is None:
        return None
    mask = df["candidate_id"].astype(str).str.upper() == str(candidate_id).strip().upper()
    result = df[mask]
    if result.empty:
        return None
    return result.iloc[0]


def candidate_summary(candidate_id: str, df: pd.DataFrame) -> Dict[str, Any]:
    candidate = get_candidate(candidate_id, df)
    if candidate is None:
        return {"error": "candidate_not_found", "candidate_id": candidate_id}

    return {
        "candidate_id": candidate_id,
        "match_percentage": int(candidate.get("match_percentage", 0) or 0),
        "recommendation": candidate.get("hiring_recommendation", "Unknown"),
        "technical_fit": int(candidate.get("technical_fit", 0) or 0),
        "behavioral_fit": int(candidate.get("behavioral_fit", 0) or 0),
        "risk_score": int(candidate.get("risk_score", 0) or 0),
        "confidence_level": candidate.get("confidence_level", "Unknown"),
        "availability_fit": int(candidate.get("availability_fit", 0) or 0),
        "strengths": candidate.get("strengths", []),
        "risks": candidate.get("risks", []),
        "executive_summary": candidate.get("executive_summary", ""),
        "recommended_interview_focus": candidate.get("recommended_interview_focus", []),
    }


def explain_candidate(candidate_id: str, df: pd.DataFrame) -> Dict[str, Any]:
    candidate = get_candidate(candidate_id, df)
    if candidate is None:
        return {"error": "candidate_not_found", "candidate_id": candidate_id}

    return {
        "candidate_id": candidate_id,
        "technical_fit": int(candidate.get("technical_fit", 0) or 0),
        "risk_score": int(candidate.get("risk_score", 0) or 0),
        "availability_fit": int(candidate.get("availability_fit", 0) or 0),
        "recommendation": candidate.get("hiring_recommendation", "Unknown"),
        "confidence_level": candidate.get("confidence_level", "Unknown"),
        "strengths": candidate.get("strengths", []),
        "risks": candidate.get("risks", []),
        "executive_summary": candidate.get("executive_summary", ""),
    }


def compare_candidates(cand1: str, cand2: str, df: pd.DataFrame) -> Dict[str, Any]:
    primary = get_candidate(cand1, df)
    secondary = get_candidate(cand2, df)
    if primary is None or secondary is None:
        return {
            "error": "candidate_not_found",
            "missing_candidates": [cid for cid, cand in ((cand1, primary), (cand2, secondary)) if cand is None],
        }

    def candidate_info(candidate: pd.Series) -> Dict[str, Any]:
        return {
            "candidate_id": candidate.get("candidate_id"),
            "match_percentage": int(candidate.get("match_percentage", 0) or 0),
            "technical_fit": int(candidate.get("technical_fit", 0) or 0),
            "behavioral_fit": int(candidate.get("behavioral_fit", 0) or 0),
            "risk_score": int(candidate.get("risk_score", 0) or 0),
            "recommendation": candidate.get("hiring_recommendation", "Unknown"),
            "confidence_level": candidate.get("confidence_level", "Unknown"),
            "availability_fit": int(candidate.get("availability_fit", 0) or 0),
        }

    return {
        "candidate_1": candidate_info(primary),
        "candidate_2": candidate_info(secondary),
    }


def _parse_years(text: str) -> Optional[float]:
    if not text:
        return None
    match = re.search(r"(\d+(?:\.\d+)?)\s*(?:years|yrs|year)", text, re.I)
    if not match:
        return None
    try:
        return float(match.group(1))
    except ValueError:
        return None


def search_by_role(role: str, df: pd.DataFrame) -> pd.DataFrame:
    if df is None:
        return pd.DataFrame([])
    resolved = _resolve_role_terms(role)
    return _filter_by_text(df, resolved, fields=["executive_summary", "strengths", "recommended_interview_focus"])


def search_by_skill(skill: str, df: pd.DataFrame) -> pd.DataFrame:
    if df is None:
        return pd.DataFrame([])
    return _filter_by_text(df, skill, fields=["executive_summary", "strengths", "recommended_interview_focus"])


def search_by_company(company: str, df: pd.DataFrame) -> pd.DataFrame:
    if df is None:
        return pd.DataFrame([])
    return _filter_by_text(df, company, fields=["executive_summary", "strengths"])


def search_by_location(location: str, df: pd.DataFrame) -> pd.DataFrame:
    if df is None:
        return pd.DataFrame([])
    return _filter_by_text(df, location, fields=["executive_summary", "strengths"])


def search_by_experience(experience: str, df: pd.DataFrame) -> pd.DataFrame:
    if df is None:
        return pd.DataFrame([])
    target_years = _parse_years(str(experience))
    if target_years is None:
        return _filter_by_text(df, experience, fields=["executive_summary", "strengths"])

    def candidate_matches(series: pd.Series) -> bool:
        aggregated = _aggregate_search_text(series)
        found_years = _parse_years(aggregated)
        return found_years is not None and found_years >= target_years

    filtered = df[df.apply(candidate_matches, axis=1)]
    return filtered.sort_values("match_percentage", ascending=False)


def search_by_confidence_level(confidence: str, df: pd.DataFrame) -> pd.DataFrame:
    if df is None:
        return pd.DataFrame([])
    return df[df["confidence_level"].astype(str).str.contains(str(confidence), case=False, na=False)]


def search_by_recommendation(recommendation: str, df: pd.DataFrame) -> pd.DataFrame:
    if df is None:
        return pd.DataFrame([])
    return df[df["hiring_recommendation"].astype(str).str.contains(str(recommendation), case=False, na=False)]


def search_by_availability(availability: str, df: pd.DataFrame) -> pd.DataFrame:
    if df is None:
        return pd.DataFrame([])
    value = str(availability).strip().lower()
    if value.isdigit():
        threshold = int(value)
        return df[df["availability_fit"].astype(float) >= threshold]
    return _filter_by_text(df, availability, fields=["executive_summary", "strengths"])


def calculate_recommendation_score(candidate: pd.Series) -> float:
    match = float(candidate.get("match_percentage", 0) or 0) / 100.0
    technical = float(candidate.get("technical_fit", 0) or 0) / 100.0
    behavioral = float(candidate.get("behavioral_fit", 0) or 0) / 100.0
    availability = float(candidate.get("availability_fit", 0) or 0) / 100.0
    risk = float(candidate.get("risk_score", 0) or 0) / 100.0
    return 0.4 * match + 0.2 * technical + 0.15 * behavioral + 0.1 * availability + 0.15 * max(0.0, 1.0 - risk)


def recommend_best_candidates(df: pd.DataFrame, n: int = 5) -> pd.DataFrame:
    if df is None or df.empty:
        return pd.DataFrame([])
    df = df.copy()
    df["recommendation_score"] = df.apply(calculate_recommendation_score, axis=1)
    return df.sort_values(["recommendation_score", "match_percentage"], ascending=[False, False]).head(n)


def recommend_best_candidate(role: str, df: pd.DataFrame, n: int = 5) -> pd.DataFrame:
    if df is None:
        return pd.DataFrame([])
    if role:
        candidates = search_by_role(role, df)
    else:
        candidates = df
    return recommend_best_candidates(candidates, n=n)


def generate_interview_questions(candidate_id: str, df: pd.DataFrame) -> Dict[str, Any]:
    candidate = get_candidate(candidate_id, df)
    if candidate is None:
        return {"error": "candidate_not_found", "candidate_id": candidate_id}

    return {
        "candidate_id": candidate_id,
        "recommendation": candidate.get("hiring_recommendation", "Unknown"),
        "technical_fit": int(candidate.get("technical_fit", 0) or 0),
        "behavioral_fit": int(candidate.get("behavioral_fit", 0) or 0),
        "availability_fit": int(candidate.get("availability_fit", 0) or 0),
        "strengths": candidate.get("strengths", []),
        "risks": candidate.get("risks", []),
        "recommended_interview_focus": candidate.get("recommended_interview_focus", []),
        "executive_summary": candidate.get("executive_summary", ""),
    }


def hiring_report(candidate_id: str, df: pd.DataFrame) -> Dict[str, Any]:
    candidate = get_candidate(candidate_id, df)
    if candidate is None:
        return {"error": "candidate_not_found", "candidate_id": candidate_id}

    return {
        "candidate_id": candidate_id,
        "match_percentage": int(candidate.get("match_percentage", 0) or 0),
        "recommendation": candidate.get("hiring_recommendation", "Unknown"),
        "technical_fit": int(candidate.get("technical_fit", 0) or 0),
        "behavioral_fit": int(candidate.get("behavioral_fit", 0) or 0),
        "risk_score": int(candidate.get("risk_score", 0) or 0),
        "confidence_level": candidate.get("confidence_level", "Unknown"),
        "availability_fit": int(candidate.get("availability_fit", 0) or 0),
        "strengths": candidate.get("strengths", []),
        "risks": candidate.get("risks", []),
        "executive_summary": candidate.get("executive_summary", ""),
        "recommended_interview_focus": candidate.get("recommended_interview_focus", []),
    }


def top_n_candidates(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    return top_candidates(df, n=n)
