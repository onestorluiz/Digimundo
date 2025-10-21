import logging, sys

def setup_logging(level: str = "INFO") -> logging.Logger:
    logger = logging.getLogger("scripturemon")
    if logger.handlers:
        return logger
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))
    handler = logging.StreamHandler(sys.stdout)
    fmt = "[%(asctime)s] %(levelname)s %(name)s: %(message)s"
    handler.setFormatter(logging.Formatter(fmt))
    logger.addHandler(handler)
    return logger

def get_logger(name: str = "scripturemon") -> logging.Logger:
    return setup_logging()
