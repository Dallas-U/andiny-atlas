import json

from app.core.settings import settings
from app.logging.logger import logger


class CaseRepository:
    """Handles persistence of investigation cases."""

    def __init__(self):
        self.database = settings.database_path

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
