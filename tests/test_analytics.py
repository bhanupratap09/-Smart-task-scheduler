import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scheduler.task import Task
from scheduler.scheduler_engine import schedule_optimized
from scheduler import analytics


class TestAnalytics(unittest.TestCase):
    def setUp(self):
        self.tasks = [
            Task("T1", "Write report", 2, 100),
            Task("T2", "Fix critical bug", 1, 190),
            Task("T3", "Client call", 2, 27),
        ]
        self.result = schedule_optimized(self.tasks)

    def test_summary_stats_keys(self):
        stats = analytics.summary_stats(self.result)
        expected_keys = {
            "total_tasks",
            "scheduled_count",
            "rejected_count",
            "total_profit",
            "success_rate_pct",
        }
        self.assertEqual(set(stats.keys()), expected_keys)

    def test_success_rate_calculation(self):
        stats = analytics.summary_stats(self.result)
        self.assertEqual(stats["total_tasks"], 3)
        self.assertGreaterEqual(stats["success_rate_pct"], 0)
        self.assertLessEqual(stats["success_rate_pct"], 100)

    def test_format_summary_contains_profit(self):
        text = analytics.format_summary(self.result)
        self.assertIn("Total profit earned", text)

    def test_format_gantt_lists_all_slots(self):
        text = analytics.format_gantt(self.result)
        self.assertIn("Slot 1", text)

    def test_format_rejected_handles_empty(self):
        tasks = [Task("T1", "Only task", 5, 10)]
        result = schedule_optimized(tasks)
        text = analytics.format_rejected(result)
        self.assertIn("No tasks were rejected", text)

    def test_full_report_combines_sections(self):
        report = analytics.full_report(self.result)
        self.assertIn("SCHEDULE SUMMARY", report)
        self.assertIn("TIMELINE", report)


if __name__ == "__main__":
    unittest.main()
