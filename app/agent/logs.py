from pathlib import Path
import logging

LOG_DIR = Path(__file__).parent.parent / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "agent.log"

logger = logging.getLogger("redrob_ai_recruiter")
logger.setLevel(logging.INFO)

if not logger.handlers:
    handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.propagate = False


def log_intent(intent: dict, query: str, latency: float) -> None:
    logger.info(
        "intent_detected intent=%s query=%s latency=%.3f",
        intent.get("intent"),
        query,
        latency,
    )


def log_tool(tool_name: str, result_type: str, latency: float, details: dict | None = None) -> None:
    logger.info(
        "tool_executed tool=%s result_type=%s latency=%.3f details=%s",
        tool_name,
        result_type,
        latency,
        details or {},
    )


def log_error(message: str, context: dict | None = None) -> None:
    logger.error("error message=%s context=%s", message, context or {})
