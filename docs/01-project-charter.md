# MTACS Project Charter

> **Iterative updates rule:** Update this document when the problem, stakeholders, scope, objectives, assumptions, risks, or success criteria change. Add a dated or tagged change entry; do not silently rewrite an adopted decision.

> **Document status:** Draft for team and Jira-assignment preparation.
>
> **Change tag:** `[CHANGELOG: PHASE-ONE DESIGN]`

## 1. Project identity

- **Name:** MTACS — Multi-Agentic Traffic Control System
- **Course context:** Software Engineering group project
- **Team size:** Three students; individual ownership to be assigned later
- **Country context:** Indonesia
- **Current phase:** Phase-one design and Jira preparation

## 2. Problem statement

Traffic-light timing affects congestion, travel time, queues, vehicle stops, and potentially fuel consumption and emissions. MTACS will provide a software-only simulation in which traffic demand and traffic-light behavior can be observed, a controller can propose signal actions, and the result can be evaluated repeatedly.

The project does not require access to real traffic lights. It will imitate a real-world data pipeline and control loop while keeping the actuator inside a simulator.

## 3. Vision

Build a live public-facing simulation demo that shows how a constrained, data-driven controller can improve traffic flow in a defined area while respecting signal-safety rules and considering emissions as a secondary objective.

## 4. First vertical slice

The first vertical slice is one simulated area containing one intersection. It must demonstrate:

1. Vehicles or traffic demand entering the intersection.
2. A simulated traffic signal with defined phases.
3. A fixed-time controller.
4. A state/observation pipeline.
5. Simulated actuation.
6. Feedback from the changed signal state.
7. Measurable traffic and environmental-proxy metrics.
8. A path toward a later live web demonstration.

The one-intersection scope is a starting point, not the final system scale.

## 5. Objectives

### Primary objective

Optimize traffic flow, measured by lower delay and travel time, shorter queues, higher throughput, and fewer unnecessary stops.

### Secondary objective

Reduce estimated emissions or fuel consumption when the simulator provides a defensible proxy. Environmental optimization must not override safety or create unfair starvation of an approach.

### Engineering objectives

- Produce reproducible scenarios and metrics.
- Keep the simulation and controller runnable locally at minimal cost.
- Separate proposed actions from deterministic safety validation.
- Design a live demo rather than only a recorded result.
- Provide traceable Jira issues and evidence for class deliverables.

## 6. Non-goals

- Controlling public Indonesian traffic lights.
- Claiming production safety certification.
- Depending on an unconfirmed Google or other external traffic API.
- Training an AI model before fixed-time and heuristic baselines exist.
- Deploying one expensive cloud AI service per intersection.

## 7. Stakeholders

- Three-student project team.
- Software Engineering instructor and evaluators.
- Class audience viewing the live demonstration.
- Future maintainers who need reproducible experiments and documentation.

## 8. Success criteria for the first slice

- A fixed scenario can be run repeatedly with the same seed and configuration.
- The fixed-time controller produces valid signal phases.
- Metrics are recorded for traffic flow and, if supported, an emissions proxy.
- The system can show current simulated state in a local or later hosted interface.
- The project can be extended to a heuristic or learned controller without redesigning the data contract.
- No component can issue commands to real traffic infrastructure.

## 9. Current assumptions and risks

| Assumption or risk | Current response |
|---|---|
| Simulator product is not selected | Define selection criteria before installation or implementation |
| External data is unknown | Keep synthetic/simulator-generated data as the required path |
| Jira requirements may change | Keep the Jira design provisional until the assignment is provided |
| Live hosting may have free-tier limits | Design laptop-first execution with a small public demo surface |
| Three students have limited time | Deliver one vertical slice before multi-intersection or advanced AI work |

## 10. Immediate next action

Obtain the second-assignment requirements, then convert this charter into Jira epics, stories, tasks, spikes, acceptance criteria, and a delivery sequence. Do not begin full Milestone 0 implementation until that Jira structure is reviewed by the team.

## Change log

- `[CHANGELOG: PHASE-ONE DESIGN]` Initial charter created from the accepted records and user clarifications.
