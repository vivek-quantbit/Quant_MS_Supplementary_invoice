from qr_demo.qr_code import get_qr_code
import frappe


@frappe.whitelist()
def generate_qr_code(current_doc):
    doc=frappe.get_doc("Sales Invoice",current_doc)
    qr_content = str(doc.name)
    return get_qr_code(qr_content)  