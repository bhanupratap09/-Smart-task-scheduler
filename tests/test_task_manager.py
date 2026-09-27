import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scheduler.task_manager import TaskManager
from scheduler.exceptions import (
    DuplicateTaskError,
    TaskNotFoundError,
    InvalidTaskDataError,
    EmptyTaskListError,
)


class TestTaskManager(unittest.TestCase):
    def setUp(self):
        self.mgr = TaskManager()

    def test_add_task_success(self):
        task = self.mgr.add_task("T1", "Write report", 2, 100)
        self.assertEqual(task.task_id, "T1")
        self.assertEqual(len(self.mgr), 1)

    def test_add_duplicate_task_raises(self):
        self.mgr.add_task("T1", "Task one", 1, 50)
        with self.assertRaises(DuplicateTaskError):
            self.mgr.add_task("T1", "Task one dup", 2, 20)

    def test_add_invalid_deadline_raises(self):
        with self.assertRaises(InvalidTaskDataError):
            self.mgr.add_task("T1", "Bad deadline", 0, 50)

    def test_add_negative_profit_raises(self):
        with self.assertRaises(InvalidTaskDataError):
            self.mgr.add_task("T1", "Bad profit", 2, -10)

    def test_remove_task(self):
        self.mgr.add_task("T1", "Task", 1, 10)
        self.mgr.remove_task("T1")
        self.assertEqual(len(self.mgr), 0)

    def test_remove_missing_task_raises(self):
        with self.assertRaises(TaskNotFoundError):
            self.mgr.remove_task("GHOST")

    def test_edit_task_partial_update(self):
        self.mgr.add_task("T1", "Old name", 1, 10)
        updated = self.mgr.edit_task("T1", profit=999)
        self.assertEqual(updated.name, "Old name")
        self.assertEqual(updated.profit, 999)

    def test_require_non_empty_raises_when_empty(self):
        with self.assertRaises(EmptyTaskListError):
            self.mgr.require_non_empty()

    def test_save_and_load_roundtrip(self, tmp_path="test_tasks_tmp.json"):
        self.mgr.add_task("T1", "Task one", 2, 50)
        self.mgr.add_task("T2", "Task two", 1, 30)
        self.mgr.save_to_file(tmp_path)

        new_mgr = TaskManager()
        count = new_mgr.load_from_file(tmp_path)
        self.assertEqual(count, 2)
        self.assertEqual(len(new_mgr), 2)

        os.remove(tmp_path)

    def test_load_sample_data(self):
        count = self.mgr.load_sample_data()
        self.assertGreater(count, 0)
        self.assertEqual(len(self.mgr), count)


if __name__ == "__main__":
    unittest.main()
