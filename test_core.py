"""
Unit Tests for AegisKernel Core Architecture (v0.2.0)
"""

import unittest
from aegis.core.taint import TaintedString, taint, is_tainted
from aegis.core.policy import Capability, SecurityPolicy, SecurityViolationException
from aegis.core.interceptor import Interceptor
from aegis.core.audit import AuditLogger

class TestAegisCore(unittest.TestCase):
    def test_taint_propagation(self):
        """Verify that taint propagates across string operations without laundering."""
        base = taint("malicious_command; rm -rf /")
        self.assertTrue(is_tainted(base))
        self.assertIsInstance(base, TaintedString)

        # Concat
        derived = "PREFIX: " + base + " :SUFFIX"
        self.assertTrue(is_tainted(derived))

        # Upper/Lower
        self.assertTrue(is_tainted(base.upper()))
        self.assertTrue(is_tainted(base.lower()))

        # Slicing
        self.assertTrue(is_tainted(base[:10]))

        # Split
        parts = base.split(" ")
        self.assertTrue(any(is_tainted(p) for p in parts))

    def test_capability_enforcement(self):
        """Verify that tools without granted capabilities are immediately blocked."""
        policy = SecurityPolicy(allowed_capabilities={Capability.FILE_READ})
        interceptor = Interceptor(policy=policy)

        def shell_tool(cmd: str):
            return f"Executed {cmd}"

        protected_shell = interceptor.wrap(shell_tool, required_capability=Capability.SHELL_EXEC)

        with self.assertRaises(SecurityViolationException) as ctx:
            protected_shell("ls -la")

        self.assertEqual(ctx.exception.violation_type, "MISSING_CAPABILITY")

    def test_taint_exploit_interception(self):
        """Verify that dangerous payloads with tainted input are blocked even if capability exists."""
        policy = SecurityPolicy(
            allowed_capabilities={Capability.SHELL_EXEC},
            allow_tainted_execution=False
        )
        interceptor = Interceptor(policy=policy)

        def bash_tool(cmd: str):
            return "ok"

        protected_bash = interceptor.wrap(bash_tool, required_capability=Capability.SHELL_EXEC)

        with self.assertRaises(SecurityViolationException) as ctx:
            protected_bash("cat .env")

        self.assertEqual(ctx.exception.violation_type, "TAINTED_EXPLOIT_DETECTED")
        self.assertLess(ctx.exception.latency_ms, 2.0)  # Must be fast (< 2ms)

    def test_audit_logging(self):
        """Verify that audit records are properly cataloged."""
        logger = AuditLogger()
        policy = SecurityPolicy.strict()
        interceptor = Interceptor(policy=policy, logger=logger)

        def dangerous_action():
            return 123

        wrapped = interceptor.wrap(dangerous_action, required_capability=Capability.DATABASE_MODIFY)

        try:
            wrapped()
        except SecurityViolationException:
            pass

        summary = logger.get_summary()
        self.assertEqual(summary["blocked_attacks"], 1)
        self.assertGreater(len(logger.records[0].signature), 0)

if __name__ == "__main__":
    unittest.main()
