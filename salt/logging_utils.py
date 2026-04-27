from __future__ import annotations

import logging
import sys


LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)-18s | %(message)s"
LOG_DATE_FORMAT = "%H:%M:%S"


def configure_logging(level_name: str = "WARNING") -> None:
    level = _parse_level(level_name)
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(logging.Formatter(LOG_FORMAT, datefmt=LOG_DATE_FORMAT))

    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    root_logger.addHandler(handler)
    root_logger.setLevel(level)


def _parse_level(level_name: str) -> int:
    level = getattr(logging, level_name.upper(), None)
    if not isinstance(level, int):
        return logging.WARNING
    return level
