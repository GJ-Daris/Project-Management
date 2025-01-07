// Helper function: Toggle read_only on specified fields
function set_fields_read_only(frm, fields, read_only) {
    fields.forEach(field => frm.set_df_property(field, "read_only", read_only ? 1 : 0));
}

// Helper function: Fetch a field value from DB and set it in the form
function fetch_and_set_value(doctype, filters, source_field, frm, target_field) {
    return frappe.db.get_value(doctype, filters, source_field)
        .then(r => {
            frm.set_value(
                target_field,
                r.message ? r.message[source_field] : ""
            );
        })
        .catch(() => {
            frm.set_value(target_field, "");
        });
}

frappe.ui.form.on("Task", {
    refresh(frm) {
        // Check if user has the "Task Manager" role
        const is_manager = frappe.user.has_role("Task Manager");

        // 1) Handle read-only for exp_start_date & exp_end_date on existing documents
        if (!frm.is_new() && (frm.doc.exp_start_date || frm.doc.exp_end_date)) {
            set_fields_read_only(frm, ["exp_start_date", "exp_end_date"], !is_manager);
        }

        // 2) Fetch project name
        if (frm.doc.project) {
            fetch_and_set_value(
                "Project",
                { name: frm.doc.project },
                "project_name",
                frm,
                "custom_project_name"
            );
        }

        // 3) Fetch parent task’s subject
        if (frm.doc.parent_task) {
            fetch_and_set_value(
                "Task",
                { name: frm.doc.parent_task },
                "subject",
                frm,
                "custom_parent_task_name"
            );
        }

        // 4) Make 'custom_is_overdue' editable only if user has 'Task Manager' role
        frm.set_df_property("custom_is_overdue", "read_only", !is_manager);

        // 5) Disable 'status' 
        //    - or user is not Task Manager
        const disable_status =
            !is_manager &&
            (!frm.doc.exp_end_date || new Date() > new Date(frm.doc.exp_end_date))
        frm.set_df_property("status", "read_only", disable_status);
    },
});

// Listview indicator
frappe.listview_settings["Task"] = {
    get_indicator: function (doc) {
        const colors = {
            Open: "orange",
            Assign: "orange",
            Working: "orange",
            Clearify: "orange",
            Testing: "orange",
            "Testing Fail": "red",
            "Pending Review": "blue",
            Completed: "green",
            Cancelled: "dark grey",
            Template: "blue",
        };
        return [__(doc.status), colors[doc.status], "status,=," + doc.status];
    },
};
