# Assistive Records

> **Role of this file:** This file is the persistent memory and design record for the MTACS project and for future communication about it. It records agreed decisions, assumptions, open questions, rationale, and next actions so that later conversations can continue from the same context.
>
> **Iterative updates rule:** Update this file whenever a project decision, requirement, architecture assumption, technology choice, risk, or next action changes. Add new dated entries rather than silently rewriting history. Mark superseded decisions as superseded and preserve the reason for the change.

- **Project:** MTACS — Multi-Agentic Traffic Control System
- **Context:** Software Engineering class group project
- **Domain:** Nature/environment-aware urban mobility and agentic AI
- **Country context:** Indonesia
- **Current phase:** First technical vertical slice implemented and validated; documentation and authority discovery remain in progress
- **Last updated:** 2026-10-15
- **Decision status:** Records, technology stack, and documentation plan accepted; Jira details remain provisional

## 1. Executive design position

MTACS is a software-only, simulation-first traffic-control research and engineering project. It should model an area containing intersections, traffic lights, roads, vehicles, traffic demand, and environmental conditions; ingest or synthesize observations; recommend signal decisions; validate those decisions against safety rules; and apply them only inside the simulator.

The project should not connect to, or attempt to control, public Indonesian traffic lights. Public-infrastructure control is safety-critical, legally controlled, and outside the scope of a student software project. The system may imitate the interfaces that a real deployment would use, but its actuator must be a simulated actuator.

The design is good as a closed-loop concept, but it needs stricter separation between:

### Implementation status — 2026-10-15

The first executable slice now exists under `src/mtacs`. It includes a standard-library-only one-intersection simulator, seeded arrivals, fixed-time signal control, deterministic phase-transition validation, simulated actuation, and reproducible metrics. Five unit tests pass, and the CLI demo runs locally. The current implementation intentionally does not connect to field hardware, authority systems, external traffic services, MongoDB, or Vercel.

1. **Observation:** What is measured or generated about vehicles, roads, signals, weather, and incidents.
2. **State:** The trusted, timestamped representation of the area at a particular simulation time.
3. **Decision:** A proposed signal plan or phase adjustment.
4. **Safety validation:** A deterministic layer that rejects unsafe or invalid decisions.
5. **Actuation:** Applying the validated decision to the simulator.
6. **Evaluation:** Measuring travel time, queue length, throughput, stops, emissions proxy, fairness, and safety violations.

An AI model must never be the only safety boundary. The deterministic safety validator remains in control of allowed actions.

## 2. Target system boundary

### In scope for the first release

- One simulated area containing one intersection as the first vertical slice.
- Configurable traffic-light points, road topology, lanes, phases, timings, and constraints.
- Synthetic or simulator-generated vehicle observations.
- A central computer process that runs locally on a laptop.
- MongoDB for configuration, current state snapshots, events, decisions, and experiment metadata.
- A web dashboard deployed to Vercel for visualization and experiment inspection.
- A controller that starts as a deterministic baseline and later gains an AI policy.
- Reproducible experiments with fixed random seeds and recorded configurations.
- Simulated actuation only.

The one-intersection scope is not the final limitation of MTACS. It is the smallest useful area that can demonstrate the full loop: vehicles create demand, a signal controller changes phases, the simulator advances, and metrics measure the result. Multiple intersections can be added after the single-intersection loop is reproducible.

### Explicitly out of scope initially

- Direct access to real traffic-light hardware.
- Automatic control of public roads.
- A production claim that the controller is safe for deployment.
- Dependence on Google traffic data for the system to work.
- A large language model issuing raw traffic-light commands.
- One cloud deployment per traffic light.
- Training a complex model before a working baseline and evaluation harness exist.

## 3. Conceptual architecture

```text
Traffic demand / simulator / optional external context
					|
					v
		Observation and ingestion adapter
					|
					v
	 State builder and timestamped state store
					|
					v
	   Feature builder / compact control state
					|
					v
   Controller or agent coordinator proposes action
					|
					v
 Deterministic safety, legality, and constraint validator
					|
		   +--------+--------+
		   |                 |
	   accepted          rejected/modified
		   |                 |
		   v                 v
 Simulated signal       Safe fallback policy
 actuator                and event log
		   |
		   v
 Simulator advances and produces feedback
		   |
		   +-----------> metrics, dashboard, training data
```

The phrase “multi-agent” should describe independent responsibilities, not necessarily many copies of a large model. A practical first decomposition is:

- **Observation agent/adapter:** Converts simulator or external observations into a common schema.
- **State agent:** Maintains the current area state and detects stale or contradictory data.
- **Intersection controller agents:** Propose actions for individual intersections using local state and selected neighboring summaries.
- **Coordination agent:** Resolves conflicts and coordinates adjacent intersections or corridors.
- **Safety validator:** Deterministic software, not a free-form AI agent; enforces minimum green, yellow, all-red, pedestrian, conflict, and command-rate constraints.
- **Evaluation agent:** Computes metrics and compares the AI policy with baselines.

These may initially be modules in one local process. They do not need separate cloud deployments. Deployment boundaries should only be introduced when independent scaling, ownership, or failure isolation is demonstrated.

## 4. Closed-loop operation

A simulation tick is the project's definition of “present.” For example, the simulator may advance in one-second ticks while the controller makes decisions every five or ten seconds. Each observation should have:

- `areaId`
- `intersectionId` when applicable
- `simulationTime`
- `observedAt`
- source and schema version
- vehicle counts, queue estimates, speed, occupancy, and signal phase
- quality/staleness information

A recommended loop is:

1. The simulator advances to the next tick.
2. It publishes observations to the local central process.
3. The state builder creates a consistent snapshot for one simulation time.
4. The feature builder creates a compact controller input.
5. Controller agents propose actions.
6. The coordinator resolves multi-intersection conflicts.
7. The safety validator accepts, modifies, or rejects the proposal.
8. The simulated actuator applies the safe action.
9. The simulator advances using the result.
10. Metrics and events are persisted for replay and comparison.

The system should use an event identifier and simulation timestamp to make updates idempotent and replayable. A real-world HTTPS update pattern can be represented by an adapter, but internal simulation communication should not require an internet round trip for every traffic-light color change.

## 5. Role of external traffic data

External traffic data and simulated traffic-light data are not interchangeable.

- **Traffic-light state** answers: “What phase is the controller showing now?”
- **Vehicle/traffic state** answers: “How many vehicles are present, how fast are they moving, and where are queues forming?”
- **External traffic context** answers: “What broader demand or congestion pattern may be entering this area, including conditions outside the simulated boundary?”

If a traffic simulator already generates vehicles and queues, Google or another external traffic service is not required for the control loop. It can be used as optional calibration or scenario context, for example:

- Estimating typical demand by time of day.
- Comparing a simulated corridor's congestion pattern with an observed congestion category.
- Supplying boundary demand changes for an incident or event scenario.
- Providing a baseline for a report, if the API's terms, coverage, quota, and cost allow it.

Do not treat a Google traffic API as a guaranteed real-time traffic-light API. Traffic services commonly provide routing, travel-time, speed, or congestion information rather than authoritative public signal-phase data. Verify current API products, Indonesian coverage, terms, quota, and billing before integration. The project must continue to work from generated scenarios if no suitable public source exists.

The cleanest first experiment is to run three data conditions:

1. **Synthetic only:** simulator generates demand and signal observations.
2. **Calibrated synthetic:** demand parameters are adjusted using permitted aggregate external traffic context.
3. **External-context scenario:** external data changes boundary demand, while the simulator remains the source of truth for vehicle and signal state.

This makes the external data's value measurable instead of adding it merely because it is available.

## 6. Simulation recommendation

Use a traffic microsimulator or a small custom discrete-event simulator. A traffic microsimulator is preferable if the team can learn it quickly because it provides vehicle movement, queues, lanes, intersections, and signal timing. A custom simulator is acceptable for the first vertical slice if the class focuses more on software architecture than traffic science.

Recommended progression:

- **Phase A:** One intersection, deterministic demand, fixed-time baseline.
- **Phase B:** Multiple intersections, variable demand, actuated baseline.
- **Phase C:** Incidents, uneven demand, weather/environmental scenarios, and neighboring intersections.
- **Phase D:** Controller comparison, replay, sensitivity analysis, and ablation experiments.

Every experiment should record the scenario, seed, controller version, traffic-light configuration, simulator version, and metrics. A minimum comparison must include fixed-time control and a simple queue-aware heuristic. An AI controller is only useful if it beats or meaningfully complements those baselines under repeatable scenarios.

Useful metrics:

- Average and 95th-percentile travel time.
- Average and maximum queue length.
- Throughput and delay.
- Number of stops.
- Emergency-vehicle or priority delay, if modeled.
- Fairness across approaches, so one direction is not starved.
- Estimated fuel/emissions proxy, if supported by the simulator.
- Safety-validator interventions and invalid proposals.
- Compute time and decision latency.

## 7. AI and agent strategy

Do not begin by training an LLM or building a model from scratch. Raw traffic-light control is a numerical sequential-decision problem, not primarily a language problem. LLM calls add token cost, latency, nondeterminism, and a difficult safety case.

Recommended controller progression:

1. **Fixed-time baseline:** Known phase schedule.
2. **Rule-based baseline:** Extend or shorten phases using queue thresholds while obeying constraints.
3. **Optimization baseline:** Select a safe phase plan that minimizes weighted queue and delay over a short horizon.
4. **Learning controller:** Consider reinforcement learning or imitation learning after the simulator, state representation, reward, safety wrapper, and evaluation harness are stable.
5. **Optional LLM assistant:** Use only for explanations, scenario generation, experiment planning, or operator-facing summaries; never for unconstrained raw actuation.

For a group project, the wisest first AI option is a lightweight learned policy or reinforcement-learning policy trained offline in simulation, wrapped by the deterministic safety validator. Candidate approaches include a discrete-action policy for phase selection, multi-agent reinforcement learning for neighboring intersections, or a centralized policy with decentralized execution. Start with one controller and only split it into multiple agents when the experiment demonstrates a coordination benefit.

The model input should be compact and numerical: queue lengths, occupancy, speeds, current phase, elapsed phase time, neighbor summaries, demand trend, and priority flags. The model output should be a small bounded action such as “extend current phase by N seconds,” “select next valid phase,” or “request a safe plan.” It should not output arbitrary electrical commands.

Training should be offline and reproducible. The runtime controller should load a versioned model artifact and perform inference locally when possible. This minimizes HTTPS traffic, cloud spending, and dependency on an always-on model endpoint. If cloud inference is later demonstrated to be necessary, use a single small service or an on-demand job rather than one deployment per intersection.

## 8. Proposed technology stack

### Required or preferred choices

- **Language:** Python for simulation, data generation, model training, and controller experimentation; TypeScript/React for the web dashboard if the team chooses a web frontend.
- **Database:** MongoDB for operational documents, configuration, snapshots, events, decisions, and experiment metadata. Use TTL indexes for disposable high-frequency data and retain summarized runs for analysis.
- **Frontend hosting:** Vercel free tier for the dashboard and documentation-style public view. The frontend should not expose MongoDB credentials.
- **Central computer:** Laptop-first local Python process. Treat a cloud machine as optional, not required.
- **API:** A small HTTP API for dashboard and control adapters, with authentication and schema validation even in development.
- **Validation:** Automated tests for state transitions, safety constraints, idempotency, and metric calculations.
- **Experiment storage:** MongoDB for metadata/results and local versioned files for model artifacts initially. Avoid adding a paid data warehouse.
- **Version control:** GitHub with pull requests and protected `prod` branch when available.
- **Project management:** Jira for backlog, sprint planning, acceptance criteria, linked pull requests, defects, and weekly class deliverables.

### Python's role

Python belongs in the core of this project because it has strong simulator, scientific-computing, optimization, reinforcement-learning, and data-analysis support. It should not be added only for the sake of using AI. It is the natural language for the central simulator/controller service and offline experiments. The dashboard can use TypeScript if the team wants a responsive browser interface.

### Cost policy

The default deployment should cost zero:

- Run simulation, controller, and training locally.
- Use MongoDB Atlas free tier only if its limits and educational account terms are acceptable; otherwise run MongoDB locally for development.
- Use Vercel's free tier within its limits.
- Avoid an always-on cloud VM, managed Kubernetes, paid model APIs, and per-request LLM calls.
- Check current free-tier, student, and educational-license terms before committing them to the report.
- Keep external traffic APIs optional because quota and billing policies can change.

## 9. Branch and environment model

The proposed branch names are usable, but their responsibilities need to be explicit:

- **`dev`:** Main integration branch for the platform, schemas, dashboard, API, simulator interfaces, and baseline controller. It should remain runnable without external traffic data or cloud AI.
- **`devsim`:** Simulation-focused work and experiments. It should contain scenario definitions, simulator adapters, training/evaluation scripts, and simulation-only changes. Changes intended for shared platform behavior should be merged back into `dev` through pull requests.
- **`prod`:** Stable demonstration/public branch. Only reviewed, tested, documented changes should enter it. It should not imply real-world traffic-control production; call it the public demo/release environment in documentation.

A possible later refinement is to use short-lived feature branches from `dev` and reserve the three named branches for environments. Do not duplicate the entire application across branches. Configuration should select local simulation, demo, or public-safe behavior, and production must keep the simulated actuator enabled.

## 10. Jira setup aligned with coursework

Create a Jira project using a Scrum or Kanban template, depending on the class requirement. Recommended issue hierarchy:

- **Epics:** Architecture and platform, simulation, data pipeline, controller/AI, dashboard, testing/evaluation, documentation/report, deployment/demo.
- **Stories:** User-observable capabilities with acceptance criteria.
- **Tasks:** Technical work that supports a story.
- **Bugs:** Reproducible defects with scenario, expected result, actual result, and evidence.
- **Spikes:** Time-boxed research such as checking traffic API availability, comparing simulators, or evaluating a model approach.

Suggested initial stories:

1. Define one-intersection simulation scope and success metrics.
2. Record traffic-light, road, vehicle, and observation schemas.
3. Build a deterministic fixed-time baseline.
4. Implement a queue-aware heuristic baseline.
5. Persist replayable simulation events and experiment metadata.
6. Display current simulation state and metrics in the dashboard.
7. Compare controller performance across repeatable scenarios.
8. Document safety boundaries and public-data limitations.

Each issue should include: purpose, scope, acceptance criteria, dependencies, owner, estimate, test evidence, and documentation impact. Use labels such as `architecture`, `simulation`, `ai`, `data`, `frontend`, `research`, `documentation`, and `class-week-N`. Create one spike before integrating any external traffic API.

## 11. Documentation plan

Recommended files, each with the same iterative-update rule at the top:

- `README.md` — project overview, quick start, scope, and links.
- `docs/01-project-charter.md` — problem, stakeholders, goals, non-goals, risks, and success criteria.
- `docs/02-system-architecture.md` — components, data flow, boundaries, and deployment model.
- `docs/03-data-contracts.md` — schemas, timestamps, event identity, validation, and retention.
- `docs/04-simulation-and-experiments.md` — scenarios, seeds, baselines, metrics, and reproducibility.
- `docs/05-ai-controller.md` — controller progression, model decisions, training, inference, and safety wrapper.
- `docs/06-technology-and-cost.md` — stack, free-tier assumptions, and cost controls.
- `docs/07-operations-and-security.md` — secrets, access, logging, failure handling, and demo deployment.
- `docs/08-jira-delivery-plan.md` — epics, milestones, class-week mapping, and Definition of Done.
- `docs/09-report-outline.md` — final report structure and evidence to collect.
- `docs/decisions/` — dated architecture decision records for important changes.

This file is the immediate design memory. The individual documentation files can be created incrementally as the team implements each area.

## 12. Main risks and mitigations

| Risk | Mitigation |
|---|---|
| Model makes unsafe or invalid decisions | Deterministic safety validator and safe fallback controller |
| External traffic API is unavailable or expensive | Synthetic/local data path is the default |
| Multi-agent architecture becomes unnecessary complexity | Start modularly; require an experiment to justify distributed agents |
| MongoDB receives excessive high-frequency writes | Local event buffering, aggregation, TTL indexes, and summarized runs |
| Team trains a model without a meaningful baseline | Implement fixed-time and heuristic baselines first |
| Cloud costs exceed the budget | Laptop-first execution, no always-on cloud inference, free tiers only |
| Results cannot be reproduced | Fixed seeds, versioned scenario/config/model metadata, replayable events |
| Public demo is mistaken for real traffic control | Clearly label it as simulation-only and keep actuators simulated |
| Data privacy or API terms are misunderstood | Use aggregate/permitted data only and document provider terms and limitations |

## 13. Proposed first milestone

**Milestone 0 — Design and Jira foundation**

- Agree on the one-area, one-to-three-intersection scope.
- Create the Jira project, epics, first spikes, and class-week labels.
- Confirm `dev`, `devsim`, and `prod` responsibilities.
- Record success metrics and the simulation-only safety boundary.
- Decide whether to use an existing traffic simulator or a deliberately small custom simulator.
- Verify MongoDB and Vercel free-tier eligibility before relying on them.
- Do not integrate Google traffic data or train an AI model in this milestone.

**Milestone 1 — Reproducible baseline**

- Produce one deterministic scenario.
- Simulate signal phases and vehicle demand.
- Run a fixed-time controller.
- Store/replay observations and metrics.
- Show the state in a local dashboard or simple report.

Only after Milestone 1 is repeatable should the team implement a learned controller or external-data adapter.

## 14. Open questions for the team

1. Which simulator, if any, is permitted by the class and manageable by the team?
2. Does the instructor require Scrum, Kanban, sprint reports, or specific Jira artifacts?
3. Which team members will own backend/data, simulation/AI, frontend, testing, and documentation?
4. What external data is legally and financially available for calibration, if any?
5. Which emissions or fuel-consumption proxy is credible and supported by the selected simulator?

## 15. Clarified decisions [CHANGELOG: USER CLARIFICATION]

### Simulator meaning [CHANGELOG: USER CLARIFICATION]

In this project, a **simulator** means software that represents the traffic world and advances it through time. It should model at least roads or approaches, vehicles or vehicle demand, queues, traffic-light phases, signal timing, and the effects of a controller's actions. The simulator is not a real traffic-light monitoring service and does not need real hardware access.

The simulator may eventually be an existing traffic-simulation package or a small custom discrete-event simulator. The product choice remains undecided. Selection must be based on traffic-light control support, Python integration, reproducibility, ease of local execution, live-demo compatibility, documentation, and zero-cost suitability.

### Initial intersection count [CHANGELOG: USER CLARIFICATION]

The first implementation target is one intersection. A later area may contain multiple connected intersections, but that expansion should happen only after the one-intersection closed loop and fixed-time baseline work reliably. This avoids confusing system-scale complexity with controller correctness.

### Environmental objective [CHANGELOG: USER CLARIFICATION]

The primary objective is to optimize traffic flow as much as possible, measured through delay, travel time, queue length, throughput, and stops. Reducing emissions is a secondary objective or penalty when the simulator supports a credible emissions or fuel-consumption proxy. The controller must not improve traffic metrics by starving one approach or violating safety constraints.

### Jira requirements and team [CHANGELOG: USER CLARIFICATION]

The Jira workflow and required artifacts are not yet known. The current Jira design is therefore provisional and will be revised after the second-assignment details are provided. The team consists of three students; individual ownership will be assigned later.

### Public demonstration [CHANGELOG: USER CLARIFICATION]

The final demonstration is expected to be live later in the course, probably near the final exam. A recorded or replay-only experiment is not sufficient as the final presentation. The live demonstration will still be a public-facing simulation demo and must never control real traffic infrastructure.

### External data [CHANGELOG: USER CLARIFICATION]

No external traffic-data source has been confirmed. External data is not a current dependency. An investigation spike may later evaluate availability, Indonesian coverage, terms, quota, cost, and usefulness; synthetic or simulator-generated data remains the required fallback.

### Current execution decision [CHANGELOG: USER CLARIFICATION]

The first phase is documentation and Jira preparation for Milestone 0. The first controller progression is the specification of a fixed-time controller baseline, not AI training or production code. Toolchain and environment setup will happen only after the Jira assignment and the simulator choice are sufficiently defined.

## 16. Change log

- **Initial design record:** Established simulation-only scope, safety validator, laptop-first execution, optional external traffic data, staged controller strategy, branch responsibilities, Jira structure, and documentation plan.
- **User clarification:** Clarified simulator meaning, selected one intersection for the first vertical slice, prioritized traffic optimization with emissions reduction as a secondary objective, deferred Jira requirements and team ownership, confirmed a future live public simulation demo, and deferred external-data selection.

## 17. Project-management assignment guidance [CHANGELOG: LECTURER SLIDE REVIEW]

The lecturer's slide screenshots emphasize a lightweight but disciplined software project-management process:

- Understand project content, scope, and timeframe.
- Identify the development process, methods, tools, languages, documentation, and support.
- Define the organizational structure and participant responsibilities.
- Develop a schedule with milestones and an initial minimal capability.
- Develop a staffing/ownership plan.
- Identify, prioritize, and continuously retire or mitigate risks.
- Identify documents to be produced.
- Conduct structured meetings with agendas, time allocation, action items, decisions, and progress review.
- Consider build-versus-buy and technology-selection tradeoffs.

The slides also present formal concepts such as SPMP, SCMP, SQAP, SRS, SDD, testing plans, hierarchical/peer/matrix organizations, risk likelihood-impact-retirement-cost prioritization, and fixed-delivery scheduling. MTACS should apply the underlying practices at a student-project scale rather than reproduce every corporate artifact.

## 18. Provisional board recommendation [CHANGELOG: LECTURER SLIDE REVIEW]

Use **Trello for the class project-management assignment**, unless the instructor explicitly requires Jira. Trello is sufficient for a three-student team because the immediate need is visible scope, ownership, schedule, risks, decisions, and action items—not enterprise-scale workflow, reporting, or issue traceability.

Use **GitHub Issues/Projects or a simple link from Trello cards** for implementation traceability later. Do not maintain both Jira and Trello as equal sources of truth. If the lecturer requires Jira terminology or artifacts, use Jira with a deliberately minimal project configuration instead of adopting its advanced features.

### Proposed Trello workspace

Board name: `MTACS — Project Management`

Lists:

1. `Project Charter / Scope`
2. `Backlog / Not Started`
3. `This Week`
4. `In Progress`
5. `Review / Waiting`
6. `Done`
7. `Risks & Retirement`
8. `Decisions & Meeting Actions`

Card conventions:

- Each work card has an owner, target date, objective, acceptance/evidence criteria, dependencies, and linked document.
- Use labels for `Planning`, `Simulation`, `Data`, `Controller`, `Dashboard`, `Documentation`, `Risk`, and `Class Assignment`.
- Use checklists for subtasks rather than creating excessive cards.
- Use a card template for meeting notes and a separate template for risks.
- Attach or link the relevant repository document, branch, pull request, or report section.

### Required board content for the assignment

- Project scope and non-goals.
- Three-student team and provisional responsibilities.
- Milestones and class-week dates.
- Technology-selection and simulator-selection tasks.
- Risk register with likelihood, impact, retirement/mitigation plan, responsible person, and target date.
- Document list and responsible owner.
- Meeting agenda, decisions, and action items.
- Initial minimal capability: one intersection, deterministic demand, and fixed-time controller specification.

## 19. Jira alternative [CHANGELOG: LECTURER SLIDE REVIEW]

Choose Jira instead if the assignment explicitly requires Jira, issue IDs, Scrum/Kanban reports, traceability, or formal workflow evidence. Keep it minimal:

- One project.
- One backlog.
- Epics only for major deliverables.
- Tasks, stories, spikes, and bugs only when needed.
- A simple workflow: `To Do → In Progress → Review → Done`.
- Labels for class week and work area.
- A risk register and decision log as linked issues or project pages.
- No complex automation, dashboards, components, releases, or multi-project hierarchy unless required.

## 20. Recommended setup sequence [CHANGELOG: LECTURER SLIDE REVIEW]

1. Read the assignment rubric and identify mandatory tool/artifact requirements.
2. Rework the team report to match the required project-management evidence.
3. Agree on Trello or Jira as the single project-management source of truth.
4. Add the three team members and provisional responsibilities.
5. Add scope, milestones, documents, risks, technology decisions, and meeting templates.
6. Create the initial minimal-capability cards and assign target dates.
7. Review the board weekly: schedule progress, risks, decisions, action items, and newly perceived risks.
8. Only after this board is accepted should the team execute Milestone 0 and establish the development toolchain.

## 21. Project-management execution status [CHANGELOG: REPORT REWORK AND ASSIGNMENT EXECUTION]

The team report was provided and analyzed. `Team Class Report & Documentation.md` was created with the reworked Chapter 1, the project-management assignment content, and the Trello setup/invitation procedure. The Trello-first proposal is now the adopted execution plan, subject to revision if the lecturer's rubric explicitly requires Jira.

The external Trello board has not been created because it requires the team's accounts and the user's account session. The next execution action outside the repository is to create the board, invite the three team members, assign responsibilities, and add the first cards described in the team document.

## 22. Changelog [CHANGELOG: REPORT REWORK AND ASSIGNMENT EXECUTION]

- Analyzed the supplied Group 14 Chapter 1 and preserved its congestion and multi-intersection motivation while correcting scope, terminology, tense, safety boundaries, and unsupported claims.
- Created `Team Class Report & Documentation.md` as the consolidated working report and project-management record.
- Added the one-intersection first vertical slice, fixed-time controller baseline, traffic-first objective, emissions-secondary objective, and live-demo boundary to the reworked chapter.
- Executed the lightweight project-management plan with team structure, milestones, work breakdown, meeting protocol, risk register, document tracker, Definition of Ready, and Definition of Done.
- Adopted Trello as the project-management tool unless the instructor explicitly requires Jira; documented board lists, labels, card templates, invitation procedure, operating rules, and Jira migration path.

## 23. Trello setup status [CHANGELOG: USER CONFIRMATION]

The Trello board has been created, the team members have been invited, and all invited members have successfully joined. The board-and-membership setup is complete. The overall class assignment remains pending final verification against the lecturer's rubric, including required cards/artifacts, roles, schedule, risk register, meeting evidence, and submission requirements.

## 24. Report restructuring and team assignment [CHANGELOG: USER APPROVAL]

The user approved restructuring `Team Class Report & Documentation.md` into exactly two report chapters: Chapter 1 — Introduction, containing the reworked source TXT, and Chapter 2 — Project Management, containing the class assignment and Trello execution plan. The source analysis remains as an editorial note outside the two chapters.

The initial working responsibility division is approved:

- Samuel Tanaka S — project coordinator, report integration, and Trello administrator.
- Alfonsus Tanara G — simulation and controller research.
- Ade Zaskia Azzahra — platform/data/dashboard planning and quality tracking.

## 25. Trello automation direction [CHANGELOG: USER REQUEST]

Python can be used to manage the Trello board through the Trello REST API. Automation is deferred until the user installs the isolated Python dependencies and the required Trello API credentials are configured securely. API keys and tokens must not be committed to the repository or placed in markdown files.

## 26. Submission document [CHANGELOG: SUBMISSION PREPARATION]

Created `Team Class Report & Documentation (submit).md` as a clean submission-ready version. It contains exactly two formal chapters: Chapter 1 — Introduction and Chapter 2 — Project Management. Editorial notes, footnotes, and changelogs were excluded from the submission version. The document presents the Trello board setup and team membership as completed, while excluding Trello API automation because it is not required for the class assignment.

## 27. Real-world integration scope [CHANGELOG: LECTURER REQUIREMENT]

The lecturer has changed the project requirement from a simulation-only concept to a real-world project involving government or local authorities. The target context is a university commuter-rail station area with a university bus stop beside a bidirectional main road, a pedestrian crossing, and an existing traffic light with a pedestrian-request button.

This requirement changes the integration plan but does not authorize direct access to the traffic-light cabinet, wiring, controller, or public road. The first field phase is observation and authority-approved shadow mode. The system must use a hardware-agnostic adapter and preserve the simulator as a safe development and fallback environment. Autonomous public-road actuation is prohibited until written authorization, an authority-supplied interface specification, a safety case, testing approval, and an approved fallback procedure exist.

The team must first discover the responsible authorities, signal ownership, controller documentation, available telemetry, pedestrian-button behavior, maintenance process, communications security, and permitted test conditions. Existing code should be integrated behind abstract observation, proposal, validation, and actuation interfaces rather than rewritten around guessed hardware assumptions.
