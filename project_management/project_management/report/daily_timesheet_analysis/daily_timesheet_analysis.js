// Copyright (c) 2025, goingjesse and contributors
// For license information, please see license.txt

frappe.query_reports["Daily Timesheet Analysis"] = {
	"filters": [
        {
            "fieldname": "date",
            "label": __("Date Timesheet"),
            "fieldtype": "Date",
            "default": frappe.datetime.get_today(),
            "mandatory": 0,
            "wildcard_filter": 0
        },
        {
            "fieldname": "task_name_null",
            "label": __("Has Tasks"),
            "fieldtype": "Check",
            "default": 1,
            "mandatory": 0,
            "wildcard_filter": 0
        },
        {
            "fieldname": "employee_id",
            "label": __("Employee"),
            "fieldtype": "Link",
            "options": "Employee",
            "mandatory": 0,
            "wildcard_filter": 0
        },
        {
            "fieldname": "department",
            "label": __("Department"),
            "fieldtype": "Link",
            "options": "Department",
            "mandatory": 0,
            "wildcard_filter": 0
        },
        {
            "fieldname": "project",
            "label": __("Project"),
            "fieldtype": "Link",
            "options": "Project",
            "mandatory": 0,
            "wildcard_filter": 0
        }
    ]
};
