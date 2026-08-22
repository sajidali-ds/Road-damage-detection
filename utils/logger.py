import logging
import os

from config import LOG_PATH

os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")

    file_handler = logging.FileHandler(LOG_PATH)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger
