from typing import Any, Dict, List, Optional

from agent.executor import agent_executor


def recruiter_agent(query: str, df, history: Optional[List[Dict[str, str]]] = None):
    """Run the recruiter agent pipeline and return the answer, tool result, and history."""
    result = agent_executor(query, df, history)
    return result["answer"], result["tool_result"], result["conversation_history"]
