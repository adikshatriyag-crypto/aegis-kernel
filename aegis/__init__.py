"""
AegisKernel: Zero-Trust Security Runtime for Autonomous AI Agents
"""

from .shield import AegisShield, SecurityViolationException
from .integrations import secure_tools, protect_agent

__version__ = "0.1.1"
__all__ = [
    "AegisShield",
    "SecurityViolationException",
    "secure_tools",
    "protect_agent",
]
