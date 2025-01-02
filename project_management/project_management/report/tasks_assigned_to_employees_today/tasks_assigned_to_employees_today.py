import frappe
from frappe import _

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        {
            "label": _("Employee"),
            "fieldname": "employee_name",
            "fieldtype": "Data",
            "width": 150
        },
        {
            "label": _("Department"),
            "fieldname": "department",
            "fieldtype": "Data",
            "width": 200
        },
        {
            "label": _("Task Start Date"),
            "fieldname": "task_start_date",
            "fieldtype": "Date",
            "width": 150
        },
        {
            "label": _("Priority"),  # Added field for Priority
            "fieldname": "priority",
            "fieldtype": "Data",
            "width": 100
        },
        {
            "label": _("Task Status"),
            "fieldname": "task_status",
            "fieldtype": "Data",  # You can change this to "Select" if you want to show predefined statuses
            "width": 150
        },
        {
            "label": _("Project Name"),
            "fieldname": "project_name",
            "fieldtype": "Data",
            "width": 200
        },
        {
            "label": _("Task Code"),
            "fieldname": "task_code",
            "fieldtype": "Link",  # Set fieldtype to "Link"
            "options": "Task",    # Link to the "Task" doctype
            "width": 200
        },
        {
            "label": _("Task Name"),
            "fieldname": "subject",
            "fieldtype": "Data",
            "width": 200
        },
        {
            "label": _("Created By"),
            "fieldname": "created_by",
            "fieldtype": "Data",  # You can change this to "Link" if you want to link to the User profile
            "width": 200
        }
    ]

def get_data(filters):
    """
    This function fetches the data based on the filters provided.
    """
    # Use filters.get() to safely retrieve values with default fallbacks
    date_filter = filters.get('date')  # Get the date filter, it will be None if not provided
    task_name_null = filters.get('task_name_null', 0)  # Default to 0 if task_name_null filter is not provided
    employee_id_filter = filters.get('employee_id')  # Get the employee_id filter
    department_filter = filters.get('department')  # Get the department filter
    project_filter = filters.get('project')  # Get the project filter
    
    # Building SQL query with employee filters (if provided)
    sql_query = """
        SELECT
            emp.name AS employee_id, 
            emp.employee_name AS employee_name,
            emp.department AS department,
            task.name AS task_code,
            task.exp_start_date AS task_start_date,
            task.subject AS subject,
            proj.name AS project_code,
            proj.project_name AS project_name,
            task.owner AS created_by,  -- Add the 'owner' (Created By) field from the task
            task.status AS task_status,  -- Add the 'status' field to fetch task status,
            task.priority AS priority  -- Added priority field
        FROM 
            `tabEmployee` emp
        LEFT JOIN 
            `tabTask` task ON JSON_CONTAINS(task._assign, CONCAT('"', emp.user_id, '"'))
             AND (
                DATE(%(date)s) BETWEEN DATE(task.exp_start_date) AND DATE(task.exp_end_date) 
                OR DATE(task.exp_start_date) = %(date)s
            )
        LEFT JOIN 
            `tabProject` proj ON task.project = proj.name  -- Join with project table
        WHERE
            (%(task_name_null)s = 0 AND task.name IS NULL) OR (%(task_name_null)s = 1 AND task.name IS NOT NULL)
            AND task.status NOT IN ('Complete', 'Cancel')
    """
    
    # Add employee ID filter if provided
    if employee_id_filter:
        sql_query += " AND emp.name = %(employee_id)s"
    
    # Add department filter if provided
    if department_filter:
        sql_query += " AND emp.department = %(department)s"
    
    # Add project filter if provided
    if project_filter:
        sql_query += " AND task.project = %(project)s"
    
    # Order the results
    sql_query += " ORDER BY emp.employee_name, emp.last_name;"
    
    # Execute the query with the filters passed
    data = frappe.db.sql(sql_query, {
        'date': date_filter,
        'task_name_null': task_name_null,
        'employee_id': employee_id_filter,
        'department': department_filter,
        'project': project_filter
    }, as_dict=True)
    
    return data
