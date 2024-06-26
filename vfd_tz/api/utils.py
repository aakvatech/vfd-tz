# -*- coding: utf-8 -*-
# Copyright (c) 2020, Aakvatech and contributors
# For license information, please see license.txt

import frappe
from frappe import _
import base64
import re
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization.pkcs12 import (
    load_key_and_certificates,
)
from cryptography.hazmat.backends import default_backend


def to_base64(value):
    data_bytes = value.encode("ascii")
    data = base64.b64encode(data_bytes)
    return str(data)[2:-1]


def get_signature(data, doc):
    """
    doc is registration doc
    """
    if not doc.certificate:
        return
    p12 = get_p12_certificate(doc)
    pkey = p12[0]

    sign = pkey.sign(data.encode(), padding.PKCS1v15(), hashes.SHA1())
    data_base64 = base64.b64encode(sign)
    signature = str(data_base64)[2:-1]

    return signature


def get_cert_serial(registration_doc):
    if not registration_doc.certificate:
        return
    p12 = get_p12_certificate(registration_doc)
    cert = p12[1]
    cert_serial = cert.serial_number
    cert_serial_hex = "{0:#0{1}x}".format(cert_serial, 4)[2:]
    t = iter(cert_serial_hex)
    cert_serial_hex_spaced = " ".join(a + b for a, b in zip(t, t))
    return cert_serial_hex_spaced


def get_absolute_path(file_name, is_private=False):
    from frappe.utils import cstr

    site_name = cstr(frappe.local.site)
    if file_name.startswith("/files/"):
        file_name = file_name[7:]
    return (
        frappe.utils.get_bench_path()
        + "/sites/"
        + site_name
        + "/"
        + frappe.utils.get_path(
            "private" if is_private else "public", "files", file_name
        )[1:]
    )


def get_p12_certificate(registration_doc):
    link = get_absolute_path(registration_doc.certificate)
    key_file = open(link, "rb")
    key = key_file.read()
    key_file.close()
    password = registration_doc.get_password("certificate_password").encode()
    p12 = load_key_and_certificates(key, password, default_backend())
    return p12


def remove_special_characters(text):
    return re.sub("[^A-Za-z0-9 ]+", "", text)


def remove_all_except_numbers(text=None):
    if not text:
        return ""
    return re.sub("[^0-9]+", "", text)


def get_latest_registration_doc(company, throw=True):
    doc_list = frappe.get_all(
        "VFD Registration",
        filters={"docstatus": 1, "company": company, "r_status": "Active"},
    )
    if not len(doc_list):
        if throw:
            frappe.throw(
                _(
                    "No active registration found for {0}. Please contact VFD Provider."
                ).format(company)
            )
        return
    doc = frappe.get_doc("VFD Registration", doc_list[0].name)
    if doc.is_blocked:
        frappe.log_error(
            _("VFD for {0} is blocked").format(company),
            "VFD Blocked",
        )
        if throw:
            frappe.throw(
                _(
                    "VFD is BLOCKED for <b>{1}</b>.<br>Message from TRA:<br><b>{0}</b>".format(
                        doc.tra_message, company
                    )
                )
            )
        else:
            frappe.msgprint(
                _(
                    "VFD is BLOCKED for <b>{1}</b>.<br>Message from TRA:<br><b>{0}</b>".format(
                        doc.tra_message, company
                    )
                )
            )
    if not doc.vfd_start_date:
        frappe.log_error(
            (_("VFD Start Date not set for {0} in VFD Registration").format(company)),
            "VFD Not Started",
        )
        frappe.throw(
            _(
                "VFD Start Date not set in VFD Registration. Please set it in VFD Registration"
            )
        )
    return doc


def check_vfd_status():
    from vfd_tz.vfd_tz.doctype.vfd_token.vfd_token import (
        check_vfd_status as _check_vfd_status,
    )

    _check_vfd_status()


def clean_and_update_tax_id_info(doc, method):
    cleaned_tax_id = "".join(char for char in (doc.tax_id or "") if char.isdigit())
    doc.tax_id = cleaned_tax_id
    if doc.tax_id:
        doc.vfd_cust_id_type = "1- TIN"
        doc.vfd_cust_id = doc.tax_id
    else:
        doc.vfd_cust_id_type = "6- Other"
        doc.vfd_cust_id = "999999999"
