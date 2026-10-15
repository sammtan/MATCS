# MTACS Jira Delivery Plan

> **Iterative updates rule:** Update this document when the instructor's Jira requirements, workflow, issue hierarchy, sprint cadence, ownership, acceptance criteria, or class-week mapping becomes known. Add a tagged change entry and preserve superseded planning decisions.
>
> **Document status:** Provisional design for the second assignment; instructor requirements are not yet available.
>
> **Change tag:** `[CHANGELOG: PHASE-ONE DESIGN]`

## 1. Purpose

This document is a draft for designing the team's Jira project. It is not yet the final Jira configuration. The final version must be adapted to the assignment instructions and the instructor's required artifacts.

## 2. Team

The team has three students. Names, ownership, and role rotation are intentionally undecided until the team discusses the assignment.

## 3. Proposed project structure

Use Scrum if the assignment expects sprints and sprint reviews; use Kanban if it expects continuous flow. Do not create the project until the required Jira template is known.

### Proposed epics

1. Project charter and architecture
2. Simulation foundation
3. Data pipeline and contracts
4. Controller and safety validation
5. Dashboard and live demonstration
6. Testing and evaluation
7. Documentation and final report
8. Deployment and operations

### Proposed issue types

- **Epic:** Major capability or deliverable area.
- **Story:** User-observable or stakeholder-observable capability.
- **Task:** Technical work supporting a story.
- **Spike:** Time-boxed research with a written result.
- **Bug:** Reproducible defect with evidence.

## 4. Initial spikes

- Compare simulator candidates using the documented selection criteria.
- Inspect the assignment requirements and required Jira artifacts.
- Investigate possible external traffic-data sources, coverage, terms, and cost.
- Check the feasibility of a live simulation demo within free-tier limits.

## 5. Initial stories

- Define the one-intersection scenario and success metrics.
- Document observation and control contracts.
- Implement the fixed-time controller baseline.
- Validate signal transitions with deterministic safety rules.
- Persist or replay experiment results.
- Display current simulation state and metrics.
- Compare fixed-time and queue-aware controllers.
- Prepare a live demo scenario.

## 6. Definition of Ready

An issue is ready when its purpose, scope, dependencies, owner or unassigned status, acceptance criteria, expected evidence, and documentation impact are clear.

## 7. Definition of Done

An issue is done when the implementation or research result is complete, reviewed by the team, tested or evidenced, linked to its documentation, and traceable to the relevant class-week or assignment requirement.

## 8. Acceptance-criteria pattern

Use observable criteria. Example:

- Given a fixed scenario and seed, when the fixed-time controller runs, then every phase transition follows the configured sequence.
- Given the same configuration and seed, when the run is repeated, then the recorded metrics are reproducible within the documented tolerance.
- Given an invalid proposal, when validation runs, then the proposal is rejected or replaced by the safe fallback and an event is recorded.

## 9. Labels and linking

Possible labels are `architecture`, `simulation`, `data`, `controller`, `safety`, `frontend`, `research`, `documentation`, `class-week-N`, and `assignment-N`. Use links between Jira issues, pull requests, commits, experiment runs, and documentation when implementation starts.

## 10. Information still required

- Assignment instructions and required Jira screenshots/artifacts.
- Required workflow, issue types, fields, and estimation method.
- Sprint or class-week schedule.
- Team member names and ownership.
- Instructor's expectations for AI, simulation, and live deployment.

## 11. Change log

- `[CHANGELOG: PHASE-ONE DESIGN]` Created provisional Jira structure and explicitly deferred final configuration until assignment details are available.
