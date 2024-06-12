

// frappe.pages['revenue-pivot'].on_page_load = function(wrapper) {
// 	var page = frappe.ui.make_app_page({
// 		parent: wrapper,
// 		title: 'None',
// 		single_column: true
// 	});
// }

frappe.pages['revenue-pivot'].on_page_load = function(wrapper) {
    var parent = $('<div class="container"></div>').appendTo(wrapper);

    // Load PivotTable resources and then fetch data and render component
    loadPivotTableResources().then(() => {
        frappe.require('mis.bundle.js').then(() => {
            
            fetchDataAndRenderPivotTable(parent[0]);
        });
    }).catch(error => {
        console.error("Error loading PivotTable resources:", error);
    });
};

function loadPivotTableResources() {
    return new Promise((resolve, reject) => {
        var cssLoaded = false;
        var jsLoaded = false;
        var customCssLoaded = false;

        // Load PivotTable CSS
        var cssLink = document.createElement('link');
        cssLink.rel = 'stylesheet';
        cssLink.type = 'text/css';
        cssLink.href = 'https://cdnjs.cloudflare.com/ajax/libs/pivottable/2.23.0/pivot.min.css';
        cssLink.onload = function() {
            cssLoaded = true;
            if (cssLoaded && jsLoaded && customCssLoaded) resolve();
        };
        cssLink.onerror = reject;
        document.head.appendChild(cssLink);

        // Load PivotTable JS
        var script = document.createElement('script');
        script.src = 'https://cdnjs.cloudflare.com/ajax/libs/pivottable/2.23.0/pivot.min.js';
        script.onload = function() {
            jsLoaded = true;
            if (cssLoaded && jsLoaded && customCssLoaded) resolve();
        };
        script.onerror = reject;
        document.head.appendChild(script);

        var navbar = document.querySelectorAll('header.navbar');
        var header_top = window.getComputedStyle(navbar[0]).getPropertyValue('height')
        // Load Custom CSS
        var customCss = document.createElement('style');
        customCss.type = 'text/css';
        customCss.innerHTML = `
            .pvtDropdownValue.pvtDropdownCurrent {
                -webkit-text-size-adjust:100%;background:#F3F3F3;border:1px solid #DEDEDE;padding:2px 5px;white-space:nowrap;-webkit-border-radius:5px;-moz-border-radius:5px;border-radius:5px
            }
            .pvtTable {
                width: 100%;
                border-collapse: collapse;
            }
            .pvtDropdownValue {
                display: flex;
                align-items: center; 
                position: relative;
            }
            
            .pvtDropdownIcon {
                position: absolute; /* Position the icon absolutely */
                right: 5px; /* Adjust the right position as needed */
                top: 50%; /* Vertically center the icon */
                transform: translateY(-50%);
            }

            
            .pvtUi {
                width: 100%; /* Make the table take full width */
                overflow-x: auto; /* Enable horizontal scrolling if needed */
            }
            
            /* Media query for smaller screens */
            @media screen and (max-width: 768px) {
                .pvtUi {
                    font-size: 14px; /* Decrease font size for smaller screens */
                }
            }
                .pvtTable thead {
                position: -webkit-sticky; /* for Safari */
                position: sticky;
                top: ` + header_top + `;
                z-index: 2;
            }

            .pvtTable tbody th {
                position: sticky;
                position: -webkit-sticky;
                width: 100px;
                min-width: 100px;
                max-width: 100px;
                left: 0px;
                z-index: 1;
            }
        `;
        customCss.onload = function() {
            customCssLoaded = true;
            if (cssLoaded && jsLoaded && customCssLoaded) resolve();
        };
        customCss.onerror = reject;
        document.head.appendChild(customCss);
    });
}


function fetchDataAndRenderPivotTable(parentElement) {
    let user = frappe.session.user;
    let user_fullname = frappe.session.user_fullname;

    if (user_fullname === "Administrator") {
        frappe.call({
            method: "frappe.client.get_list",
            args: {
                doctype: "MIS Sales Person User Mapping",
                fields: ["mis_sales_person_name"]
            },
            callback: function(response) {
                if (response.message.length > 0) {
                    sales_persons = response.message.map(item => item.mis_sales_person_name);
                    console.log(sales_persons);
                } else {
                    console.log("No sales person mapped to the user");
                }

                fetchAndRenderReport(sales_persons, parentElement);
            }
        });
    
    } else {
        frappe.call({
            method: "frappe.client.get_list",
            args: {
                doctype: "MIS Sales Person User Mapping",
                filters: {
                    "erp_user_link_user": user
                },
                fields: ["mis_sales_person_name"]
            },
            callback: function(response) {
                if (response.message.length > 0) {
                    sales_persons = response.message.map(item => item.mis_sales_person_name);
                    console.log(sales_persons);
                } else {
                    console.log("No sales person mapped to the user");
                }

                fetchAndRenderReport(sales_persons, parentElement);
            }
        });
    }

    // if (user_fullname === "Administrator") {
    //     fetchAndRenderReport(sales_persons, parentElement);
    // }
}

function fetchAndRenderReport(sales_persons, parentElement) {
    frappe.call({
        method: "frappe.desk.query_report.run",
        args: {
            report_name: "Revenue Pivot",
            filters: {
                current_user: sales_persons
            }
        },
        callback: function(r) {
            if (r.message && r.message.result) {
                const data = r.message.result;
                window.mis.renderPivotTableComponent(parentElement, data);
            } else {
                console.log("No data found");
            }
        }
    });
}

