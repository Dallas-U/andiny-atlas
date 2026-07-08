import logging
from pathlib import Path

# Create the logs directory if it does not exist
log_directory = Path("logs")
log_directory.mkdir(exist_ok=True)

# Configure the application logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=[
        logging.FileHandler(log_directory / "andiny_atlas.log"),
        logging.StreamHandler(),
    ],
)

logger = logging.getLogger("andiny_atlas")
