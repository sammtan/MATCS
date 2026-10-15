from __future__ import annotations

import random

from .controller import FixedTimeController, QueueAwareController
from .metrics import MetricsCollector
from .models import Approach, ScenarioConfig, SignalPhase, SimulationState
from .safety import SafetyValidator


class SimulatedActuator:
    def apply(self, state: SimulationState, phase: SignalPhase) -> None:
        if state.signal.phase == phase:
            return
        state.signal.phase = phase
        state.signal.elapsed_seconds = 0


class TrafficSimulator:
    def __init__(self, config: ScenarioConfig, controller_name: str = "fixed_time") -> None:
        self.config = config
        self.random = random.Random(config.seed)
        self.state = SimulationState()
        if controller_name == "fixed_time":
            self.controller = FixedTimeController(config.timing)
        elif controller_name == "queue_aware":
            self.controller = QueueAwareController(
                config.timing,
                config.queue_pressure_weight,
                config.starvation_threshold_seconds,
            )
        else:
            raise ValueError(f"unknown controller: {controller_name}")
        self.validator = SafetyValidator()
        self.actuator = SimulatedActuator()
        self.metrics = MetricsCollector()

    def run(self) -> tuple[SimulationState, object]:
        for _ in range(self.config.duration_seconds):
            self.step()
        return self.state.copy(), self.metrics.finalize(self.state)

    def step(self) -> None:
        self._generate_arrivals()
        proposal = self.controller.propose(self.state)
        validation = self.validator.validate(self.state, proposal)
        if validation.accepted:
            self.actuator.apply(self.state, validation.phase)
        else:
            self.state.validation_interventions += 1
        self._move_vehicles()
        for approach in Approach:
            if self.state.queues[approach] > 0:
                self.state.waiting_seconds_by_approach[approach] += 1
        self.state.simulation_time += 1
        self.state.signal.elapsed_seconds += 1
        self.state.accumulated_delay += sum(self.state.queues.values())
        self.metrics.observe(self.state)

    def _generate_arrivals(self) -> None:
        probabilities = self.config.demand_profile.probabilities(
            self.config.arrival_probability
        )
        for approach in Approach:
            if self.random.random() < probabilities[approach]:
                self.state.queues[approach] += 1
                self.state.arrivals += 1
                self.state.stops += 1

    def _move_vehicles(self) -> None:
        for approach in self.state.signal.phase.green_approaches:
            departing = min(self.config.service_rate, self.state.queues[approach])
            self.state.queues[approach] -= departing
            self.state.departures += departing
