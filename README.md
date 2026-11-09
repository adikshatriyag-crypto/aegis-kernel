# 🛡️ AegisKernel: Deterministic Security Runtime for Autonomous AI Agents

> **Deterministic capability-based security runtime that intercepts unauthorized tool execution, path traversal, and subshell escapes for autonomous AI agents in <0.016ms with zero LLM token overhead.**

[![CI Security Audit](https://github.com/adikshatriyag-crypto/aegis-kernel/actions/workflows/security_audit.yml/badge.svg)](https://github.com/adikshatriyag-crypto/aegis-kernel/actions)
[![PyPI version](https://img.shields.io/badge/PyPI-v0.6.0-blue.svg)](https://pypi.org/project/aegis-kernel/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![Latency Overhead](https://img.shields.io/badge/Latency-%3C0.016ms-purple.svg)]()

---

> 🚀 **Building Autonomous Agents?** AegisKernel is free and open-source on PyPI.  
> 🔗 **[Try the Live Web Sandbox](https://adikshatriyag-crypto.github.io/aegis-kernel/)** | **[PyPI Package](https://pypi.org/project/aegis-kernel/)** | **[Report an Issue](https://github.com/adikshatriyag-crypto/aegis-kernel/issues)**

---

## 🚨 The Problem in Autonomous AI Agents

Modern AI Agents (**CrewAI, LangChain, Claude Code, Browser Agents**) execute tools with direct access to file systems, databases, and bash terminals.

Traditional guardrails rely on **probabilistic LLMs** (asking a secondary LLM *"is this bash command safe?"* or using regex allowlists). Attackers bypass them easily using:
- **Indirect Prompt Injection** (concealed within scraped websites, emails, or PDFs)
- **Base64 Payload Cloaking & Subshell Piping** (`echo ... | base64 -d | sh`)
- **Path Traversal & Secret Theft** (`cat ../../.env`, `~/.ssh/id_rsa`)
- **Latency & Cost Overhead** (secondary LLM checks add 800ms+ and extra API costs to every single tool invocation)

---

## ⚡ The Solution: Deterministic Capability Enforcement

AegisKernel removes probabilistic guessing from execution safety. Instead of asking an LLM to evaluate semantic safety, AegisKernel binds tools to deterministic **Capability Tokens**:

```
External Untrusted Data (Prompt/Web/Document)
        ↓
  [LLM Reasoning] ---> Emits Tool Call Arguments
        ↓
  [Aegis Interceptor] <--- Validates Capability Boundary (In-Memory Process Tree)
        ↓
    ALLOWED: If within task capability allowlist (e.g., read ./workspace/data)
    DROPPED: In <0.016ms if unauthorized execve, egress socket, or traversal attempted!
```

---

## 🏗️ Architecture: Dual-Layer Defense Model

To provide practical developer protection today while building toward ring-0 host safety:

1. **Layer 1: Process Capability Boundary (v0.6.0 - PyPI: `aegis-kernel`):**
   - In-memory process tree wrapper intercepting agent tool invocations (`@shield.protect_tool`).
   - Deterministic path sandboxing restricting `openat` filesystem access to task-scoped roots.
   - Blocks interactive subshell spawning (`bash -i`, `sh`) and destructive binaries before `execve`.
   - Overhead: **< 0.016ms** with zero LLM API calls.

2. **Layer 2: Host eBPF / LSM Kernel Module (Active Benchmark & Roadmap):**
   - Ring-0 host enforcement hooking Linux Security Module (`security_bprm_check`, `security_file_open`).
   - Guarantees capability containment across spawned children and native C libraries.

---

## 📊 Benchmark Scorecard (CrewAI Multi-Agent Audit)

Reproduction script: `python benchmark_crewai.py`:

```
===========================================================================
🛡️  CREWAI MULTI-AGENT SECURITY AUDIT (AegisKernel v0.6.0)
===========================================================================
Attack Vector                    | Standard CrewAI  | With AegisKernel    
---------------------------------------------------------------------------
Destructive Root Injection       | EXPLOITED ❌      | BLOCKED (0.018ms) 🛡️
Path Traversal (.env leak)       | EXPLOITED ❌      | BLOCKED (0.015ms) 🛡️
Database Drop Injection          | EXPLOITED ❌      | BLOCKED (0.014ms) 🛡️
Command Chaining Hijack          | EXPLOITED ❌      | BLOCKED (0.016ms) 🛡️
---------------------------------------------------------------------------
Latency Overhead                 | +800ms (LLM)     | <0.016ms (Deterministic)
===========================================================================
```

---

## 💻 2-Line Drop-In Integration

Install via PyPI:
```bash
pip install aegis-kernel
```

### Universal Tool Protection:
```python
import os
from aegis import AegisShield, SecurityPolicy

# Define capability scope for the agent tool
shield = AegisShield(policy=SecurityPolicy.strict(allowed_paths=["./workspace", "./data"]))

# Wrap any agent tool function
@shield.protect_tool
def run_command(cmd: str):
    return os.system(cmd)  # Unauthorized execve/openat dropped in <0.016ms
```

### CrewAI & LangChain Integration:
```python
from aegis.integrations import protect_agent

# Pass your existing CrewAI or LangChain agent instance
hardened_agent = protect_agent(agent)
```

---

## 🛠️ Local Development & Testing

```bash
# Clone the repository
git clone https://github.com/adikshatriyag-crypto/aegis-kernel.git
cd aegis-kernel

# Install dependencies in editable mode
pip install -e .

# Run test suite
python test_core.py
python test_shell_breakout.py

# Run benchmark
python benchmark_crewai.py
```

---

## 🌐 Live Interactive Web Sandbox

Test live capability enforcement in browser:
Open [https://adikshatriyag-crypto.github.io/aegis-kernel/](https://adikshatriyag-crypto.github.io/aegis-kernel/) or open `demo.html` locally.

---

## 🚀 Design Partners & Production Staging

Deploying agents with terminal, database, or filesystem execution in production? We are onboarding **5 early design partners** to shape the enterprise capability runtime:

- **Centralized Audit Telemetry:** Hosted cryptographic SHA-256 HMAC violation stream and forensic compliance logs.
- **eBPF Host Isolation:** Pre-release benchmark access for ring-0 child process containment below the runtime.
- **Custom Capability Matrix Design:** Dedicated integration support for LangChain, CrewAI, AutoGen, and custom agent runtimes.

**Direct Channels:**
- ✉️ Email: [`adikshatriyag@gmail.com`](mailto:adikshatriyag@gmail.com)
- 💬 Discord: `@adityawebde`
- 🐛 Issues & Staging: Open an [Issue](https://github.com/adikshatriyag-crypto/aegis-kernel/issues)

---

## 🤝 Contributing & Community

AegisKernel is an open-source runtime built for the AI builder community.
- Have feedback or found an evasion? Open an [Issue](https://github.com/adikshatriyag-crypto/aegis-kernel/issues).
- Want to test AegisKernel on your scrapers or agent workflows? Ping `adikshatriyag@gmail.com` or join the discussions.

---

## 📄 License

Distributed under the **MIT License**. See `LICENSE` for more information.
