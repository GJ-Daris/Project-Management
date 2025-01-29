import frappe
from frappe.utils import today, add_days

def set_tasks_as_overdue():
    # Current date captured once to avoid multiple calls to 'today()'
    current_date = today()

    # Get all tasks that are not Cancelled or Completed, and are overdue
    tasks = frappe.get_all(
        "Task",
        filters={
            'status': ['not in', ["Cancelled", "Completed"]],
            'exp_end_date': ['<', current_date],  # Directly filter overdue tasks
        },
        fields=["name", "exp_end_date"]
    )

    # Update overdue tasks in bulk
    for task in tasks:
        # Direct database update without loading the document
        frappe.db.set_value("Task", task.name, "custom_is_overdue", True, update_modified=False)

    # Commit changes if not in a transaction
    frappe.db.commit()
