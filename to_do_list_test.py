import unittest
import os
import tempfile
# Ensure this matches your actual Python filename (e.g., if your file is named todo.py, keep as 'from todo import ...')
from To_do_list import Task, To_do_list


class TestTodoList(unittest.TestCase):

    def setUp(self):
        """Creates a fresh instance and an isolated temporary file for each test."""
        self.todo = To_do_list()

        self.temp_file = tempfile.NamedTemporaryFile(delete=False)
        self.temp_filename = self.temp_file.name
        self.temp_file.close()

    def tearDown(self):
        """Cleans up temporary files after test execution."""
        if os.path.exists(self.temp_filename):
            os.remove(self.temp_filename)

    def test_add_task(self):
        """Verify adding a task appends to the list with correct initial properties."""
        self.todo.add_task("Buy groceries")
        
        # Sync alias if singular self.task was used internally
        tasks = getattr(self.todo, "tasks", getattr(self.todo, "task", []))
        
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].title, "Buy groceries")
        self.assertFalse(tasks[0].completed)

    def test_toggle_task(self):
        """Verify toggling flips completion status between True and False."""
        self.todo.add_task("Write unit tests")
        tasks = getattr(self.todo, "tasks", getattr(self.todo, "task", []))
        task_id = tasks[0].task_id

        self.assertFalse(tasks[0].completed)
        self.todo.toggle_task(task_id)
        self.assertTrue(tasks[0].completed)

    def test_delete_task(self):
        """Verify task deletion removes the correct element by ID."""
        self.todo.add_task("Task 1")
        self.todo.add_task("Task 2")
        tasks = getattr(self.todo, "tasks", getattr(self.todo, "task", []))
        self.assertEqual(len(tasks), 2)

        self.todo.delete_task(1)
        tasks_after = getattr(self.todo, "tasks", getattr(self.todo, "task", []))
        self.assertEqual(len(tasks_after), 1)
        self.assertEqual(tasks_after[0].title, "Task 2")

    def test_save_and_load(self):
        """Verify JSON serialization and deserialization across file operations."""
        self.todo.add_task("Persistent Task")
        self.todo.save_to_file(self.temp_filename)

        new_todo = To_do_list()
        new_todo.load_from_file(self.temp_filename)
        
        tasks = getattr(new_todo, "tasks", getattr(new_todo, "task", []))
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].title, "Persistent Task")


if __name__ == "__main__":
    unittest.main()