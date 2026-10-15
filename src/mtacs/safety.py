from __future__ import annotations

from .models import ControllerProposal, SignalPhase, SimulationState, ValidationResult


class SafetyValidator:
    """Validates abstract phase proposals before simulated actuation."""

    def validate(
        self, state: SimulationState, proposal: ControllerProposal
    ) -> ValidationResult:
        if proposal.simulation_time != state.simulation_time:
            return ValidationResult(False, state.signal.phase, "stale_simulation_time")

        sequence = list(SignalPhase)
        current_index = sequence.index(state.signal.phase)
        requested_index = sequence.index(proposal.requested_phase)
        expected_index = (current_index + 1) % len(sequence)

        if proposal.requested_phase == state.signal.phase:
            return ValidationResult(True, state.signal.phase, "keep_current_phase")
        if requested_index != expected_index:
            return ValidationResult(False, state.signal.phase, "invalid_phase_transition")

        return ValidationResult(True, proposal.requested_phase, "valid_next_phase")
