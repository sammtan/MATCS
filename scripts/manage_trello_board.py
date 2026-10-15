"""Populate the MATCS Trello board with the Chapter 2 project-management plan."""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import requests
from dotenv import load_dotenv

BASE_URL = "https://api.trello.com/1"
ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class CardSpec:
    name: str
    list_name: str
    owner: str
    backup: str
    label: str
    objective: str
    acceptance: tuple[str, ...]
    document: str


def api_request(
    session: requests.Session,
    method: str,
    path: str,
    **kwargs: Any,
) -> Any:
    response = session.request(method, f"{BASE_URL}{path}", timeout=30, **kwargs)
    if not response.ok:
        raise RuntimeError(
            f"Trello API request failed: {method} {path} "
            f"({response.status_code}): {response.text[:500]}"
        )
    if not response.content:
        return None
    return response.json()


def member_id(members: list[dict[str, Any]], name_part: str) -> str:
    target = name_part.casefold()
    for member in members:
        values = [
            str(member.get("fullName", "")),
            str(member.get("username", "")),
        ]
        if any(target in value.casefold() for value in values):
            return str(member["id"])
    raise RuntimeError(f"Could not find Trello member matching: {name_part}")


def card_description(spec: CardSpec) -> str:
    checklist = "\n".join(f"- [ ] {item}" for item in spec.acceptance)
    return (
        f"Objective:\n{spec.objective}\n\n"
        f"Owner: {spec.owner}\n"
        f"Backup: {spec.backup}\n\n"
        f"Acceptance/evidence criteria:\n{checklist}\n\n"
        f"Related document: {spec.document}\n\n"
        "Target date: To be assigned from the class schedule.\n"
        "Dependencies: None recorded.\n"
    )


def main() -> int:
    load_dotenv(ROOT / ".env")
    api_key = os.getenv("TRELLO_API_KEY")
    token = os.getenv("TRELLO_TOKEN")
    board_id = os.getenv("TRELLO_BOARD_ID")
    if not all((api_key, token, board_id)):
        raise RuntimeError(
            "TRELLO_API_KEY, TRELLO_TOKEN, and TRELLO_BOARD_ID must be present in .env"
        )

    session = requests.Session()
    session.params.update({"key": api_key, "token": token})
    board = api_request(session, "GET", f"/boards/{board_id}", params={"fields": "id,name"})
    lists = api_request(session, "GET", f"/boards/{board_id}/lists", params={"filter": "all"})
    labels = api_request(session, "GET", f"/boards/{board_id}/labels", params={"limit": 100})
    members = api_request(
        session,
        "GET",
        f"/boards/{board_id}/members",
        params={"filter": "all", "fields": "id,fullName,username"},
    )
    cards = api_request(
        session,
        "GET",
        f"/boards/{board_id}/cards",
        params={"filter": "all", "fields": "id,name,idList,idMembers,idLabels"},
    )

    print(f"Board: {board['name']}")
    print(f"Board ID: {board['id']}")

    list_by_name = {item["name"].casefold(): item for item in lists}
    required_lists = [
        "Project Charter / Scope",
        "Backlog / Not Started",
        "This Week",
        "In Progress",
        "Review / Waiting",
        "Done",
        "Risks & Retirement",
        "Decisions & Meeting Actions",
    ]
    for list_name in required_lists:
        existing = list_by_name.get(list_name.casefold())
        if existing:
            continue
        created = api_request(
            session,
            "POST",
            f"/boards/{board_id}/lists",
            params={"name": list_name, "pos": "bottom"},
        )
        list_by_name[list_name.casefold()] = created
        print(f"Created list: {list_name}")

    label_colors = {
        "Planning": "blue",
        "Simulation": "green",
        "Data": "sky",
        "Controller": "orange",
        "Dashboard": "purple",
        "Documentation": "yellow",
        "Risk": "red",
        "Class Assignment": "pink",
    }
    label_by_name = {label["name"].casefold(): label for label in labels}
    for label_name, color in label_colors.items():
        if label_name.casefold() in label_by_name:
            continue
        created = api_request(
            session,
            "POST",
            f"/boards/{board_id}/labels",
            params={"name": label_name, "color": color},
        )
        label_by_name[label_name.casefold()] = created
        print(f"Created label: {label_name}")

    owners = {
        "Samuel": member_id(members, "Sam Tan"),
        "Alfonsus": member_id(members, "Alfonsus Tanara"),
        "Ade": member_id(members, "Ade Zaskia"),
    }
    backup = {"Samuel": "Ade", "Alfonsus": "Samuel", "Ade": "Alfonsus"}

    cards_by_name = {card["name"].casefold(): card for card in cards}
    specs = [
        CardSpec("Project scope and non-goals", "Project Charter / Scope", "Samuel", "Ade", "Planning", "Record the approved project boundary and exclusions.", ("Scope is written in the team report", "Non-goals include real traffic-light control and unconfirmed external data"), "Team Class Report & Documentation (submit).md"),
        CardSpec("One-intersection first vertical slice", "Project Charter / Scope", "Alfonsus", "Samuel", "Simulation", "Define the smallest complete simulation loop.", ("One area and one intersection are specified", "Traffic demand, signal phases, and feedback are described"), "docs/04-simulation-and-experiments.md"),
        CardSpec("Project objectives and success metrics", "Project Charter / Scope", "Alfonsus", "Samuel", "Planning", "Define traffic-first objectives and the secondary environmental objective.", ("Delay, travel time, queue, throughput, and stops are listed", "Emissions/fuel proxy is marked conditional on simulator support"), "Team Class Report & Documentation (submit).md"),
        CardSpec("Simulation-only safety boundary", "Project Charter / Scope", "Ade", "Alfonsus", "Risk", "Ensure all actuation remains inside the simulator.", ("Real infrastructure control is explicitly excluded", "Deterministic validation and safe fallback are documented"), "docs/02-system-architecture.md"),
        CardSpec("Review assignment rubric", "Backlog / Not Started", "Samuel", "Ade", "Class Assignment", "Confirm that board and report artifacts satisfy the lecturer's requirements.", ("Rubric requirements are recorded", "Required evidence and submission format are checked"), "Team Class Report & Documentation (submit).md"),
        CardSpec("Confirm team roles and backups", "Backlog / Not Started", "Samuel", "Ade", "Planning", "Confirm the approved working responsibility division.", ("Three primary owners are confirmed", "Each responsibility has a backup"), "Team Class Report & Documentation (submit).md"),
        CardSpec("Compare simulator candidates", "Backlog / Not Started", "Alfonsus", "Samuel", "Simulation", "Select a manageable, reproducible, zero-cost simulator or custom approach.", ("Candidates are compared using documented criteria", "A selected option and fallback are recorded"), "docs/04-simulation-and-experiments.md"),
        CardSpec("Define the initial schedule", "Backlog / Not Started", "Samuel", "Ade", "Planning", "Map milestones to the actual class schedule.", ("M0 through M6 have target class weeks or dates", "Dependencies and review points are recorded"), "Team Class Report & Documentation (submit).md"),
        CardSpec("Create the risk register", "Backlog / Not Started", "Samuel", "Ade", "Risk", "Initialize and prioritize the project's risks.", ("Likelihood, impact, retirement cost, plan, owner, and status are present", "Risks are reviewed in the regular meeting"), "Team Class Report & Documentation (submit).md"),
        CardSpec("Create the document tracker", "Backlog / Not Started", "Ade", "Samuel", "Documentation", "Track report and technical documents with owners and status.", ("Each planned document has an owner", "Document status and evidence are linked"), "Team Class Report & Documentation (submit).md"),
        CardSpec("Define observation and state contracts", "Backlog / Not Started", "Ade", "Alfonsus", "Data", "Define the data needed for the closed-loop simulation.", ("Observation, state, proposal, validation, actuation, and metrics are described", "Simulation time and event identity rules are recorded"), "docs/03-data-contracts.md"),
        CardSpec("Specify fixed-time controller", "Backlog / Not Started", "Alfonsus", "Ade", "Controller", "Specify the first deterministic controller baseline.", ("Phase order and durations are defined", "Safety validation remains mandatory", "Baseline metrics are identified"), "docs/05-ai-controller.md"),
        CardSpec("Define meeting process", "Backlog / Not Started", "Samuel", "Ade", "Planning", "Create a repeatable weekly meeting and decision process.", ("Agenda, timekeeper, note taker, decisions, and action items are defined", "Meeting evidence is stored in Trello"), "Team Class Report & Documentation (submit).md"),
        CardSpec("Review populated MATCS board with team", "This Week", "Samuel", "Ade", "Class Assignment", "Have the team review the automated board structure and accept ownership.", ("All members confirm their cards", "Missing dates, owners, or requirements are recorded"), "Team Class Report & Documentation (submit).md"),
    ]

    for number in range(1, 9):
        specs.append(
            CardSpec(
                f"R-{number:02d} risk review",
                "Risks & Retirement",
                "Samuel" if number in (2, 6, 8) else ("Alfonsus" if number in (1, 3, 5) else "Ade"),
                backup["Samuel" if number in (2, 6, 8) else ("Alfonsus" if number in (1, 3, 5) else "Ade")],
                "Risk",
                "Track, retire, or mitigate this risk according to the risk register.",
                ("Likelihood, impact, and retirement cost are reviewed", "A mitigation/retirement action and target date are recorded", "Progress is discussed in the next team meeting"),
                "Team Class Report & Documentation (submit).md",
            )
        )

    specs.extend(
        [
            CardSpec("Weekly meeting template", "Decisions & Meeting Actions", "Samuel", "Ade", "Planning", "Record agendas, decisions, risks, and action items consistently.", ("Attendees and agenda are recorded", "Decisions and owner/date action items are recorded"), "Team Class Report & Documentation (submit).md"),
            CardSpec("Decision log template", "Decisions & Meeting Actions", "Samuel", "Ade", "Planning", "Keep project decisions traceable outside chat.", ("Decision, rationale, owner, and affected documents are recorded", "Superseded decisions retain their history"), "Assistive Records.md"),
        ]
    )

    for spec in specs:
        key = spec.name.casefold()
        list_id = list_by_name[spec.list_name.casefold()]["id"]
        owner_id = owners[spec.owner]
        label_id = label_by_name[spec.label.casefold()]["id"]
        description = card_description(spec)
        existing = cards_by_name.get(key)
        if existing:
            api_request(
                session,
                "PUT",
                f"/cards/{existing['id']}",
                params={"desc": description, "idMembers": owner_id, "idLabels": label_id},
            )
            print(f"Updated card: {spec.name}")
            continue
        created = api_request(
            session,
            "POST",
            "/cards",
            params={"idList": list_id, "name": spec.name, "desc": description, "pos": "bottom", "idMembers": owner_id, "idLabels": label_id},
        )
        cards_by_name[key] = created
        print(f"Created card: {spec.name} [{spec.list_name}]")

    print("TRELLO_AUTOMATION=COMPLETED")
    print("Existing starter content was preserved; no cards or lists were deleted.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
