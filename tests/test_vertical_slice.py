import unittest

from mtacs.controller import FixedTimeController
from mtacs.models import (
    ControllerProposal,
    ScenarioConfig,
    SignalPhase,
    SimulationState,
    TimingPlan,
)
from mtacs.safety import SafetyValidator
from mtacs.simulator import TrafficSimulator


class VerticalSliceTests(unittest.TestCase):
    def test_fixed_time_controller_advances_after_green_duration(self):
        timing = TimingPlan(green_seconds=2, yellow_seconds=1, all_red_seconds=1)
        controller = FixedTimeController(timing)
        state = SimulationState()
        state.signal.elapsed_seconds = 1
        proposal = controller.propose(state)
        self.assertEqual(proposal.requested_phase, SignalPhase.NORTH_SOUTH_YELLOW)

    def test_validator_rejects_skipping_a_phase(self):
        state = SimulationState()
        proposal = ControllerProposal(
            simulation_time=0,
            requested_phase=SignalPhase.EAST_WEST_GREEN,
            controller_name="test",
            controller_version="0",
        )
        result = SafetyValidator().validate(state, proposal)
        self.assertFalse(result.accepted)
        self.assertEqual(result.reason, "invalid_phase_transition")

    def test_validator_rejects_stale_proposal(self):
        state = SimulationState(simulation_time=2)
        proposal = ControllerProposal(
            simulation_time=1,
            requested_phase=SignalPhase.NORTH_SOUTH_GREEN,
            controller_name="test",
            controller_version="0",
        )
        result = SafetyValidator().validate(state, proposal)
        self.assertFalse(result.accepted)
        self.assertEqual(result.reason, "stale_simulation_time")

    def test_simulation_is_reproducible(self):
        config = ScenarioConfig(seed=7, duration_seconds=60)
        first = TrafficSimulator(config).run()[1].as_dict()
        second = TrafficSimulator(config).run()[1].as_dict()
        self.assertEqual(first, second)

    def test_simulation_produces_feedback_metrics(self):
        final_state, metrics = TrafficSimulator(
            ScenarioConfig(seed=7, duration_seconds=60)
        ).run()
        self.assertEqual(final_state.simulation_time, 60)
        self.assertGreater(metrics.total_arrivals, 0)
        self.assertGreaterEqual(metrics.total_arrivals, metrics.total_departures)
        self.assertGreaterEqual(metrics.maximum_queue_length, metrics.final_queue_length)


if __name__ == "__main__":
    unittest.main()
