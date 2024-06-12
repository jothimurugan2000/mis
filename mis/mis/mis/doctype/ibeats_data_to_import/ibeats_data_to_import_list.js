frappe.listview_settings['iBeats Data To Import'] = {
    onload: function(listview) {
        // Declare processButton outside the onload function
        var processButton;

        processButton = listview.page.add_inner_button(__("Add to Revenue"), function() {
            console.log("Process Started");
            process_data(listview);
            setTimeout(function() {
                checkJobStatus(listview);
            }, 1000);
            
        });

        function checkJobStatus(listview) {
            frappe.call({
                method: 'mis.mis.doctype.ibeats_data_to_import.ibeats_data_to_import.rq_last_month_data',
                args: {},
                callback: function (r) {
                    // console.log("callback")
                    var status = r.message;
                    console.log(status)
                    if (r.message) {
                        // console.log("checking job status")
                        processButton.prop('disabled', true);
                        setTimeout(function() {
                            checkJobStatus(listview);
                        }, 30000);
                    } else {
                        processButton.prop('disabled', false);
                    }
                }
            });
        }
        
    
    }
};

function process_data(listview) {
    console.log('Processing data...');
    frappe.call({
        method: 'mis.mis.doctype.ibeats_data_to_import.ibeats_data_to_import.enqueue_last_month_data',
        args: {},
        callback: function (r) {
            // console.log(r.message);
        }
    });
}
