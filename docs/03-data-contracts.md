# MTACS Data Contracts

> **Iterative updates rule:** Update this document when a field, event identity rule, timestamp rule, validation rule, or retention policy changes. Add a tagged change entry and preserve superseded contracts.
>
> **Document status:** Draft contract for the first vertical slice.
>
> **Change tag:** `[CHANGELOG: PHASE-ONE DESIGN]`

## 1. Contract principles

- Every record belongs to an `areaId`; the first area has one intersection.
- Simulation time is separate from wall-clock time.
- Events are replayable and idempotent.
- Controller proposals are not accepted actions until validated.
- Schemas include a version so simulator adapters can evolve safely.

## 2. Common metadata

| Field | Meaning |
|---|---|
| `schemaVersion` | Version of the record contract |
| `areaId` | Simulated area identifier |
| `intersectionId` | Intersection identifier when applicable |
| `simulationTime` | Time inside the simulated world |
| `observedAt` | Wall-clock creation time, if available |
| `source` | Simulator, controller, validator, or demo source |
| `eventId` | Unique identifier for idempotency and replay |

## 3. Observation record

An observation represents what the simulator reports, not what the controller wishes were true.

Minimum conceptual fields:

- Current signal phase and elapsed phase time.
- Vehicle count or queue estimate per approach/lane.
- Speed or occupancy when supported.
- Arrivals, departures, and stopped-vehicle count.
- Scenario and seed identifiers.
- Quality or staleness status.

## 4. State snapshot

A state snapshot is the internally consistent state used by a controller decision. It must identify the simulation time and include the signal state, traffic features, and any priority or incident flags.

A controller must not combine observations from incompatible simulation times without explicitly marking the state as stale or incomplete.

## 5. Controller proposal

A proposal contains:

- `proposalId`
- controller name and version
- input state identifier
- proposed abstract action
- requested duration or target phase, when applicable
- reason/features used for traceability
- proposal simulation time

Example action categories are `KEEP_PHASE`, `EXTEND_PHASE`, and `REQUEST_NEXT_PHASE`. Arbitrary electrical commands are not valid contract values.

## 6. Validation result and actuation event

The validator records:

- proposal identifier
- accepted, modified, or rejected status
- rule results
- fallback action, if used
- applied action
- validator version

The simulator actuator records the final applied action and resulting signal state.

## 7. Metrics record

Metrics should include scenario, seed, controller version, and run identifier. The first slice should calculate travel time or delay, queue length, throughput, stops, phase changes, validator interventions, and safety violations. An emissions or fuel proxy is optional until simulator support is confirmed.

## 8. Storage policy

High-frequency observations may be buffered locally and aggregated before MongoDB persistence. Retain experiment summaries and enough event data to replay selected runs. Disposable development records may use TTL indexes. Do not put database credentials in the frontend.

## 9. Change log

- `[CHANGELOG: PHASE-ONE DESIGN]` Defined initial metadata, observation, state, proposal, validation, actuation, and metrics contract concepts.
