frappe.ui.form.on('Task', {
    refresh: function(frm) {
        // ซ่อนฟิลด์ task_weight
        frm.toggle_display('task_weight', false);
    },
    custom_work_stage: function(frm) {
        // ตั้งค่า status ตาม custom_work_stage ถ้าเป็นค่าในลิสต์ที่กำหนดไว้
        const valid_statuses = ['Open', 'Working', 'Pending Review', 'Overdue', 'Template', 'Completed', 'Cancelled'];
        frm.set_value('status', valid_statuses.includes(frm.doc.custom_work_stage) ? frm.doc.custom_work_stage : 'Working');
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
