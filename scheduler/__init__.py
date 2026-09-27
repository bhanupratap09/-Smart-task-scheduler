"""
Smart Task Scheduler
=====================
A Greedy Job-Sequencing-with-Deadlines scheduler.

Package layout:
    task.py             - Task data model
    task_manager.py      - Module 1: task input, storage, persistence
    scheduler_engine.py  - Module 2: greedy scheduling algorithm
    analytics.py         - Module 3: reporting & statistics
    validators.py        - Shared input validation helpers
    logger_config.py     - Centralized logging setup
    exceptions.py        - Custom exception hierarchy
"""

from scheduler.task import Task
from scheduler.task_manager import TaskManager
from scheduler.scheduler_engine import (
    ScheduleResult,
    schedule_naive,
    schedule_optimized,
)

__all__ = [
    "Task",
    "TaskManager",
    "ScheduleResult",
    "schedule_naive",
    "schedule_optimized",
]

__version__ = "1.0.0"
