from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class Approach(str, Enum):
    NORTH = "north"
    SOUTH = "south"
    EAST = "east"
    WEST = "west"


class DemandProfile(str, Enum):
    BALANCED = "balanced"
    NORTH_SOUTH_HEAVY = "north_south_heavy"
    EAST_WEST_HEAVY = "east_west_heavy"
    STRESS = "stress"

    def probabilities(self, base_probability: float) -> dict[Approach, float]:
        if self is DemandProfile.NORTH_SOUTH_HEAVY:
            return {
                Approach.NORTH: min(1.0, base_probability * 1.6),
                Approach.SOUTH: min(1.0, base_probability * 1.6),
                Approach.EAST: base_probability * 0.6,
                Approach.WEST: base_probability * 0.6,
            }
        if self is DemandProfile.EAST_WEST_HEAVY:
            return {
                Approach.NORTH: base_probability * 0.6,
                Approach.SOUTH: base_probability * 0.6,
                Approach.EAST: min(1.0, base_probability * 1.6),
                Approach.WEST: min(1.0, base_probability * 1.6),
            }
        if self is DemandProfile.STRESS:
            return {approach: min(1.0, base_probability * 1.8) for approach in Approach}
        return {approach: base_probability for approach in Approach}


class SignalPhase(str, Enum):
    NORTH_SOUTH_GREEN = "north_south_green"
    NORTH_SOUTH_YELLOW = "north_south_yellow"
    ALL_RED_TO_EAST_WEST = "all_red_to_east_west"
    EAST_WEST_GREEN = "east_west_green"
    EAST_WEST_YELLOW = "east_west_yellow"
    ALL_RED_TO_NORTH_SOUTH = "all_red_to_north_south"

    @property
    def green_approaches(self) -> frozenset[Approach]:
        if self is SignalPhase.NORTH_SOUTH_GREEN:
            return frozenset({Approach.NORTH, Approach.SOUTH})
        if self is SignalPhase.EAST_WEST_GREEN:
            return frozenset({Approach.EAST, Approach.WEST})
        return frozenset()

    @property
    def is_yellow(self) -> bool:
        return self in {
            SignalPhase.NORTH_SOUTH_YELLOW,
            SignalPhase.EAST_WEST_YELLOW,
        }


@dataclass(frozen=True)
class TimingPlan:
    green_seconds: int = 20
    yellow_seconds: int = 4
    all_red_seconds: int = 2
    max_green_seconds: int = 35

    def __post_init__(self) -> None:
        if self.green_seconds < 1:
            raise ValueError("green_seconds must be positive")
        if self.yellow_seconds < 1:
            raise ValueError("yellow_seconds must be positive")
        if self.all_red_seconds < 1:
            raise ValueError("all_red_seconds must be positive")
        if self.max_green_seconds < self.green_seconds:
            raise ValueError("max_green_seconds must be at least green_seconds")


@dataclass(frozen=True)
class ScenarioConfig:
    seed: int = 42
    duration_seconds: int = 120
    arrival_probability: float = 0.25
    service_rate: int = 1
    demand_profile: DemandProfile = DemandProfile.BALANCED
    queue_pressure_weight: float = 1.0
    starvation_threshold_seconds: int = 45
    timing: TimingPlan = field(default_factory=TimingPlan)

    def __post_init__(self) -> None:
        if self.duration_seconds < 1:
            raise ValueError("duration_seconds must be positive")
        if not 0 <= self.arrival_probability <= 1:
            raise ValueError("arrival_probability must be between 0 and 1")
        if self.service_rate < 1:
            raise ValueError("service_rate must be positive")
        if self.queue_pressure_weight <= 0:
            raise ValueError("queue_pressure_weight must be positive")
        if self.starvation_threshold_seconds < 1:
            raise ValueError("starvation_threshold_seconds must be positive")


@dataclass
class SignalState:
    phase: SignalPhase = SignalPhase.NORTH_SOUTH_GREEN
    elapsed_seconds: int = 0


@dataclass
class SimulationState:
    simulation_time: int = 0
    signal: SignalState = field(default_factory=SignalState)
    queues: dict[Approach, int] = field(
        default_factory=lambda: {approach: 0 for approach in Approach}
    )
    arrivals: int = 0
    departures: int = 0
    stops: int = 0
    accumulated_delay: int = 0
    waiting_seconds_by_approach: dict[Approach, int] = field(
        default_factory=lambda: {approach: 0 for approach in Approach}
    )
    maximum_queue_by_approach: dict[Approach, int] = field(
        default_factory=lambda: {approach: 0 for approach in Approach}
    )
    validation_interventions: int = 0

    def copy(self) -> "SimulationState":
        return SimulationState(
            simulation_time=self.simulation_time,
            signal=SignalState(self.signal.phase, self.signal.elapsed_seconds),
            queues=dict(self.queues),
            arrivals=self.arrivals,
            departures=self.departures,
            stops=self.stops,
            accumulated_delay=self.accumulated_delay,
            waiting_seconds_by_approach=dict(self.waiting_seconds_by_approach),
            maximum_queue_by_approach=dict(self.maximum_queue_by_approach),
            validation_interventions=self.validation_interventions,
        )


@dataclass(frozen=True)
class ControllerProposal:
    simulation_time: int
    requested_phase: SignalPhase
    controller_name: str
    controller_version: str


@dataclass(frozen=True)
class ValidationResult:
    accepted: bool
    phase: SignalPhase
    reason: str


@dataclass(frozen=True)
class RunMetrics:
    duration_seconds: int
    total_arrivals: int
    total_departures: int
    final_queue_length: int
    maximum_queue_length: int
    total_stops: int
    accumulated_delay: int
    throughput_per_minute: float
    mean_queue_length: float
    fairness_index: float
    waiting_seconds_by_approach: dict[str, int]
    maximum_queue_by_approach: dict[str, int]
    validation_interventions: int

    def as_dict(self) -> dict[str, int | float]:
        return {
            "duration_seconds": self.duration_seconds,
            "total_arrivals": self.total_arrivals,
            "total_departures": self.total_departures,
            "final_queue_length": self.final_queue_length,
            "maximum_queue_length": self.maximum_queue_length,
            "total_stops": self.total_stops,
            "accumulated_delay": self.accumulated_delay,
            "throughput_per_minute": self.throughput_per_minute,
            "mean_queue_length": self.mean_queue_length,
            "fairness_index": self.fairness_index,
            "waiting_seconds_by_approach": self.waiting_seconds_by_approach,
            "maximum_queue_by_approach": self.maximum_queue_by_approach,
            "validation_interventions": self.validation_interventions,
        }
