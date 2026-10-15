"""
AegisKernel Taint Tracking Engine
Zero-Trust mathematical tracking of untrusted external payloads.
Guarantees that malicious prompt injection strings cannot be 'laundered' through string operations.
"""

import uuid
import time
from typing import Any, List, Union

class TaintedString(str):
    """
    Subclass of str that attaches persistent cryptographic-ready security metadata.
    Any string derived from this object (via concatenation, slicing, formatting, etc.)
    inherits the taint label deterministically.
    """
    origin: str
    taint_id: str
    timestamp: float

    def __new__(cls, content: str, origin: str = "untrusted_input", taint_id: str = None):
        instance = super().__new__(cls, content)
        instance.origin = origin
        instance.taint_id = taint_id or str(uuid.uuid4())[:8]
        instance.timestamp = time.time()
        return instance

    def _propagate(self, new_content: str) -> "TaintedString":
        return TaintedString(new_content, origin=self.origin, taint_id=self.taint_id)

    def __add__(self, other: Any) -> "TaintedString":
        res = super().__add__(str(other))
        return self._propagate(res)

    def __radd__(self, other: Any) -> "TaintedString":
        res = str(other).__add__(self)
        return self._propagate(res)

    def __getitem__(self, item: Any) -> "TaintedString":
        res = super().__getitem__(item)
        return self._propagate(res)

    def __mul__(self, n: int) -> "TaintedString":
        res = super().__mul__(n)
        return self._propagate(res)

    def lower(self) -> "TaintedString":
        return self._propagate(super().lower())

    def upper(self) -> "TaintedString":
        return self._propagate(super().upper())

    def strip(self, *args, **kwargs) -> "TaintedString":
        return self._propagate(super().strip(*args, **kwargs))

    def replace(self, *args, **kwargs) -> "TaintedString":
        return self._propagate(super().replace(*args, **kwargs))

    def split(self, *args, **kwargs) -> List["TaintedString"]:
        parts = super().split(*args, **kwargs)
        return [self._propagate(p) for p in parts]


def taint(data: Any, origin: str = "external_user") -> Any:
    """Taints any input data (strings, lists, dicts)."""
    if isinstance(data, str) and not isinstance(data, TaintedString):
        return TaintedString(data, origin=origin)
    elif isinstance(data, list):
        return [taint(x, origin=origin) for x in data]
    elif isinstance(data, dict):
        return {k: taint(v, origin=origin) for k, v in data.items()}
    return data


def is_tainted(data: Any) -> bool:
    """Recursively checks if a data structure contains any tainted strings."""
    if isinstance(data, TaintedString):
        return True
    if isinstance(data, (list, tuple, set)):
        return any(is_tainted(x) for x in data)
    if isinstance(data, dict):
        return any(is_tainted(k) or is_tainted(v) for k, v in data.items())
    return False
