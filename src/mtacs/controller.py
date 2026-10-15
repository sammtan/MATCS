from __future__ import annotations

from dataclasses import dataclass

from .models import ControllerProposal, SignalPhase, SimulationState, TimingPlan


@dataclass(frozen=True)
class FixedTimeController:
    timing: TimingPlan
    name: str = "fixed_time"
    version: str = "0.1.0"

    def propose(self, state: SimulationState) -> ControllerProposal:
        phase = state.signal.phase
        elapsed = state.signal.elapsed_seconds
        next_phase = self._next_phase(phase)
        duration = self._duration(phase)
        requested = next_phase if elapsed + 1 >= duration else phase
        return ControllerProposal(
            simulation_time=state.simulation_time,
            requested_phase=requested,
            controller_name=self.name,
            controller_version=self.version,
        )

    def _duration(self, phase: SignalPhase) -> int:
        if phase in {
            SignalPhase.NORTH_SOUTH_GREEN,
            SignalPhase.EAST_WEST_GREEN,
        }:
            return self.timing.green_seconds
        if phase in {
            SignalPhase.NORTH_SOUTH_YELLOW,
            SignalPhase.EAST_WEST_YELLOW,
        }:
            return self.timing.yellow_seconds
        return self.timing.all_red_seconds

    @staticmethod
    def _next_phase(phase: SignalPhase) -> SignalPhase:
        sequence = list(SignalPhase)
        return sequence[(sequence.index(phase) + 1) % len(sequence)]


@dataclass(frozen=True)
class QueueAwareController:
    timing: TimingPlan
    queue_pressure_weight: float = 1.0
    starvation_threshold_seconds: int = 45
    name: str = "queue_aware"
    version: str = "0.1.0"

    def propose(self, state: SimulationState) -> ControllerProposal:
        phase = state.signal.phase
        requested = phase
        if phase in {
            SignalPhase.NORTH_SOUTH_GREEN,
            SignalPhase.EAST_WEST_GREEN,
        }:
            elapsed = state.signal.elapsed_seconds
            current_pressure = sum(
                state.queues[approach] for approach in phase.green_approaches
            )
            current_pressure += self.queue_pressure_weight * sum(
                state.waiting_seconds_by_approach[approach]
                for approach in phase.green_approaches
            )
            opposing_approaches = set(state.queues) - set(phase.green_approaches)
            opposing_pressure = sum(state.queues[approach] for approach in opposing_approaches)
            opposing_pressure += self.queue_pressure_weight * sum(
                state.waiting_seconds_by_approach[approach]
                for approach in opposing_approaches
            )
            starvation = any(
                state.waiting_seconds_by_approach[approach]
                >= self.starvation_threshold_seconds
                for approach in opposing_approaches
            )
            minimum_reached = elapsed + 1 >= self.timing.green_seconds
            maximum_reached = elapsed + 1 >= self.timing.max_green_seconds
            if minimum_reached and (
                maximum_reached or starvation or opposing_pressure > current_pressure
            ):
                requested = self._next_phase(phase)
        elif state.signal.elapsed_seconds + 1 >= self._duration(phase):
            requested = self._next_phase(phase)
        return ControllerProposal(
            simulation_time=state.simulation_time,
            requested_phase=requested,
            controller_name=self.name,
            controller_version=self.version,
        )

    def _duration(self, phase: SignalPhase) -> int:
        if phase in {
            SignalPhase.NORTH_SOUTH_GREEN,
            SignalPhase.EAST_WEST_GREEN,
        }:
            return self.timing.green_seconds
        if phase in {
            SignalPhase.NORTH_SOUTH_YELLOW,
            SignalPhase.EAST_WEST_YELLOW,
        }:
            return self.timing.yellow_seconds
        return self.timing.all_red_seconds

    @staticmethod
    def _next_phase(phase: SignalPhase) -> SignalPhase:
        sequence = list(SignalPhase)
        return sequence[(sequence.index(phase) + 1) % len(sequence)]
