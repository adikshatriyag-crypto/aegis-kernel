"""
AegisKernel LangChain Adapter
Zero-Trust Deterministic Interception for LangChain Agents & Tools.
"""

import time
from typing import Any, Dict, List, Optional
from aegis.shield import AegisShield, SecurityViolationException
from aegis.core.policy import SecurityPolicy

class AegisSecurityCallbackHandler:
    """
    Standard LangChain Callback Handler that intercepts tool executions.
    Can be passed directly to any LangChain agent executor:
        agent_executor = AgentExecutor(agent=agent, tools=tools, callbacks=[AegisSecurityCallbackHandler()])
    """
    def __init__(self, shield: Optional[AegisShield] = None):
        self.shield = shield or AegisShield(policy=SecurityPolicy.strict())
        self.blocked_attacks: List[Dict[str, Any]] = []

    def on_tool_start(
        self,
        serialized: Dict[str, Any],
        input_str: str,
        **kwargs: Any
    ) -> None:
        """Called before a LangChain tool executes."""
        tool_name = serialized.get("name", "unknown_tool")
        start = time.perf_counter()

        # Check for exploit patterns in tool input
        input_lower = str(input_str).lower()
        is_sensitive = any(p in input_lower for p in self.shield.sensitive_patterns)

        if is_sensitive:
            latency_ms = (time.perf_counter() - start) * 1000
            violation_event = {
                "tool": tool_name,
                "input": input_str,
                "latency_ms": latency_ms,
                "timestamp": time.time()
            }
            self.blocked_attacks.append(violation_event)
            raise SecurityViolationException(
                f"[AegisKernel LangChain Interceptor] Blocked exploit attempt on '{tool_name}' in {latency_ms:.4f}ms! "
                f"Payload: '{input_str}'"
            )

def wrap_langchain_tool(langchain_tool: Any, shield: Optional[AegisShield] = None) -> Any:
    """Wraps an individual LangChain BaseTool instance with Aegis protection."""
    active_shield = shield or AegisShield()
    if hasattr(langchain_tool, "_run"):
        original_run = langchain_tool._run
        langchain_tool._run = active_shield.protect_tool(original_run)
    return langchain_tool
