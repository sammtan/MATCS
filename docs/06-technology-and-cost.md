# MTACS Technology and Cost Plan

> **Iterative updates rule:** Update this document when a technology, version, hosting target, dependency, licensing assumption, or cost policy changes. Add a tagged change entry and preserve superseded choices.
>
> **Document status:** Accepted direction; exact versions are intentionally deferred until the Jira assignment and simulator choice are known.
>
> **Change tag:** `[CHANGELOG: PHASE-ONE DESIGN]`

## 1. Accepted direction

- Python for simulation, controller experimentation, data processing, and future model training.
- MongoDB for configuration, current state, events, decisions, and experiment metadata.
- Vercel for the eventual web dashboard/public demo surface.
- Laptop-first execution for the central process and experiments.
- GitHub and Jira for source control and delivery tracking.

## 2. Environment policy before coding

Before implementation starts, the team must select the simulator and then record:

- operating-system support
- Python version
- package/dependency manager
- MongoDB local or free-tier choice
- frontend runtime/version if a dashboard is created
- test and formatting tools
- environment variables and secret-handling rules
- license and free-tier constraints

No package installation or cloud resource creation is required for the current documentation phase.

## 3. Cost controls

- Run the simulator, controller, and training locally by default.
- Avoid always-on cloud machines and per-request LLM APIs.
- Keep external traffic APIs optional until terms, quota, coverage, and cost are checked.
- Use MongoDB locally or an eligible free tier; do not assume a paid plan.
- Use Vercel's free tier only within its current limits.
- Keep the public demo small and simulation-only.
- Record any educational license or free-tier dependency in the report.

## 4. Data and security rules

The browser must not contain MongoDB credentials. Secrets belong in local environment configuration or the hosting provider's secret store. Public demo endpoints must expose only controlled simulation operations and read-safe data.

## 5. Change log

- `[CHANGELOG: PHASE-ONE DESIGN]` Confirmed Python, MongoDB, Vercel, laptop-first execution, and zero-cost preference; deferred exact tool versions until implementation readiness.
