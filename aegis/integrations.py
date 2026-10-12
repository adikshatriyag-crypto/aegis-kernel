"""
AegisKernel Framework Integrations
Zero-Trust Deterministic Interception for LangChain, CrewAI, and Autonomous Agent Frameworks.
"""

from typing import List, Any, Callable
from aegis.shield import AegisShield, SecurityViolationException

# Global high-performance runtime shield instance
_global_shield = AegisShield()

def secure_tools(tools: List[Any], shield: AegisShield = None) -> List[Any]:
    """
    Auto-hardens a list of agent tools (callables, LangChain tools, CrewAI tools)
    with AegisKernel deterministic zero-trust interception.

    Usage:
        from aegis.integrations import secure_tools
        hardened_tools = secure_tools([terminal_exec, sql_query, file_read])
    """
    active_shield = shield or _global_shield
    hardened = []

    for tool in tools:
        if callable(tool):
            # Wrap regular Python functions or tool callables
            protected_func = active_shield.protect_tool(tool)
            hardened.append(protected_func)
        elif hasattr(tool, "_run"):
            # LangChain BaseTool style object
            original_run = tool._run
            tool._run = active_shield.protect_tool(original_run)
            hardened.append(tool)
        elif hasattr(tool, "func") and callable(tool.func):
            # CrewAI style tool wrapper
            tool.func = active_shield.protect_tool(tool.func)
            hardened.append(tool)
        else:
            # Fallback wrapper
            hardened.append(active_shield.protect_tool(tool))

    return hardened


def protect_agent(agent: Any) -> Any:
    """
    1-Line hardening for agent instances.
    Extracts all attached tools and wraps them in the Aegis zero-trust boundary.
    """
    if hasattr(agent, "tools") and isinstance(agent.tools, list):
        agent.tools = secure_tools(agent.tools)
    return agent
