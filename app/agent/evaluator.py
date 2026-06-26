from typing import Any, Dict


def score_intent_accuracy(predicted_intent: str, expected_intent: str) -> float:
    return 1.0 if predicted_intent == expected_intent else 0.0


def score_tool_accuracy(tool_name: str, expected_tool: str) -> float:
    return 1.0 if tool_name == expected_tool else 0.0


def score_execution_time(milliseconds: float) -> float:
    if milliseconds <= 500:
        return 1.0
    if milliseconds <= 1000:
        return 0.8
    if milliseconds <= 2000:
        return 0.5
    return 0.2


def score_response_quality(response: str) -> float:
    if not response:
        return 0.0
    length = len(response)
    if length < 50:
        return 0.4
    if length < 150:
        return 0.7
    return 1.0


def evaluate_run(metrics: Dict[str, Any]) -> Dict[str, float]:
    return {
        "intent_accuracy": score_intent_accuracy(metrics.get("predicted_intent", ""), metrics.get("expected_intent", "")),
        "tool_accuracy": score_tool_accuracy(metrics.get("tool_name", ""), metrics.get("expected_tool", "")),
        "execution_time": score_execution_time(metrics.get("execution_time_ms", 0.0)),
        "response_quality": score_response_quality(metrics.get("response", "")),
    }
