# AstroAgent/utils/logger.py

import logging
from config import LOG_LEVEL

def setup_logger(name="AstroAgent"):
    level = getattr(logging, LOG_LEVEL.upper(), logging.INFO)
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:
        ch = logging.StreamHandler()
        ch.setLevel(level)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)

    return logger
