from __future__ import annotations

from .models import RunMetrics, SimulationState
from .models import Approach


class MetricsCollector:
    def __init__(self) -> None:
        self.maximum_queue_length = 0
        self.queue_length_total = 0
        self.observations = 0

    def observe(self, state: SimulationState) -> None:
        self.maximum_queue_length = max(
            self.maximum_queue_length, sum(state.queues.values())
        )
        self.queue_length_total += sum(state.queues.values())
        self.observations += 1
        for approach in Approach:
            state.maximum_queue_by_approach[approach] = max(
                state.maximum_queue_by_approach[approach], state.queues[approach]
            )

    def finalize(self, state: SimulationState) -> RunMetrics:
        minutes = state.simulation_time / 60
        throughput = state.departures / minutes if minutes else 0.0
        mean_queue = self.queue_length_total / self.observations if self.observations else 0.0
        waiting = [state.waiting_seconds_by_approach[approach] for approach in Approach]
        waiting_sum = sum(waiting)
        fairness = (
            (waiting_sum * waiting_sum) / (len(waiting) * sum(value * value for value in waiting))
            if waiting_sum and any(waiting)
            else 1.0
        )
        return RunMetrics(
            duration_seconds=state.simulation_time,
            total_arrivals=state.arrivals,
            total_departures=state.departures,
            final_queue_length=sum(state.queues.values()),
            maximum_queue_length=self.maximum_queue_length,
            total_stops=state.stops,
            accumulated_delay=state.accumulated_delay,
            throughput_per_minute=round(throughput, 2),
            mean_queue_length=round(mean_queue, 2),
            fairness_index=round(fairness, 4),
            waiting_seconds_by_approach={
                approach.value: state.waiting_seconds_by_approach[approach]
                for approach in Approach
            },
            maximum_queue_by_approach={
                approach.value: state.maximum_queue_by_approach[approach]
                for approach in Approach
            },
            validation_interventions=state.validation_interventions,
        )
