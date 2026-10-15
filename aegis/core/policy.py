"""
AegisKernel Capability-Based Policy Engine
Enforces strict capability matrices at the tool/syscall boundary.
"""

from enum import Enum, auto
from typing import Set, List, Optional

class Capability(Enum):
    FILE_READ = auto()
    FILE_WRITE = auto()
    SHELL_EXEC = auto()
    NETWORK_OUTBOUND = auto()
    DATABASE_MODIFY = auto()
    ENVIRONMENT_ACCESS = auto()

class SecurityViolationException(Exception):
    """Raised when an agent attempts an action that violates zero-trust capability rules."""
    def __init__(self, message: str, tool_name: str = "unknown", violation_type: str = "POLICY_VIOLATION", latency_ms: float = 0.0):
        super().__init__(message)
        self.tool_name = tool_name
        self.violation_type = violation_type
        self.latency_ms = latency_ms

class SecurityPolicy:
    """
    Capability-based access control matrix.
    Default Deny: Any capability not explicitly granted is rejected.
    """
    def __init__(
        self,
        allowed_capabilities: Optional[Set[Capability]] = None,
        allow_tainted_execution: bool = False,
        sensitive_patterns: Optional[List[str]] = None
    ):
        self.allowed_capabilities = allowed_capabilities or set()
        self.allow_tainted_execution = allow_tainted_execution
        self.sensitive_patterns = sensitive_patterns or [
            ".env", "secret", "password", "key", "token", "credential",
            "id_rsa", "shadow", "drop table", "drop database", "rm -rf",
            "/etc/passwd", "--no-preserve-root", "curl ", "wget ", "nc "
        ]

    def validate(self, tool_name: str, required_capability: Capability, payload: str, is_tainted: bool = True):
        # 1. Capability Grant Check
        if required_capability not in self.allowed_capabilities:
            raise SecurityViolationException(
                f"[AegisKernel] Capability '{required_capability.name}' not granted to tool '{tool_name}'.",
                tool_name=tool_name,
                violation_type="MISSING_CAPABILITY"
            )

        # 2. Taint Check on Dangerous Capabilities
        dangerous_caps = {Capability.SHELL_EXEC, Capability.FILE_WRITE, Capability.DATABASE_MODIFY}
        if is_tainted and required_capability in dangerous_caps and not self.allow_tainted_execution:
            # Check for critical exploit signatures in payload
            payload_lower = payload.lower()
            for pattern in self.sensitive_patterns:
                if pattern in payload_lower:
                    raise SecurityViolationException(
                        f"[AegisKernel] Tainted input matched high-risk pattern '{pattern}' under '{required_capability.name}'.",
                        tool_name=tool_name,
                        violation_type="TAINTED_EXPLOIT_DETECTED"
                    )

    @classmethod
    def strict(cls) -> "SecurityPolicy":
        """Pre-configured zero-trust policy: safe file reads only."""
        return cls(
            allowed_capabilities={Capability.FILE_READ},
            allow_tainted_execution=False
        )

    @classmethod
    def permissive(cls) -> "SecurityPolicy":
        """Permissive development policy."""
        return cls(
            allowed_capabilities=set(Capability),
            allow_tainted_execution=True
        )
