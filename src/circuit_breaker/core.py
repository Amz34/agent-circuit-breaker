"""Core Circuit Breaker logic for LLM agent loops."""
from dataclasses import dataclass, field
import time
from typing import Dict, List, Optional, Callable

class CircuitBreakerOpenException(Exception):
    """Raised when an autonomous agent execution exceeds safety thresholds."""
    pass

@dataclass
class AgentCircuitBreaker:
    name: str
    max_steps: int = 25
    max_tokens: int = 100_000
    max_cost_usd: float = 2.50
    token_cost_per_million: float = 3.00
    current_steps: int = 0
    total_tokens: int = 0
    total_cost_usd: float = 0.0
    trip_reasons: List[str] = field(default_factory=list)
    is_open: bool = False

    def record_step(self, tokens_used: int = 0, step_cost_usd: Optional[float] = None) -> None:
        if self.is_open:
            raise CircuitBreakerOpenException(f"Circuit '{self.name}' is OPEN: {'; '.join(self.trip_reasons)}")
        
        self.current_steps += 1
        self.total_tokens += tokens_used
        
        if step_cost_usd is not None:
            self.total_cost_usd += step_cost_usd
        else:
            self.total_cost_usd += (tokens_used / 1_000_000.0) * self.token_cost_per_million

        # Evaluate safety invariants
        if self.current_steps > self.max_steps:
            self._trip(f"Step ceiling exceeded ({self.current_steps} > {self.max_steps})")
        
        if self.total_tokens > self.max_tokens:
            self._trip(f"Token ceiling exceeded ({self.total_tokens} > {self.max_tokens})")

        if self.total_cost_usd > self.max_cost_usd:
            self._trip(f"Budget ceiling exceeded (${self.total_cost_usd:.4f} > ${self.max_cost_usd:.2f})")

    def _trip(self, reason: str) -> None:
        self.is_open = True
        self.trip_reasons.append(reason)
        raise CircuitBreakerOpenException(f"EMERGENCY TRIP [{self.name}]: {reason}")

    def status(self) -> Dict:
        return {
            "name": self.name,
            "is_open": self.is_open,
            "steps": f"{self.current_steps}/{self.max_steps}",
            "tokens": f"{self.total_tokens}/{self.max_tokens}",
            "cost_usd": f"${self.total_cost_usd:.4f}/${self.max_cost_usd:.2f}",
            "trip_reasons": self.trip_reasons
        }
