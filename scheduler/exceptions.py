"""
exceptions.py
-------------
Custom exception types for the Smart Task Scheduler.

Using specific exception classes (instead of generic Exception/ValueError
everywhere) makes error handling in the CLI layer precise and makes the
error-handling strategy explicit and testable, per the non-functional
requirement on error handling.
"""


class SchedulerError(Exception):
    """Base class for all scheduler-related errors."""


class DuplicateTaskError(SchedulerError):
    """Raised when a task with an already-used task_id is added."""


class TaskNotFoundError(SchedulerError):
    """Raised when a requested task_id does not exist in the store."""


class InvalidTaskDataError(SchedulerError):
    """Raised when task data fails validation (bad deadline/profit/etc.)."""


class EmptyTaskListError(SchedulerError):
    """Raised when an operation requires tasks but none are present."""
