"""Configuration module"""

from dataclasses import dataclass
from logging import getLogger
from os import getenv

from dotenv import load_dotenv

REQ_ENV_VARS = ["EXAMPLE"]

logger = getLogger(__name__)


@dataclass
class Configuration:
    """Represents the configuration settings for the application."""

    debug: bool = False
    example: str = ""

    def load(self) -> bool:
        """Load and validate environment variables."""

        if load_dotenv():
            logger.info("Loading environment variables from .env file")

        if not self.check_environment():
            raise RuntimeError("Missing required environment variables")

        self.register_envvars()

        return True

    def check_environment(self) -> bool:
        """Check if all required environment variables are set."""

        for env_var in REQ_ENV_VARS:
            if not getenv(env_var):
                logger.error("Missing environment variable: %s", env_var)
                return False
        return True

    def register_envvars(self) -> bool:
        """Register rquired and optional env vars."""

        # Required
        self.example = getenv("EXAMPLE", "")

        # Optional
        self.debug = getenv("DEBUG", "").strip().lower() == "true"

        return True


config = Configuration()
