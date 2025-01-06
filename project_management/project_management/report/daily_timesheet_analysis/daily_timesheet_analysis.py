import frappe
from frappe import _

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        {"label": _(label), "fieldname": fieldname, "fieldtype": fieldtype, "width": width, "options": options if 'options' in locals() else None}
        for label, fieldname, fieldtype, width, options in [
            ("Timesheet", "timesheet_name", "Link", 150, "Timesheet"),
            ("Date", "timesheet_start_date", "Date", 150, None),
            ("Employee", "employee_name", "Data", 150, None),
            ("Department", "department", "Data", 150, None),
            ("Task Priority", "task_priority", "Data", 150, None),  # Added Task Priority
            ("Task Status", "task_status", "Data", 150, None),
            ("Project", "project_name", "Data", 150, None),
            ("Task Code", "task_code", "Link", 170, "Task"),
            ("Task Name", "subject", "Data", 300, None),
            ("Created By", "created_by", "Data", 200, None),
            ("Time Sheet Hours", "time_sheet_hours", "Float", 150, None),
        ]
    ]

def get_data(filters):
    filters = filters or {}

    # SQL Query for joining Employee, Task, Project, Timesheet Detail, and Timesheet tables
    sql_query = """
        SELECT
            ts.name AS timesheet_name,
            emp.employee_name AS employee_name,
            emp.department AS department,
            ts.start_date AS timesheet_start_date,
            ts.end_date AS timesheet_end_date,
            task.exp_start_date AS task_start_date,
            task.priority AS task_priority,  -- Added Task Priority
            task.subject AS subject,
            proj.project_name AS project_name,
            task.name AS task_code,
            task.owner AS created_by,
            task.status AS task_status,
            SUM(tsd.hours) AS time_sheet_hours
        FROM
            `tabEmployee` emp
        LEFT JOIN
            `tabTimesheet` ts ON ts.employee = emp.name
            AND (
                    DATE(%(date)s) BETWEEN DATE(ts.start_date) AND DATE(ts.end_date) 
                    OR DATE(ts.start_date) = %(date)s
                )
        LEFT JOIN
            `tabTimesheet Detail` tsd ON tsd.parent = ts.name
        LEFT JOIN
            `tabTask` task ON tsd.task = task.name
        LEFT JOIN
            `tabProject` proj ON proj.name = task.project
        WHERE
            (%(task_name_null)s = 0 AND task.name IS NULL)
            OR (%(task_name_null)s = 1 AND task.name IS NOT NULL)
    """

    # Add dynamic filters if provided
    if filters.get('employee_id'):
        sql_query += " AND emp.name = %(employee_id)s"
    if filters.get('department'):
        sql_query += " AND emp.department = %(department)s"
    if filters.get('project'):
        sql_query += " AND task.project = %(project)s"

    # Add grouping and sorting
    sql_query += """
        GROUP BY ts.name, emp.name, task.name
        ORDER BY emp.employee_name, emp.last_name
    """

    # Execute the query
    return frappe.db.sql(sql_query, {
        'date': filters.get('date'),
        'task_name_null': filters.get('task_name_null', 0),
        'employee_id': filters.get('employee_id'),
        'department': filters.get('department'),
        'project': filters.get('project'),
    }, as_dict=True)
