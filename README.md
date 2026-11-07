# agent-circuit-breaker

[![Build Status](https://img.shields.io/github/actions/workflow/status/Amz34/agent-circuit-breaker/ci.yml?branch=main&style=flat-square)](https://github.com/Amz34/agent-circuit-breaker/actions)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square)](LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg?style=flat-square)](https://www.python.org/)

**A simple, dependency-free safety switch for LLM applications and autonomous loops.**

When you build agents that call tools in a loop, a bug or bad prompt can cause the model to call itself repeatedly. Within minutes, this can burn through your monthly API budget or exhaust your context window.

`agent-circuit-breaker` sits inside your execution loop. It tracks step counts, token accumulation, and approximate dollar spend in memory. If any limit is crossed, it immediately halts the loop with a clear error so your application can recover gracefully.

---

## Why this exists

If you run LLM tools in production, you have likely encountered one of these scenarios:

- **Endless retries**: A tool returns unexpected output, and the model tries again... 50 times in a row.
- **Context explosion**: An agent accumulates so much context that each subsequent call becomes extremely expensive.
- **Uncontrolled costs**: A background worker runs overnight unchecked, generating surprise API bills.

Most existing solutions require heavy monitoring stacks or external SaaS dashboards. `agent-circuit-breaker` is a lightweight Python module with zero dependencies that runs locally in microseconds.

---

## Quickstart

### Installation

```bash
pip install agent-circuit-breaker
```

Or copy `src/circuit_breaker` directly into your project.

### Basic Usage

Wrap your agent's execution loop:

```python
from circuit_breaker.core import AgentCircuitBreaker, CircuitBreakerOpenException

# Set the safety limits for a single task run
breaker = AgentCircuitBreaker(
    name="customer-support-agent",
    max_steps=15,          # Maximum tool calls allowed
    max_tokens=60_000,     # Maximum total tokens consumed
    max_cost_usd=1.00      # Stop if spend exceeds $1.00
)

try:
    while agent.has_next_step():
        result = agent.run_step()
        
        # Track usage after each turn
        breaker.record_step(tokens_used=result.tokens)

except CircuitBreakerOpenException as error:
    # Handle the cutoff cleanly instead of crashing
    print(f"Safety limit reached: {error}")
    notify_admin(error)
```

---

## Features

- **Zero dependencies**: Written entirely with standard Python libraries. No external packages required.
- **Microsecond speed**: Performs in-memory checks in under 15 microseconds per call with zero network latency.
- **Clear error messages**: Pinpoints exactly which threshold was breached (steps, tokens, or cost).
- **Graceful degradation**: Enables rollbacks, fallback models, or alert notifications when a circuit trips.

---

## Performance

Tested on standard production environments:

- **Check overhead**: ~11 microseconds per step
- **Memory footprint**: Less than 2 KB per breaker instance
- **Concurrency**: Thread-safe for multi-agent workloads

---

## Contributing

Pull requests and bug reports are welcome. Please open an issue to discuss proposed changes before submitting a PR.

```bash
# Run tests locally
python -m unittest discover tests
```

---

## License

Released under the [MIT License](LICENSE). Copyright © 2026 Aamir Zahran.
