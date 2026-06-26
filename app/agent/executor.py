import time
from typing import Any, Dict, List, Optional

import pandas as pd

from agent.gemini_agent import ask_gemini
from agent.intent_parser import parse_intent
from agent.logs import log_error, log_intent, log_tool
from agent.planner import plan_intent
from agent.tools import (
    candidate_summary,
    compare_candidates,
    explain_candidate,
    generate_interview_questions,
    hiring_report,
    high_technical_fit,
    low_risk,
    recommend_best_candidate,
    search_by_company,
    search_by_experience,
    search_by_location,
    search_by_availability,
    search_by_role,
    search_by_skill,
    strong_hires,
    top_candidates,
)


def _format_dataframe_response(df: pd.DataFrame) -> Dict[str, Any]:
    if df is None or df.empty:
        return {"type": "dataframe", "data": [], "message": "No candidates found."}
    return {"type": "dataframe", "data": df.to_dict(orient="records"), "columns": list(df.columns)}


def _format_dict_response(result: Any) -> Dict[str, Any]:
    if isinstance(result, dict):
        return {"type": "object", "data": result}
    if isinstance(result, str):
        return {"type": "text", "data": {"message": result}}
    return {"type": "unknown", "data": {"value": result}}


def _candidate_explanation_prompt(candidate: Dict[str, Any], query: str) -> str:
    return f"""
You are a senior technical recruiter.
Use only the supplied candidate data.
Do not invent any new facts.
Do not return raw JSON.
Do not use tables.
Write a concise explanation for why this candidate is a strong hire.
Include recruiter strengths, confidence, risk, availability, and an overall recommendation.

Candidate data:
{candidate}

User question:
{query}
"""


def _build_candidate_explanation_fallback(candidate: Dict[str, Any], query: str) -> str:
    lines = []
    if candidate.get("candidate_id"):
        lines.append(f"Candidate: {candidate.get('candidate_id')}")
    if candidate.get("executive_summary"):
        lines.append(f"Profile summary: {candidate.get('executive_summary')}")
    if candidate.get("technical_fit") is not None:
        lines.append(f"Technical fit: {candidate.get('technical_fit')}%.")
    if candidate.get("confidence_level"):
        lines.append(f"Confidence level: {candidate.get('confidence_level')}.")
    if candidate.get("risk_score") is not None:
        lines.append(f"Risk score: {candidate.get('risk_score')}.")
    if candidate.get("availability_fit") is not None:
        lines.append(f"Availability fit: {candidate.get('availability_fit')}.")
    if candidate.get("recommendation"):
        lines.append(f"Recommendation: {candidate.get('recommendation')}.")
    if candidate.get("strengths"):
        strengths = ", ".join(str(x) for x in candidate.get("strengths", [])[:4])
        lines.append(f"Strengths: {strengths}.")
    if candidate.get("risks"):
        risks = ", ".join(str(x) for x in candidate.get("risks", []))
        lines.append(f"Risks: {risks}.")

    body = "\n".join(f"- {line}" for line in lines if line)
    recommendation = candidate.get("recommendation", "Strong hire")
    return f"Why this candidate?\n{body}\n\nOverall recommendation: {recommendation}."


def _generate_candidate_explanation(candidate: Dict[str, Any], query: str) -> str:
    prompt = _candidate_explanation_prompt(candidate, query)
    explanation = ask_gemini(prompt)

    if not explanation or explanation.startswith("Gemini Error"):
        return _build_candidate_explanation_fallback(candidate, query)

    return explanation.strip()


def _build_cards(tool_result: Dict[str, Any]) -> List[Dict[str, Any]]:
    if tool_result.get("type") == "dataframe":
        return list(tool_result.get("data", []))

    if tool_result.get("type") == "text" and isinstance(tool_result.get("candidate"), dict):
        return [tool_result.get("candidate")]

    data = tool_result.get("data")
    if isinstance(data, dict):
        if data.get("candidate_1") and data.get("candidate_2"):
            return [data["candidate_1"], data["candidate_2"]]
        if data.get("candidate_id"):
            return [data]
    return []


def _build_summary(intent: str, tool_result: Dict[str, Any], args: Dict[str, Any]) -> str:
    tool_type = tool_result.get("type")
    data = tool_result.get("data")

    if tool_type == "dataframe":
        count = len(data or [])
        if count == 0:
            return "No candidates matched the request."
        return f"Found {count} candidates matching the request."

    if tool_type == "object" and isinstance(data, dict):
        if data.get("error"):
            return f"{data.get('error').replace('_', ' ').capitalize()}."
        if intent == "candidate_summary":
            return _build_candidate_summary_text(data)
        if intent == "candidate_explanation":
            return data.get("message", "Recruiter explanation unavailable. Displaying recruiter results.")
        if intent == "compare_candidates":
            return f"Compared candidates {args.get('candidate_1')} and {args.get('candidate_2')} successfully."
        return "Tool returned structured candidate information."

    if tool_type == "text":
        return tool_result.get("data", {}).get("message", "Request completed.")

    return "Recruiter results are available."


def _build_candidate_summary_text(data: Dict[str, Any]) -> str:
    sections = ["Recruiter Review:"]
    if data.get("executive_summary"):
        sections.append(f"Role / Company / Experience: {data.get('executive_summary')}")
    if data.get("recommendation"):
        sections.append(f"Recommendation: {data.get('recommendation')}")
    if data.get("confidence_level"):
        sections.append(f"Confidence: {data.get('confidence_level')}")
    if data.get("technical_fit") is not None:
        sections.append(f"Technical fit: {data.get('technical_fit')}")
    if data.get("availability_fit") is not None:
        sections.append(f"Availability: {data.get('availability_fit')}")
    if data.get("risk_score") is not None:
        sections.append(f"Risk score: {data.get('risk_score')}")
    if data.get("strengths"):
        strengths = "; ".join(str(x) for x in data.get("strengths", []))
        sections.append(f"Strengths: {strengths}")
    if data.get("risks"):
        risks = "; ".join(str(x) for x in data.get("risks", []))
        sections.append(f"Risks: {risks}")
    if data.get("recommended_interview_focus"):
        focus = "; ".join(str(x) for x in data.get("recommended_interview_focus", []))
        sections.append(f"Interview Focus: {focus}")

    sections.append("Overall Assessment: Review this candidate for next-stage interview.")
    return "\n".join(sections)


def _execute_tool_by_name(tool_name: str, args: Dict[str, Any], df: pd.DataFrame) -> Dict[str, Any]:
    if tool_name == "explain_candidate":
        tool_name = "candidate_explanation"

    base_df = df if df is not None else pd.DataFrame([])

    if tool_name == "top_candidates":
        return _format_dataframe_response(top_candidates(base_df))
    if tool_name == "strong_hires":
        return _format_dataframe_response(strong_hires(base_df))
    if tool_name == "low_risk":
        return _format_dataframe_response(low_risk(base_df))
    if tool_name == "high_technical_fit":
        return _format_dataframe_response(high_technical_fit(base_df))
    if tool_name == "candidate_summary":
        return _format_dict_response(candidate_summary(args.get("candidate_id"), base_df))
    if tool_name == "candidate_explanation":
        candidate = explain_candidate(args.get("candidate_id"), base_df)
        if candidate.get("error"):
            return _format_dict_response(candidate)
        explanation = _generate_candidate_explanation(candidate, args.get("query", ""))
        return {"type": "text", "data": {"message": explanation}, "candidate": candidate}
    if tool_name == "compare_candidates":
        return _format_dict_response(compare_candidates(args.get("candidate_1"), args.get("candidate_2"), base_df))
    if tool_name == "role_search":
        return _format_dataframe_response(search_by_role(args.get("role") or args.get("query"), base_df))
    if tool_name == "skills_search":
        return _format_dataframe_response(search_by_skill(args.get("skill") or args.get("query"), base_df))
    if tool_name == "search_by_company":
        return _format_dataframe_response(search_by_company(args.get("company") or args.get("query"), base_df))
    if tool_name == "search_by_location":
        return _format_dataframe_response(search_by_location(args.get("location") or args.get("query"), base_df))
    if tool_name == "search_by_experience":
        return _format_dataframe_response(search_by_experience(args.get("experience") or args.get("query"), base_df))
    if tool_name == "availability":
        return _format_dataframe_response(search_by_availability(args.get("availability") or args.get("query"), base_df))
    if tool_name == "recommend_best_candidate":
        return _format_dataframe_response(recommend_best_candidate(args.get("role") or args.get("query"), base_df, n=5))
    if tool_name == "generate_interview_questions":
        return _format_dict_response(generate_interview_questions(args.get("candidate_id"), base_df))
    if tool_name == "hiring_report":
        return _format_dict_response(hiring_report(args.get("candidate_id"), base_df))
    if tool_name == "custom_filter":
        filtered = base_df
        if args.get("role"):
            filtered = search_by_role(args.get("role"), filtered)
        if args.get("skill"):
            filtered = search_by_skill(args.get("skill"), filtered)
        if args.get("company"):
            filtered = search_by_company(args.get("company"), filtered)
        if args.get("location"):
            filtered = search_by_location(args.get("location"), filtered)
        if args.get("experience"):
            filtered = search_by_experience(args.get("experience"), filtered)
        if args.get("availability"):
            filtered = search_by_availability(args.get("availability"), filtered)
        return _format_dataframe_response(filtered)

    return {"type": "text", "data": {"message": "No recruiter tool matched the request."}}


def execute_tool(intent: Dict[str, Any], df: pd.DataFrame) -> Dict[str, Any]:
    intent_name = intent.get("intent", "unknown")
    args = intent.copy()
    plan = intent.get("plan") or plan_intent(intent)
    selected = plan[0] if plan else {"tool": intent_name, "args": intent, "reason": "Select the most appropriate recruiter tool."}
    tool_name = selected.get("tool", intent_name)
    args = selected.get("args", args)

    try:
        tool_result = _execute_tool_by_name(tool_name, args, df)
    except Exception as exc:
        log_error("tool_execution_failed", {"intent": intent_name, "tool": tool_name, "error": str(exc), "args": args})
        return {
            "status": "error",
            "intent": intent_name,
            "message": "Recruiter tool execution failed.",
            "table": None,
            "cards": [],
            "summary": "Recruiter tool execution failed.",
            "tool_result": None,
            "plan": plan,
            "selected_tool": tool_name,
            "selection_reason": selected.get("reason"),
        }

    tool_result["plan"] = plan
    tool_result["selected_tool"] = tool_name
    tool_result["selection_reason"] = selected.get("reason")

    table = None
    if tool_result.get("type") == "dataframe":
        table = pd.DataFrame(tool_result.get("data", []))
    cards = _build_cards(tool_result)
    summary = _build_summary(intent_name, tool_result, args)
    message = summary if tool_result.get("type") != "text" else tool_result.get("data", {}).get("message", summary)

    return {
        "status": "success",
        "intent": intent_name,
        "message": message,
        "table": table,
        "cards": cards,
        "summary": summary,
        "tool_result": tool_result,
        "plan": plan,
        "selected_tool": tool_name,
        "selection_reason": selected.get("reason"),
    }


def agent_executor(query: str, df: pd.DataFrame, history: Optional[list] = None) -> Dict[str, Any]:
    start_intent = time.time()
    try:
        intent = parse_intent(query, history)
    except Exception as exc:
        log_error("intent_parsing_failed", {"error": str(exc), "query": query})
        intent = {"intent": "unknown", "query": query}

    intent_latency = time.time() - start_intent
    log_intent(intent, query, intent_latency)

    start_tool = time.time()
    result = execute_tool(intent, df)
    tool_latency = time.time() - start_tool
    log_tool("executor", result.get("status", "unknown"), tool_latency, {"intent": intent.get("intent"), "query": query})

    answer = result.get("summary", result.get("message", ""))
    return {
        "status": result.get("status", "error"),
        "intent": result.get("intent", "unknown"),
        "message": result.get("message", ""),
        "table": result.get("table"),
        "cards": result.get("cards", []),
        "summary": result.get("summary", ""),
        "answer": answer,
        "tool_result": result.get("tool_result"),
        "plan": result.get("plan"),
        "selected_tool": result.get("selected_tool"),
        "selection_reason": result.get("selection_reason"),
        "conversation_history": history or [],
    }
