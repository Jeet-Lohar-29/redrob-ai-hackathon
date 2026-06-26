from agent.gemini_agent import ask_gemini
import json
import re
from typing import Any, Dict, List, Optional

SUPPORTED_INTENTS = [
    "top_candidates",
    "strong_hires",
    "low_risk",
    "high_technical_fit",
    "candidate_summary",
    "explain_candidate",
    "candidate_explanation",
    "compare_candidates",
    "search_by_role",
    "search_by_skill",
    "search_by_experience",
    "search_by_company",
    "search_by_location",
    "recommend_best_candidate",
    "generate_interview_questions",
    "hiring_report",
    "general_question",
    "chat",
    "unknown",
]


def _extract_json(raw_text: str) -> Optional[Dict[str, Any]]:
    if not raw_text:
        return None

    text = raw_text.strip()
    text = text.replace("```json", "").replace("```", "").strip()

    match = re.search(r"\{.*\}", text, re.S)
    if not match:
        return None

    candidate = match.group(0)

    try:
        return json.loads(candidate)
    except json.JSONDecodeError:
        cleaned = candidate.replace("'", '"')
        cleaned = re.sub(r",\s*}\s*$", "}", cleaned)
        cleaned = re.sub(r",\s*\]", "]", cleaned)
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            return None


def _history_text(history: Optional[List[Dict[str, str]]]) -> str:
    if not history:
        return "No prior history."
    lines: List[str] = []
    for item in history[-8:]:
        role = item.get("role", "user")
        content = item.get("content", "")
        lines.append(f"{role}: {content}")
    return "\n".join(lines)


def _rule_based_intent(query: str) -> Optional[Dict[str, Any]]:
    normalized = query.strip().lower()
    if not normalized:
        return None

    compare_match = re.search(r"compare\s+([a-z0-9_]+)\s+(?:and|vs\.?|versus)\s+([a-z0-9_]+)", normalized)
    if compare_match:
        return {
            "intent": "compare_candidates",
            "candidate_1": compare_match.group(1).upper(),
            "candidate_2": compare_match.group(2).upper(),
            "query": query,
        }

    explain_match = re.search(r"why is\s+([a-z0-9_]+)\s+recommended", normalized)
    if explain_match:
        return {
            "intent": "candidate_explanation",
            "candidate_id": explain_match.group(1).upper(),
            "query": query,
        }

    report_match = re.search(r"generate hiring report(?: for)?\s+([a-z0-9_]+)", normalized)
    if report_match:
        return {
            "intent": "hiring_report",
            "candidate_id": report_match.group(1).upper(),
            "query": query,
        }

    summarize_match = re.search(r"(?:summarize|summarise|summary of|summarize details for)\s+([a-z0-9_]+)", normalized)
    if summarize_match:
        return {
            "intent": "candidate_summary",
            "candidate_id": summarize_match.group(1).upper(),
            "query": query,
        }

    if "show top candidates" in normalized or "top candidates" in normalized:
        return {"intent": "top_candidates", "query": query}

    if "strong hires" in normalized or "strong hire" in normalized:
        return {"intent": "strong_hires", "query": query}

    if "low risk" in normalized or "low-risk" in normalized:
        return {"intent": "low_risk", "query": query}

    if "recommend the best" in normalized or "best ai engineer" in normalized or "recommend best" in normalized:
        role = "AI Engineer" if "ai" in normalized else normalized.replace("recommend the best", "").strip()
        return {"intent": "recommend_best_candidate", "role": role, "query": query}

    if "find ai engineer" in normalized or "ai engineers" in normalized or "ai engineer" in normalized:
        return {"intent": "search_by_role", "role": "AI Engineer", "query": query}

    if "find backend engineer" in normalized or "backend engineers" in normalized or "backend engineer" in normalized:
        return {"intent": "search_by_role", "role": "Backend Engineer", "query": query}

    if "generate interview questions" in normalized or "interview questions" in normalized:
        candidate_match = re.search(r"for\s+([a-z0-9_]+)", normalized)
        return {
            "intent": "generate_interview_questions",
            "candidate_id": candidate_match.group(1).upper() if candidate_match else None,
            "query": query,
        }

    return None


def parse_intent(query: str, history: Optional[List[Dict[str, str]]] = None) -> Dict[str, Any]:
    rule_intent = _rule_based_intent(query)
    if rule_intent:
        return rule_intent

    prompt = f"""
You are an AI recruiter intent parser.
Return a single JSON object only.
Do not return any explanation, markdown, or any text outside the JSON.
Supported intents: {', '.join(SUPPORTED_INTENTS)}.

If the user refers to a previous candidate, uses pronouns like him/her/them, or says "the previous candidate" or "that candidate",
infer context from the conversation history.

History:
{_history_text(history)}

User query:
{query}

Return valid JSON with keys such as: intent, candidate_id, candidate_1, candidate_2, role, skill, experience, company, location, query.
If the query is a general recruiter question not tied to a specific tool, use intent "general_question".
If the user is chatting or greeting, use intent "chat".
If you cannot confidently map the query, use intent "unknown".
"""

    response = ask_gemini(prompt)
    parsed = _extract_json(response)

    if not parsed or not isinstance(parsed, dict):
        return {"intent": "unknown", "query": query}

    intent = parsed.copy()
    intent["query"] = query
    if intent.get("intent") == "explain_candidate":
        intent["intent"] = "candidate_explanation"
    if intent.get("intent") not in SUPPORTED_INTENTS:
        return {"intent": "unknown", "query": query}

    return intent
