# MATCS Team Class Report & Documentation

> **Role of this file:** This is the working class-report and project-management document for Group 14's MATCS project. It combines the reworked report content, project-management assignment evidence, decisions, and operational instructions for the team.
>
> **Iterative updates rule:** Update this document whenever the report, scope, requirements, schedule, team ownership, risks, technology choices, or project-management process changes. Add a dated or tagged changelog entry for each meaningful update. Do not silently replace an adopted decision; mark it as superseded and preserve the reason.

- **Project:** Multi-Agent Traffic Control System (MATCS)
- **Course:** Software Engineering
- **Team:** Group 14
- **Institution:** Universitas Indonesia
- **Current stage:** First simulator baselines, experiment evidence, and report refinement
- **Project-management tool:** Trello, provisionally, unless the lecturer requires Jira
- **Implementation status:** One-intersection simulator, fixed-time baseline, queue-aware heuristic, 13 automated tests, and 80 reproducible experiment runs completed
- **Document status:** Working draft for team review

## Editorial note: Chapter 1 rework

### Strengths to preserve

The original draft has several useful foundations:

- It identifies urban traffic congestion as a meaningful problem.
- It explains why fixed traffic-light timing may not reflect changing traffic demand.
- It introduces the relationship between queues at one intersection and traffic conditions at another.
- It gives a clear motivation for coordination between intersection-level controllers.
- It connects the project to agentic AI and software engineering rather than presenting AI as an isolated technology.

### Problems to correct

#### Terminology

The title and body use both “Multi-Agent Traffic Control System” and “Agentic AI-based traffic light control system.” The recommended official name is **Multi-Agent Traffic Control System (MATCS)**. “Agentic AI” describes the proposed technical approach, not a second project name.

#### Claims about implementation

The original text says that the group “developed” the system and describes agents as if they already monitor, decide, and communicate. At the current stage, the system is a proposed, simulation-first project. The report should use terms such as “proposes,” “designs,” “will model,” and “will evaluate” until implementation and experiments provide evidence.

#### Scope

The original introduction starts with several intersections, but the agreed first implementation target is one area containing one intersection. Multi-intersection coordination remains the intended expansion and research direction, not the first completed capability.

#### Safety and real-world boundary

The report should explicitly state that MATCS will not control public Indonesian traffic lights. Its actuator will be simulated. This prevents the report from implying government access, field deployment, or production safety certification.

#### Evidence and performance

The original text suggests that the system is expected to reduce buildup and waiting time, but it does not define how this will be measured. The report should identify traffic-flow metrics such as delay, travel time, queue length, throughput, and stops. Emissions or fuel consumption should be treated as a secondary objective only when the selected simulator provides a credible proxy.

#### Problem framing

The introduction repeats the same idea in several paragraphs. It should progress more directly:

1. Traffic congestion changes over time.
2. Fixed timing may waste capacity.
3. Connected intersections create a coordination problem.
4. MATCS proposes a simulation-based adaptive-control concept.
5. The first scope is one intersection; multi-intersection coordination is future work.
6. The report explains the requirements, design, management, implementation, and evaluation plan.

### Reworking decisions

- Use **MATCS** consistently as the project abbreviation.
- Present the project as a proposed software system at the current phase.
- Define the first vertical slice as one simulated intersection.
- Keep multi-agent coordination as a later expansion after a single-intersection baseline works.
- Describe agent roles as software modules initially; do not imply one cloud deployment per intersection.
- Add the simulation-only and safety boundary.
- Replace unsupported outcome claims with measurable evaluation objectives.
- Keep the introduction focused on the problem and project direction; move detailed architecture and AI strategy to later chapters.

## CHAPTER 1 — INTRODUCTION

### 1.1 Background

Traffic congestion is a common problem in urban areas. The number of vehicles using a road can change according to the time of day, commuting patterns, weather, public activities, incidents, and other conditions. Because traffic demand changes over time, a traffic-management system that uses only a fixed pattern may not always use the available road capacity effectively.

Traffic lights are important for organizing vehicle movement through road intersections. They assign right-of-way to different approaches and help prevent conflicting movements. However, if every approach receives the same timing even when its traffic demand is different, one approach may develop a long queue while another approach has unused green-light time. This situation can increase waiting time, the number of vehicle stops, and the overall delay experienced by road users.

The problem becomes more difficult when several intersections are connected by the same road corridor. Vehicles released from one intersection may travel toward another intersection and create a queue there. Therefore, a decision that reduces congestion at one intersection may transfer congestion to a neighboring intersection if the wider traffic condition is not considered. A traffic-control approach for connected intersections should consider both local conditions and, when the system is expanded, relevant information from neighboring intersections.

Artificial intelligence can support traffic-management research by helping a system analyze changing traffic conditions and select actions according to a defined objective. Agentic AI is relevant to this problem because the system can be organized into software components with specific responsibilities. For example, one component can process observations, another can maintain the current state, and a controller can propose a signal action. In a multi-intersection expansion, local controller agents may coordinate through summarized information from connected intersections.

Based on this problem, Group 14 proposes the **Multi-Agent Traffic Control System (MATCS)**. MATCS is a software-only, simulation-first project that models traffic demand, vehicle movement, traffic-light phases, and controller decisions in a defined area. The system will receive or synthesize traffic observations, create a representation of the current simulation state, propose a traffic-light action, validate that action using deterministic safety rules, and apply the validated action to the simulator.

The first implementation target is one simulated area containing one intersection. This scope is intentionally limited so that the team can demonstrate the complete feedback loop before introducing the additional complexity of multiple connected intersections. The first controller will be a fixed-time baseline. Later work may compare it with a queue-aware controller and, if the results and project schedule justify it, an optimization or learned controller.

MATCS will not connect to or control public traffic-light hardware. The system will imitate the interfaces and feedback flow of a possible real-world system while keeping actuation inside the simulator. This boundary is necessary because public traffic control is safety-critical, legally controlled, and outside the scope of this student project.

The main objective of the project is to investigate whether a data-driven traffic-light controller can improve traffic-flow measures such as travel time, delay, queue length, throughput, and the number of stops in repeatable simulation scenarios. Reducing estimated emissions or fuel consumption may be considered as a secondary objective when the selected simulator provides a credible measurement proxy. Any improvement must still respect signal-safety constraints and must not unfairly starve one approach.

The final project is intended to support a live public-facing demonstration of the simulation near the end of the course. The demonstration will show simulated traffic and controller behavior, not real-world traffic-light control. This report documents the project background, requirements, architecture, simulation approach, controller progression, project-management process, risks, implementation, and evaluation results as the project develops.

### 1.2 Problem statement

Urban traffic demand changes over time, but fixed traffic-light schedules may not respond to those changes. This can create unnecessary delay and queues. Connected intersections introduce an additional coordination problem because releasing traffic from one intersection can affect downstream conditions.

MATCS addresses this problem as a simulation and software-engineering study: how can a traffic-control system represent changing traffic conditions, propose safe signal actions, and evaluate local and coordinated control strategies using reproducible experiments?

### 1.3 Project objectives

#### Primary objective

Design and evaluate a simulation-based traffic-control system that aims to improve traffic flow by reducing delay, travel time, queue length, and unnecessary stops while maintaining safe signal transitions.

#### Secondary objective

Investigate whether improved traffic flow can also reduce an emissions or fuel-consumption proxy when the selected simulator supports such a measurement.

#### Engineering objectives

- Define a reproducible one-intersection simulation scenario.
- Implement or configure a fixed-time controller baseline.
- Define observation, state, proposal, validation, actuation, and metric contracts.
- Compare later controllers against the fixed-time baseline using matched scenarios.
- Keep the system simulation-only and suitable for a live public demonstration.
- Manage the project using a traceable, lightweight process appropriate for a three-student team.

### 1.4 Scope and limitations

#### Initial scope

- One simulated area.
- One intersection.
- Simulated vehicles or traffic demand.
- Simulated traffic-light phases and timing.
- A local central process.
- Deterministic safety validation.
- Fixed-time controller as the first baseline.
- Metrics and a later live dashboard/demo path.

#### Current implemented scope

- Standard-library Python simulator for one four-approach intersection.
- Fixed-time and queue-aware controllers behind a deterministic safety validator.
- Balanced, directional-heavy, and stress demand profiles.
- Per-approach waiting, maximum queue, fairness, throughput, delay, and intervention metrics.
- CSV and JSON experiment artifacts generated from matched seeds and configurations.

#### Future scope

- Multiple connected intersections.
- Coordination between local intersection controllers.
- Optimization-based control and later learned policies.
- Offline-trained learning policies.
- Optional external traffic context for scenario calibration.

#### Limitations

- The project does not control real traffic lights.
- No external real-time traffic-data source has been confirmed.
- Results will depend on the selected simulator and scenario assumptions.
- The queue-aware heuristic is not universally better than fixed timing in the current synthetic evidence; it improves some directional-heavy cases and slightly worsens some balanced/stress short-horizon cases.
- The project budget is effectively zero, so laptop-first execution and free-tier services are preferred.

### 1.5 Report organization

The remaining report chapters should be developed progressively as the class introduces the relevant topics. Recommended future sections are:

- Requirements and stakeholders
- Project-management plan
- System architecture and data contracts
- Simulation and controller design
- Technology and deployment plan
- Risk and quality management
- Implementation
- Testing and evaluation
- Live demonstration
- Results, limitations, and future work

## CHAPTER 7 — IMPLEMENTATION, TESTING, AND EXPERIMENT RESULTS

### 7.1 Implemented vertical slice

The first executable MATCS slice models one four-approach intersection using Python's standard library. Each tick generates seeded arrivals, obtains a proposal from either the fixed-time or queue-aware controller, validates the proposal against the configured phase sequence, applies accepted changes to a simulated actuator, moves vehicles on green approaches, and records metrics. The system intentionally has no traffic-hardware, public-network, authority-system, MongoDB, or cloud dependency.

### 7.2 Test evidence

The automated suite contains 13 tests. It covers controller transitions, stale and skipped-phase rejection, reproducibility, all demand profiles and durations, matched controller inputs, stress execution, zero demand, fairness bounds, starvation protection, per-approach metric keys, and CSV/JSON artifact schemas. The complete suite passed with `Ran 13 tests ... OK`.

### 7.3 Experiment design and results

The batch experiment contains 80 matched runs: four demand profiles, two durations (120 and 600 seconds), five seeds, and two controllers. Raw runs are stored in `results/experiments/raw_runs.csv`; metadata, records, grouped means, and population standard deviations are stored in `results/experiments/summary.json`.

The most informative 120-second grouped results were:

| Profile | Delay change with queue-aware | Mean queue change | Throughput change/min | Fairness change |
|---|---:|---:|---:|---:|
| Balanced | +1.84% | +1.83% | -1.40 | 0.9782 -> 0.9845 |
| North/south heavy | -1.33% | -1.33% | 0.00 | 0.9747 -> 0.9765 |
| East/west heavy | -5.77% | -5.77% | +1.60 | 0.9153 -> 0.9699 |
| Stress | +2.00% | +2.00% | -0.80 | 0.9931 -> 0.9960 |

These results support a limited conclusion: the transparent queue-aware rule is promising when demand is directionally imbalanced, especially for the east/west-heavy profile. They do not support a claim that it is universally superior. The stress and balanced short-horizon cases show small regressions, and the model uses synthetic demand rather than calibrated observations. The next software phase is therefore controlled heuristic refinement and review, not AI training or field deployment.

## CHAPTER 2 — PROJECT MANAGEMENT

### 2.1 Project-management approach

MATCS will use a lightweight iterative process. The team will plan a small amount of work, execute it, review evidence, retire risks, and update the report and board. The process follows the lecturer's principles without reproducing unnecessary corporate complexity.

The project-management source of truth will be Trello unless the lecturer's assignment rubric explicitly requires Jira. GitHub will remain the source of truth for code, branches, pull requests, and version history.

### 2.2 Team organization

The team has three students:

| Member | Student ID | Current role status |
|---|---:|---|
| Samuel Tanaka S | 2206059710 | Project coordinator, report integration, and Trello administrator |
| Alfonsus Tanara G | 2306267126 | Simulation and controller research |
| Ade Zaskia Azzahra | 2406344353 | Platform/data/dashboard planning and quality tracking |

The following responsibilities are proposed as a starting structure. They do not permanently assign roles until the team agrees:

| Responsibility area | Primary owner | Backup | Main evidence |
|---|---|---|---|
| Project coordination and report integration | To be assigned | To be assigned | Charter, schedule, meeting decisions |
| Simulation, controller, and experiments | To be assigned | To be assigned | Simulator comparison, scenarios, metrics |
| Platform, data, dashboard, and quality | To be assigned | To be assigned | Data contracts, tests, dashboard evidence |

Every responsibility should have a backup. The team leader or coordinator is responsible for ensuring that gaps are visible, not for performing every task personally.

### 2.3 Project milestones

Exact class-week dates are pending. The milestone order is adopted:

| Milestone | Objective | Evidence | Status |
|---|---|---|---|
| M0 — Project management foundation | Finalize scope, board, risks, documents, and ownership | Trello board, report section, risk register | In preparation |
| M1 — Simulator decision | Compare candidates and select a manageable simulator or custom approach | Decision card and comparison table | Pending |
| M2 — Reproducible baseline | Run one deterministic one-intersection scenario | Scenario config, fixed-time result, metrics | Pending |
| M3 — Platform vertical slice | Connect state, controller, validation, storage, and display path | Working local demonstration | Pending |
| M4 — Controller comparison | Compare fixed-time with a queue-aware or other justified controller | Experiment table and analysis | Pending |
| M5 — Live demonstration | Present the simulation publicly | Live demo checklist and evidence | Pending |
| M6 — Final report | Consolidate requirements, process, implementation, results, and limitations | Final report and contribution record | Pending |

### 2.5 Initial work breakdown

#### Planning and management

- Rework Chapter 1.
- Review the assignment rubric.
- Create and configure the Trello board.
- Assign provisional owners and backups.
- Create the risk register.
- Create the document tracker.
- Define the meeting and decision process.

#### Technical preparation

- Compare simulator candidates.
- Define the one-intersection scenario.
- Define signal phases and safety constraints.
- Define observation and state contracts.
- Define primary traffic metrics and a possible emissions proxy.
- Confirm the local development environment after simulator selection.

#### Initial implementation

- Build or configure the traffic scenario.
- Implement the fixed-time controller.
- Implement deterministic validation.
- Record replayable state and metric data.
- Display the current simulation state.

### 2.6 Meeting protocol

The team should hold a regular meeting at least once per project week or class milestone. Each meeting should use this agenda:

1. Confirm agenda and time allocation.
2. Review completed evidence and current board progress.
3. Review the schedule and upcoming milestones.
4. Review active risks and retirement progress.
5. Discuss decisions and unresolved questions.
6. Assign action items with owners and target dates.
7. Confirm the next meeting and expected evidence.

One member records decisions and action items. Another member monitors time. The meeting record should be attached or linked from the Trello `Decisions & Meeting Actions` list.

### 2.7 Risk register

Risk priority is provisionally calculated as:

`Priority = Likelihood × Impact × (11 − Retirement Cost)`

Likelihood, impact, and retirement cost use a 1–10 scale. Higher priority risks should be handled first. The calculation can be changed if the instructor requires another method.

| ID | Risk | Likelihood | Impact | Retirement cost | Retirement/mitigation plan | Responsible | Target | Status |
|---|---|---:|---:|---:|---|---|---|---|
| R-01 | Simulator is too difficult or incompatible with the team | 7 | 8 | 4 | Time-box candidate comparison and select a simpler fallback | To assign | Before M1 | Open |
| R-02 | Project scope grows beyond three students and course time | 8 | 9 | 2 | Freeze first scope at one intersection and defer expansion | To assign | M0 | Open |
| R-03 | No suitable external traffic data is available | 7 | 5 | 2 | Make synthetic/simulator data the required path; investigate only as a spike | To assign | Before external integration | Open |
| R-04 | Live demo depends on one unreliable laptop or service | 6 | 8 | 5 | Prepare a controlled public demo path and a local recovery path | To assign | Before M5 | Open |
| R-05 | AI complexity produces no measurable benefit | 6 | 7 | 4 | Require fixed-time and heuristic baselines before learning work | To assign | Before AI work | Open |
| R-06 | Trello/Jira assignment requirements are misunderstood | 5 | 8 | 2 | Review rubric and update the board/report before execution | To assign | Before M0 completion | Open |
| R-07 | High-frequency simulation data creates storage or cost problems | 5 | 6 | 3 | Buffer locally, aggregate writes, and retain summarized runs | To assign | Before platform slice | Open |
| R-08 | Team responsibility gaps delay work | 6 | 7 | 2 | Assign primary and backup owners for each responsibility | To assign | M0 | Open |

### 2.8 Document production plan

| Document | Purpose | Owner | Status |
|---|---|---|---|
| `README.md` | Project overview and navigation | To assign | Existing minimal file |
| `Assistive Records.md` | Persistent project memory and decisions | Project coordinator | Active |
| `Team Class Report & Documentation.md` | Class report and project-management evidence | Team | Active |
| `docs/01-project-charter.md` | Scope, goals, stakeholders, and success criteria | To assign | Draft |
| `docs/02-system-architecture.md` | Components and data flow | To assign | Draft |
| `docs/03-data-contracts.md` | Event and state contracts | To assign | Draft |
| `docs/04-simulation-and-experiments.md` | Scenarios, baselines, and metrics | To assign | Draft |
| `docs/05-ai-controller.md` | Controller progression and safety wrapper | To assign | Draft |
| `docs/06-technology-and-cost.md` | Stack and cost controls | To assign | Draft |
| `docs/08-jira-delivery-plan.md` | Alternative formal issue-management plan | To assign | Provisional |
| `docs/09-report-outline.md` | Future final-report structure | To assign | Draft |

### 2.9 Definition of Ready

A work item is ready when its objective, scope, owner or unassigned status, dependencies, target date, acceptance/evidence criteria, and documentation impact are clear.

### 2.10 Definition of Done

A work item is done when:

- The planned work or research has been completed.
- Evidence exists, such as a decision, document, test, screenshot, experiment, or pull request.
- Another team member has reviewed it.
- The relevant Trello card is updated and moved to `Done`.
- Related report or repository documentation is updated.
- Known risks and follow-up work are recorded.

### 2.11 Trello setup instructions

#### Create the board

1. Sign in to Trello using the account that will administer the team board.
2. Select **Create** and then **Create board**.
3. Name it `MATCS — Project Management`.
4. Set visibility according to the assignment. Use Workspace-visible or private visibility if the board contains personal information; use public visibility only if the lecturer explicitly requires it.
5. Add the lists below in this order:
   - `Project Charter / Scope`
   - `Backlog / Not Started`
   - `This Week`
   - `In Progress`
   - `Review / Waiting`
   - `Done`
   - `Risks & Retirement`
   - `Decisions & Meeting Actions`

#### Create labels

Create these labels:

- Planning
- Simulation
- Data
- Controller
- Dashboard
- Documentation
- Risk
- Class Assignment

Use one primary work-area label and add `Risk` or `Class Assignment` when relevant.

#### Create the first cards

Create these cards in `Project Charter / Scope`:

- Project scope and non-goals
- One-intersection first vertical slice
- Project objectives and success metrics
- Simulation-only safety boundary

Create these cards in `Backlog / Not Started`:

- Review assignment rubric
- Confirm team roles and backups
- Compare simulator candidates
- Define the initial schedule
- Create the risk register
- Create the document tracker
- Define observation and state contracts
- Specify fixed-time controller
- Define meeting-note process

Move the first weekly priorities into `This Week`. Do not move a card to `In Progress` until someone has accepted ownership.

#### Card template

Use this description structure for normal work cards:

```text
Objective:

Scope:

Owner:

Backup:

Target date:

Dependencies:

Acceptance/evidence criteria:
- [ ]
- [ ]

Related document:

Related branch or pull request:

Risks or decisions:
```

Use a checklist for subtasks and comments for progress updates. Do not use comments as a replacement for the final evidence link.

#### Risk-card template

```text
Risk ID:

Description:

Likelihood (1-10):
Impact (1-10):
Retirement cost (1-10):
Priority:

Retirement/mitigation plan:

Responsible person:

Target date:

Current evidence/status:

Decision:
```

#### Meeting-card template

```text
Meeting date:
Attendees:
Facilitator:
Note taker:

Agenda:
1.
2.
3.

Decisions:
-

Action items:
- [ ] Action — Owner — Target date

Risks discussed:
-

Next meeting:
```

### 2.12 Inviting the three team members to Trello

You will need each member's Trello account email address or the email address associated with their Atlassian account. Do not guess usernames or share account credentials.

#### Standard invitation procedure

1. Open the `MATCS — Project Management` board.
2. Select **Invite** or **Share** near the board title.
3. Enter the first team member's Trello/Atlassian email address.
4. Select the appropriate member permission. Use normal **Member** access; do not grant administrator access unless necessary.
5. Send the invitation.
6. Repeat for the second and third team members.
7. Ask each person to accept the invitation and verify that they can open the board.
8. Add each accepted member to cards only after roles are agreed.

The exact button names may differ slightly depending on Trello's current interface and workspace plan. The account owner should never request or store another member's password.

#### Invitation checklist

- [ ] Samuel Tanaka S invited
- [ ] Alfonsus Tanara G invited
- [ ] Ade Zaskia Azzahra invited
- [ ] All invitations accepted
- [ ] Board visibility reviewed
- [ ] Member permissions checked
- [ ] Roles and backups agreed
- [ ] First weekly cards assigned

### 2.13 Trello operating rules

- Trello is the single project-management source of truth.
- GitHub is the software source of truth.
- Every active card has one primary owner.
- A card cannot be `Done` without evidence.
- Risks are reviewed in every weekly meeting.
- Decisions are recorded rather than left only in chat.
- Dates and owners are updated when circumstances change.
- The board is kept small enough for three students to understand at a glance.
- Do not create a separate card for every sentence of a document.
- If the lecturer later requires Jira, migrate the structure rather than maintaining two competing boards.

### 2.14 Jira migration path if required

If the assignment requires Jira, convert the Trello structure as follows:

| Trello concept | Jira equivalent |
|---|---|
| Project area | Jira project |
| Large deliverable | Epic |
| Work card | Story or Task |
| Research card | Spike or Task |
| Defect card | Bug |
| List status | Workflow status |
| Label | Jira label |
| Checklist | Subtasks |
| Risk card | Risk issue or linked project page |
| Meeting card | Task or project documentation page |

Use the minimal workflow `To Do → In Progress → Review → Done`. Do not enable advanced Jira configuration unless the assignment requires it.

### 2.15 Immediate next actions

1. Confirm the lecturer's exact assignment rubric and whether Trello is accepted.
2. Review this document with the three team members.
3. Agree on primary and backup responsibilities.
4. Create the Trello board and invite the three accounts.
5. Add dates based on the actual class schedule.
6. Update the risk register with named owners.
7. Finalize Chapter 1 after team review.
8. Begin Milestone 0 only after the board and report structure are accepted.

## Document changelog

- `[CHANGELOG: REPORT REWORK]` Analyzed the original Chapter 1 and created a simulation-first rework with explicit scope, safety boundaries, measurable objectives, and future multi-intersection expansion.
- `[CHANGELOG: PROJECT-MANAGEMENT EXECUTION]` Converted the lecturer-slide principles into a lightweight team process, milestones, responsibilities, risk register, document tracker, meeting protocol, and completion criteria.
- `[CHANGELOG: TRELLO SETUP]` Added the approved Trello-first board design, card templates, invitation procedure, operating rules, and Jira migration path.
