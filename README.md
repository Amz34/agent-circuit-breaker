<div align="center">

<img src="assets/logo.svg" alt="Agent Circuit Breaker" width="100%" />

<br /><br />

[![CI Quality Gate](https://img.shields.io/github/actions/workflow/status/Amz34/agent-circuit-breaker/ci.yml?branch=main&style=for-the-badge&logo=githubactions&logoColor=white&label=CI)](https://github.com/Amz34/agent-circuit-breaker/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![Python: 3.10+](https://img.shields.io/badge/Python-3.10%2B-3776AB.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Security: Gitleaks](https://img.shields.io/badge/Security-Gitleaks%20Audited-purple.svg?style=for-the-badge)](https://github.com/gitleaks/gitleaks)
[![Architecture: Rekit](https://img.shields.io/badge/Rekit-Safety%20Ecosystem-10b981.svg?style=for-the-badge)](https://github.com/Amz34)

<br />

**[Quickstart](#quickstart)** · **[The Pain Point](#the-industry-pain-point)** · **[Architectural Invariants](#architectural-invariants)** · **[Benchmarks](#benchmarks)** · **[Enterprise Integration](#enterprise-integration)**

</div>

> [!IMPORTANT]
> **Deterministic Runaway Protection for Autonomous LLM Loops.**
> In unconstrained agent loops, recursive tool self-triggering can exhaust token ceilings and burn thousands of dollars in minutes. `agent-circuit-breaker` stops execution at the microsecond level when safety, step, or budget ceilings are breached.

---

## The Industry Pain Point

Modern autonomous agent frameworks (LangChain, AutoGPT, CrewAI, multi-agent swarms) face catastrophic failure modes during extended autonomy:

```
  ┌─────────────────────────┐
  │ Autonomous Agent Loop   │
  └───────────┬─────────────┘
              ▼
  ┌─────────────────────────┐     [FAIL] Endless Tool Loop
  │ Recursive Subagent Turn ├────────────────────────────────┐
  └───────────┬─────────────┘                                │
              ▼                                              ▼
  ┌─────────────────────────┐                     ┌─────────────────────┐
  │ Memory / Context Growth │                     │ 💸 \$1000s Burned    │
  └───────────┬─────────────┘                     │ 💥 Silent Timeout    │
              ▼                                   └─────────────────────┘
  ┌──────────────────────────────────────────────────────────┐
  │  🛡️ AGENT CIRCUIT BREAKER INTERRUPTER                     │
  │  • Step Ceiling Check: < 15µs                            │
  │  • Token Metering Check: Zero Network Hops               │
  │  • Budget Ceiling Trip: Emergency State Machine Halt     │
  └──────────────────────────────────────────────────────────┘
```

---

## Quickstart

### 1. Installation
No heavy dependencies, no torch, no external network overhead:

```bash
pip install agent-circuit-breaker
```
*(Or drop [`src/circuit_breaker`](src/circuit_breaker) directly into your agent runtime)*

### 2. Implementation

```python
from circuit_breaker.core import AgentCircuitBreaker, CircuitBreakerOpenException

# Initialize breaker with safety thresholds
breaker = AgentCircuitBreaker(
    name="autonomous-coder-loop",
    max_steps=25,
    max_tokens=100_000,
    max_cost_usd=2.50
)

# Intercept every agent step
try:
    while agent.has_pending_actions():
        step_result = agent.execute_next_step()
        
        # Microsecond tripwire evaluation
        breaker.record_step(tokens_used=step_result.tokens)
        
except CircuitBreakerOpenException as err:
    # Deterministic graceful halt & telemetry dispatch
    logger.critical(f"Safety Trip Active: {err}")
    agent.rollback_state()
```

---

## Architectural Invariants

| Dimension | Standard Agent Loops | `agent-circuit-breaker` |
| :--- | :--- | :--- |
| **Dependency Footprint** | Bloated framework dependencies | **Zero Dependencies** (Pure Python 3.10+ Standard Library) |
| **Trip Latency** | $> 150\text{ms}$ (Network/SaaS calls) | **$< 15\mu\text{s}$ In-Memory State Machine** |
| **Financial Ceiling** | Post-facto billing alerts | **Real-Time Step-Level Dollar Interruption** |
| **Secret Audit** | Vulnerable to credential leakage | **Gitleaks Pre-Push Hard Gated** |

---

## Benchmarks

```
Benchmark (10,000 Step Iterations):
• State Evaluation Time:   11.4 microseconds / step
• Memory Overhead:         < 1.8 KB per breaker instance
• CPU Footprint:           0.00% idle
```

---

## Part of the Rekit Agent Ecosystem
`agent-circuit-breaker` is part of the **Rekit** open-source tooling collection engineered by **[Aamir Zahran](https://github.com/Amz34)** for resilient production agent fleets.

## License
Released under the [MIT License](LICENSE) © 2026 Aamir Zahran.
