# MTACS AI and Controller Plan

> **Iterative updates rule:** Update this document when the controller type, agent boundaries, training method, inference location, safety wrapper, or evaluation method changes. Add a tagged change entry and preserve superseded decisions.
>
> **Document status:** Fixed-time and queue-aware baselines implemented; no AI model has been selected or trained.
>
> **Change tag:** `[CHANGELOG: PHASE-ONE DESIGN]`

## 1. Current decision

The first controller is fixed-time and deterministic. It is a baseline for architecture testing and later comparisons, not the final AI controller. In the real-world path, controller output begins as a shadow-mode recommendation and does not directly actuate the signal.

No model training or cloud inference is planned during the current Jira-preparation phase.

## 2. Controller progression

### Progression 0: Fixed-time controller

Uses a predefined safe phase sequence and durations. It establishes the simulator, data contract, actuation interface, metrics, and dashboard path.

### Progression 1: Queue-aware heuristic

Uses compact queue and waiting-time features to request safe extensions or phase changes. This tests whether traffic-responsive logic improves over fixed timing before machine learning is introduced.

The current implementation uses current queue counts, a minimum green duration, and a maximum green duration. It requests only the current phase or the next phase in the configured cycle. Directional-heavy and stress demand profiles are available for matched experiments. The heuristic is intentionally transparent and deterministic; it is not described as an AI model or as deployment-ready control logic.

### Progression 2: Optimization or learned policy

After repeatable baselines exist, evaluate a constrained optimizer, imitation-learning policy, or reinforcement-learning policy. The choice depends on simulator support, team capacity, and measured need for learning.

## 3. Multi-agent interpretation

Agents should represent responsibilities, not necessarily separate expensive deployments:

- observation/state adapter
- local intersection controller
- coordination module when multiple intersections exist
- deterministic safety validator
- evaluation/reporting module

For one intersection, these should be modules in one local process. Multi-agent coordination is only justified once multiple connected intersections create a measurable coordination problem.

## 4. Compact control state

Potential inputs include current phase, elapsed phase time, queue length by approach, waiting time, arrivals, departures, occupancy/speed where available, and priority flags. The input must use the current simulation timestamp and avoid future information.

Potential outputs are bounded abstract actions such as keeping the phase, extending it within limits, or requesting the next valid phase. The controller cannot output arbitrary hardware commands.

## 5. Safety and fallback

Every proposal passes through deterministic rules for phase conflicts, minimum green, yellow, all-red, maximum green, stale state, invalid identifiers, and command frequency. Rejected proposals use a safe fallback policy.

## 6. Real-world deployment boundary

The controller must support three modes:

1. **Simulation mode:** The proposal is validated and applied only to the simulator.
2. **Shadow mode:** Approved field observations are used to produce a recommendation; the existing signal remains in control.
3. **Supervised pilot:** Only if the authority supplies an approved interface, safety case, test window, rollback procedure, and responsible operator.

The controller must never infer electrical commands from a signal image or undocumented cabinet behavior.

## 7. Cost and deployment

Prefer local offline training and local inference. Do not use an LLM in the real-time control loop. An LLM may later assist with explanations, scenario descriptions, or report drafting, but its output must not directly actuate the simulator.

## 8. Evaluation gate

A learned controller cannot be accepted merely because it runs. It must be compared with fixed-time and heuristic baselines under matched scenarios and seeds, with traffic metrics, fairness, safety-validator interventions, runtime, and an emissions proxy where supported.

The same gate applies to the heuristic when evaluating it as a project result: use identical seeds and configurations, test multiple demand profiles and durations, preserve the fixed-time baseline, and report cases where the heuristic does not improve a metric. All conclusions remain simulation-bound until authority-approved observation and calibration are complete.

## 9. Change log

- `[CHANGELOG: PHASE-ONE DESIGN]` Established fixed-time as the first controller progression and deferred AI model selection/training.
- `[CHANGELOG: REAL-WORLD INTEGRATION]` Added simulation, shadow-mode, and authority-approved pilot modes; prohibited direct actuation from undocumented field observations.
- `[CHANGELOG: QUEUE-AWARE BASELINE]` Implemented a bounded queue-aware heuristic and expanded the evaluation gate to scaled matched experiments.
