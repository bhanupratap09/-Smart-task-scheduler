"""
validators.py
--------------
Small, reusable validation helpers for parsing raw CLI/user input into
clean typed values, raising InvalidTaskDataError with a clear message
on failure. Kept separate from task_manager so both the CLI and any
future interface (e.g. a web form) can reuse the same rules.
"""

from __future__ import annotations

from scheduler.exceptions import InvalidTaskDataError


def parse_positive_int(raw: str, field_name: str = "value") -> int:
    try:
        value = int(str(raw).strip())
    except (ValueError, TypeError) as exc:
        raise InvalidTaskDataError(f"{field_name} must be a whole number, got '{raw}'.") from exc
    if value <= 0:
        raise InvalidTaskDataError(f"{field_name} must be greater than 0, got {value}.")
    return value


def parse_non_negative_float(raw: str, field_name: str = "value") -> float:
    try:
        value = float(str(raw).strip())
    except (ValueError, TypeError) as exc:
        raise InvalidTaskDataError(f"{field_name} must be a number, got '{raw}'.") from exc
    if value < 0:
        raise InvalidTaskDataError(f"{field_name} cannot be negative, got {value}.")
    return value


def parse_non_empty_str(raw: str, field_name: str = "value") -> str:
    value = str(raw).strip()
    if not value:
        raise InvalidTaskDataError(f"{field_name} cannot be empty.")
    return value
