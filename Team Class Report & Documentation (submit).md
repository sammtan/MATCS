# MULTI-AGENT TRAFFIC CONTROL SYSTEM

## Group 14

1. Samuel Tanaka S — 2206059710
2. Alfonsus Tanara G — 2306267126
3. Ade Zaskia Azzahra — 2406344353

Computer Engineering Study Program  
Faculty of Engineering  
Universitas Indonesia  
2026

# CHAPTER 1
# INTRODUCTION

## 1.1 Background

Traffic congestion is a common problem in urban areas. The number of vehicles using a road can change according to the time of day, commuting patterns, weather, public activities, incidents, and other conditions. Because traffic demand changes over time, a traffic-management system that uses only a fixed pattern may not always use available road capacity effectively.

Traffic lights are important for organizing vehicle movement through road intersections. They assign the right of way to different approaches and help prevent conflicting movements. However, if every approach receives the same timing even when its traffic demand is different, one approach may develop a long queue while another approach has unused green-light time. This can increase waiting time, vehicle stops, and overall delay.

The problem becomes more difficult when several intersections are connected by the same road corridor. Vehicles released from one intersection may travel toward another intersection and create a queue there. Therefore, a decision that reduces congestion at one intersection may transfer congestion to a neighboring intersection if the wider traffic condition is not considered. A traffic-control approach for connected intersections should consider local conditions and, when the system is expanded, relevant information from neighboring intersections.

Artificial intelligence can support traffic-management research by helping a system analyze changing traffic conditions and select actions according to a defined objective. Agentic AI is relevant to this problem because the system can be organized into software components with specific responsibilities. For example, one component can process observations, another can maintain the current state, and a controller can propose a signal action. In a multi-intersection expansion, local controller agents may coordinate through summarized information from connected intersections.

Based on this problem, Group 14 proposes the **Multi-Agent Traffic Control System (MATCS)**. MATCS is a software-only, simulation-first project that models traffic demand, vehicle movement, traffic-light phases, and controller decisions in a defined area. The system receives or synthesizes traffic observations, creates a representation of the current simulation state, proposes a traffic-light action, validates that action using deterministic safety rules, and applies the validated action to the simulator.

The first implementation target is one simulated area containing one intersection. This scope is intentionally limited so that the team can demonstrate the complete feedback loop before introducing the additional complexity of multiple connected intersections. The first controller is a fixed-time baseline. Later work may compare it with a queue-aware controller and, if the results and project schedule justify it, an optimization or learned controller.

MATCS does not connect to or control public traffic-light hardware. The system imitates the interfaces and feedback flow of a possible real-world system while keeping actuation inside the simulator. This boundary is necessary because public traffic control is safety-critical, legally controlled, and outside the scope of this student project.

The main objective of the project is to investigate whether a data-driven traffic-light controller can improve traffic-flow measures such as travel time, delay, queue length, throughput, and the number of stops in repeatable simulation scenarios. Reducing estimated emissions or fuel consumption may be considered a secondary objective when the selected simulator provides a credible measurement proxy. Any improvement must still respect signal-safety constraints and must not unfairly starve one approach.

The project supports a live public-facing demonstration of the simulation near the end of the course. The demonstration shows simulated traffic and controller behavior, not real-world traffic-light control. This report presents the project background, requirements, project-management process, risk management, and initial technical direction.

## 1.2 Problem Statement

Urban traffic demand changes over time, but fixed traffic-light schedules may not respond to those changes. This can create unnecessary delay and queues. Connected intersections introduce an additional coordination problem because releasing traffic from one intersection can affect downstream conditions.

MATCS addresses this problem as a simulation and software-engineering study: how can a traffic-control system represent changing traffic conditions, propose safe signal actions, and evaluate local and coordinated control strategies using reproducible experiments?

## 1.3 Project Objectives

### 1.3.1 Primary Objective

The primary objective is to design and evaluate a simulation-based traffic-control system that aims to improve traffic flow by reducing delay, travel time, queue length, and unnecessary stops while maintaining safe signal transitions.

### 1.3.2 Secondary Objective

The secondary objective is to investigate whether improved traffic flow can also reduce an emissions or fuel-consumption proxy when the selected simulator supports such a measurement.

### 1.3.3 Engineering Objectives

The engineering objectives are:

1. Define a reproducible one-intersection simulation scenario.
2. Implement or configure a fixed-time controller baseline.
3. Define observation, state, proposal, validation, actuation, and metric contracts.
4. Compare later controllers against the fixed-time baseline using matched scenarios.
5. Keep the system simulation-only and suitable for a live public demonstration.
6. Manage the project using a traceable and lightweight process appropriate for a three-student team.

## 1.4 Scope and Limitations

### 1.4.1 Initial Scope

The initial scope consists of:

- One simulated area.
- One intersection.
- Simulated vehicles or traffic demand.
- Simulated traffic-light phases and timing.
- A local central process.
- Deterministic safety validation.
- A fixed-time controller as the first baseline.
- Metrics and a future live dashboard or demonstration path.

### 1.4.2 Future Scope

Future development may include:

- Multiple connected intersections.
- Coordination between local intersection controllers.
- Queue-aware or optimization-based control.
- Offline-trained learning policies.
- Optional external traffic context for scenario calibration.

### 1.4.3 Limitations

The project has the following limitations:

- The system does not control real traffic lights.
- No external real-time traffic-data source is required or assumed.
- Results depend on the selected simulator and scenario assumptions.
- The project does not claim that AI improves traffic until experiments provide evidence.
- The project budget is effectively zero, so laptop-first execution and free-tier services are preferred.

# CHAPTER 2
# PROJECT MANAGEMENT

## 2.1 Project-Management Approach

MATCS uses a lightweight iterative project-management process. The team plans a small amount of work, executes it, reviews evidence, retires risks, and updates the report and project board. This approach applies the lecturer's project-management principles while avoiding unnecessary corporate complexity.

Trello is the project's project-management source of truth. GitHub is the source of truth for source code, branches, pull requests, documentation history, and implementation artifacts.

The project-management process covers:

- Project scope and objectives
- Team organization and responsibilities
- Schedule and milestones
- Risk identification and retirement
- Document production
- Meetings and decisions
- Technology selection
- Evidence and completion criteria

## 2.2 Team Organization and Responsibilities

The project team consists of three students. Each responsibility area has a primary owner and a backup owner so that progress does not depend on only one person.

| Team member | Student ID | Primary responsibility |
|---|---:|---|
| Samuel Tanaka S | 2206059710 | Project coordination, report integration, and Trello administration |
| Alfonsus Tanara G | 2306267126 | Simulation and controller research |
| Ade Zaskia Azzahra | 2406344353 | Platform/data/dashboard planning and quality tracking |

### 2.2.1 Samuel — Project Coordinator, Report Integration, and Trello Administrator

Samuel is responsible for:

- Maintaining the Trello board structure, labels, dates, and member permissions.
- Converting project requirements into cards and acceptance criteria.
- Maintaining the team report and coordinating report integration.
- Facilitating regular meetings and recording decisions and action items.
- Maintaining the milestone schedule and coordinating risk-register reviews.
- Confirming that completed cards contain sufficient evidence before they are marked as done.

### 2.2.2 Alfonsus — Simulation and Controller Research

Alfonsus is responsible for:

- Comparing simulator candidates using the defined selection criteria.
- Defining the first one-intersection scenario with traffic demand and signal phases.
- Specifying the fixed-time controller baseline.
- Identifying traffic-flow metrics and a possible emissions or fuel-consumption proxy.
- Recording simulation decisions, assumptions, and research evidence.

### 2.2.3 Ade — Platform, Data, Dashboard, and Quality Tracking

Ade is responsible for:

- Defining observation, state, proposal, validation, actuation, and metrics contracts.
- Planning MongoDB collections and data-retention boundaries.
- Planning the dashboard and eventual Vercel live-demo boundary.
- Maintaining the quality checklist and identifying test and evidence requirements.
- Reviewing completed technical cards for traceability and documentation impact.

All team members are responsible for reviewing one another's work, reporting risks early, and updating their assigned Trello cards.

## 2.3 Project Milestones

Exact dates follow the course schedule and are maintained in the Trello board.

| Milestone | Objective | Required evidence | Status |
|---|---|---|---|
| M0 — Project-management foundation | Finalize scope, board, risks, documents, and ownership | Trello board, report section, risk register | Completed |
| M1 — Simulator decision | Compare candidates and select a manageable simulator or custom approach | Decision record and comparison table | Planned |
| M2 — Reproducible baseline | Run one deterministic one-intersection scenario | Scenario configuration, fixed-time result, and metrics | Planned |
| M3 — Platform vertical slice | Connect state, controller, validation, storage, and display paths | Working local demonstration | Planned |
| M4 — Controller comparison | Compare fixed-time control with a justified alternative | Experiment table and analysis | Planned |
| M5 — Live demonstration | Present the simulation publicly | Live demonstration checklist and evidence | Planned |
| M6 — Final report | Consolidate requirements, process, implementation, results, and limitations | Final report and contribution record | Planned |

## 2.4 Initial Work Breakdown

### 2.4.1 Planning and Management

- Define project scope and non-goals.
- Rework Chapter 1.
- Create and configure the Trello board.
- Invite all team members.
- Assign primary and backup responsibilities.
- Create the risk register.
- Create the document tracker.
- Define the meeting and decision process.

### 2.4.2 Technical Preparation

- Compare simulator candidates.
- Define the one-intersection scenario.
- Define signal phases and safety constraints.
- Define observation and state contracts.
- Define primary traffic metrics and a possible emissions proxy.
- Confirm the local development environment after simulator selection.

### 2.4.3 Initial Implementation

- Build or configure the traffic scenario.
- Implement the fixed-time controller.
- Implement deterministic validation.
- Record replayable state and metric data.
- Display the current simulation state.

## 2.5 Meeting Protocol

The team holds a regular meeting at least once per project week or class milestone. Each meeting follows this agenda:

1. Confirm the agenda and time allocation.
2. Review completed evidence and current board progress.
3. Review the schedule and upcoming milestones.
4. Review active risks and retirement progress.
5. Discuss decisions and unresolved questions.
6. Assign action items with owners and target dates.
7. Confirm the next meeting and expected evidence.

One member records decisions and action items, while another monitors the meeting time. The meeting record is attached or linked from the Trello `Decisions & Meeting Actions` list.

## 2.6 Risk Management

The team continuously identifies, prioritizes, and retires risks. Risk priority is calculated using:

`Priority = Likelihood × Impact × (11 − Retirement Cost)`

Likelihood, impact, and retirement cost use a scale from 1 to 10. Higher priority risks are handled first.

| ID | Risk | Likelihood | Impact | Retirement cost | Mitigation or retirement plan | Responsible | Status |
|---|---|---:|---:|---:|---|---|---|
| R-01 | Simulator is too difficult or incompatible with the team | 7 | 8 | 4 | Time-box candidate comparison and select a simpler fallback | Alfonsus | Open |
| R-02 | Project scope grows beyond the team and course timeframe | 8 | 9 | 2 | Freeze the first scope at one intersection and defer expansion | Samuel | Open |
| R-03 | No suitable external traffic data is available | 7 | 5 | 2 | Use synthetic or simulator-generated data as the required path | Alfonsus | Open |
| R-04 | Live demonstration depends on one unreliable computer or service | 6 | 8 | 5 | Prepare a controlled public-demo path and a local recovery path | Ade | Open |
| R-05 | AI complexity produces no measurable benefit | 6 | 7 | 4 | Require fixed-time and heuristic baselines before learning work | Alfonsus | Open |
| R-06 | Project-management requirements are misunderstood | 5 | 8 | 2 | Review the assignment requirements and update the board and report | Samuel | Open |
| R-07 | High-frequency simulation data creates storage or cost problems | 5 | 6 | 3 | Buffer locally, aggregate writes, and retain summarized runs | Ade | Open |
| R-08 | Responsibility gaps delay work | 6 | 7 | 2 | Maintain primary and backup owners for each responsibility | Samuel | Open |

Risks are reviewed during regular meetings. New risks are added to the Trello `Risks & Retirement` list with a responsible member and a target date.

## 2.7 Document Production Plan

| Document | Purpose | Responsible member | Status |
|---|---|---|---|
| `README.md` | Project overview and navigation | Samuel | Existing |
| `Assistive Records.md` | Persistent project memory and decisions | Samuel | Active |
| `Team Class Report & Documentation (submit).md` | Submitted report and project-management documentation | Team | Completed |
| `docs/01-project-charter.md` | Scope, goals, stakeholders, and success criteria | Samuel | Draft |
| `docs/02-system-architecture.md` | Components and data flow | Ade | Draft |
| `docs/03-data-contracts.md` | Event and state contracts | Ade | Draft |
| `docs/04-simulation-and-experiments.md` | Scenarios, baselines, and metrics | Alfonsus | Draft |
| `docs/05-ai-controller.md` | Controller progression and safety wrapper | Alfonsus | Draft |
| `docs/06-technology-and-cost.md` | Technology stack and cost controls | Ade | Draft |
| `docs/08-jira-delivery-plan.md` | Alternative formal issue-management plan | Samuel | Provisional |
| `docs/09-report-outline.md` | Future final-report structure | Samuel | Draft |

## 2.8 Definition of Ready

A work item is ready when its objective, scope, owner, dependencies, target date, acceptance or evidence criteria, and documentation impact are clear.

## 2.9 Definition of Done

A work item is complete when:

- The planned work or research has been completed.
- Evidence exists, such as a decision, document, test, screenshot, experiment, or pull request.
- Another team member has reviewed it.
- The Trello card has been updated and moved to `Done`.
- Related report or repository documentation has been updated.
- Known risks and follow-up work have been recorded.

## 2.10 Trello Project-Management Board

The team uses a Trello board named **MATCS — Project Management**.

The board uses the following lists:

1. `Project Charter / Scope`
2. `Backlog / Not Started`
3. `This Week`
4. `In Progress`
5. `Review / Waiting`
6. `Done`
7. `Risks & Retirement`
8. `Decisions & Meeting Actions`

The board uses labels for:

- Planning
- Simulation
- Data
- Controller
- Dashboard
- Documentation
- Risk
- Class Assignment

Each work card contains an objective, scope, owner, backup, target date, dependencies, acceptance or evidence criteria, related document, and related branch or pull request when applicable.

The initial project-management cards cover:

- Project scope and non-goals
- One-intersection first vertical slice
- Project objectives and success metrics
- Simulation-only safety boundary
- Simulator comparison
- Initial schedule
- Risk register
- Document tracker
- Observation and state contracts
- Fixed-time controller specification
- Meeting process

## 2.11 Board Setup and Team Membership

The Trello board has been created and configured. All three group members have been invited and have successfully joined the board.

The completed membership checklist is:

- Samuel Tanaka S joined
- Alfonsus Tanara G joined
- Ade Zaskia Azzahra joined
- Board visibility reviewed
- Member permissions checked
- Initial responsibilities assigned
- Initial project-management cards prepared

Trello is used for planning, ownership, schedule, risks, decisions, and project evidence. GitHub is used for source code, branches, pull requests, and repository documentation.

## 2.12 Board Operating Rules

- Trello is the single project-management source of truth.
- GitHub is the software source of truth.
- Every active card has one primary owner.
- Every major responsibility has a backup.
- A card cannot be moved to `Done` without evidence.
- Risks are reviewed in every regular meeting.
- Decisions are recorded instead of remaining only in chat.
- Dates and owners are updated when circumstances change.
- The board remains small enough for three students to understand at a glance.
- The team does not maintain Jira and Trello as competing sources of truth.

## 2.13 Conclusion

The MATCS project has established a manageable project-management foundation for a three-student Software Engineering team. The project begins with a clearly bounded, simulation-only one-intersection system and a fixed-time controller baseline. Trello provides a lightweight way to manage scope, responsibilities, milestones, risks, documents, meetings, and evidence.

The next technical stage is to compare simulator candidates, select an appropriate zero-cost or locally runnable option, and prepare the reproducible baseline scenario. Later development may expand the system to multiple intersections and more advanced controllers after the first vertical slice has been evaluated.
