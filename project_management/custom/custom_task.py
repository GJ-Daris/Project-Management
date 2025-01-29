import frappe
from frappe.utils import today, getdate

def set_tasks_as_overdue():
    # Current date captured once to avoid multiple calls to 'today()'
    current_date = today()

    # Get all tasks that are not Cancelled or Completed, and have a set expiration date
    tasks = frappe.get_all(
        "Task",
        filters={
            'status': ['not in', ["Cancelled", "Completed"]],
            'exp_end_date': ['is', 'set']  # Ensure exp_end_date is not null
        },
        fields=["name", "exp_end_date", "status", "review_date"]
    )

    # Update overdue tasks in bulk
    for task in tasks:
        # Skip tasks that are 'Pending Review' and have a future review date
        if task['status'] == "Pending Review" and getdate(task['review_date']) > getdate(current_date):
            continue

        # Check if the expiration date is past the current date
        if getdate(task['exp_end_date']) < getdate(current_date):
            # Direct database update without loading the document
            frappe.db.set_value("Task", task['name'], "custom_is_overdue", True, update_modified=False)

    # Commit changes if not in a transaction
    frappe.db.commit()
