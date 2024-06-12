# Copyright (c) 2024, B & K Securities and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import date, datetime, timedelta

class iBeatsDataMTD(Document):
	pass

@frappe.whitelist()
def truncateIBeatsMTDTable():
    frappe.db.truncate("iBeats Data MTD")

@frappe.whitelist()
def mis_MTD():
    # Logic from last_run function
    sql_last_run = """
        SELECT
            SUBSTRING_INDEX(job_attribute_1, '~', -1) AS `Total Records`,
            SUBSTRING_INDEX(SUBSTRING_INDEX(job_attribute_1, '~', 1),'~',-1 ) AS `From Date`,
            SUBSTRING_INDEX(SUBSTRING_INDEX(job_attribute_1, '~', 2),'~',-1 ) AS `To Date`,
            last_run_time AS `Last Run time`
        FROM
            `tabLast Run`
        WHERE
            job_type="{type}"
    """.format(type="IBEATS_MTD_FETCH")
    results_last_run = frappe.db.sql(sql_last_run, as_dict=True)

    # Logic from mis_data_to_imp function
    min_max_date = """
        SELECT
            MIN(trx_date) AS from_date,
            MAX(trx_date) AS to_date,
            count(*) as ibeats_count
        FROM
            `tabiBeats Data MTD`;
    """
    min_max = frappe.db.sql(min_max_date, as_dict=True)
    from_date = min_max[0]['from_date']
    to_date = min_max[0]['to_date']
    ibeats_count=min_max[0]['ibeats_count']
    
    revenue_brokerage_query = """
        SELECT
        COUNT(*) as revenue_count,
           sum(net_brokerage_mgmt) as revenue_brokerage
        FROM
            tabRevenue
        WHERE
            trx_date BETWEEN '{from_date}' AND '{to_date}';
    """.format(from_date=from_date, to_date=to_date)
 
    revenue_brokerage_result = frappe.db.sql(revenue_brokerage_query, as_dict=True)
    
    revenue_raw_brokerage_query = """
        SELECT
        COUNT(*) as revenue_raw_count,
           sum(net_brokerage_mgmt) as revenue_raw_brokerage
        FROM
            `tabRevenue Raw`
        WHERE
            trx_date BETWEEN '{from_date}' AND '{to_date} AND deleted=0';
    """.format(from_date=from_date, to_date=to_date)
 
    revenue_raw_brokerage_result = frappe.db.sql(revenue_raw_brokerage_query, as_dict=True)
    

    ibeats_data_imp_brokerage = """
        SELECT
            sum(net_brokerage_mgmt) as ibeats_brokerage
        FROM
            `tabiBeats Data MTD`;
    """
    ibeats_data_imp_brokerage_result = frappe.db.sql(ibeats_data_imp_brokerage, as_dict=True)
    
    last_run_datetime_string=results_last_run[0]['Last Run time']
    
    date_from = datetime.strptime(str(from_date), '%Y-%m-%d')
    formatted_date_from = date_from.strftime('%d-%b-%Y')
    date_to = datetime.strptime(str(to_date), '%Y-%m-%d')
    formatted_date_to = date_to.strftime('%d-%b-%Y')
    last_run_datetime = datetime.strptime(str(last_run_datetime_string), '%Y-%m-%d %H:%M:%S')
    formatted_datetime_last_run = last_run_datetime.strftime('%d-%b-%Y %H:%M:%S')
    
    ibeats_brokerage = ibeats_data_imp_brokerage_result[0]['ibeats_brokerage']
    revenue_brokerage = revenue_brokerage_result[0]['revenue_brokerage']
    revenue_raw_brokerage=revenue_raw_brokerage_result[0]['revenue_raw_brokerage']
    revenue_records=revenue_brokerage_result[0]['revenue_count']
    revenue_raw_records=revenue_raw_brokerage_result[0]['revenue_raw_count']
    ibeats_brokerage_cur = frappe.format(ibeats_brokerage, dict(fieldtype='Currency'))
    revenue_brokerage_cur = frappe.format(revenue_brokerage, dict(fieldtype='Currency'))
    revenue_raw_brokerage_cur=frappe.format(revenue_raw_brokerage, dict(fieldtype='Currency'))
    # Prepare the result dictionary
    result_dict = {
        "last_run_data": results_last_run,
        "ibeats_brokerage": ibeats_brokerage_cur,
        "ibeats_record":ibeats_count,
        "revenue_brokerage": revenue_brokerage_cur,
        "from_date": formatted_date_from,
        "to_date": formatted_date_to,
        "revenue_records":revenue_records,
        "revenue_raw_records":revenue_raw_records,
        "revenue_raw_brokerage":revenue_raw_brokerage_cur,
        "datetime_last_run":formatted_datetime_last_run
    }

    return result_dict