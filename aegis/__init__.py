"""
AegisKernel: Zero-Trust Security Runtime for Autonomous AI Agents
Deterministic capability enforcement and taint tracking for LangChain, CrewAI, AutoGen, and Swarm.
"""

from aegis.shield import AegisShield, SecurityViolationException
from aegis.integrations import secure_tools, protect_agent
from aegis.core.taint import TaintedString, taint, is_tainted
from aegis.core.policy import Capability, SecurityPolicy
from aegis.core.audit import AuditLogger, AuditRecord
from aegis.core.interceptor import Interceptor

__version__ = "0.2.0"
__all__ = [
    "AegisShield",
    "SecurityViolationException",
    "secure_tools",
    "protect_agent",
    "TaintedString",
    "taint",
    "is_tainted",
    "Capability",
    "SecurityPolicy",
    "AuditLogger",
    "AuditRecord",
    "Interceptor"
]
