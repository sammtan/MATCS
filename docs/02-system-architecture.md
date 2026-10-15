# MTACS System Architecture

> **Iterative updates rule:** Update this document when components, interfaces, deployment boundaries, safety rules, or data flow change. Add a tagged change entry and preserve superseded decisions.
>
> **Document status:** Draft for phase-one design.
>
> **Change tag:** `[CHANGELOG: PHASE-ONE DESIGN]`

## 1. Architecture boundary

MTACS is a simulation-backed system with a future, authority-governed field-integration path. The simulated actuator remains the default development actuator. No API, agent, dashboard, or deployment may send commands to public traffic infrastructure without written authorization, an authority-supplied interface, a safety review, and an approved rollback procedure.

The first technical slice contains one area and one intersection. The first real-world slice is one pedestrian crossing and its associated signal near the university station and bus stop. All student components may run on one laptop during development.

## 2. Logical components

```text
Scenario/configuration
		|
		v
Traffic simulator ---- observations ----> Observation adapter <---- approved field data
		^                                      |
		|                                      v
 Simulated actuator <---- safe action ---- Safety validator ---- authority review package
		^                                      ^
		|                                      |
		+---- signal state <---- Controller proposal
											   ^
											   |
									Feature/state builder
											   |
									  MongoDB and event log
											   |
											   v
									  Dashboard/read API
```

### Components

- **Scenario manager:** Loads area topology, signal phases, demand, seed, and experiment settings.
- **Traffic simulator:** Advances the modeled world and produces vehicle/signal observations.
- **Observation adapter:** Converts simulator output or approved field data to the internal observation contract.
- **State builder:** Creates a consistent snapshot for a simulation time.
- **Feature builder:** Produces compact numerical controller input.
- **Controller:** Initially fixed-time; later heuristic, optimization, or learned policy.
- **Safety validator:** Deterministically checks phase conflicts, minimum durations, yellow/all-red transitions, and command validity.
- **Simulated actuator:** Applies only validated commands to the simulator.
- **Field integration adapter:** Handles only approved, documented field telemetry. It is read-only during the initial real-world phase.
- **Authority gateway:** A future authority-controlled boundary for any approved pilot; it is not implemented or assumed to exist.
- **Event/metrics store:** Persists replayable events and experiment summaries.
- **Dashboard/read API:** Shows state, signal phase, decisions, and metrics without direct database credentials in the browser.

## 3. Closed-loop sequence

1. Load a versioned scenario and random seed.
2. Advance the simulator by one tick.
3. Convert observations to the internal schema.
4. Build the current state snapshot.
5. Invoke the controller at its decision interval.
6. Validate the proposed action.
7. Apply the safe action to the simulated actuator.
8. Continue simulation and record feedback.
9. Aggregate traffic and environmental-proxy metrics.
10. Expose the current state and results to the dashboard.

For field observation, the adapter adds site identity, source, observation quality, and approval metadata. Field data enters the normalized state model; it does not bypass validation or grant actuation permission.

## 4. Deployment stages

### Local development

All components run on the laptop. MongoDB may run locally or use an approved free tier. No cloud AI endpoint is required.

### Public live demonstration

The eventual public demo should expose a controlled simulation session, calibrated digital twin, or shadow-mode recommendation view through Vercel and a minimal backend/runtime. It must clearly identify simulated, observed, and recommended values. It must not send commands to the real signal.

### Authority-approved field pilot

Only after written approval and a documented safety process may an authority-controlled gateway be considered. The team must not connect directly to a cabinet, controller, pedestrian button, relay, or public network.

### Real-world deployment

Not part of this project. Any real deployment would require government authorization, certified safety engineering, operational redundancy, hardware integration, and a separate governance process.

## 5. Safety boundary

The controller can propose an abstract action such as `NEXT_PHASE` or `EXTEND_CURRENT_PHASE`. The safety validator translates it into an allowed simulator command or a recommendation for authority review. Invalid, stale, conflicting, or unavailable decisions use a safe fallback policy.

The dashboard is read-oriented. It may allow a demo user to select a scenario, but it must not expose arbitrary signal commands.

## 6. Change log

- `[CHANGELOG: PHASE-ONE DESIGN]` Defined the one-intersection logical architecture and live-demo boundary.
