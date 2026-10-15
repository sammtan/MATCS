# MTACS UML Models

> **Status:** First executable vertical slice; diagrams are maintained as Mermaid source so the team can render them in Markdown-compatible tools.
>
> **Assumption:** The five lecturer-required fundamentals are use-case, class, sequence, activity, and state-machine diagrams. Component and deployment views are included as supplementary architecture diagrams.

## 1. Use-case diagram — required fundamental

```mermaid
flowchart LR
	Student[Student developer]
	Authority[Authority / site stakeholder]
	Reviewer[Lecturer / reviewer]
	Simulator((Run simulation))
	Compare((Compare controllers))
	Inspect((Inspect metrics and replay metadata))
	Review((Review safety boundary))
	Observe((Approve field observation scope))

	Student --> Simulator
	Student --> Compare
	Student --> Inspect
	Reviewer --> Inspect
	Reviewer --> Review
	Authority --> Observe
	Student --> Observe
	Compare -. includes .-> Simulator
	Inspect -. includes .-> Simulator
```

The authority actor can approve or constrain observation scope, but cannot be treated as an implicit authorization to actuate public infrastructure.

## 2. Class diagram — required fundamental

```mermaid
classDiagram
	class ScenarioConfig {
		+int seed
		+int duration_seconds
		+float arrival_probability
		+int service_rate
		+DemandProfile demand_profile
		+TimingPlan timing
	}
	class DemandProfile {
		<<enumeration>>
		BALANCED
		NORTH_SOUTH_HEAVY
		EAST_WEST_HEAVY
		STRESS
		+probabilities(base_probability)
	}
	class TimingPlan {
		+int green_seconds
		+int yellow_seconds
		+int all_red_seconds
		+int max_green_seconds
	}
	class SimulationState {
		+int simulation_time
		+SignalState signal
		+dict queues
		+int arrivals
		+int departures
		+int stops
		+int accumulated_delay
	}
	class SignalState {
		+SignalPhase phase
		+int elapsed_seconds
	}
	class ControllerProposal {
		+int simulation_time
		+SignalPhase requested_phase
		+str controller_name
		+str controller_version
	}
	class FixedTimeController {
		+propose(state) ControllerProposal
	}
	class QueueAwareController {
		+propose(state) ControllerProposal
	}
	class SafetyValidator {
		+validate(state, proposal) ValidationResult
	}
	class SimulatedActuator {
		+apply(state, phase)
	}
	class TrafficSimulator {
		+run()
		+step()
	}
	class RunMetrics {
		+int total_arrivals
		+int total_departures
		+int final_queue_length
		+int maximum_queue_length
		+int accumulated_delay
		+float throughput_per_minute
	}

	ScenarioConfig *-- TimingPlan
	ScenarioConfig --> DemandProfile
	SimulationState *-- SignalState
	FixedTimeController --> TimingPlan
	QueueAwareController --> TimingPlan
	FixedTimeController ..> ControllerProposal : creates
	QueueAwareController ..> ControllerProposal : creates
	TrafficSimulator --> ScenarioConfig
	TrafficSimulator --> SimulationState
	TrafficSimulator --> FixedTimeController : selects
	TrafficSimulator --> QueueAwareController : selects
	TrafficSimulator --> SafetyValidator
	TrafficSimulator --> SimulatedActuator
	TrafficSimulator ..> RunMetrics : produces
```

## 3. Sequence diagram — required fundamental

```mermaid
sequenceDiagram
	participant CLI
	participant Simulator as TrafficSimulator
	participant Controller as FixedTime or QueueAware
	participant Validator as SafetyValidator
	participant Actuator as SimulatedActuator
	participant Metrics as MetricsCollector

	CLI->>Simulator: run(config, controller)
	loop each simulation tick
		Simulator->>Simulator: generate arrivals from seeded profile
		Simulator->>Controller: propose(current state)
		Controller-->>Simulator: ControllerProposal
		Simulator->>Validator: validate(state, proposal)
		Validator-->>Simulator: ValidationResult
		alt proposal accepted
			Simulator->>Actuator: apply(state, validated phase)
		else proposal rejected
			Simulator->>Simulator: retain safe current phase
		end
		Simulator->>Simulator: move vehicles and accumulate delay
		Simulator->>Metrics: observe(state)
		Simulator->>Simulator: advance simulation time
	end
	Simulator-->>CLI: final state and RunMetrics
```

## 4. Activity diagram — required fundamental

```mermaid
flowchart TD
	Start([Start run]) --> Configure[Load seed, timing, demand profile, controller]
	Configure --> Init[Initialize state and metrics]
	Init --> Tick{Duration reached?}
	Tick -- No --> Arrivals[Generate seeded arrivals]
	Arrivals --> Propose[Controller proposes abstract phase]
	Propose --> Validate{Safety validation accepted?}
	Validate -- Yes --> Apply[Apply phase to simulated actuator]
	Validate -- No --> Fallback[Keep current safe phase]
	Apply --> Move[Move vehicles on green approaches]
	Fallback --> Move
	Move --> Measure[Accumulate delay and observe metrics]
	Measure --> Advance[Advance simulation tick]
	Advance --> Tick
	Tick -- Yes --> Report[Finalize reproducible metrics]
	Report --> End([End run])
```

## 5. State-machine diagram — required fundamental

```mermaid
stateDiagram-v2
	[*] --> NorthSouthGreen
	NorthSouthGreen --> NorthSouthYellow: minimum green reached
	NorthSouthYellow --> AllRedToEastWest: yellow duration reached
	AllRedToEastWest --> EastWestGreen: all-red duration reached
	EastWestGreen --> EastWestYellow: minimum green and queue policy / maximum reached
	EastWestYellow --> AllRedToNorthSouth: yellow duration reached
	AllRedToNorthSouth --> NorthSouthGreen: all-red duration reached

	NorthSouthGreen --> NorthSouthGreen: keep phase
	EastWestGreen --> EastWestGreen: keep phase
	NorthSouthYellow --> NorthSouthYellow: keep phase
	EastWestYellow --> EastWestYellow: keep phase
	AllRedToEastWest --> AllRedToEastWest: keep phase
	AllRedToNorthSouth --> AllRedToNorthSouth: keep phase
```

The controller can propose only the current state or the next state. The validator rejects stale proposals and skipped transitions.

## 6. Component diagram — supplementary

```mermaid
flowchart LR
	Demand[Demand profile generator]
	Observation[Observation adapter]
	State[Simulation state]
	Controller[Controller strategy\nfixed-time / queue-aware]
	Safety[Deterministic safety validator]
	Actuator[Simulated actuator]
	Metrics[Metrics collector]
	CLI[Local CLI]
	Field[Future authority-approved\nfield observation adapter]
	Gateway[Future authority gateway]

	Demand --> Observation
	Field -. authority approval required .-> Observation
	Observation --> State
	State --> Controller
	Controller --> Safety
	Safety --> Actuator
	Actuator --> State
	State --> Metrics
	CLI --> Controller
	CLI --> Demand
	Gateway -. future supervised boundary .-> Actuator
```

## 7. Deployment diagram — supplementary

```mermaid
flowchart TB
	Developer[Developer laptop]
	Python[Local Python process]
	Simulator[TrafficSimulator]
	Tests[unittest suite]
	Docs[Version-controlled documentation]
	Authority[University / local authority environment]
	ApprovedData[Approved observation data]
	PublicInfra[Public signal infrastructure]

	Developer --> Python
	Python --> Simulator
	Developer --> Tests
	Developer --> Docs
	Authority --> ApprovedData
	ApprovedData -. future controlled input .-> Python
	Python -. no current connection .-> PublicInfra
```

## 8. Review checklist

- Confirm the five required fundamentals against the lecturer’s exact terminology before submission.
- Keep controller proposals abstract and route every proposal through deterministic validation.
- Label field observation, shadow mode, and supervised pilot as future authority-gated stages.
- Update diagrams when the simulator, controller contract, or authority integration boundary changes.
