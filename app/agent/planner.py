from typing import Any, Dict, List


def _normalize_tool(intent: Dict[str, Any]) -> Dict[str, Any]:
    normalized = intent.copy()
    if normalized.get("intent") == "explain_candidate":
        normalized["intent"] = "candidate_explanation"
    return normalized


def _contains_text(value: str, patterns: List[str]) -> bool:
    lowered = str(value or "").lower()
    return any(pattern in lowered for pattern in patterns)


def _reason_for_tool(intent_name: str, query: str) -> str:
    if intent_name == "search_by_role":
        return "Search for candidates by role to match the recruiter’s hiring need."
    if intent_name == "search_by_skill":
        return "Search for candidates by skill keywords and technical fit."
    if intent_name == "recommend_best_candidate":
        return "Rank candidates and recommend the best fit for the requested role."
    if intent_name == "candidate_summary":
        return "Produce a recruiter review for the selected candidate with strengths, risks, and recommendation."
    if intent_name == "candidate_explanation":
        return "Generate recruiter rationale for why the requested candidate is recommended."
    if intent_name == "compare_candidates":
        return "Compare two candidates to surface differences in fit and risk."
    if intent_name == "search_by_company":
        return "Find candidates with the requested company background."
    if intent_name == "search_by_location":
        return "Filter candidates by geographic location."
    if intent_name == "search_by_experience":
        return "Filter candidates by years of experience or related profile signals."
    if intent_name == "generate_interview_questions":
        return "Create interview questions tailored to the selected candidate."
    if intent_name == "hiring_report":
        return "Summarize the candidate’s hiring readiness in a concise report."
    if intent_name == "top_candidates":
        return "Surface the top-ranked candidates in the pool."
    if intent_name == "strong_hires":
        return "Surface candidates with strong hiring recommendations."
    if intent_name == "low_risk":
        return "Surface candidates with the lowest hiring risk."
    if intent_name == "high_technical_fit":
        return "Surface candidates with the highest technical fit." 
    return "Select the most appropriate recruiter tool for this query."


def _build_plan(intent: Dict[str, Any]) -> List[Dict[str, Any]]:
    intent_name = intent.get("intent")
    query = str(intent.get("query", "")).lower()
    plan = []

    if intent_name == "search_by_role":
        plan.append({"tool": "search_by_role", "args": intent, "reason": _reason_for_tool(intent_name, query)})
        if _contains_text(query, ["low risk", "low-risk"]):
            plan.append({"tool": "low_risk", "args": intent, "reason": _reason_for_tool("low_risk", query)})
        if _contains_text(query, ["strong hire", "strong hires", "recommended"]):
            plan.append({"tool": "strong_hires", "args": intent, "reason": _reason_for_tool("strong_hires", query)})
        return plan

    if intent_name == "search_by_skill":
        plan.append({"tool": "search_by_skill", "args": intent, "reason": _reason_for_tool(intent_name, query)})
        if _contains_text(query, ["low risk", "low-risk"]):
            plan.append({"tool": "low_risk", "args": intent, "reason": _reason_for_tool("low_risk", query)})
        return plan

    if intent_name == "recommend_best_candidate":
        return [{"tool": "recommend_best_candidate", "args": intent, "reason": _reason_for_tool(intent_name, query)}]

    if intent_name in {"top_candidates", "strong_hires", "low_risk", "high_technical_fit", "candidate_summary", "candidate_explanation", "compare_candidates", "search_by_company", "search_by_location", "search_by_experience", "generate_interview_questions", "hiring_report", "general_question", "chat", "unknown"}:
        return [{"tool": intent_name, "args": intent, "reason": _reason_for_tool(intent_name, query)}]

    return [{"tool": "unknown", "args": intent, "reason": _reason_for_tool(intent_name, query)}]


def plan_intent(intent: Dict[str, Any]) -> List[Dict[str, Any]]:
    normalized = _normalize_tool(intent)
    return _build_plan(normalized)
