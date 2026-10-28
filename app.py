import json
from pathlib import Path
from datetime import date

FILE = Path(__file__).with_name("tasks.json")


def load_tasks():
    if FILE.exists():
        try:
            with open(FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            print("Could not load saved tasks.")
    return []


def save_tasks(tasks):
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=4)


def add_task(tasks):
    print("\n--- ADD STUDY TASK ---")
    subject = input("Enter subject: ").strip()
    title = input("Enter assignment name: ").strip()

    if not subject or not title:
        print("Subject and assignment cannot be empty.")
        return

    while True:
        deadline = input("Enter deadline (YYYY-MM-DD): ").strip()
        try:
            date.fromisoformat(deadline)
            break
        except ValueError:
            print("Invalid date. Example: 2026-11-05")

    priority = input("Priority (High/Medium/Low): ").strip().title()
    if priority not in ["High", "Medium", "Low"]:
        priority = "Medium"

    task_id = max((t["id"] for t in tasks), default=0) + 1

    tasks.append({
        "id": task_id,
        "subject": subject,
        "title": title,
        "deadline": deadline,
        "priority": priority,
        "completed": False
    })

    save_tasks(tasks)
    print("Task added and saved successfully!")


def view_tasks(tasks):
    print("\n--- YOUR STUDY TASKS ---")

    if not tasks:
        print("No tasks found.")
        return

    today = date.today()

    for task in sorted(tasks, key=lambda t: t["deadline"]):
        deadline = date.fromisoformat(task["deadline"])

        if task["completed"]:
            status = "Completed"
        elif deadline < today:
            status = "Overdue"
        elif deadline == today:
            status = "Due Today"
        else:
            status = "Upcoming"

        print("-" * 35)
        print("ID       :", task["id"])
        print("Subject  :", task["subject"])
        print("Task     :", task["title"])
        print("Deadline :", task["deadline"])
        print("Priority :", task["priority"])
        print("Status   :", status)


def complete_task(tasks):
    view_tasks(tasks)

    if not tasks:
        return

    try:
        task_id = int(input("\nEnter task ID to complete: "))
    except ValueError:
        print("Enter a valid number.")
        return

    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = True
            save_tasks(tasks)
            print("Task marked as completed!")
            return

    print("Task ID not found.")


def show_progress(tasks):
    total = len(tasks)
    completed = sum(t["completed"] for t in tasks)

    print("\n--- STUDY PROGRESS ---")
    print("Total tasks     :", total)
    print("Completed tasks :", completed)
    print("Remaining tasks :", total - completed)

    if total:
        percentage = completed / total * 100
        print(f"Progress        : {percentage:.1f}%")
        bars = int(percentage // 10)
        print("[" + "#" * bars + "-" * (10 - bars) + "]")
    else:
        print("Add tasks to start tracking progress.")


def delete_task(tasks):
    view_tasks(tasks)

    if not tasks:
        return

    try:
        task_id = int(input("\nEnter task ID to delete: "))
    except ValueError:
        print("Enter a valid number.")
        return

    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            save_tasks(tasks)
            print("Task deleted successfully!")
            return

    print("Task ID not found.")


def main():
    tasks = load_tasks()

    while True:
        print("\n" + "=" * 42)
        print("       SMART STUDENT STUDY PLANNER")
        print("=" * 42)
        print("1. Add Study Task")
        print("2. View All Tasks")
        print("3. Mark Task Completed")
        print("4. View Progress")
        print("5. Delete Task")
        print("6. Save and Exit")

        choice = input("Enter choice (1-6): ").strip()

        if choice == "1":
            add_task(tasks)
        elif choice == "2":
            view_tasks(tasks)
        elif choice == "3":
            complete_task(tasks)
        elif choice == "4":
            show_progress(tasks)
        elif choice == "5":
            delete_task(tasks)
        elif choice == "6":
            save_tasks(tasks)
            print("Tasks saved. Happy studying!")
            break
        else:
            print("Invalid choice. Enter 1 to 6.")


if __name__ == "__main__":
    main()