frappe.query_reports["Tasks Assigned to Employees Today"] = {
    "filters": [
        {
            "fieldname": "date",
            "label": __("Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.get_today(),
            "mandatory": 0,
            "wildcard_filter": 0
        },
        {
            "fieldname": "task_name_null",
            "label": __("Has Tasks"),
            "fieldtype": "Check",
            "default": 0,
            "mandatory": 0,
            "wildcard_filter": 0
        },
        {
            "fieldname": "employee",
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

var chart = new frappe.Chart("#chart-container", {
    title: "Tasks by Project and Status",
    data: chart_data,  // Pass the data returned from the backend
    type: 'bar',  // Specify the chart type (bar chart)
    height: 300,  // Set the chart height
    colors: ['#ff0000', '#00ff00', '#0000ff']  // Customize colors for each status
});