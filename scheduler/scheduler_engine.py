"""
scheduler_engine.py
--------------------
MODULE 2: Scheduling Engine

Implements the classic "Job Sequencing with Deadlines" Greedy algorithm:

    Given N tasks, each with a deadline and a profit, find a subset of
    tasks (each occupying exactly one unit-time slot) that can be
    completed within their deadlines while MAXIMIZING total profit.

Two implementations are provided for comparison (see report -> Design
Decisions & Rationale):

    1. schedule_naive()      - O(n^2) time,  O(D) space   (simple, intuitive)
    2. schedule_optimized()  - O(n log n) time, O(D) space (Union-Find / DSU)

Both return the same result; schedule_optimized() is the one used by
default because it scales to large task lists (performance requirement).

Greedy correctness argument (exchange argument):
    Sorting tasks by profit descending and always placing a task in the
    LATEST free slot at or before its deadline is optimal because:
      - Placing a task as late as possible never blocks an earlier,
        still-available slot from being used by a future (lower-profit)
        task.
      - Since tasks are processed in decreasing profit order, any task
        that CAN be scheduled without conflict is scheduled immediately,
        guaranteeing no higher-profit task is ever dropped in favor of a
        lower-profit one.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

from scheduler.task import Task
from scheduler.exceptions import EmptyTaskListError


@dataclass
class ScheduleResult:
    """Outcome of running the scheduling engine."""

    scheduled: List[Task] = field(default_factory=list)   # in time-slot order
    rejected: List[Task] = field(default_factory=list)
    slot_assignment: List[Optional[str]] = field(default_factory=list)  # index = slot-1

    @property
    def total_profit(self) -> float:
        return sum(t.profit for t in self.scheduled)

    @property
    def total_tasks(self) -> int:
        return len(self.scheduled) + len(self.rejected)

    @property
    def success_rate(self) -> float:
        if self.total_tasks == 0:
            return 0.0
        return len(self.scheduled) / self.total_tasks * 100


class _DisjointSet:
    """Union-Find with path compression, used to find the latest free slot
    at-or-before a given deadline in near-O(1) amortized time."""

    def __init__(self, size: int) -> None:
        self.parent = list(range(size + 1))

    def find(self, x: int) -> int:
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]  # path compression
            x = self.parent[x]
        return x

    def union(self, x: int, y: int) -> None:
        self.parent[self.find(x)] = self.find(y)


def schedule_naive(tasks: List[Task]) -> ScheduleResult:
    """O(n^2) reference implementation: for each task (profit-desc order),
    scan slots from its deadline down to 1 for a free one."""
    if not tasks:
        raise EmptyTaskListError("No tasks available. Add tasks before scheduling.")

    ordered = sorted(tasks, key=lambda t: t.profit, reverse=True)
    max_deadline = max(t.deadline for t in ordered)
    slots: List[Optional[str]] = [None] * (max_deadline + 1)  # 1-indexed

    scheduled_ids = set()
    for task in ordered:
        for slot in range(min(task.deadline, max_deadline), 0, -1):
            if slots[slot] is None:
                slots[slot] = task.task_id
                scheduled_ids.add(task.task_id)
                break

    return _build_result(tasks, ordered, scheduled_ids, slots[1:])


def schedule_optimized(tasks: List[Task]) -> ScheduleResult:
    """O(n log n) implementation using Union-Find to jump directly to the
    latest free slot at-or-before a task's deadline."""
    if not tasks:
        raise EmptyTaskListError("No tasks available. Add tasks before scheduling.")

    ordered = sorted(tasks, key=lambda t: t.profit, reverse=True)
    max_deadline = max(t.deadline for t in ordered)

    dsu = _DisjointSet(max_deadline)
    slots: List[Optional[str]] = [None] * (max_deadline + 1)  # 1-indexed

    scheduled_ids = set()
    for task in ordered:
        capped_deadline = min(task.deadline, max_deadline)
        free_slot = dsu.find(capped_deadline)
        if free_slot > 0:
            slots[free_slot] = task.task_id
            scheduled_ids.add(task.task_id)
            dsu.union(free_slot, free_slot - 1)  # mark slot as used

    return _build_result(tasks, ordered, scheduled_ids, slots[1:])


def _build_result(
    original_order: List[Task],
    profit_ordered: List[Task],
    scheduled_ids: set,
    slot_assignment: List[Optional[str]],
) -> ScheduleResult:
    by_id = {t.task_id: t for t in original_order}
    scheduled_in_slot_order = [by_id[tid] for tid in slot_assignment if tid is not None]
    rejected = [t for t in profit_ordered if t.task_id not in scheduled_ids]
    return ScheduleResult(
        scheduled=scheduled_in_slot_order,
        rejected=rejected,
        slot_assignment=slot_assignment,
    )
