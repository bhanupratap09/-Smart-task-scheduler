"""
main.py
-------
CLI entry point for the Smart Task Scheduler.

Presents an interactive menu that lets the user:
    1. Add a task
    2. Edit a task
    3. Remove a task
    4. List all tasks
    5. Load sample data
    6. Run the scheduler (Greedy Job Sequencing with Deadlines)
    7. Save / load tasks to/from a JSON file
    8. Exit

Run with:  python main.py
"""

from __future__ import annotations

import logging
import time

from scheduler.task_manager import TaskManager
from scheduler.scheduler_engine import schedule_optimized, schedule_naive
from scheduler import analytics
from scheduler.validators import parse_positive_int, parse_non_negative_float, parse_non_empty_str
from scheduler.exceptions import SchedulerError
from scheduler.logger_config import configure_logging

DATA_FILE = "data/tasks.json"

MENU = """
============================
 SMART TASK SCHEDULER (CLI)
============================
1. Add task
2. Edit task
3. Remove task
4. List tasks
5. Load sample data
6. Run scheduler (Greedy)
7. Compare naive vs optimized performance
8. Save tasks to file
9. Load tasks from file
0. Exit
----------------------------
"""


def prompt_new_task(manager: TaskManager) -> None:
    try:
        task_id = parse_non_empty_str(input("Task ID (e.g. T1): "), "Task ID")
        name = parse_non_empty_str(input("Task name: "), "Task name")
        deadline = parse_positive_int(input("Deadline (positive integer time slot): "), "Deadline")
        profit = parse_non_negative_float(input("Profit: "), "Profit")
        task = manager.add_task(task_id, name, deadline, profit)
        print(f"✔ Added: {task}")
    except SchedulerError as exc:
        print(f"✘ Error: {exc}")


def prompt_edit_task(manager: TaskManager) -> None:
    task_id = input("Task ID to edit: ").strip()
    print("Leave a field blank to keep its current value.")
    try:
        name = input("New name: ").strip() or None
        deadline_raw = input("New deadline: ").strip()
        profit_raw = input("New profit: ").strip()
        deadline = parse_positive_int(deadline_raw, "Deadline") if deadline_raw else None
        profit = parse_non_negative_float(profit_raw, "Profit") if profit_raw else None
        task = manager.edit_task(task_id, name=name, deadline=deadline, profit=profit)
        print(f"✔ Updated: {task}")
    except SchedulerError as exc:
        print(f"✘ Error: {exc}")


def prompt_remove_task(manager: TaskManager) -> None:
    task_id = input("Task ID to remove: ").strip()
    try:
        manager.remove_task(task_id)
        print(f"✔ Removed task {task_id}")
    except SchedulerError as exc:
        print(f"✘ Error: {exc}")


def list_tasks(manager: TaskManager) -> None:
    tasks = manager.list_tasks()
    if not tasks:
        print("No tasks yet. Use option 1 to add one, or 5 to load sample data.")
        return
    print(f"\n{len(tasks)} task(s):")
    for t in sorted(tasks, key=lambda x: x.task_id):
        print(f"  {t}")


def run_scheduler(manager: TaskManager) -> None:
    try:
        manager.require_non_empty()
        result = schedule_optimized(manager.list_tasks())
        print("\n" + analytics.full_report(result))
    except SchedulerError as exc:
        print(f"✘ Error: {exc}")


def compare_performance(manager: TaskManager) -> None:
    """Demonstrates the performance non-functional requirement by timing
    both algorithm implementations on the current task set."""
    try:
        manager.require_non_empty()
    except SchedulerError as exc:
        print(f"✘ Error: {exc}")
        return

    tasks = manager.list_tasks()

    start = time.perf_counter()
    naive_result = schedule_naive(tasks)
    naive_time = time.perf_counter() - start

    start = time.perf_counter()
    opt_result = schedule_optimized(tasks)
    opt_time = time.perf_counter() - start

    print("\n" + "=" * 50)
    print("PERFORMANCE COMPARISON")
    print("=" * 50)
    print(f"Tasks in set          : {len(tasks)}")
    print(f"Naive   (O(n^2))      : {naive_time*1000:.4f} ms | profit={naive_result.total_profit:.2f}")
    print(f"Optimized (O(n log n)): {opt_time*1000:.4f} ms | profit={opt_result.total_profit:.2f}")
    assert naive_result.total_profit == opt_result.total_profit, "Algorithms disagree!"
    print("Both algorithms agree on total profit ✔")
    print("=" * 50)


def save_tasks(manager: TaskManager) -> None:
    try:
        manager.save_to_file(DATA_FILE)
        print(f"✔ Saved {len(manager)} task(s) to {DATA_FILE}")
    except OSError as exc:
        print(f"✘ Could not save file: {exc}")


def load_tasks(manager: TaskManager) -> None:
    try:
        count = manager.load_from_file(DATA_FILE)
        print(f"✔ Loaded {count} task(s) from {DATA_FILE}")
    except FileNotFoundError as exc:
        print(f"✘ {exc}")


def main() -> None:
    configure_logging()
    logger = logging.getLogger("scheduler.main")
    logger.info("Smart Task Scheduler started.")

    manager = TaskManager()

    actions = {
        "1": lambda: prompt_new_task(manager),
        "2": lambda: prompt_edit_task(manager),
        "3": lambda: prompt_remove_task(manager),
        "4": lambda: list_tasks(manager),
        "5": lambda: print(f"✔ Loaded {manager.load_sample_data()} sample task(s).")
        if len(manager) == 0
        else print("Sample data skipped (tasks already exist)."),
        "6": lambda: run_scheduler(manager),
        "7": lambda: compare_performance(manager),
        "8": lambda: save_tasks(manager),
        "9": lambda: load_tasks(manager),
    }

    while True:
        print(MENU)
        choice = input("Choose an option: ").strip()
        if choice == "0":
            logger.info("Smart Task Scheduler exiting.")
            print("Goodbye!")
            break
        action = actions.get(choice)
        if action is None:
            print("✘ Invalid option, please try again.")
            continue
        try:
            action()
        except Exception as exc:  # last-resort safety net (reliability)
            logger.exception("Unexpected error while handling option %s", choice)
            print(f"✘ Unexpected error: {exc}")


if __name__ == "__main__":
    main()
