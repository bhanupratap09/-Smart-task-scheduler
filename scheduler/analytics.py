"""
analytics.py
------------
MODULE 3: Analytics & Reporting

Responsible for turning a raw ScheduleResult (module 2 output) into
human-readable reports:
    - Summary statistics (total profit, success rate, counts)
    - A text-based Gantt-style timeline of slot assignments
    - A rejected-tasks breakdown

Keeping reporting separate from scheduling means the algorithm module
stays pure/testable, and the presentation layer can change (e.g. CLI
today, a future web dashboard) without touching the algorithm.
"""

from __future__ import annotations

from typing import List

from scheduler.scheduler_engine import ScheduleResult


def summary_stats(result: ScheduleResult) -> dict:
    return {
        "total_tasks": result.total_tasks,
        "scheduled_count": len(result.scheduled),
        "rejected_count": len(result.rejected),
        "total_profit": result.total_profit,
        "success_rate_pct": round(result.success_rate, 2),
    }


def format_summary(result: ScheduleResult) -> str:
    stats = summary_stats(result)
    lines = [
        "=" * 50,
        "SCHEDULE SUMMARY",
        "=" * 50,
        f"Total tasks submitted : {stats['total_tasks']}",
        f"Tasks scheduled       : {stats['scheduled_count']}",
        f"Tasks rejected        : {stats['rejected_count']}",
        f"Success rate          : {stats['success_rate_pct']}%",
        f"Total profit earned   : {stats['total_profit']:.2f}",
        "=" * 50,
    ]
    return "\n".join(lines)


def format_gantt(result: ScheduleResult) -> str:
    """Render slot assignments as a simple text Gantt chart, e.g.:

        Slot 1: [T2] Fix critical bug   (profit 190)
        Slot 2: [T1] Write report       (profit 100)
        Slot 3: [T5] Deploy release     (profit 80)
    """
    by_id = {t.task_id: t for t in result.scheduled}
    lines = ["-" * 50, "TIMELINE (Gantt view)", "-" * 50]
    for idx, task_id in enumerate(result.slot_assignment, start=1):
        if task_id is None:
            lines.append(f"Slot {idx}: [ -- idle -- ]")
        else:
            t = by_id[task_id]
            lines.append(f"Slot {idx}: [{t.task_id}] {t.name:<20} (profit {t.profit:.2f})")
    lines.append("-" * 50)
    return "\n".join(lines)


def format_rejected(result: ScheduleResult) -> str:
    if not result.rejected:
        return "No tasks were rejected — all tasks fit within their deadlines."
    lines = ["-" * 50, "REJECTED TASKS (deadline conflicts)", "-" * 50]
    for t in result.rejected:
        lines.append(str(t))
    lines.append("-" * 50)
    return "\n".join(lines)


def full_report(result: ScheduleResult) -> str:
    return "\n\n".join(
        [format_summary(result), format_gantt(result), format_rejected(result)]
    )
