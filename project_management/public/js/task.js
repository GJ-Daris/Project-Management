frappe.ui.form.on('Task', {
    refresh: function (frm) {
        if (frm.doc.project) {
            // Fetch project name by project
            frappe.db.get_value('Project', { name: frm.doc.project }, 'project_name')
                .then(r => frm.set_value('custom_project_name', r.message ? r.message.project_name : ''))
                .catch(() => frm.set_value('custom_project_name', ''));
        }

        if (frm.doc.parent_task) {
            // Fetch parent task's subject
            frappe.db.get_value('Task', { name: frm.doc.parent_task }, 'subject')
                .then(r => frm.set_value('custom_parent_task_name', r.message ? r.message.subject : ''))
                .catch(() => frm.set_value('custom_parent_task_name', ''));
        }
    },
});

frappe.listview_settings["Task"] = {
    get_indicator: function (doc) {
        var colors = {
            Open: "orange",
            Assign: "orange",
            Working: "orange",
            Clearify: "orange",
            Testing: "orange",
            "Testing Fail": "red",
            "Pending Review": "blue",
            Working: "orange",
            Completed: "green",
            Cancelled: "dark grey",
            Template: "blue",
        };
        return [__(doc.status), colors[doc.status], "status,=," + doc.status];
    },
};
