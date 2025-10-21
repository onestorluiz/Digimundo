import logging, sys
def setup_logging(level: str = 'INFO'):
    logger = logging.getLogger('scripturemon')
    if logger.handlers: return logger
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))
    h = logging.StreamHandler(sys.stdout)
    h.setFormatter(logging.Formatter('[%(asctime)s] %(levelname)s %(name)s: %(message)s'))
    logger.addHandler(h)
    return logger
def get_logger(name: str = 'scripturemon'):
    return setup_logging()
