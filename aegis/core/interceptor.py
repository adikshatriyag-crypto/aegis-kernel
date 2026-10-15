"""
AegisKernel Syscall & Tool Execution Interceptor (The Shield)
Deterministic gatekeeper between autonomous agent reasoning and system execution.
"""

import functools
import time
from typing import Callable, Any, Optional

from aegis.core.taint import is_tainted
from aegis.core.policy import SecurityPolicy, Capability, SecurityViolationException
from aegis.core.audit import AuditLogger

class Interceptor:
    def __init__(self, policy: Optional[SecurityPolicy] = None, logger: Optional[AuditLogger] = None):
        self.policy = policy or SecurityPolicy.strict()
        self.logger = logger or AuditLogger()

    def wrap(self, tool_func: Callable, required_capability: Capability = Capability.SHELL_EXEC) -> Callable:
        """
        Wraps any tool function with zero-trust interception.
        Enforces policy checks and logs forensic audit trails.
        """
        @functools.wraps(tool_func)
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            tool_name = getattr(tool_func, "__name__", "anonymous_tool")
            all_inputs = " ".join([str(a) for a in args] + [f"{k}={v}" for k, v in kwargs.items()])

            # Check if any input argument carries taint
            tainted = kwargs.get("is_tainted", None)
            if tainted is None:
                tainted = is_tainted(args) or is_tainted(kwargs) or True

            try:
                # Deterministic Policy Validation
                self.policy.validate(
                    tool_name=tool_name,
                    required_capability=required_capability,
                    payload=all_inputs,
                    is_tainted=tainted
                )
                latency_ms = (time.perf_counter() - start) * 1000
                self.logger.record_allowed(tool_name, latency_ms, all_inputs)
                return tool_func(*args, **kwargs)

            except SecurityViolationException as sve:
                latency_ms = (time.perf_counter() - start) * 1000
                sve.latency_ms = latency_ms
                self.logger.record_blocked(
                    tool_name=tool_name,
                    latency_ms=latency_ms,
                    payload=all_inputs,
                    violation_type=sve.violation_type,
                    details=str(sve)
                )
                raise sve

        return wrapper
