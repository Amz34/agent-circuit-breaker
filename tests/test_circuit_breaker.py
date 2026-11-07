import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
from circuit_breaker.core import AgentCircuitBreaker, CircuitBreakerOpenException

class TestAgentCircuitBreaker(unittest.TestCase):
    def test_circuit_trips_on_step_runaway(self):
        cb = AgentCircuitBreaker(name="test-runaway", max_steps=3)
        cb.record_step(tokens_used=100)
        cb.record_step(tokens_used=100)
        cb.record_step(tokens_used=100)
        with self.assertRaises(CircuitBreakerOpenException):
            cb.record_step(tokens_used=100)
        self.assertTrue(cb.is_open)

    def test_circuit_trips_on_cost(self):
        cb = AgentCircuitBreaker(name="test-cost", max_cost_usd=0.05, token_cost_per_million=50.0)
        cb.record_step(tokens_used=200)
        with self.assertRaises(CircuitBreakerOpenException):
            cb.record_step(tokens_used=2_000_000)
        self.assertTrue(cb.is_open)

if __name__ == "__main__":
    unittest.main()
