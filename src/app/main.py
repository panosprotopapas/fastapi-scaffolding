"""Main"""

import logging
import os
from datetime import date
from typing import Optional

from fastapi import FastAPI

from src.app import routes
from src.app.config import config

LOG_DIR = "/logs"
LOG_PREFIX = "fastapiapp"
LOG_MSG_FMT = (
    "%(asctime)s %(levelname)-8s %(name)s %(filename)s#L%(lineno)d %(message)s"
)
LOG_DT_FMT = "%Y-%m-%d %H:%M:%S"


class DailyFileHandler(logging.Handler):
    """Writes to LOG_PREFIX_YYYYMMDD.log and switches file when the day changes."""

    def __init__(self, log_dir: str, prefix: str, encoding: str = "utf-8") -> None:
        super().__init__()
        self.log_dir = log_dir
        self.prefix = prefix
        self.encoding = encoding
        self._current_date: Optional[date] = None
        self._file_handler: Optional[logging.FileHandler] = None

        os.makedirs(self.log_dir, exist_ok=True)
        self._open_for(date.today())

    def _filename_for(self, day: date) -> str:
        return os.path.join(self.log_dir, f"{self.prefix}_{day.strftime('%Y%m%d')}.log")

    def _open_for(self, day: date) -> None:
        if self._file_handler is not None:
            self._file_handler.close()

        self._file_handler = logging.FileHandler(
            self._filename_for(day),
            mode="a",
            encoding=self.encoding,
        )
        if self.formatter is not None:
            self._file_handler.setFormatter(self.formatter)

        self._current_date = day

    def setFormatter(self, fmt: Optional[logging.Formatter]) -> None:
        super().setFormatter(fmt)
        if self._file_handler is not None:
            self._file_handler.setFormatter(fmt)

    def emit(self, record: logging.LogRecord) -> None:
        try:
            self.acquire()
            today = date.today()
            if today != self._current_date:
                self._open_for(today)
            if self._file_handler is not None:
                self._file_handler.emit(record)
        except Exception:
            self.handleError(record)
        finally:
            self.release()

    def close(self) -> None:
        try:
            if self._file_handler is not None:
                self._file_handler.close()
        finally:
            super().close()


# Load config
config.load()

# Configure logging
formatter = logging.Formatter(fmt=LOG_MSG_FMT, datefmt=LOG_DT_FMT)

shandler = logging.StreamHandler()
shandler.setFormatter(formatter)

fhandler = DailyFileHandler(log_dir=LOG_DIR, prefix=LOG_PREFIX)
fhandler.setFormatter(formatter)

logging.basicConfig(
    level=logging.DEBUG if config.debug else logging.INFO,
    handlers=[shandler, fhandler],
    force=True,
)

# Silence noisy third-party logs we do not want in the API logs.
for logger_name in ("pymongo", "pymongo.command", "pymongo.connection"):
    noisy_logger = logging.getLogger(logger_name)
    noisy_logger.disabled = True
    noisy_logger.propagate = False

logger = logging.getLogger("app.main")
logger.info("Logging initialized")
if config.debug:
    logger.debug("DEBUG=True env-var set. Logging level set to DEBUG")

# Start FastAPI app
app = FastAPI()

# Add routes to the app
app.include_router(routes.healthcheck.router)
