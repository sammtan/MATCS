# MATCS

## First simulation vertical slice

The repository currently contains a dependency-light, simulation-only first slice of MATCS. It models one four-approach intersection with seeded vehicle arrivals, a fixed-time signal controller, deterministic safety validation, a simulated actuator, and traffic metrics.

The implementation does not connect to real traffic-light equipment, the university crossing, external traffic APIs, MongoDB, or cloud services.

### Run the tests

From the repository root in PowerShell:

```powershell
$env:PYTHONPATH = "src"
python -m unittest discover -s tests -v
```

### Run the demo

```powershell
$env:PYTHONPATH = "src"
python -m mtacs --seed 42 --ticks 120
```

Compare the controllers under the same demand profile and seed:

```powershell
python -m mtacs --seed 42 --ticks 300 --scenario north_south_heavy --controller fixed_time
python -m mtacs --seed 42 --ticks 300 --scenario north_south_heavy --controller queue_aware
```

Available scenarios are `balanced`, `north_south_heavy`, `east_west_heavy`, and `stress`. Available controllers are `fixed_time` and `queue_aware`.

### Generate and review experiment evidence

Generate the standard 80-run evidence matrix:

```powershell
$env:PYTHONPATH = "src"
python scripts/run_experiments.py --output-dir results/experiments
```

Review `results/experiments/raw_runs.csv` for individual runs and `results/experiments/summary.json` for grouped means and population standard deviations. The interpretation and readiness decision are recorded in `docs/04-simulation-and-experiments.md`.

The seed makes the scenario reproducible. The output includes final signal phase, arrivals, departures, queue length, delay, stops, and throughput.

### First-slice boundaries

- The first controller is fixed-time, not an AI model.
- The actuator is simulated only.
- The field integration path is represented by future adapter interfaces.
- Authority approval is required before any real-world observation or integration.
