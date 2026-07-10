import json
from json import JSONDecodeError

from app.core.settings import settings
from app.core.types import CaseCollection
from app.exceptions.exceptions import PersistenceDataException
from app.logging.logger import logger


class CaseRepository:
    """Handles persistence of investigation cases."""

    def __init__(self):
        self.database = settings.database_path

    def load_cases(self) -> CaseCollection:
        """Load persisted investigation cases."""

        logger.info("Loading investigation cases.")

        try:
            with open(self.database, "r", encoding="utf-8") as file:
                cases = json.load(file)

        except JSONDecodeError as exc:
            logger.exception(
                "Investigation data could not be decoded from '%s'.",
                self.database,
            )

            raise PersistenceDataException(
                "Persisted investigation data is invalid and could not be read."
            ) from exc

        logger.info(
            "Loaded %d investigation case(s).",
            len(cases),
        )

        return cases

    def save_cases(self, cases: CaseCollection) -> None:
        """Persist investigation cases."""

        logger.info(
            "Saving %d investigation case(s).",
            len(cases),
        )

        with open(self.database, "w", encoding="utf-8") as file:
            json.dump(cases, file, indent=4)

        logger.info("Investigation cases saved successfully.")
