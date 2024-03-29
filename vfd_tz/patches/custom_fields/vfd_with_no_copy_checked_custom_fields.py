import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields


def execute():
    fields = {
        "Customer": [
            {
                "label": "VFD Customer ID",
                "no_copy": 1,
                "insert_after": "vfd_details",
                "translatable": 1,
                "fieldname": "vfd_cust_id",
                "fieldtype": "Data",
                "module_def": "vfd-tz",
            },
            {
                "label": "VFD Customer ID Type",
                "no_copy": 1,
                "insert_after": "vfd_cust_id",
                "translatable": 1,
                "fieldname": "vfd_cust_id_type",
                "fieldtype": "Select",
                "options": "\n1- TIN\n2- Passport\n3- Driving License\n4- Voter ID\n5- Aadhaar\n6- Other",
                "module_def": "vfd-tz",
            },
            {
                "label": "VFD Customer ID",
                "no_copy": 1,
                "insert_after": "tax_category",
                "translatable": 1,
                "fieldname": "vfd_custid",
                "fieldtype": "Data",
            },
            {
                "label": "VFD Customer ID Type",
                "no_copy": 1,
                "insert_after": "vfd_custid",
                "translatable": 1,
                "fieldname": "vfd_custidtype",
                "fieldtype": "Select",
                "options": "\n1- TIN\n2- Driving License\n3- Voters Number\n4- Passport\n5- NID\\xa0 (National Identity)\n6- NIL (If there is no ID)",
            },
            {
                "label": "VFD Details",
                "no_copy": 1,
                "insert_after": "csf_tz_close_dn_after",
                "fieldname": "vfd_details",
                "fieldtype": "Section Break",
                "module_def": "vfd-tz",
            },
        ],
        "Sales Invoice": [
            {
                "fetch_from": "customer.vfd_custid",
                "no_copy": 1,
                "label": "VFD Cust ID",
                "insert_after": "vfd_cust_id_type",
                "translatable": 1,
                "fieldname": "vfd_cust_id",
                "fieldtype": "Data",
                "fetch_if_empty": 1,
            },
            {
                "fetch_from": "customer.vfd_custidtype",
                "no_copy": 1,
                "label": "VFD Cust ID Type",
                "insert_after": "vfd_serial",
                "translatable": 1,
                "fieldname": "vfd_cust_id_type",
                "fieldtype": "Data",
                "fetch_if_empty": 1,
            },
            {
                "no_copy": 1,
                "read_only": 1,
                "label": "VFD Date",
                "insert_after": "vfd_details",
                "fieldname": "vfd_date",
                "fieldtype": "Date",
            },
            {
                "no_copy": 1,
                "read_only": 1,
                "label": "VFD DC",
                "insert_after": "update_status",
                "allow_on_submit": 1,
                "fieldname": "vfd_dc",
                "fieldtype": "Int",
            },
            {
                "collapsible": 1,
                "no_copy": 1,
                "depends_on": 'eval: !in_list(frappe.user_roles, "Healthcare Receptionist")',
                "label": "VFD Details",
                "insert_after": "authotp",
                "fieldname": "vfd_details",
                "fieldtype": "Section Break",
            },
            {
                "no_copy": 1,
                "read_only": 1,
                "label": "VFD GC",
                "insert_after": "vfd_dc",
                "allow_on_submit": 1,
                "fieldname": "vfd_gc",
                "fieldtype": "Int",
            },
            {
                "no_copy": 1,
                "read_only": 1,
                "label": "VFD Posting Info",
                "insert_after": "vfd_time",
                "allow_on_submit": 1,
                "fieldname": "vfd_posting_info",
                "fieldtype": "Link",
                "options": "VFD Invoice Posting Info",
            },
            {
                "no_copy": 1,
                "read_only": 1,
                "label": "VFD RCTNUM",
                "insert_after": "vfd_posting_info",
                "allow_on_submit": 1,
                "translatable": 1,
                "fieldname": "vfd_rctnum",
                "fieldtype": "Data",
            },
            {
                "no_copy": 1,
                "read_only": 1,
                "label": "VFD RCTVNUM",
                "insert_after": "vfd_rctnum",
                "allow_on_submit": 1,
                "translatable": 1,
                "fieldname": "vfd_rctvnum",
                "fieldtype": "Data",
            },
            {
                "no_copy": 1,
                "read_only": 1,
                "label": "VFD SERIAL",
                "insert_after": "vfd_gc",
                "allow_on_submit": 1,
                "translatable": 1,
                "fieldname": "vfd_serial",
                "fieldtype": "Data",
            },
            {
                "no_copy": 1,
                "in_list_view": 1,
                "read_only": 1,
                "label": "VFD Status",
                "insert_after": "column_break_vfd",
                "allow_on_submit": 1,
                "default": "Not Sent",
                "in_standard_filter": 1,
                "translatable": 1,
                "fieldname": "vfd_status",
                "fieldtype": "Select",
                "options": "Not Sent\nPending\nFailed\nSuccess",
            },
            {
                "no_copy": 1,
                "read_only": 1,
                "label": "VFD Time",
                "insert_after": "vfd_date",
                "allow_on_submit": 1,
                "fieldname": "vfd_time",
                "fieldtype": "Time",
            },
            {
                "read_only": 1,
                "no_copy": 1,
                "label": "VFD Verification URL",
                "insert_after": "vfd_rctvnum",
                "allow_on_submit": 1,
                "translatable": 1,
                "fieldname": "vfd_verification_url",
                "fieldtype": "Data",
            },
            {
                "label": "VFD Z Report",
                "no_copy": 1,
                "insert_after": "vfd_cust_id",
                "allow_on_submit": 1,
                "fieldname": "vfd_z_report",
                "fieldtype": "Link",
                "options": "VFD Z Report",
            },
        ],
        "Item Tax Template": [
            {
                "label": "VFD Tax Code",
                "no_copy": 1,
                "insert_after": "taxes",
                "translatable": 1,
                "fieldname": "vfd_tax_code",
                "fieldtype": "Data",
                "module_def": "vfd-tz",
            },
            {
                "label": "VFD TAXCODE",
                "no_copy": 1,
                "insert_after": "taxes",
                "translatable": 1,
                "fieldname": "vfd_taxcode",
                "fieldtype": "Select",
                "options": "\n1- Standard Rate (18%)\n2- Special Rate\n3- Zero rated\n4- Special Relief\n5- Exempt",
            },
        ],
        "Mode of Payment": [
            {
                "label": "VFD Payment Type",
                "no_copy": 1,
                "insert_after": "accounts",
                "translatable": 1,
                "fieldname": "vfd_payment_type",
                "fieldtype": "Data",
                "module_def": "vfd-tz",
            },
            {
                "label": "VFD PMTTYPE",
                "no_copy": 1,
                "insert_after": "accounts",
                "translatable": 1,
                "fieldname": "vfd_pmttype",
                "fieldtype": "Select",
                "options": "\nCASH\nCHEQUE\nCCARD\nEMONEY\nINVOICE",
            },
        ],
    }

    create_custom_fields(fields, update=True)
