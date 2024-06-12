# Copyright (c) 2023, B & K Securities and contributors
# For license information, please see license.txt

from datetime import date, datetime, timedelta
import frappe
from frappe.model.document import Document
from frappe.utils.data import get_datetime, now_datetime

class iBeatsDataToImport(Document):
	pass


@frappe.whitelist()
def truncateIBeatsTable():
    frappe.db.truncate("iBeats Data To Import")
    
from frappe import enqueue

# @frappe.whitelist()
# def enqueue_process_data():
#    enqueue("mis.mis.doctype.ibeats_data_to_import.ibeats_data_to_import.mis_to_revenue_raw", queue='long', timeout=1800)

@frappe.whitelist()
def enqueue_last_month_raw_data():
    enqueue("mis.mis.doctype.ibeats_data_to_import.ibeats_data_to_import.mis_last_month_to_revenue_raw", queue='long', timeout=1800)

@frappe.whitelist()
def enqueue_mtd_raw_data():
    enqueue("mis.mis.doctype.ibeats_data_to_import.ibeats_data_to_import.mis_mtd_to_revenue_raw", queue='long', timeout=1800)

@frappe.whitelist()
def mis_mtd_to_revenue_raw():
    mis_to_revenue_raw("tabiBeats Data MTD")

@frappe.whitelist()
def mis_last_month_to_revenue_raw():
    mis_to_revenue_raw("tabiBeats Data To Import")
@frappe.whitelist()
def enqueue_last_month_data():
    enqueue("mis.mis.doctype.ibeats_data_to_import.ibeats_data_to_import.mis_last_month_to_revenue", queue='long', timeout=1800)

@frappe.whitelist()
def enqueue_mtd_data():
    enqueue("mis.mis.doctype.ibeats_data_to_import.ibeats_data_to_import.mis_mtd_to_revenue", queue='long', timeout=1800)

@frappe.whitelist()
def mis_mtd_to_revenue():
    mis_to_revenue("tabiBeats Data MTD")

@frappe.whitelist()
def mis_last_month_to_revenue():
    mis_to_revenue("tabiBeats Data To Import")


@frappe.whitelist()   
def mis_to_revenue(src_table_name):
    try:
        sql_query = """
            SELECT a.trx_date, COALESCE(b.sales_person, 'Unknown') AS sales_person, a.family_code, MAX(a.account_name) account_name, a.nse_symbol,MAX(a.exchange) AS exchange,MAX(d.corporate_name) AS corporate_name,MAX(c.name) AS name, MAX(a.scrip_name) AS scrip_name, a.buy_sell, SUM(a.bought_qty) AS bought_qty, SUM(a.sold_qty) AS sold_qty, MAX(a.mkt_turnover_amt)  AS mkt_turnover_amt, SUM(a.gross_brokerage) AS gross_brokerage, AVG(a.brokerage_percentage) AS brokerage_percentage, SUM(a.brokerage_percentage_as_per_slab) AS brokerage_percentage_as_per_slab, AVG(a.default_brokerage_percentage)  AS default_brokerage_percentage, SUM(a.stt_amt) AS stt_amt, SUM(a.stt_inclusive_amt) AS stt_inclusive_amt, SUM(a.trxn_charges) AS trxn_charges, SUM(a.trxn_charges_excl) AS trxn_charges_excl, SUM(a.stamp_duty) AS stamp_duty, SUM(a.stamp_duty_excl) AS stamp_duty_excl, SUM(a.gst_incl_brk_amt) AS gst_incl_brk_amt, SUM(a.sgst_amt) AS sgst_amt, SUM(a.cgst_amt) AS cgst_amt, SUM(a.igst_amt) AS igst_amt, SUM(a.ugst_amt) AS ugst_amt, SUM(a.net_brokerage_mgmt) AS net_brokerage_mgmt, SUM(a.net_brokerage_excl_stt_stax_stampduty_trxn_charges) AS net_brokerage_excl_stt_stax_stampduty_trxn_charges,  MAX(a.group1) AS group1, 
CASE WHEN SUM(a.bought_qty) =0 THEN NULL ELSE SUM(a.buy_market_rate*a.bought_qty)/SUM(a.bought_qty) END AS buy_market_rate, 
CASE WHEN SUM(a.sold_qty) =0 THEN NULL ELSE 
SUM(a.sell_market_rate*a.sold_qty)/SUM(a.sold_qty) END AS sell_market_rate, segment, MAX(a.pan_no) AS pan_no, MAX(a.mbrok_code) AS mbrok_code, MAX(a.bkm_code) AS bkm_code, MAX(a.product_code) AS product_code, MAX(a.option_type) AS option_type 
FROM `{src_table_name}` a 
LEFT JOIN `tabClient Sales Person Mapping` b ON a.family_code = b.client_code 
Left Join `tabCustomer` c ON a.family_code = c.client_code 
Left Join `tabCorporate` d On (a.nse_symbol=d.nse_code)
WHERE a.exchange = 'NSE' 
GROUP BY a.trx_date, a.family_code, a.nse_symbol, a.segment, a.buy_sell 
UNION 
SELECT a.trx_date, COALESCE(b.sales_person, 'Unknown') AS sales_person, a.family_code, MAX(a.account_name) account_name, a.nse_symbol,MAX(a.exchange) AS exchange,MAX(d.corporate_name) AS corporate_name,MAX(c.name) AS name, MAX(a.scrip_name) AS scrip_name, a.buy_sell, SUM(a.bought_qty) AS bought_qty, SUM(a.sold_qty) AS sold_qty, MAX(a.mkt_turnover_amt)  AS mkt_turnover_amt, SUM(a.gross_brokerage) AS gross_brokerage, AVG(a.brokerage_percentage) AS brokerage_percentage, SUM(a.brokerage_percentage_as_per_slab) AS brokerage_percentage_as_per_slab, AVG(a.default_brokerage_percentage)  AS default_brokerage_percentage, SUM(a.stt_amt) AS stt_amt, SUM(a.stt_inclusive_amt) AS stt_inclusive_amt, SUM(a.trxn_charges) AS trxn_charges, SUM(a.trxn_charges_excl) AS trxn_charges_excl, SUM(a.stamp_duty) AS stamp_duty, SUM(a.stamp_duty_excl) AS stamp_duty_excl, SUM(a.gst_incl_brk_amt) AS gst_incl_brk_amt, SUM(a.sgst_amt) AS sgst_amt, SUM(a.cgst_amt) AS cgst_amt, SUM(a.igst_amt) AS igst_amt, SUM(a.ugst_amt) AS ugst_amt, SUM(a.net_brokerage_mgmt) AS net_brokerage_mgmt, SUM(a.net_brokerage_excl_stt_stax_stampduty_trxn_charges) AS net_brokerage_excl_stt_stax_stampduty_trxn_charges,  MAX(a.group1) AS group1, 
CASE WHEN SUM(a.bought_qty) =0 THEN NULL ELSE SUM(a.buy_market_rate*a.bought_qty)/SUM(a.bought_qty) END AS buy_market_rate, 
CASE WHEN SUM(a.sold_qty) =0 THEN NULL ELSE 
SUM(a.sell_market_rate*a.sold_qty)/SUM(a.sold_qty) END AS sell_market_rate, segment, MAX(a.pan_no) AS pan_no, MAX(a.mbrok_code) AS mbrok_code, MAX(a.bkm_code) AS bkm_code, MAX(a.product_code) AS product_code, MAX(a.option_type) AS option_type 
FROM `{src_table_name}` a 
LEFT JOIN `tabClient Sales Person Mapping` b ON a.family_code = b.client_code 
Left Join `tabCustomer` c ON a.family_code = c.client_code 
Left Join `tabCorporate` d On (a.nse_symbol=d.nse_code)
WHERE a.exchange = 'BSE' 
GROUP BY a.trx_date, a.family_code, a.nse_symbol, a.segment, a.buy_sell; 
        """.format(src_table_name=src_table_name)
        results = frappe.db.sql(sql_query, as_dict=True)
        date_query="""SELECT MAX(trx_date) AS max_trx_date, MIN(trx_date) AS min_trx_date FROM `{src_table_name}`;
        """.format(src_table_name=src_table_name)
        max_min_date=frappe.db.sql(date_query,as_dict=True)
        for date_val in max_min_date:
            max_date=date_val.max_trx_date
            min_date=date_val.min_trx_date
        delete_previous_data = '''
                    DELETE FROM tabRevenue 
                    WHERE trx_date BETWEEN "{min_date}" AND "{max_date}";
                '''.format(min_date=min_date, max_date=max_date)
        delete_data=frappe.db.sql(delete_previous_data)
        
        for source_doc in results:
            target_doc = frappe.get_doc({
                "doctype": "Revenue",
					"trx_date": source_doc.trx_date,
					"account_name": source_doc.account_name,
					"client": source_doc.name,
					"sales_person": source_doc.sales_person,
					"buy_sell": source_doc.buy_sell,
					"corporate": source_doc.corporate_name,
					"gross_brokerage": source_doc.gross_brokerage,
					"stt_amt": source_doc.stt_amt,
					"stamp_duty": source_doc.stamp_duty,
					"cgst_amt": source_doc.cgst_amt,
                    "net_brokerage_excl_stt_stax_stampduty_trxn_charges": source_doc.net_brokerage_excl_stt_stax_stampduty_trxn_charges,
                    "buy_market_rate": source_doc.buy_market_rate,
                    "bkm_code": source_doc.bkm_code,
                    "family_code": source_doc.family_code,
                    "sub_account_code": source_doc.sub_account_code,
                    "bought_qty": source_doc.bought_qty,
                    "brokerage_percentage": source_doc.brokerage_percentage,
                    "stt_inclusive_amt": source_doc.stt_inclusive_amt,
                    "stamp_duty_excl": source_doc.stamp_duty_excl,
                    "igst_amt": source_doc.igst_amt,
                    "exchange": source_doc.exchange,
                    "sell_market_rate": source_doc.sell_market_rate,
                    "account_code": source_doc.account_code,
                    "nse_symbol": source_doc.nse_symbol,
                    "sold_qty": source_doc.sold_qty,
                    "brokerage_percentage_as_per_slab": source_doc.brokerage_percentage_as_per_slab,
                    "trxn_charges": source_doc.trxn_charges,
                    "gst_incl_brk_amt": source_doc.gst_incl_brk_amt,
                    "ugst_amt": source_doc.ugst_amt,
                    "net_brokerage_mgmt": source_doc.net_brokerage_mgmt,
                    "segment": source_doc.segment,
                    "cp_code": source_doc.cp_code,
                    "scrip_name": source_doc.scrip_name,
                    "mkt_turnover_amt": source_doc.mkt_turnover_amt,
                    "default_brokerage_percentage": source_doc.default_brokerage_percentage,
                    "trxn_charges_excl": source_doc.trxn_charges_excl,
                    "sgst_amt": source_doc.sgst_amt,
                    "group1": source_doc.group1,
                    "pan_no": source_doc.pan_no,
                    "mbrok_code": source_doc.mbrok_code
            })

            target_doc.save()
            frappe.db.commit()
            
           
    except Exception as e:
        frappe.log_error(f"Error in send_data_to_revenue: {str(e)}")
        return f"Error occurred during data transfer: {str(e)}"

@frappe.whitelist()
def rq_last_month_data():
    processes = frappe.get_all("RQ Job", filters={"job_name": "mis.mis.doctype.ibeats_data_to_import.ibeats_data_to_import.mis_last_month_to_revenue", "status":('in',('started','queued'))})
    if processes:
        return 1
    else:
        return None

@frappe.whitelist()
def rq_mtd_data():
    processes = frappe.get_all("RQ Job", filters={"job_name": "mis.mis.doctype.ibeats_data_to_import.ibeats_data_to_import.mis_mtd_to_revenue", "status":('in',('started','queued'))})
    if processes:
        return 1
    else:
        return None


@frappe.whitelist()
def mis_to_revenue_raw(src_table_name):
    try:
        sql_query = """
            SELECT 
                a.trx_date,
                a.contract_no,
                a.trx_key,
                b.sales_person AS sales_person,
                a.family_code,
                a.account_name AS account_name,
                a.nse_symbol,
                a.exchange AS exchange,
                d.corporate_name AS corporate_name,
                c.name AS name,
                a.scrip_name AS scrip_name,
                a.buy_sell,
                a.bought_qty AS bought_qty,
                a.sold_qty AS sold_qty,
                a.mkt_turnover_amt AS mkt_turnover_amt,
                a.gross_brokerage AS gross_brokerage,
                a.brokerage_percentage AS brokerage_percentage,
                a.brokerage_percentage_as_per_slab AS brokerage_percentage_as_per_slab,
                a.default_brokerage_percentage AS default_brokerage_percentage,
                a.stt_amt AS stt_amt,
                a.stt_inclusive_amt AS stt_inclusive_amt,
                a.trxn_charges AS trxn_charges,
                a.trxn_charges_excl AS trxn_charges_excl,
                a.stamp_duty AS stamp_duty,
                a.stamp_duty_excl AS stamp_duty_excl,
                a.gst_incl_brk_amt AS gst_incl_brk_amt,
                a.sgst_amt AS sgst_amt,
                a.cgst_amt AS cgst_amt,
                a.igst_amt AS igst_amt,
                a.ugst_amt AS ugst_amt,
                a.net_brokerage_mgmt AS net_brokerage_mgmt,
                a.net_brokerage_excl_stt_stax_stampduty_trxn_charges AS net_brokerage_excl_stt_stax_stampduty_trxn_charges,
                a.group1 AS group1,  
                a.buy_market_rate AS buy_market_rate, 
                a.sell_market_rate AS sell_market_rate, 
                a.segment,
                a.pan_no AS pan_no,
                a.mbrok_code AS mbrok_code,
                a.bkm_code AS bkm_code,
                a.product_code AS product_code,
                a.option_type AS option_type, 
                a.account_code AS account_code,
                a.cp_code AS cp_code,
                a.sub_account_code AS sub_account_code
            FROM 
                `{src_table_name}` a 
            LEFT JOIN 
                `tabClient Sales Person Mapping` b ON a.family_code = b.client_code 
            LEFT JOIN 
                `tabCustomer` c ON a.family_code = c.client_code 
            LEFT JOIN 
                `tabCorporate` d ON a.nse_symbol = d.nse_code
            WHERE 
                a.exchange = 'NSE' 

            UNION 

            SELECT 
                a.trx_date,
                a.contract_no,
                a.trx_key,
                b.sales_person AS sales_person,
                a.family_code,
                a.account_name AS account_name,
                a.nse_symbol,
                a.exchange AS exchange,
                d.corporate_name AS corporate_name,
                c.name AS name,
                a.scrip_name AS scrip_name,
                a.buy_sell,
                a.bought_qty AS bought_qty,
                a.sold_qty AS sold_qty,
                a.mkt_turnover_amt AS mkt_turnover_amt,
                a.gross_brokerage AS gross_brokerage,
                a.brokerage_percentage AS brokerage_percentage,
                a.brokerage_percentage_as_per_slab AS brokerage_percentage_as_per_slab,
                a.default_brokerage_percentage AS default_brokerage_percentage,
                a.stt_amt AS stt_amt,
                a.stt_inclusive_amt AS stt_inclusive_amt,
                a.trxn_charges AS trxn_charges,
                a.trxn_charges_excl AS trxn_charges_excl,
                a.stamp_duty AS stamp_duty,
                a.stamp_duty_excl AS stamp_duty_excl,
                a.gst_incl_brk_amt AS gst_incl_brk_amt,
                a.sgst_amt AS sgst_amt,
                a.cgst_amt AS cgst_amt,
                a.igst_amt AS igst_amt,
                a.ugst_amt AS ugst_amt,
                a.net_brokerage_mgmt AS net_brokerage_mgmt,
                a.net_brokerage_excl_stt_stax_stampduty_trxn_charges AS net_brokerage_excl_stt_stax_stampduty_trxn_charges,
                a.group1 AS group1,  
                a.buy_market_rate AS buy_market_rate, 
                a.sell_market_rate AS sell_market_rate, 
                a.segment,
                a.pan_no AS pan_no,
                a.mbrok_code AS mbrok_code,
                a.bkm_code AS bkm_code,
                a.product_code AS product_code,
                a.option_type AS option_type, 
                a.account_code AS account_code,
                a.cp_code AS cp_code,
                a.sub_account_code AS sub_account_code
            FROM 
                `{src_table_name}` a 
            LEFT JOIN 
                `tabClient Sales Person Mapping` b ON a.family_code = b.client_code 
            LEFT JOIN 
                `tabCustomer` c ON a.family_code = c.client_code 
            LEFT JOIN 
                `tabCorporate` d ON a.nse_symbol = d.nse_code
            WHERE 
                a.exchange = 'BSE' 
                
        """.format(src_table_name=src_table_name)

        results = frappe.db.sql(sql_query, as_dict=True)
        
        salesperson_mapping_query="""SELECT t1.family_code,t3.customer_name
        FROM `{src_table_name}` AS t1
        LEFT JOIN `tabCustomer` AS t3 ON t1.family_code = t3.client_code
        WHERE t1.family_code  IN (
            SELECT t2.client_code
            FROM `tabClient Sales Person Mapping` AS t2
            
            );""".format(src_table_name=src_table_name)
        salesperson_mapping_result=frappe.db.sql(salesperson_mapping_query,as_dict=True)  
        for sales_person_value in   salesperson_mapping_result:
            frappe.get_doc({
                "doctype":"Client Sales Person Mapping",
                "client_code":sales_person_value.family_code,
                "client_name":sales_person_value.customer_name,
                "sales_person":"Unknown"
            })
        
        min_trx_date = frappe.db.sql("""SELECT MIN(trx_date) FROM `{src_table_name}`""".format(src_table_name=src_table_name))[0][0]
        max_trx_date = frappe.db.sql("""SELECT MAX(trx_date) FROM `{src_table_name}`""".format(src_table_name=src_table_name))[0][0]
        for source_doc in results:
            existing_doc = frappe.get_all(doctype="Revenue Raw", filters={"trx_key": source_doc.trx_key, "trx_date": ["between", [min_trx_date, max_trx_date]]})
            for doc in existing_doc:
                name=  doc["name"]
            if existing_doc:
                target_doc = frappe.get_doc("Revenue Raw", name)
                
                target_doc.contract_no = source_doc.contract_no
                target_doc.trx_key = source_doc.trx_key
                target_doc.trx_date = source_doc.trx_date
                target_doc.account_name = source_doc.account_name
                target_doc.client = source_doc.name
                target_doc.sales_person = source_doc.sales_person
                target_doc.buy_sell = source_doc.buy_sell
                target_doc.corporate = source_doc.corporate_name
                target_doc.gross_brokerage = source_doc.gross_brokerage
                target_doc.stt_amt = source_doc.stt_amt
                target_doc.stamp_duty = source_doc.stamp_duty
                target_doc.cgst_amt = source_doc.cgst_amt
                target_doc.net_brokerage_excl_stt_stax_stampduty_trxn_charges = source_doc.net_brokerage_excl_stt_stax_stampduty_trxn_charges
                target_doc.buy_market_rate = source_doc.buy_market_rate
                target_doc.bkm_code = source_doc.bkm_code
                target_doc.family_code = source_doc.family_code
                target_doc.sub_account_code = source_doc.sub_account_code
                target_doc.bought_qty = source_doc.bought_qty
                target_doc.brokerage_percentage = source_doc.brokerage_percentage
                target_doc.stt_inclusive_amt = source_doc.stt_inclusive_amt
                target_doc.stamp_duty_excl = source_doc.stamp_duty_excl
                target_doc.igst_amt = source_doc.igst_amt
                target_doc.exchange = source_doc.exchange
                target_doc.sell_market_rate = source_doc.sell_market_rate
                target_doc.account_code = source_doc.account_code
                target_doc.nse_symbol = source_doc.nse_symbol
                target_doc.sold_qty = source_doc.sold_qty
                target_doc.brokerage_percentage_as_per_slab = source_doc.brokerage_percentage_as_per_slab
                target_doc.trxn_charges = source_doc.trxn_charges
                target_doc.gst_incl_brk_amt = source_doc.gst_incl_brk_amt
                target_doc.ugst_amt = source_doc.ugst_amt
                target_doc.net_brokerage_mgmt = source_doc.net_brokerage_mgmt
                target_doc.segment = source_doc.segment
                target_doc.cp_code = source_doc.cp_code
                target_doc.scrip_name = source_doc.scrip_name
                target_doc.mkt_turnover_amt = source_doc.mkt_turnover_amt
                target_doc.default_brokerage_percentage = source_doc.default_brokerage_percentage
                target_doc.trxn_charges_excl = source_doc.trxn_charges_excl
                target_doc.sgst_amt = source_doc.sgst_amt
                target_doc.group1 = source_doc.group1
                target_doc.pan_no = source_doc.pan_no
                target_doc.mbrok_code = source_doc.mbrok_code
                target_doc.deleted = 0
                
                target_doc.save()
                frappe.db.commit()
            else:
                if min_trx_date <= source_doc.trx_date <= max_trx_date:# Insert new document
                    target_doc = frappe.get_doc({
                        "doctype": "Revenue Raw",
                        "contract_no": source_doc.contract_no,
                        "trx_key": source_doc.trx_key,
                        "trx_date": source_doc.trx_date,
                        "account_name": source_doc.account_name,
                        "client": source_doc.name,
                        "sales_person": source_doc.sales_person,
                        "buy_sell": source_doc.buy_sell,
                        "corporate": source_doc.corporate_name,
                        "gross_brokerage": source_doc.gross_brokerage,
                        "stt_amt": source_doc.stt_amt,
                        "stamp_duty": source_doc.stamp_duty,
                        "cgst_amt": source_doc.cgst_amt,
                        "net_brokerage_excl_stt_stax_stampduty_trxn_charges": source_doc.net_brokerage_excl_stt_stax_stampduty_trxn_charges,
                        "buy_market_rate": source_doc.buy_market_rate,
                        "bkm_code": source_doc.bkm_code,
                        "family_code": source_doc.family_code,
                        "sub_account_code": source_doc.sub_account_code,
                        "bought_qty": source_doc.bought_qty,
                        "brokerage_percentage": source_doc.brokerage_percentage,
                        "stt_inclusive_amt": source_doc.stt_inclusive_amt,
                        "stamp_duty_excl": source_doc.stamp_duty_excl,
                        "igst_amt": source_doc.igst_amt,
                        "exchange": source_doc.exchange,
                        "sell_market_rate": source_doc.sell_market_rate,
                        "account_code": source_doc.account_code,
                        "nse_symbol": source_doc.nse_symbol,
                        "sold_qty": source_doc.sold_qty,
                        "brokerage_percentage_as_per_slab": source_doc.brokerage_percentage_as_per_slab,
                        "trxn_charges": source_doc.trxn_charges,
                        "gst_incl_brk_amt": source_doc.gst_incl_brk_amt,
                        "ugst_amt": source_doc.ugst_amt,
                        "net_brokerage_mgmt": source_doc.net_brokerage_mgmt,
                        "segment": source_doc.segment,
                        "cp_code": source_doc.cp_code,
                        "scrip_name": source_doc.scrip_name,
                        "mkt_turnover_amt": source_doc.mkt_turnover_amt,
                        "default_brokerage_percentage": source_doc.default_brokerage_percentage,
                        "trxn_charges_excl": source_doc.trxn_charges_excl,
                        "sgst_amt": source_doc.sgst_amt,
                        "group1": source_doc.group1,
                        "pan_no": source_doc.pan_no,
                        "mbrok_code": source_doc.mbrok_code
                    })
                    target_doc.save()
                    frappe.db.commit()
        update_query = """
    UPDATE `tabRevenue Raw`
    SET deleted = 1, deleted_time = %s
    WHERE deleted_time IS NULL And trx_date BETWEEN %s AND %s 
    and trx_key IN (
                SELECT DISTINCT trx_key
                FROM `tabRevenue Raw`
                WHERE trx_key NOT IN (
                    SELECT DISTINCT trx_key
                    FROM `{src_table_name}`
                )
            );""".format(src_table_name=src_table_name)
        current_datetime = datetime.now()
        current_datetime_formatted = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
        frappe.db.sql(update_query, (current_datetime_formatted,min_trx_date, max_trx_date))
        frappe.db.commit()

    except Exception as e:
        frappe.log_error(f"Error in test: {str(e)}")
        


@frappe.whitelist()
def dashboard_data():
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
    """.format(type="IBEATS_LAST_MONTH_FETCH")
    results_last_run = frappe.db.sql(sql_last_run, as_dict=True)

    # Logic from mis_data_to_imp function
    min_max_date = """
        SELECT
            MIN(trx_date) AS from_date,
            MAX(trx_date) AS to_date,
            count(*) as ibeats_count
        FROM
            `tabiBeats Data To Import`;
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
            `tabiBeats Data To Import`;
    """
    ibeats_data_imp_brokerage_result = frappe.db.sql(ibeats_data_imp_brokerage, as_dict=True)
    from_date_last=results_last_run[0]['From Date']
    to_date_last=results_last_run[0]['To Date']
    last_run_datetime_string=results_last_run[0]['Last Run time']
    
    date_from = datetime.strptime(from_date_last, '%Y-%m-%d')
    formatted_date_from = date_from.strftime('%d-%b-%Y')
    date_to = datetime.strptime(to_date_last, '%Y-%m-%d')
    formatted_date_to = date_to.strftime('%d-%b-%Y')
    last_run_datetime = datetime.strptime(str(last_run_datetime_string), '%Y-%m-%d %H:%M:%S')
    # last_run_datetime = datetime.strptime(last_run_datetime_string, '%Y-%m-%d %H:%M:%S')
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
        "ibeats_record":ibeats_count,
        "ibeats_brokerage": ibeats_brokerage_cur,
        "revenue_brokerage": revenue_brokerage_cur,
        "from_date": formatted_date_from,
        "to_date": formatted_date_to,
        "revenue_records":revenue_records,
        "revenue_raw_records":revenue_raw_records,
        "revenue_raw_brokerage":revenue_raw_brokerage_cur,
        "datetime_last_run":formatted_datetime_last_run
    }

    return result_dict


@frappe.whitelist()
def get_ibeats_data_to_imp_revenue_raw_version_count():
    count_query = """
        SELECT count(*) as count
        FROM tabVersion 
        WHERE ref_doctype = 'Revenue Raw' 
        AND docname IN (
            SELECT name 
            FROM `tabRevenue Raw`
            WHERE family_code != 'ERR' 
            AND trx_date BETWEEN  (
        SELECT MIN(trx_date) 
        FROM `tabiBeats Data To Import`
    ) AND (SELECT MAX(trx_date) 
        FROM `tabiBeats Data To Import`) 
        );
    """
    result = frappe.db.sql(count_query, as_dict=True)
    return result[0]['count'] 

@frappe.whitelist()
def get_ibeats_data_to_imp_revenue_raw_deleted_count():
    count_query = """
        SELECT
        COUNT(*) as count
        FROM
            `tabRevenue Raw`
        WHERE
            trx_date BETWEEN  (
        SELECT MIN(trx_date) 
        FROM `tabiBeats Data To Import`
    ) AND (SELECT MAX(trx_date) 
        FROM `tabiBeats Data To Import`) AND deleted=1
    """
    result = frappe.db.sql(count_query, as_dict=True)
    return result[0]['count'] 

@frappe.whitelist()
def get_ibeats_mtd_revenue_raw_deleted_count():
    count_query = """
        SELECT
        COUNT(*) as count
        FROM
            `tabRevenue Raw`
        WHERE
            deleted=1
            AND
            trx_date BETWEEN  (
        SELECT MIN(trx_date) 
        FROM `tabiBeats Data MTD`
    ) AND (SELECT MAX(trx_date) 
        FROM `tabiBeats Data MTD`)
    """
    result = frappe.db.sql(count_query, as_dict=True)
    return result[0]['count'] 

@frappe.whitelist()
def get_ibeats_mtd_revenue_raw_version_count():
    count_query = """
        SELECT count(*) as count
        FROM tabVersion 
        WHERE ref_doctype = 'Revenue Raw' 
        AND docname IN (
            SELECT name 
            FROM `tabRevenue Raw`
            WHERE family_code != 'ERR' 
            AND trx_date BETWEEN  (
        SELECT MIN(trx_date) 
        FROM `tabiBeats Data MTD`
    ) AND (SELECT MAX(trx_date) 
        FROM `tabiBeats Data MTD`) 
        );
    """
    result = frappe.db.sql(count_query, as_dict=True)
    return result[0]['count'] 