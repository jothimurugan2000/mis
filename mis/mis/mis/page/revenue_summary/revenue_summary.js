

frappe.pages['revenue-summary'].on_page_load = function(wrapper) {
    var parent = $('<div class="container"></div>').appendTo(wrapper);

    // Load jQuery
    var jqueryScript = document.createElement('script');
    jqueryScript.src = 'https://cdnjs.cloudflare.com/ajax/libs/jquery/3.7.1/jquery.min.js';
    jqueryScript.onload = function() {
        loadPivotTableResources().then(() => {
            fetchDataAndRenderPivotTable(parent);
        }).catch(error => {
            console.error("Error loading PivotTable resources:", error);
        });
    };
    jqueryScript.onerror = function() {
        console.error("Error loading jQuery");
    };
    document.head.appendChild(jqueryScript);
};

function loadPivotTableResources() {
    return new Promise((resolve, reject) => {
        var cssLoaded = false;
        var pivotJsLoaded = false;
        var subtotalJsLoaded = false;
        var customCssLoaded = false;
        var jqueryUILoaded = false;

        // Load PivotTable CSS
        var cssLinkPivot = document.createElement('link');
        cssLinkPivot.rel = 'stylesheet';
        cssLinkPivot.type = 'text/css';
        cssLinkPivot.href = 'https://cdnjs.cloudflare.com/ajax/libs/pivottable/2.23.0/pivot.min.css';
        cssLinkPivot.onload = function() {
            cssLoaded = true;
            if (cssLoaded && pivotJsLoaded && subtotalJsLoaded && customCssLoaded && jqueryUILoaded) resolve();
        };
        cssLinkPivot.onerror = reject;
        document.head.appendChild(cssLinkPivot);

        // Load Subtotal CSS
        var cssLinkSubtotal = document.createElement('link');
        cssLinkSubtotal.rel = 'stylesheet';
        cssLinkSubtotal.type = 'text/css';
        cssLinkSubtotal.href = 'https://cdnjs.cloudflare.com/ajax/libs/subtotal/1.10.0/subtotal.min.css';
        cssLinkSubtotal.onload = function() {
            cssLoaded = true;
            if (cssLoaded && pivotJsLoaded && subtotalJsLoaded && customCssLoaded && jqueryUILoaded) resolve();
        };
        cssLinkSubtotal.onerror = reject;
        document.head.appendChild(cssLinkSubtotal);

        // Load jQuery UI JS
        var jqueryUIScript = document.createElement('script');
        jqueryUIScript.src = 'https://cdnjs.cloudflare.com/ajax/libs/jqueryui/1.11.4/jquery-ui.min.js';
        jqueryUIScript.onload = function() {
            jqueryUILoaded = true;
            if (cssLoaded && pivotJsLoaded && subtotalJsLoaded && customCssLoaded && jqueryUILoaded) resolve();
        };
        jqueryUIScript.onerror = reject;
        document.head.appendChild(jqueryUIScript);


        // Load PivotTable JS
        var pivotScript = document.createElement('script');
        pivotScript.src = 'https://cdnjs.cloudflare.com/ajax/libs/pivottable/2.23.0/pivot.min.js';
        pivotScript.onload = function() {
            pivotJsLoaded = true;
            if (cssLoaded && pivotJsLoaded && subtotalJsLoaded && customCssLoaded && jqueryUILoaded) resolve();
        };
        pivotScript.onerror = reject;
        document.head.appendChild(pivotScript);

       
        
         // Load Subtotal JS
         var subtotalScript = document.createElement('script');
         subtotalScript.src = 'https://cdnjs.cloudflare.com/ajax/libs/subtotal/1.10.0/subtotal.min.js';
         subtotalScript.onload = function() {
             subtotalJsLoaded = true;
             if (cssLoaded && pivotJsLoaded && subtotalJsLoaded && customCssLoaded && jqueryUILoaded) resolve();
         };
         subtotalScript.onerror = reject;
         document.head.appendChild(subtotalScript);
 
        // Load Custom CSS
        var navbar = document.querySelectorAll('header.navbar');
        var header_top = window.getComputedStyle(navbar[0]).getPropertyValue('height');

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
                top: ${header_top};
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
            if (cssLoaded && pivotJsLoaded && subtotalJsLoaded && customCssLoaded && jqueryUILoaded) resolve();
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
                fields: ["distinct mis_sales_person_name"]
            },
            callback: function(response) {
                if (response.message.length > 0) {
                    let sales_persons = response.message.map(item => item.mis_sales_person_name);
                    fetchAndRenderReport(sales_persons, parentElement);
                } else {
                    console.log("No sales person mapped to the user");
                    fetchAndRenderReport([], parentElement);
                }
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
                fields: ["distinct mis_sales_person_name"]
            },
            callback: function(response) {
                if (response.message.length > 0) {
                    let sales_persons = response.message.map(item => item.mis_sales_person_name);
                    fetchAndRenderReport(sales_persons, parentElement);
                } else {
                    console.log("No sales person mapped to the user");
                    fetchAndRenderReport([], parentElement);
                }
            }
        });
    }
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

                const sort = (order) => {
					return (a, b) => {
						return order.indexOf(a) - order.indexOf(b);
					};
				};
				
				const uniqueMonths = Array.from(new Set(data.map(row => row.trx_date)));
				const sortedMonths = uniqueMonths.sort((a, b) => {
					const [monthA, yearA] = a.split(' ');
					const [monthB, yearB] = b.split(' ');
					if (parseInt(yearA) !== parseInt(yearB)) {
						return parseInt(yearA) - parseInt(yearB);
					}
					const monthOrder = {
						"January": 1, "February": 2, "March": 3, "April": 4, "May": 5, "June": 6,
						"July": 7, "August": 8, "September": 9, "October": 10, "November": 11, "December": 12
					};
					return monthOrder[monthA] - monthOrder[monthB];
				});
				

                if (Array.isArray(data) && data.length > 0 && typeof data[0] === 'object') {
					var dataClass = $.pivotUtilities.SubtotalPivotData;
                    var dateFormat = $.pivotUtilities.derivers.dateFormat;
                    var sortAs =           $.pivotUtilities.sortAs;
                    $(parentElement).pivotUI(
                        data, 
						{dataClass: dataClass,
                            rows: ["sales_person","family_code"],
                            cols: ["trx_date", "segment"],
                            vals: ["net_brokerage_mgmt"],
                            aggregatorName: "Sum",
                            renderers: $.extend(
                                $.pivotUtilities.renderers,
                                $.pivotUtilities.export_renderers,
                                $.pivotUtilities.subtotal_renderers,
                                $.pivotUtilities.plotly_renderers,
                            ),
                            rendererName: "Table With Subtotal",
                            derivedAttributes: {
                                "Month": dateFormat("trx_date", "%n"),
                                "Year": dateFormat("trx_date", "%y")
                            },
							rendererOptions: {
								rowSubtotalDisplay: {
									collapseAt: 0
								},
								colSubtotalDisplay: {
									collapseAt:0
								}
							},
							sorters: {
                                "Month": sortAs(["Jan","Feb","Mar","Apr", "May",
                                "Jun","Jul","Aug","Sep","Oct","Nov","Dec"]),
                                'trx_date': sort(sortedMonths)
							  }
                        }
                    );
                } else {
                    console.error("Invalid data format:", data);
                }
            } else {
                console.log("No data found");
            }
        }
    });
}
