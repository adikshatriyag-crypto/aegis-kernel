"""
Melaya Agent Tool Sandbox with AegisKernel
Shows how autonomous agents deployed on Melaya (melaya.org) can safely call
outside tools while keeping zero-trust containment in place.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from aegis.core.taint import taint
from aegis.core.policy import SecurityPolicy, Capability, SecurityViolationException
from aegis.core.interceptor import Interceptor

class MelayaAgentSandbox:
    def __init__(self, allowed_capabilities=None):
        self.policy = SecurityPolicy(
            allowed_capabilities=allowed_capabilities or {
                Capability.FILE_READ,
                Capability.FILE_WRITE,
            },
            allow_tainted_execution=False
        )
        self.interceptor = Interceptor(policy=self.policy)

    def register_tool(self, tool_func, required_capability: Capability):
        """Wrap a Melaya agent tool with deterministic capability evaluation."""
        return self.interceptor.wrap(tool_func, required_capability=required_capability)

# Example tools
def file_writer(path: str, content: str):
    return f"Wrote {len(content)} bytes to {path}"

def shell_runner(command: str):
    return f"Ran command: {command}"

def main():
    print("=" * 60)
    print("Melaya Agent Sandbox with AegisKernel Interceptor")
    print("=" * 60)

    sandbox = MelayaAgentSandbox(allowed_capabilities={Capability.FILE_WRITE})
    safe_writer = sandbox.register_tool(file_writer, Capability.FILE_WRITE)
    safe_shell = sandbox.register_tool(shell_runner, Capability.SHELL_EXEC)

    # 1. Normal Agent Action
    result = safe_writer("output/result.csv", "name,score\nagent1,98")
    print(f"[OK] Normal Agent Tool: {result}")

    # 2. Rogue Agent Injection (Overwriting SSH keys)
    try:
        print("\nTesting Rogue Agent Injection: Attempting to write to ~/.ssh/id_rsa...")
        safe_writer(taint("~/.ssh/id_rsa"), "malicious_key_payload")
    except SecurityViolationException as e:
        print(f"[BLOCKED] Blast radius contained in {e.latency_ms:.4f}ms: {e}")

    # 3. Rogue Agent Injection (Reverse Shell)
    try:
        print("\nTesting Rogue Agent Injection: Attempting reverse shell...")
        safe_shell(taint("rm -rf / --no-preserve-root"))
    except SecurityViolationException as e:
        print(f"[BLOCKED] Process killed in {e.latency_ms:.4f}ms: {e}")

if __name__ == "__main__":
    main()
