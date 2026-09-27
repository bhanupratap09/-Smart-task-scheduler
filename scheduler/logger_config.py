"""
logger_config.py
-----------------
Centralized logging setup (non-functional requirement: logging/monitoring).

Logs are written both to the console (WARNING and above, to keep the CLI
clean) and to a rotating log file (INFO and above, for full traceability).
"""

from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


def configure_logging(log_dir: str | Path = "data", filename: str = "scheduler.log") -> None:
    log_dir = Path(log_dir)
    log_dir.mkdir(parents=True, exist_ok=True)
    log_path = log_dir / filename

    root_logger = logging.getLogger("scheduler")
    root_logger.setLevel(logging.INFO)

    if root_logger.handlers:
        # Avoid duplicate handlers if configure_logging() is called twice
        return

    file_handler = RotatingFileHandler(log_path, maxBytes=200_000, backupCount=2)
    file_handler.setLevel(logging.INFO)
    file_formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
    )
    file_handler.setFormatter(file_formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    console_handler.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))

    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
