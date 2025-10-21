from loguru import logger
import sys, os

def setup_logging():
    logger.remove()
    logger.add(sys.stderr, level="INFO", enqueue=True)
    os.makedirs("./conhecimento/logs", exist_ok=True)
    logger.add("./conhecimento/logs/run_{time}.log", rotation="10 MB", retention="14 days", level="DEBUG")
    return logger
