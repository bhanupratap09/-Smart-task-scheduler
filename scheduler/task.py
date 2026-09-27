"""
task.py
--------
Defines the Task data model used throughout the Smart Task Scheduler.

A Task represents a single job that:
    - has a unique identifier
    - has a deadline (the latest time slot by which it must be completed)
    - has a profit/priority value (reward earned if scheduled before deadline)

This module has no dependencies on other modules, so it can be tested
and reused independently.
"""

from dataclasses import dataclass


@dataclass
class Task:
    """Represents a single job/task to be scheduled.

    Attributes:
        task_id: Unique human-readable identifier (e.g. "T1").
        name: Short descriptive name of the task.
        deadline: Positive integer representing the last time slot
                  (1-indexed) by which the task must finish.
        profit: Value earned if the task is completed by its deadline.
                Must be non-negative.
    """

    task_id: str
    name: str
    deadline: int
    profit: float

    def __post_init__(self) -> None:
        if self.deadline <= 0:
            raise ValueError(
                f"Task '{self.task_id}': deadline must be a positive integer, "
                f"got {self.deadline}."
            )
        if self.profit < 0:
            raise ValueError(
                f"Task '{self.task_id}': profit cannot be negative, "
                f"got {self.profit}."
            )
        if not self.task_id.strip():
            raise ValueError("Task id cannot be empty.")
        if not self.name.strip():
            raise ValueError("Task name cannot be empty.")

    def __str__(self) -> str:
        return (
            f"{self.task_id} | {self.name:<20} | "
            f"deadline={self.deadline:<3} | profit={self.profit:>8.2f}"
        )
