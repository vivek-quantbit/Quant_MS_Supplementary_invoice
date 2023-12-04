# Copyright (c) 2023, Quantbit and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class RateAdjustmentRequest(Document):
	@frappe.whitelist()
	def get_item_details(self):
		for i in self.get("old_blanket_order"):
			frappe.msgprint(str(i.old_blanket_order))