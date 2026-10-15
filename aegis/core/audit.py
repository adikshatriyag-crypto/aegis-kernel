"""
AegisKernel Forensic Audit Logging Engine
Cryptographic, tamper-evident audit trail for AI agent tool executions and intercepted attacks.
"""

import time
import json
import hashlib
from typing import List, Dict, Any, Optional

class AuditRecord:
    def __init__(
        self,
        tool_name: str,
        status: str,
        latency_ms: float,
        payload_preview: str,
        violation_type: Optional[str] = None,
        violation_details: Optional[str] = None
    ):
        self.timestamp = time.time()
        self.tool_name = tool_name
        self.status = status  # "BLOCKED" or "ALLOWED"
        self.latency_ms = latency_ms
        self.payload_preview = payload_preview[:120]
        self.violation_type = violation_type
        self.violation_details = violation_details
        self.signature = self._compute_signature()

    def _compute_signature(self) -> str:
        raw = f"{self.timestamp}:{self.tool_name}:{self.status}:{self.latency_ms}:{self.payload_preview}"
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp,
            "tool": self.tool_name,
            "status": self.status,
            "latency_ms": round(self.latency_ms, 4),
            "payload": self.payload_preview,
            "violation_type": self.violation_type,
            "signature": self.signature
        }

class AuditLogger:
    def __init__(self):
        self.records: List[AuditRecord] = []

    def record_blocked(self, tool_name: str, latency_ms: float, payload: str, violation_type: str, details: str) -> AuditRecord:
        rec = AuditRecord(
            tool_name=tool_name,
            status="BLOCKED",
            latency_ms=latency_ms,
            payload_preview=payload,
            violation_type=violation_type,
            violation_details=details
        )
        self.records.append(rec)
        return rec

    def record_allowed(self, tool_name: str, latency_ms: float, payload: str) -> AuditRecord:
        rec = AuditRecord(
            tool_name=tool_name,
            status="ALLOWED",
            latency_ms=latency_ms,
            payload_preview=payload
        )
        self.records.append(rec)
        return rec

    def get_summary(self) -> Dict[str, Any]:
        blocked = sum(1 for r in self.records if r.status == "BLOCKED")
        allowed = sum(1 for r in self.records if r.status == "ALLOWED")
        avg_latency = (
            sum(r.latency_ms for r in self.records) / len(self.records)
            if self.records else 0.0
        )
        return {
            "total_calls": len(self.records),
            "blocked_attacks": blocked,
            "allowed_calls": allowed,
            "immunity_rate_pct": (blocked / (blocked + allowed) * 100) if (blocked + allowed) > 0 else 100.0,
            "avg_latency_ms": round(avg_latency, 4)
        }
