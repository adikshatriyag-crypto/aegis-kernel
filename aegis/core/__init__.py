"""
AegisKernel Core Engine Modules
"""

from aegis.core.taint import TaintedString, taint, is_tainted
from aegis.core.policy import Capability, SecurityPolicy, SecurityViolationException
from aegis.core.audit import AuditLogger, AuditRecord
from aegis.core.interceptor import Interceptor

__all__ = [
    "TaintedString",
    "taint",
    "is_tainted",
    "Capability",
    "SecurityPolicy",
    "SecurityViolationException",
    "AuditLogger",
    "AuditRecord",
    "Interceptor"
]
