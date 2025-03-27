"""Main"""

import logging
from logging.handlers import RotatingFileHandler

from fastapi import FastAPI

from src.app import routes

from .config import Configuration

LOG_FILE_MAX_BYTES = 50e6
LOG_MSG_FMT = (
    "%(asctime)s %(levelname)-8s %(name)s %(filename)s#L%(lineno)d %(message)s"
)
LOG_DT_FMT = "%Y-%m-%d %H:%M:%S"

# setting of the logger
formatter = logging.Formatter(fmt=LOG_MSG_FMT, datefmt=LOG_DT_FMT)
shandler = logging.StreamHandler()
shandler.setFormatter(formatter)

fhandler = RotatingFileHandler(
    "logs.txt", mode="w", backupCount=1, maxBytes=LOG_FILE_MAX_BYTES
)
fhandler.setFormatter(formatter)
logging.basicConfig(level=logging.INFO, handlers=[shandler, fhandler])

# set config from environment variables
config = Configuration()
config.load()

# Start FastAPI app
app = FastAPI()

# Add routes to the app
app.include_router(routes.healthcheck.router)
