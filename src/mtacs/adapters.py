from __future__ import annotations

from typing import Protocol

from .models import ControllerProposal, SimulationState, ValidationResult


class ObservationAdapter(Protocol):
    """Future boundary for simulator or authority-approved field observations."""

    def read_state(self) -> SimulationState:
        ...


class Actuator(Protocol):
    """Boundary for simulated actuation or a future authority gateway."""

    def apply(self, validation: ValidationResult) -> None:
        ...


class Controller(Protocol):
    def propose(self, state: SimulationState) -> ControllerProposal:
        ...
