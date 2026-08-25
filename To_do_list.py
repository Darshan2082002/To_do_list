import json 
import os 
import argparse
import sys

BASE_DIR = os.path.dirname(os.path.abspath(sys.argv[0]))
DEFAULT_DB = os.path.join(BASE_DIR, "task.json")


class Task():
    def __init__(self, task_id, title, completed=False):
        self.task_id = task_id
        self.title = title
        self.completed = completed

class To_do_list():
    def __init__(self):
        self.tasks = []  # Changed to self.tasks (plural)

    def add_task(self, title):
        new_id = len(self.tasks) + 1
        new_task = Task(task_id=new_id, title=title)
        self.tasks.append(new_task)
        print(f"Added: '{title}' (ID: {new_id})")

    def delete_task(self, task_id):
        for t in self.tasks:
            if t.task_id == task_id:
                self.tasks.remove(t)
                print(f"Deleted task {task_id}")
                return 
        print("Nothing to delete (ID not found)")

    def save_to_file(self, filename="task.json"):
        data = []
        for t in self.tasks:
            data.append({
                "task_id": t.task_id,
                "title": t.title,
                "completed": t.completed
            })
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)
        print("Tasks saved successfully!")

    def load_from_file(self, filename="task.json"):
        if not os.path.exists(filename):
            print("No saved file found. Starting with an empty list.")
            return 
        with open(filename, "r") as f:
            data = json.load(f)
        
        self.tasks = []
        for item in data:
            reconstructed_task = Task(
                task_id=item["task_id"], 
                title=item["title"], 
                completed=item["completed"]
            )
            self.tasks.append(reconstructed_task)

    def view_task(self):
        if not self.tasks:
            print("No tasks found.")
            return 
        for t in self.tasks:
            status = "[X]" if t.completed else "[ ]"
            print(f"{t.task_id}. {status} {t.title}")
    
    def toggle_task(self, task_id):
        for t in self.tasks:
            if t.task_id == task_id:
                t.completed = not t.completed
                status = "completed" if t.completed else "incomplete"
                print(f"Task {task_id} marked as {status}")
                return
        print("Task ID not found")


def main():
    todo = To_do_list()
    todo.load_from_file()  # Load first

    parser = argparse.ArgumentParser(description="Terminal To-Do List App")
    subparsers = parser.add_subparsers(dest="command")

    parser_add = subparsers.add_parser("add", help="Add a new task")
    parser_add.add_argument("title", type=str, help="Task description")

    subparsers.add_parser("view", help="View all tasks")

    parser_toggle = subparsers.add_parser("toggle", help="Toggle task status")
    parser_toggle.add_argument("id", type=int, help="Task ID to toggle")

    parser_delete = subparsers.add_parser("delete", help="Delete a task")
    parser_delete.add_argument("id", type=int, help="Task ID to delete")

    args = parser.parse_args()

    # Save to file automatically after mutations
    if args.command == "add":
        todo.add_task(args.title)
        todo.save_to_file()
    elif args.command == "view":
        todo.view_task()
    elif args.command == "toggle":
        todo.toggle_task(args.id)
        todo.save_to_file()
    elif args.command == "delete":
        todo.delete_task(args.id)
        todo.save_to_file()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()