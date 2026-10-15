import json
import tempfile
import unittest
from pathlib import Path

from mtacs.controller import QueueAwareController
from mtacs.models import Approach, DemandProfile, ScenarioConfig, SignalPhase, SimulationState, TimingPlan
from mtacs.simulator import TrafficSimulator


class StrengthenedSimulationTests(unittest.TestCase):
    def test_zero_demand_has_no_arrivals_and_perfect_fairness(self):
        final_state, metrics = TrafficSimulator(
            ScenarioConfig(seed=1, duration_seconds=60, arrival_probability=0.0)
        ).run()
        self.assertEqual(final_state.arrivals, 0)
        self.assertEqual(final_state.departures, 0)
        self.assertEqual(metrics.accumulated_delay, 0)
        self.assertEqual(metrics.fairness_index, 1.0)

    def test_metrics_include_per_approach_observability(self):
        _, metrics = TrafficSimulator(
            ScenarioConfig(seed=4, duration_seconds=90, demand_profile=DemandProfile.STRESS)
        ).run()
        self.assertEqual(set(metrics.waiting_seconds_by_approach), {approach.value for approach in Approach})
        self.assertEqual(set(metrics.maximum_queue_by_approach), {approach.value for approach in Approach})
        self.assertGreaterEqual(metrics.mean_queue_length, 0)
        self.assertGreaterEqual(metrics.fairness_index, 0)
        self.assertLessEqual(metrics.fairness_index, 1)

    def test_starvation_protection_requests_opposing_phase(self):
        timing = TimingPlan(green_seconds=2, yellow_seconds=1, all_red_seconds=1, max_green_seconds=20)
        state = SimulationState()
        state.signal.phase = SignalPhase.NORTH_SOUTH_GREEN
        state.signal.elapsed_seconds = 2
        state.waiting_seconds_by_approach[Approach.EAST] = 50
        controller = QueueAwareController(timing, starvation_threshold_seconds=45)
        proposal = controller.propose(state)
        self.assertEqual(proposal.requested_phase, SignalPhase.NORTH_SOUTH_YELLOW)

    def test_batch_runner_writes_csv_and_json_schema(self):
        from scripts.run_experiments import run_batch

        with tempfile.TemporaryDirectory() as directory:
            result = run_batch(Path(directory), (3,), (20,))
            self.assertEqual(result["runs"], len(tuple(DemandProfile)) * 2)
            self.assertTrue(Path(result["raw_csv"]).exists())
            payload = json.loads(Path(result["summary_json"]).read_text(encoding="utf-8"))
            self.assertEqual(len(payload["runs"]), result["runs"])
            self.assertTrue(payload["summaries"])
            self.assertIn("mean_accumulated_delay", payload["summaries"][0])


if __name__ == "__main__":
    unittest.main()
