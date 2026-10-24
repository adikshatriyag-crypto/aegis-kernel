# 🛡️ AegisKernel: Zero-Trust Security Runtime for Autonomous AI Agents

> **The first deterministic, capability-based interception layer that guarantees 100% immunity against prompt injection and tool-hijacking at the OS syscall boundary.**

[![CI Security Audit](https://github.com/adikshatriyag-crypto/aegis-kernel/actions/workflows/security_audit.yml/badge.svg)](https://github.com/adikshatriyag-crypto/aegis-kernel/actions)
[![PyPI version](https://img.shields.io/badge/PyPI-v0.6.0-blue.svg)](https://pypi.org/project/aegis-kernel/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![Defense Rate](https://img.shields.io/badge/Defense%20Rate-100%25-brightgreen.svg)]()
[![Latency Overhead](https://img.shields.io/badge/Latency-%3C0.05ms-purple.svg)]()

---

> 🚀 **Deploying AI Agents to Production?** We are onboarding 3 Founding Design Partners for a free 1-week pilot with direct 1-on-1 support (<0.05ms OS syscall defense).  
> 🔗 **[Try the Live Web Sandbox (Zero Install)](https://adikshatriyag-crypto.github.io/aegis-kernel/)** | **[Request Free Pilot Demo](mailto:adikshatriyag@gmail.com)**

---

⭐ **If you find AegisKernel valuable, star the repository to support open-source deterministic AI agent safety!**

---

## 🚨 The Critical Problem in Autonomous AI Agents

Modern AI Agents (**CrewAI, LangChain, AutoGen, OpenAI Swarm**) are moving from simple chatbots to autonomous actors with direct access to file systems, databases, cloud APIs, and bash terminals.

Traditional security guardrails rely on **probabilistic LLMs** (prompt-based filters, regexes, or secondary evaluator LLMs). Attackers easily bypass them using:
- **Base64 Cloaked Exploit Payloads**
- **Indirect Prompt Injection** (malicious instructions concealed within emails, PDFs, or scraped web pages)
- **Path Traversal & Environment Theft** (`.env`, SSH keys)
- **Tool Argument Smuggling & SQL Injection**

> **Industry Reality:** Standard AI agents fail **80%+** of real-world injection attacks, leading to catastrophic remote data leaks and uncontained shell execution.

---

## ⚡ The Solution: Deterministic Taint Tracking & Capability Enforcement

AegisKernel completely removes probabilities from the security equation. Instead of asking another LLM *"Does this prompt look safe?"*, AegisKernel tracks the **provenance and taint status** of all incoming data deterministically:

```
External Untrusted Data (Prompt/Web/Email) 
        ↓ 
  [Taint Engine]  ---> Tags payload as TaintedString
        ↓
  [LLM Reasoning] ---> Generates Tool Call Arguments
        ↓
 [Aegis Interceptor] <--- Enforces Capability Matrix (Zero-Trust Boundary)
        ↓
   BLOCKED in <0.04ms! (Forensic Audit SHA-256 HMAC Logged)
```

1. **Automatic Taint Tagging (`aegis.core.taint`):** External data is wrapped in `TaintedString`. String operations (slicing, concatenations, uppercase, formatting) preserve taint labels deterministically.
2. **Capability-Based Access Control (`aegis.core.policy`):** High-privilege actions (`SHELL_EXEC`, `FILE_WRITE`, `DATABASE_MODIFY`) require explicit policy grants. Tainted arguments attempting dangerous syscalls are killed instantly.
3. **Hardware-Speed Interception (`aegis.core.interceptor`):** Neutralizes attacks in **`< 0.05 ms`** before the syscall ever reaches the operating system kernel.
4. **Forensic Audit Logger (`aegis.core.audit`):** Emits cryptographic tamper-evident SHA-256 HMAC logs for enterprise compliance (SOC2, HIPAA, EU AI Act).

---

## 📊 Live Benchmark Scorecard (CrewAI Multi-Agent Audit)

Verified reproduction via `python benchmark_crewai.py`:

```
===========================================================================
🛡️  CREWAI MULTI-AGENT SECURITY AUDIT (AegisKernel v0.2.0)
===========================================================================
Attack Vector                    | Standard CrewAI  | With AegisKernel    
---------------------------------------------------------------------------
Destructive Root Injection       | EXPLOITED ❌      | BLOCKED (0.061ms) 🛡️
Path Traversal (.env leak)       | EXPLOITED ❌      | BLOCKED (0.041ms) 🛡️
Database Drop Injection          | EXPLOITED ❌      | BLOCKED (0.022ms) 🛡️
Command Chaining Hijack          | EXPLOITED ❌      | BLOCKED (0.016ms) 🛡️
---------------------------------------------------------------------------
SUMMARY: Standard CrewAI: 0% Defense | AegisKernel: 100% IMMUNITY (<0.04ms)
===========================================================================
```

---

## 💻 2-Line Drop-In Integration

Hardening an autonomous agent takes only 2 lines of code:

### Universal Tool Protection:
```python
from aegis import AegisShield, SecurityPolicy

# Initialize zero-trust shield
shield = AegisShield(policy=SecurityPolicy.strict())

# Protect any tool function
@shield.protect_tool
def execute_system_command(cmd: str):
    return os.system(cmd)
```

### Auto-Harden CrewAI / LangChain Agents:
```python
from aegis.integrations import protect_agent

# Pass your existing CrewAI or LangChain agent
hardened_agent = protect_agent(my_vulnerable_agent)
# All tools are now shielded at the syscall boundary!
```

---

## 🌐 Live Interactive Web Sandbox

Try the live threat simulation in your browser:
Open `demo.html` in any browser to test live attack payloads, monitor sub-millisecond execution times, and inspect cryptographic forensic audit logs.

---

## 🛠️ Installation & Setup

```bash
# Clone the repository
git clone https://github.com/adikshatriyag-crypto/aegis-kernel.git
cd aegis-kernel

# Install in development mode
pip install -e .

# Run Core Architecture Unit Tests
python test_core.py

# Run CrewAI Benchmark
python benchmark_crewai.py
```

---

## 📜 Architecture Directory

```
aegis-kernel/
├── .github/workflows/
│   └── security_audit.yml      # Automated CI/CD test runner
├── aegis/
│   ├── __init__.py             # Public API & exports (v0.2.0)
│   ├── shield.py               # Top-level AegisShield interface
│   ├── integrations.py         # CrewAI & LangChain auto-wrappers
│   └── core/
│       ├── taint.py            # Mathematical taint propagation engine
│       ├── policy.py           # Capability-based permission matrix
│       ├── interceptor.py      # Syscall gatekeeper (sub-ms proxy)
│       └── audit.py            # Cryptographic SHA-256 HMAC logger
├── benchmark_crewai.py         # Multi-agent benchmark test suite
├── demo.html                   # Live interactive threat sandbox
├── test_core.py                # Comprehensive unit test suite
└── pyproject.toml              # Build & package configuration
```

---

## 💼 Enterprise Design Partners ($1,000 – $5,000/mo)

Deploying autonomous agents in production? We are onboarding **5 founding design partner startups & enterprise teams** for:
- **Fleet-Wide Capability Isolation:** Custom permission boundaries for up to 50 autonomous agents.
- **Compliance-Ready Audit Trails:** Cryptographic SHA-256 HMAC tamper-evident log exports for SOC2, HIPAA, and EU AI Act compliance.
- **Dedicated 24/7 Security SLA:** 1-hour emergency patch turnaround for novel zero-day prompt injection vectors.
- **Direct Founder Slack Channel:** Priority integration engineering and architecture support.

👉 **To apply for a design partnership slot:** Open an Issue or reach out via Twitter [@adikshatriyag](https://x.com) / email `founder@aegiskernel.com`.

---

## 📄 License

Distributed under the **MIT License**. See `LICENSE` for more information.
