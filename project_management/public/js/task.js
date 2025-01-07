// Helper function: Toggle read_only on specified fields
function toggleReadOnly(frm, fields, isReadOnly) {
    fields.forEach(field => frm.set_df_property(field, "read_only", isReadOnly ? 1 : 0));
}

// Helper function: Fetch and set a value from the database to the form
async function fetchAndSetValue(doctype, filters, sourceField, frm, targetField) {
    try {
        const { message } = await frappe.db.get_value(doctype, filters, sourceField);
        frm.set_value(targetField, message ? message[sourceField] : "");
    } catch (error) {
        console.error(`Error fetching ${sourceField} for ${doctype}:`, error);
        frm.set_value(targetField, "");
    }
}

// Form events for Task
frappe.ui.form.on("Task", {
    refresh(frm) {
        const isManager = frappe.user.has_role("Task Manager");

        // Set exp_start_date & exp_end_date as read-only for non-managers on existing documents
        /*
            if (!frm.is_new() && (frm.doc.exp_start_date || frm.doc.exp_end_date)) {
                toggleReadOnly(frm, ["exp_start_date", "exp_end_date"], !isManager);
            }
        */

        // Fetch project name and set in custom_project_name
        if (frm.doc.project) {
            fetchAndSetValue("Project", { name: frm.doc.project }, "project_name", frm, "custom_project_name");
        }

        // Fetch parent task’s subject and set in custom_parent_task_name
        if (frm.doc.parent_task) {
            fetchAndSetValue("Task", { name: frm.doc.parent_task }, "subject", frm, "custom_parent_task_name");
        }

        // Make custom_is_overdue editable only for Task Managers
        frm.set_df_property("custom_is_overdue", "read_only", !isManager);
    },
});

// ListView settings for Task
frappe.listview_settings["Task"] = {
    get_indicator(doc) {
        const statusColors = {
            Open: "red",
            Assign: "orange",
            Working: "orange",
            Clearify: "orange",
            Testing: "orange",
            "Testing Fail": "red",
            "Pending Review": "blue",
            Completed: "green",
            Cancelled: "dark grey",
            Template: "blue",
            Overdue: "red"
        };

        const color = statusColors[doc.status] || "grey";
        return [__(doc.status), color, `status,=,${doc.status}`];
    }
};
