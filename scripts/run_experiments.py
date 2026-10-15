from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path
from statistics import mean, pstdev

from mtacs.models import DemandProfile, ScenarioConfig
from mtacs.simulator import TrafficSimulator


DEFAULT_SEEDS = (7, 17, 23, 42, 99)
DEFAULT_DURATIONS = (120, 600)
CONTROLLERS = ("fixed_time", "queue_aware")


def run_batch(output_dir: Path, seeds: tuple[int, ...], durations: tuple[int, ...]) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    records = []
    for profile in DemandProfile:
        for duration in durations:
            for seed in seeds:
                for controller in CONTROLLERS:
                    config = ScenarioConfig(
                        seed=seed,
                        duration_seconds=duration,
                        demand_profile=profile,
                    )
                    metrics = TrafficSimulator(config, controller).run()[1]
                    record = {
                        "profile": profile.value,
                        "duration_seconds": duration,
                        "seed": seed,
                        "controller": controller,
                        **metrics.as_dict(),
                    }
                    records.append(record)

    raw_csv = output_dir / "raw_runs.csv"
    fieldnames = [
        "profile", "duration_seconds", "seed", "controller",
        "total_arrivals", "total_departures", "final_queue_length",
        "maximum_queue_length", "total_stops", "accumulated_delay",
        "throughput_per_minute", "mean_queue_length", "fairness_index",
        "validation_interventions", "waiting_seconds_by_approach",
        "maximum_queue_by_approach",
    ]
    with raw_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for record in records:
            row = dict(record)
            row["waiting_seconds_by_approach"] = json.dumps(
                row["waiting_seconds_by_approach"], sort_keys=True
            )
            row["maximum_queue_by_approach"] = json.dumps(
                row["maximum_queue_by_approach"], sort_keys=True
            )
            writer.writerow(row)

    grouped = defaultdict(list)
    for record in records:
        grouped[(record["profile"], record["duration_seconds"], record["controller"])].append(record)
    summaries = []
    for (profile, duration, controller), group in sorted(grouped.items()):
        summary = {
            "profile": profile,
            "duration_seconds": duration,
            "controller": controller,
            "runs": len(group),
        }
        for metric in (
            "final_queue_length", "maximum_queue_length", "accumulated_delay",
            "throughput_per_minute", "mean_queue_length", "fairness_index",
        ):
            values = [float(record[metric]) for record in group]
            summary[f"mean_{metric}"] = round(mean(values), 4)
            summary[f"stdev_{metric}"] = round(pstdev(values), 4)
        summaries.append(summary)

    summary_json = output_dir / "summary.json"
    summary_json.write_text(
        json.dumps(
            {
                "experiment": {
                    "seeds": list(seeds),
                    "durations": list(durations),
                    "profiles": [profile.value for profile in DemandProfile],
                    "controllers": list(CONTROLLERS),
                },
                "runs": records,
                "summaries": summaries,
            },
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )
    return {"raw_csv": str(raw_csv), "summary_json": str(summary_json), "runs": len(records)}


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate reproducible MATCS experiment artifacts")
    parser.add_argument("--output-dir", default="results/experiments")
    parser.add_argument("--seeds", nargs="+", type=int, default=list(DEFAULT_SEEDS))
    parser.add_argument("--durations", nargs="+", type=int, default=list(DEFAULT_DURATIONS))
    args = parser.parse_args()
    result = run_batch(Path(args.output_dir), tuple(args.seeds), tuple(args.durations))
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
