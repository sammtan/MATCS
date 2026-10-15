import unittest

from mtacs.controller import QueueAwareController
from mtacs.models import (
    DemandProfile,
    ScenarioConfig,
    SignalPhase,
    SimulationState,
    TimingPlan,
)
from mtacs.safety import SafetyValidator
from mtacs.simulator import TrafficSimulator


class ExperimentComparisonTests(unittest.TestCase):
    def test_all_profiles_and_scales_produce_reproducible_runs(self):
        durations = (30, 120, 600)
        profiles = tuple(DemandProfile)
        for duration in durations:
            for profile in profiles:
                config = ScenarioConfig(
                    seed=17,
                    duration_seconds=duration,
                    demand_profile=profile,
                )
                first = TrafficSimulator(config).run()[1].as_dict()
                second = TrafficSimulator(config).run()[1].as_dict()
                with self.subTest(duration=duration, profile=profile):
                    self.assertEqual(first, second)
                    self.assertGreaterEqual(
                        first["total_arrivals"], first["total_departures"]
                    )
                    self.assertGreaterEqual(
                        first["maximum_queue_length"], first["final_queue_length"]
                    )

    def test_matched_controller_comparison_is_replayable(self):
        for profile in DemandProfile:
            config = ScenarioConfig(
                seed=23,
                duration_seconds=240,
                demand_profile=profile,
            )
            fixed = TrafficSimulator(config, "fixed_time").run()[1].as_dict()
            heuristic = TrafficSimulator(config, "queue_aware").run()[1].as_dict()
            with self.subTest(profile=profile):
                self.assertEqual(fixed["total_arrivals"], heuristic["total_arrivals"])
                self.assertGreaterEqual(fixed["total_arrivals"], fixed["total_departures"])
                self.assertGreaterEqual(
                    heuristic["total_arrivals"], heuristic["total_departures"]
                )

    def test_queue_aware_controller_never_skips_phase(self):
        timing = TimingPlan(green_seconds=3, yellow_seconds=1, all_red_seconds=1)
        controller = QueueAwareController(timing)
        validator = SafetyValidator()
        state = SimulationState()
        for tick in range(40):
            state.simulation_time = tick
            state.queues = {
                approach: (tick + index) % 7
                for index, approach in enumerate(state.queues)
            }
            proposal = controller.propose(state)
            result = validator.validate(state, proposal)
            with self.subTest(tick=tick):
                self.assertTrue(result.accepted, result.reason)
                self.assertIn(
                    result.phase,
                    (state.signal.phase, controller._next_phase(state.signal.phase)),
                )
                if result.phase != state.signal.phase:
                    state.signal.phase = result.phase
                    state.signal.elapsed_seconds = 0
                else:
                    state.signal.elapsed_seconds += 1

    def test_stress_scale_completes_without_negative_queues(self):
        config = ScenarioConfig(
            seed=99,
            duration_seconds=1_200,
            demand_profile=DemandProfile.STRESS,
        )
        final_state, metrics = TrafficSimulator(config, "queue_aware").run()
        self.assertEqual(final_state.simulation_time, 1_200)
        self.assertTrue(all(queue >= 0 for queue in final_state.queues.values()))
        self.assertGreater(metrics.maximum_queue_length, 0)


if __name__ == "__main__":
    unittest.main()
