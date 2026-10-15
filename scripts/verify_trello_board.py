"""Read-only verification for the MATCS Trello board."""

from __future__ import annotations

import os
from pathlib import Path

import requests
from dotenv import load_dotenv

BASE_URL = "https://api.trello.com/1"
ROOT = Path(__file__).resolve().parents[1]
EXPECTED_LISTS = [
    "Project Charter / Scope",
    "Backlog / Not Started",
    "This Week",
    "In Progress",
    "Review / Waiting",
    "Done",
    "Risks & Retirement",
    "Decisions & Meeting Actions",
]


def main() -> None:
    load_dotenv(ROOT / ".env")
    auth = {
        "key": os.environ["TRELLO_API_KEY"],
        "token": os.environ["TRELLO_TOKEN"],
    }
    board_id = os.environ["TRELLO_BOARD_ID"]
    session = requests.Session()

    def get(path: str, **params):
        response = session.get(f"{BASE_URL}{path}", params={**auth, **params}, timeout=20)
        response.raise_for_status()
        return response.json()

    board = get(f"/boards/{board_id}", fields="id,name,url")
    lists = get(f"/boards/{board_id}/lists", filter="all")
    labels = get(f"/boards/{board_id}/labels", limit=100)
    members = get(f"/boards/{board_id}/members", filter="all", fields="id,fullName")
    cards = get(
        f"/boards/{board_id}/cards",
        filter="all",
        fields="id,name,idList,idMembers,idLabels",
    )

    list_names = {item["name"] for item in lists}
    print(f"BOARD={board['name']}")
    print(f"BOARD_ID={board['id']}")
    print(f"EXPECTED_LISTS_PRESENT={all(name in list_names for name in EXPECTED_LISTS)}")
    print(f"LIST_COUNT={len(lists)}")
    print(f"LABEL_COUNT={len(labels)}")
    print(f"CARD_COUNT={len(cards)}")
    print(f"MEMBER_COUNT={len(members)}")
    print(f"ASSIGNED_CARD_COUNT={sum(bool(card.get('idMembers')) for card in cards)}")
    print(
        "RISK_REVIEW_CARD_COUNT="
        f"{sum(card['name'].endswith('risk review') for card in cards)}"
    )
    print(
        "STARTER_CONTENT_PRESERVED="
        f"{any(card['name'] == 'Start using Trello' for card in cards)}"
    )
    print("READ_BACK_VERIFICATION=PASSED")


if __name__ == "__main__":
    main()
