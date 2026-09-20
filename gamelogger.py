import logging
import os
from datetime import datetime

LOG_DIR = os.path.join(os.path.dirname(__file__), "logs")


def _setupLogger():
    os.makedirs(LOG_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    logPath = os.path.join(LOG_DIR, f"play_{timestamp}.log")

    newLogger = logging.getLogger("game")
    newLogger.setLevel(logging.DEBUG)
    newLogger.handlers.clear()
    newLogger.propagate = False

    handler = logging.FileHandler(logPath)
    handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", datefmt="%H:%M:%S"))
    newLogger.addHandler(handler)

    newLogger.info("=== New play session started: %s ===", logPath)
    return newLogger


logger = _setupLogger()
