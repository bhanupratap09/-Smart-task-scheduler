import os
import sys
import random
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scheduler.task import Task
from scheduler.scheduler_engine import schedule_naive, schedule_optimized
from scheduler.exceptions import EmptyTaskListError


class TestSchedulerEngine(unittest.TestCase):
    def setUp(self):
        # Classic textbook example:
        # Expected optimal schedule: T2 (slot1) + T1 (slot2) + T5? depends on deadlines
        self.tasks = [
            Task("T1", "Write report", 2, 100),
            Task("T2", "Fix critical bug", 1, 190),
            Task("T3", "Client call", 2, 27),
            Task("T4", "Code review", 1, 27),
            Task("T5", "Deploy release", 3, 80),
        ]

    def test_empty_task_list_raises(self):
        with self.assertRaises(EmptyTaskListError):
            schedule_optimized([])
        with self.assertRaises(EmptyTaskListError):
            schedule_naive([])

    def test_optimized_matches_naive_total_profit(self):
        naive = schedule_naive(self.tasks)
        optimized = schedule_optimized(self.tasks)
        self.assertEqual(naive.total_profit, optimized.total_profit)
        self.assertEqual(len(naive.scheduled), len(optimized.scheduled))

    def test_known_optimal_profit(self):
        # T2(190,d1), T1(100,d2), T5(80,d3) = 370 is optimal for this set
        result = schedule_optimized(self.tasks)
        self.assertEqual(result.total_profit, 370)
        self.assertEqual(len(result.scheduled), 3)

    def test_single_task_schedules_immediately(self):
        result = schedule_optimized([Task("T1", "Solo", 1, 50)])
        self.assertEqual(len(result.scheduled), 1)
        self.assertEqual(result.total_profit, 50)

    def test_all_same_deadline_only_one_fits(self):
        tasks = [Task(f"T{i}", f"Task {i}", 1, i * 10) for i in range(1, 5)]
        result = schedule_optimized(tasks)
        self.assertEqual(len(result.scheduled), 1)
        self.assertEqual(result.scheduled[0].task_id, "T4")  # highest profit = 40

    def test_rejected_tasks_are_tracked(self):
        result = schedule_optimized(self.tasks)
        self.assertEqual(len(result.rejected) + len(result.scheduled), len(self.tasks))

    def test_randomized_agreement_between_algorithms(self):
        random.seed(42)
        for _ in range(20):
            n = random.randint(1, 15)
            tasks = [
                Task(f"T{i}", f"Task{i}", random.randint(1, n), random.randint(1, 200))
                for i in range(n)
            ]
            naive = schedule_naive(tasks)
            optimized = schedule_optimized(tasks)
            self.assertEqual(
                naive.total_profit,
                optimized.total_profit,
                msg=f"Mismatch on random set: {tasks}",
            )


if __name__ == "__main__":
    unittest.main()
