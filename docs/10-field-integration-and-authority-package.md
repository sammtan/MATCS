# MTACS Field Integration and Authority Package

> **Iterative updates rule:** Update this document whenever the target site, responsible authority, signal documentation, permitted data, interface, safety condition, or deployment phase changes. Record the source and approval status for every field assumption.
>
> **Document status:** Proposed real-world integration plan; no field connection is authorized.
>
> **Change tag:** `[CHANGELOG: REAL-WORLD INTEGRATION]`

## 1. Purpose

This document defines how MTACS can be studied and integrated with the real crossing near the university commuter-rail station and university bus stop without guessing the signal technology or bypassing public-infrastructure controls.

The first goal is not to replace the existing signal controller. The first goal is to create an authority-approved observation and decision-support pathway that can be tested against the real site while keeping the existing signal system in control.

## 2. Target site model

The target site is expected to contain:

- A commuter-rail station.
- A university bus stop serving movement between faculties or facilities.
- A bidirectional main road.
- A crossing connecting opposite sides of a side road or access road.
- A traffic signal serving the crossing.
- A pedestrian-request button.
- Existing signal-control equipment whose manufacturer, controller model, wiring, timing, and communications are not yet known.

This is a working site description, not an electrical or operational specification. Every technical detail must be confirmed by the responsible authority or an approved site survey.

## 3. Stakeholder and authority discovery

The team should identify and contact the relevant parties before collecting operational data or opening any cabinet:

- University facilities or campus operations.
- University transportation or security office.
- Local road or transport authority.
- Commuter-rail station operator, if the station property is separately managed.
- University bus operator or fleet coordinator.
- Traffic-signal maintenance contractor.
- University information-security or data-protection contact.
- Lecturer and project supervisor.

The team should request one official contact who can confirm ownership and approve the project boundary. A university contact alone may not authorize changes to a public-road signal.

## 4. Information request to authorities

Ask for the following information in writing:

### Ownership and authorization

- Who owns the road, crossing, signal, cabinet, and pedestrian button?
- Who maintains the signal and approves field tests?
- Is the site public, university-controlled, station-controlled, or shared?
- What written approval is needed for observation, data collection, equipment installation, or actuation?
- What safety review and insurance requirements apply?

### Signal operation

- Signal controller manufacturer and model.
- Signal phase and timing diagram.
- Normal operating schedule and timing plans.
- Minimum green, maximum green, yellow, and all-red constraints.
- Pedestrian-request behavior and button diagnostic behavior.
- Manual override, flashing, emergency, maintenance, and failure modes.
- Current fault and maintenance-reporting process.

### Available interfaces

- Whether read-only telemetry exists.
- Available protocol or documented API.
- Whether a data export, maintenance log, or controller report can be supplied instead.
- Whether an approved gateway already exists.
- Authentication, encryption, network segmentation, rate limits, and logging requirements.
- Whether third-party software is permitted to send any command.

### Field test conditions

- Approved observation hours.
- Approved equipment locations and power/network constraints.
- Required traffic-management personnel.
- Required emergency stop or rollback procedure.
- Maximum test duration and permitted test scenarios.
- Authority representative who must approve each test.

## 5. What the team must not do

The team must not:

- Open a signal cabinet without written authorization and qualified supervision.
- Connect a laptop, microcontroller, relay, or network device to the signal system without approval.
- Inject commands into a signal controller.
- Bypass the existing controller's safety logic.
- Treat the pedestrian button as a software API without documentation.
- Capture identifiable pedestrian video without approval, notice, and a privacy plan.
- Use a public demo to issue live traffic commands.
- Assume that a malfunctioning button or inactive signal can be repaired by student software.

## 6. Integration architecture

```text
Approved field observation / authority data
				  |
				  v
		Field observation adapter
				  |
				  v
	   Normalized site state model
				  |
		  +-------+-------+
		  |               |
		  v               v
   Digital twin /     Shadow-mode
   simulator          controller
		  |               |
		  +-------+-------+
				  |
				  v
	   Deterministic validator
				  |
				  v
	   Authority review package
				  |
	   (future only, approved)
				  v
	  Authority-controlled gateway
				  |
				  v
	   Existing signal system
```

The real field path must be separate from the simulation path. The controller should produce an abstract proposal such as a timing-plan recommendation, not an electrical signal command. An authority-controlled gateway must remain between any future student software and the actual signal controller.

## 7. Deployment phases

### Phase 0 — Authority and site discovery

Deliverables:

- Site identity and map.
- Ownership and contact record.
- Written project boundary.
- Signal documentation request.
- Data-protection and safety review questions.

No field equipment or data collection beyond permitted discussion is used.

### Phase 1 — Observation-only

Use only authority-approved sources, such as:

- Manual observation forms.
- Non-identifying counts.
- Existing authority telemetry.
- Maintenance logs.
- Approved sensors installed by authorized personnel.

The existing signal controller remains completely independent of MTACS.

### Phase 2 — Digital twin calibration

Use approved observations to calibrate the simulator. Compare simulated signal timing, pedestrian requests, vehicle demand, and queue behavior with field observations. The digital twin remains the development and testing environment.

### Phase 3 — Shadow mode

MTACS receives approved field state or periodic data and produces recommendations without sending commands. An authorized person or authority system compares the recommendation with the actual operation. All decisions are logged.

### Phase 4 — Supervised pilot, only if approved

If the authority explicitly approves it, a supervised pilot may use an authority-controlled interface. The pilot must have a documented test window, rollback, emergency stop, monitoring, and responsible authority representative.

### Phase 5 — Operational deployment

This is outside the current student scope unless the authority, university, and relevant regulators establish a separate certified project.

## 8. Hardware-agnostic contracts

### Field observation

```text
siteId
intersectionId
observedAt
source
signalPhase
pedestrianRequestState
vehicleCountByApproach
queueEstimateByApproach
observationQuality
```

### Controller proposal

```text
proposalId
siteId
simulationOrObservationTime
controllerVersion
proposalType
recommendedTimingPlan
reason
confidence
```

### Approval and actuation record

```text
approvalId
proposalId
approvedBy
approvalTime
permittedAction
validFrom
validUntil
rollbackPlan
actualAppliedBy
result
```

The field observation contract must not imply that the team can read a value that the authority has not made available. The actuation contract is a future approval artifact, not an implementation permission.

## 9. Minimal real-world deliverable

The safest realistic deliverable for the course is:

1. An authority-approved site description.
2. A documented existing signal and pedestrian-request workflow.
3. A non-identifying observation dataset or authority-provided data sample.
4. A digital-twin scenario calibrated from that information.
5. A shadow-mode MTACS recommendation report.
6. A live demonstration that clearly separates simulated behavior from the real site.

This can satisfy a real-world requirement without claiming unauthorized control of public infrastructure.

## 10. Authority-facing package

Prepare these materials before requesting access:

- One-page project summary.
- Site map and boundary diagram.
- Data-flow and safety-boundary diagram.
- Data fields requested and privacy treatment.
- No-actuation statement for the first phase.
- Proposed observation schedule.
- Risk register and mitigations.
- Team and supervisor contacts.
- Emergency and incident contact procedure.
- Questions about ownership and available interfaces.

## 11. Acceptance criteria for changing phase

The team may not move from one phase to the next until the current phase has:

- Written approval or documented authority decision.
- Named responsible authority contact.
- Defined data and security boundary.
- Tested fallback behavior.
- Updated risk assessment.
- Evidence stored in the project repository and Trello.

## 12. Change log

- `[CHANGELOG: REAL-WORLD INTEGRATION]` Added the authority-discovery package, hardware-agnostic integration architecture, observation-to-shadow-mode deployment phases, and prohibition on unauthorized field actuation.
