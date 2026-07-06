import json
from pathlib import Path


class CaseRepository:
    """Handles persistence of investigation cases."""

    def __init__(self):
        self.database = (
            Path(__file__).resolve().parents[2] / "data" / "investigations.json"
        )

    def load_cases(self) -> list[dict]:
        with open(self.database, "r") as file:
            return json.load(file)

    def save_cases(self, cases: list[dict]) -> None:
        with open(self.database, "w") as file:
            json.dump(cases, file, indent=4)
