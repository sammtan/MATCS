from __future__ import annotations

import argparse
import json

from .models import DemandProfile, ScenarioConfig
from .simulator import TrafficSimulator


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the MATCS first simulation slice")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--ticks", type=int, default=120)
    parser.add_argument(
        "--controller",
        choices=("fixed_time", "queue_aware"),
        default="fixed_time",
    )
    parser.add_argument(
        "--scenario",
        choices=tuple(profile.value for profile in DemandProfile),
        default=DemandProfile.BALANCED.value,
    )
    args = parser.parse_args()

    config = ScenarioConfig(
        seed=args.seed,
        duration_seconds=args.ticks,
        demand_profile=DemandProfile(args.scenario),
    )
    final_state, metrics = TrafficSimulator(config, args.controller).run()
    print("MATCS first vertical slice")
    print(f"controller={args.controller}")
    print(f"scenario={args.scenario}")
    print(f"simulation_seconds={final_state.simulation_time}")
    print(f"final_phase={final_state.signal.phase.value}")
    print(json.dumps(metrics.as_dict(), indent=2))
