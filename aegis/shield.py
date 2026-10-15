import functools
import time
from typing import Callable, Any

class SecurityViolationException(Exception):
    """Raised when an untrusted prompt attempts to execute a high-privilege syscall."""
    pass

class AegisShield:
    def __init__(self, strict_mode: bool = True, policy: Any = None):
        self.strict_mode = strict_mode
        self.policy = policy
        self.blocked_count = 0
        self.allowed_count = 0
        self.sensitive_patterns = [
            ".env", "secret", "password", "key", "token", "credential", 
            "id_rsa", "shadow", "drop table", "rm -rf"
        ]

    def protect_tool(self, tool_func: Callable) -> Callable:
        """Decorator to wrap any AI agent tool with the Aegis Zero-Trust Shield."""
        @functools.wraps(tool_func)
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            all_inputs = " ".join([str(a) for a in args] + [f"{k}={v}" for k, v in kwargs.items()])
            
            is_sensitive = any(p in all_inputs.lower() for p in self.sensitive_patterns)
            is_tainted = kwargs.get("is_tainted", True)

            if is_tainted and is_sensitive:
                self.blocked_count += 1
                latency = (time.perf_counter() - start) * 1000
                error_msg = (
                    f"\n[🚨 AEGIS INTERCEPTOR] Execution BLOCKED in {latency:.4f}ms!\n"
                    f"Tool: '{tool_func.__name__}' attempted unauthorized access to protected resource.\n"
                    f"Blocked Payload: '{all_inputs}'"
                )
                raise SecurityViolationException(error_msg)

            self.allowed_count += 1
            return tool_func(*args, **kwargs)
        return wrapper