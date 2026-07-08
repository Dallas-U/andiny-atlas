import json
from pathlib import Path

from app.logging.logger import logger


class CaseRepository:
    """Handles persistence of investigation cases."""

    def __init__(self):
        self.database = (
            Path(__file__).resolve().parents[2] / "data" / "investigations.json"
        )

    def load_cases(self) -> list[dict]:

        logger.info("Loading investigation cases.")

        with open(self.database, "r") as file:

            cases = json.load(file)

        logger.info(
            "Loaded %d investigation case(s).",
            len(cases),
        )

        return cases

    def save_cases(
        self,
        cases: list[dict],
    ) -> None:

        logger.info(
            "Saving %d investigation case(s).",
            len(cases),
        )

        with open(self.database, "w") as file:

            json.dump(cases, file, indent=4)

        logger.info("Investigation cases saved successfully.")
