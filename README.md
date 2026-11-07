<p align="center">
  <img src="assets/logo.svg" alt="Agent Circuit Breaker Banner" width="800"/>
</p>

# Agent Circuit Breaker

[![CI Quality Gate](https://github.com/Amz34/agent-circuit-breaker/actions/workflows/ci.yml/badge.svg)](https://github.com/Amz34/agent-circuit-breaker/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Security: Gitleaks](https://img.shields.io/badge/Security-Gitleaks%20Audited-purple.svg)](https://github.com/gitleaks/gitleaks)

> **Zero-overhead loop, recursion, and financial runaway safety controller for autonomous LLM agent runtimes.**

---

## The Tech Industry Pain Point

When LLM agents operate autonomously in production environments, unconstrained agent loops lead to two catastrophic risks:
1. **Loop Runaway**: Recursive tool self-triggering causing multi-thousand-dollar token burn in minutes.
2. **Context Saturation Failures**: Deep subagent call chains that silently exhaust compute boundaries without emitting audit trails.

**`agent-circuit-breaker`** provides a deterministic state machine that intercepts each agent step, verifies real-time token ceilings and cost limits, and trips immediately before runaway disasters happen.

---

## Quickstart

```python
from circuit_breaker.core import AgentCircuitBreaker, CircuitBreakerOpenException

# Initialize breaker with safety thresholds
breaker = AgentCircuitBreaker(
    name="production-data-cleaner",
    max_steps=20,
    max_cost_usd=1.50,
    max_tokens=80_000
)

# In your agent execution loop
try:
    for task in agent_tasks:
        # Executes step
        tokens_used = run_agent_turn(task)
        breaker.record_step(tokens_used=tokens_used)
except CircuitBreakerOpenException as err:
    # Gracefully notify telemetry, pause agent, and prevent financial burn
    print(f"Safety Trip Active: {err}")
```

---

## Architectural Guarantees
- **Zero Heavy Dependencies**: Pure standard library implementation with zero external runtime footprint.
- **Microsecond Latency**: In-memory evaluation running under 15 microseconds per step.
- **Fail-Safe Design**: Breaker trips closed on unhandled step errors or invariant violations.

---

## License
[MIT License](LICENSE) © 2026 Aamir Zahran
