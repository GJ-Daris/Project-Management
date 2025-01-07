import frappe
from frappe.utils import getdate, today

# @frappe.whitelist()
def set_tasks_as_overdue():
    """
    Custom implementation of set_tasks_as_overdue.
    Adds custom logic for handling overdue tasks.
    """
    print("Custom: Starting set_tasks_as_overdue job")

    tasks = frappe.get_all(
        "Task",
        filters={"status": ["not in", ["Cancelled", "Completed"]]},
        fields=["name", "status", "review_date"],
    )

    for task in tasks:
        if task.status == "Pending Review":
            if getdate(task.review_date) > getdate(today()):
                continue

        # Example custom logic: Log the task being processed
        print(f"Processing Task: {task.name}")

        # Update the status of the task
        task_doc = frappe.get_doc("Task", task.name)
        task_doc.update_status()

        # Custom field update (if needed)
        if hasattr(task_doc, "custom_is_overdue"):
            task_doc.custom_is_overdue = True
            task_doc.save()

    frappe.db.commit()  # Commit the changes
    print("Custom: Completed set_tasks_as_overdue job")
