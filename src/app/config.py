"""Configuration module"""

from logging import getLogger
from os import getenv

from dotenv import load_dotenv

REQ_ENV_VARS = ["EXAMPLE"]

logger = getLogger("app.config")


class Configuration:
    """Represents the configuration settings for the application."""

    def load(self) -> bool:
        """Loads the environment variables to the configuration object"""

        if load_dotenv():
            logger.info("Loading environment variables from .env file")

        assert self.check_environment(), "Missing required environment variables"

        return True

    def check_environment(self) -> bool:
        """Check if all required environment variables are set."""
        for env_var in REQ_ENV_VARS:
            if not getenv(env_var):
                logger.error("Missing environment variable: %s", env_var)
                return False

        return True


config = Configuration()
config.load()
