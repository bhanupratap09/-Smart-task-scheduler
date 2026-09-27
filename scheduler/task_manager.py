"""
task_manager.py
----------------
MODULE 1: Task Input Manager

Responsible for:
    - Accepting new tasks (with validation)
    - Storing tasks in memory (dict keyed by task_id for O(1) lookup)
    - Editing / removing tasks
    - Listing tasks
    - Persisting tasks to / loading tasks from a JSON file (data/tasks.json)

This module owns all data-entry concerns so the scheduling engine
(module 2) can stay purely algorithmic.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional

from scheduler.task import Task
from scheduler.exceptions import (
    DuplicateTaskError,
    TaskNotFoundError,
    InvalidTaskDataError,
    EmptyTaskListError,
)

logger = logging.getLogger("scheduler.task_manager")


class TaskManager:
    """In-memory task store with validation and JSON persistence."""

    def __init__(self) -> None:
        # Dict lookup keeps add/find/remove at O(1) average time.
        self._tasks: Dict[str, Task] = {}

    # ------------------------------------------------------------------ #
    # Core CRUD operations
    # ------------------------------------------------------------------ #
    def add_task(self, task_id: str, name: str, deadline: int, profit: float) -> Task:
        """Create and store a new task. Raises on duplicate id or bad data."""
        task_id = task_id.strip()
        if task_id in self._tasks:
            raise DuplicateTaskError(f"Task id '{task_id}' already exists.")
        try:
            task = Task(task_id=task_id, name=name.strip(), deadline=int(deadline), profit=float(profit))
        except (ValueError, TypeError) as exc:
            raise InvalidTaskDataError(str(exc)) from exc

        self._tasks[task_id] = task
        logger.info("Added task %s", task)
        return task

    def remove_task(self, task_id: str) -> None:
        """Remove a task by id. Raises TaskNotFoundError if missing."""
        if task_id not in self._tasks:
            raise TaskNotFoundError(f"Task id '{task_id}' not found.")
        del self._tasks[task_id]
        logger.info("Removed task %s", task_id)

    def edit_task(
        self,
        task_id: str,
        name: Optional[str] = None,
        deadline: Optional[int] = None,
        profit: Optional[float] = None,
    ) -> Task:
        """Update fields of an existing task. Only provided fields change."""
        if task_id not in self._tasks:
            raise TaskNotFoundError(f"Task id '{task_id}' not found.")

        existing = self._tasks[task_id]
        new_name = name.strip() if name is not None else existing.name
        new_deadline = int(deadline) if deadline is not None else existing.deadline
        new_profit = float(profit) if profit is not None else existing.profit

        try:
            updated = Task(task_id=task_id, name=new_name, deadline=new_deadline, profit=new_profit)
        except (ValueError, TypeError) as exc:
            raise InvalidTaskDataError(str(exc)) from exc

        self._tasks[task_id] = updated
        logger.info("Edited task %s", updated)
        return updated

    def get_task(self, task_id: str) -> Task:
        if task_id not in self._tasks:
            raise TaskNotFoundError(f"Task id '{task_id}' not found.")
        return self._tasks[task_id]

    def list_tasks(self) -> List[Task]:
        """Return all tasks currently stored (unordered)."""
        return list(self._tasks.values())

    def clear(self) -> None:
        self._tasks.clear()

    def require_non_empty(self) -> None:
        if not self._tasks:
            raise EmptyTaskListError("No tasks available. Add tasks before scheduling.")

    def __len__(self) -> int:
        return len(self._tasks)

    # ------------------------------------------------------------------ #
    # Persistence (JSON) — supports resource efficiency & reliability
    # ------------------------------------------------------------------ #
    def save_to_file(self, path: str | Path) -> None:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        payload = [
            {
                "task_id": t.task_id,
                "name": t.name,
                "deadline": t.deadline,
                "profit": t.profit,
            }
            for t in self._tasks.values()
        ]
        with open(path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)
        logger.info("Saved %d task(s) to %s", len(payload), path)

    def load_from_file(self, path: str | Path) -> int:
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"Task data file not found: {path}")

        with open(path, "r", encoding="utf-8") as f:
            raw = json.load(f)

        loaded = 0
        for entry in raw:
            try:
                self.add_task(
                    task_id=entry["task_id"],
                    name=entry["name"],
                    deadline=entry["deadline"],
                    profit=entry["profit"],
                )
                loaded += 1
            except (DuplicateTaskError, InvalidTaskDataError, KeyError) as exc:
                logger.warning("Skipped invalid entry %s: %s", entry, exc)
        logger.info("Loaded %d task(s) from %s", loaded, path)
        return loaded

    def load_sample_data(self) -> int:
        """Populate the manager with a small built-in sample dataset."""
        samples = [
            ("T1", "Write report", 2, 100),
            ("T2", "Fix critical bug", 1, 190),
            ("T3", "Client call", 2, 27),
            ("T4", "Code review", 1, 27),
            ("T5", "Deploy release", 3, 80),
            ("T6", "Update docs", 3, 50),
        ]
        for task_id, name, deadline, profit in samples:
            if task_id not in self._tasks:
                self.add_task(task_id, name, deadline, profit)
        return len(samples)
