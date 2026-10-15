# MTACS Simulation and Experiments

> **Iterative updates rule:** Update this document when the simulator, scenario model, timing, controller comparison, metrics, or reproducibility rules change. Add a tagged change entry and preserve the reason for changes.
>
> **Document status:** First-slice implementation and experiment protocol.
>
> **Change tag:** `[CHANGELOG: PHASE-ONE DESIGN]`

## 1. Simulator and digital-twin definition

The product is not selected yet. After an authority-approved observation phase, the simulator may be calibrated as a digital twin of the target crossing. The digital twin remains the safe environment for controller testing.

Before selection, compare candidates using:

- traffic-light and intersection support
- Python integration
- local execution and zero-cost suitability
- deterministic/reproducible runs
- ease of generating observations
- support for a later live demo
- documentation and team learning cost

## 2. First scenario

The first scenario should contain:

- one area
- one intersection
- defined approaches and lanes
- a small set of signal phases
- deterministic demand
- fixed simulation seed
- a known simulation duration
- no external traffic API dependency
- no direct signal-controller connection

The scenario should be simple enough to debug manually and rich enough to create queues and phase decisions.

## 3. Time model

The simulator should advance using a fixed simulation tick. The exact tick and controller decision interval will be selected with the simulator. The design requires that both are recorded in the experiment metadata.

The controller must not make decisions from future observations. Every action must be associated with the state available at its decision time.

## 4. First controller progression

The first controller progression is a fixed-time baseline:

- phases are configured in a known safe order
- each phase has configured green, yellow, and all-red durations
- the controller follows the schedule independent of traffic demand
- the safety validator still checks every transition

This is a reference controller, not the final AI. Later controllers must be evaluated against the same scenarios and seeds.

### Implemented queue-aware baseline

The queue-aware controller is the second executable baseline. It observes only the current queues and signal state. After the minimum green time, it requests the next safe phase when the opposing queue exceeds the currently served queue; it also yields at the configured maximum green time. It cannot skip yellow or all-red phases because every proposal is passed to the deterministic validator.

Demand profiles currently include:

- `balanced`: equal arrival probability on all approaches.
- `north_south_heavy`: increased north/south demand and reduced east/west demand.
- `east_west_heavy`: increased east/west demand and reduced north/south demand.
- `stress`: elevated demand on all approaches for queue-growth testing.

## 5. Later comparison sequence

1. Fixed-time baseline.
2. Queue-aware heuristic baseline.
3. Short-horizon optimization or learned policy.
4. Optional multi-agent coordination across intersections after expansion.

Do not compare controllers using different demand, seed, duration, or signal topology without documenting the difference.

## 6. Objectives and metrics

The primary objective is traffic optimization: delay, travel time, queue length, throughput, and stops. Emissions reduction is secondary and should use a simulator-supported fuel/emissions proxy if one becomes available.

Every comparison should report:

- mean and high-percentile delay/travel time
- mean and maximum queue length
- throughput
- stops
- fairness across approaches
- validator interventions and safety violations
- runtime/decision latency
- emissions or fuel proxy when available

## 7. Experiment record

Each run records scenario version, simulator version, seed, controller version, configuration, start/end simulation time, metrics, and result status. A run should be replayable from its configuration and seed.

## 8. Scaled comparison protocol

The initial automated experiment matrix uses:

| Dimension | Levels |
|---|---|
| Demand profile | balanced, north/south-heavy, east/west-heavy, stress |
| Duration | 30 seconds, 120 seconds, 600 seconds, plus a 1,200-second stress run |
| Controllers | fixed-time, queue-aware |
| Seeds | fixed seed per comparison, with additional seeds added before formal claims |

For a fair controller comparison, profile, seed, duration, timing plan, service rate, and topology must be identical. Report raw metrics and deltas for arrivals, departures, final and maximum queues, delay, stops, and throughput. A lower queue in one profile is not evidence of universal superiority; results should be interpreted by demand pattern and repeated across seeds.

The scaled tests are regression and reproducibility tests, not a substitute for statistical evaluation. Before making a performance claim, add a larger seed set, confidence intervals, and a documented scenario calibration process based on authority-approved observations.

## 9. Change log

- `[CHANGELOG: PHASE-ONE DESIGN]` Defined the simulator meaning, one-intersection scenario, fixed-time first controller, comparison sequence, and traffic-first metrics.
- `[CHANGELOG: REAL-WORLD INTEGRATION]` Extended the simulator role to a possible calibrated digital twin and prohibited direct signal-controller connection.
- `[CHANGELOG: QUEUE-AWARE BASELINE]` Added named demand profiles, matched fixed-time/queue-aware comparisons, scaled reproducibility tests, and limits on interpreting baseline results.
- `[CHANGELOG: EVIDENCE RUN]` Added richer per-approach metrics, an 80-run CSV/JSON batch experiment, evidence-based interpretation, and a phase-readiness decision.

## 10. Generated evidence and interpretation

The reproducible batch run is stored in:

- `results/experiments/raw_runs.csv`: one row for each profile, duration, seed, and controller combination.
- `results/experiments/summary.json`: experiment metadata, all raw records, and grouped means/population standard deviations.

The generated matrix contains 4 profiles x 2 durations x 5 seeds x 2 controllers = 80 runs. The 120-second grouped means below are the most useful short-horizon comparison because the 600-second runs approach a saturated steady state:

| Profile | Delay delta, queue-aware vs fixed | Mean-queue delta | Throughput delta/min | Fairness fixed -> queue-aware |
|---|---:|---:|---:|---:|
| Balanced | +1.84% | +1.83% | -1.40 | 0.9782 -> 0.9845 |
| North/south heavy | -1.33% | -1.33% | 0.00 | 0.9747 -> 0.9765 |
| East/west heavy | -5.77% | -5.77% | +1.60 | 0.9153 -> 0.9699 |
| Stress | +2.00% | +2.00% | -0.80 | 0.9931 -> 0.9960 |

Interpretation:

1. The queue-aware heuristic is promising for directional imbalance. The strongest observed result is the east/west-heavy 120-second case, where mean delay and mean queue decrease while throughput and fairness improve.
2. The heuristic is not universally better. Balanced and stress 120-second cases show slightly higher delay and queue length, despite small fairness improvements. This may reflect the deliberately simple phase-pressure rule and the short horizon.
3. At 600 seconds, differences are small in percentage terms for most profiles, while queues are larger under sustained demand. These runs demonstrate repeatability and saturation behavior, not deployment performance.
4. Validation interventions remained zero in the generated runs, which confirms that valid controller proposals stayed within the safety contract. It does not prove real-world safety.

## 11. Readiness decision

**Ready for the next software-engineering phase: controlled heuristic refinement and report/UML review.** The project has executable fixed-time and queue-aware baselines, reproducible artifacts, richer metrics, edge-case tests, and documented interpretation.

**Not ready for an AI claim, field calibration, or real-world actuation.** Before selecting a learned policy, the team should add more seeds, confidence intervals, explicit statistical tests, approach-level fairness analysis, and a calibrated demand model. The simulator remains synthetic and the actuator remains simulated.
