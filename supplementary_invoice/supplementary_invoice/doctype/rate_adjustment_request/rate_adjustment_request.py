# Copyright (c) 2023, Quantbit and contributors
# For license information, please see license.txt 
import frappe
from frappe.model.document import Document
class RateAdjustmentRequest(Document):
    #for select all check mark
	@frappe.whitelist()
	def checkall(self):
		children = self.get('item_details')
		if not children:
			return
		all_selected = all([child.check for child in children])  
		value = 0 if all_selected else 1 
		for child in children:
			child.check = value
	
 
    #To get item data into item_details table
	# @frappe.whitelist()
	# def get_item_details(self):
	# 	updated_item_rate_li=[]
	# 	new_blanket_ord_details=frappe.db.sql("""select item_code,rate,name from `tabBlanket Order Item` where parent='{0}'
	# 									""".format(self.new_blanket_order),as_dict="True")
	# 	if(new_blanket_ord_details):
	# 		for k in new_blanket_ord_details:
	# 			for i in self.get("old_blanket_order"):
	# 					old_blanket_ord_details=frappe.db.sql("""select item_code,item_name,rate from `tabBlanket Order Item` where parent="{0}" and item_code='{1}'
	# 												""".format(i.old_blanket_order,k.item_code),as_dict="True")
	# 					if(old_blanket_ord_details):
	# 						for j in old_blanket_ord_details:
	# 							updated_item_rate_li.append({
	# 								"item_code":str(j["item_code"]),
	# 								"item_name":str(j["item_name"]),
	# 								"old_rate":float(j["rate"]),
	# 								"new_rate":float(k.rate),
	# 								"old_blanket_ord_name":i.old_blanket_order,
	# 								"new_blanket_ord_name":self.new_blanket_order
	# 							})
	# 							self.append("item_details",{"item_code":str(j["item_code"]),"item_name":str(j["item_name"]),"old_rate":float(j["rate"]),"old_blanket_order":i.old_blanket_order,"new_rate":float(k.rate),"new_blanket_ord_name":self.new_blanket_order})
     
		
	@frappe.whitelist()
	def get_item_details(self):
		updated_item_rate_li=[]
		new_blanket_ord_details=frappe.db.sql("""select item_code,rate,name from `tabOpen Order Details` where parent='{0}'
										""".format(self.new_blanket_order),as_dict="True")
		# frappe.throw(str(new_blanket_ord_details))
		if(new_blanket_ord_details):
			for k in new_blanket_ord_details:
				for i in self.get("old_blanket_order"):
						old_blanket_ord_details=frappe.db.sql("""select item_code,item_name,rate from `tabOpen Order Details` where parent="{0}" and item_code='{1}'
													""".format(i.old_blanket_order,k.item_code),as_dict="True")
						# frappe.throw(str(old_blanket_ord_details))
						if(old_blanket_ord_details):
							for j in old_blanket_ord_details:
								updated_item_rate_li.append({
									"item_code":str(j["item_code"]),
									"item_name":str(j["item_name"]),
									"old_rate":float(j["rate"]),
									"new_rate":float(k.rate),
									"old_blanket_ord_name":i.old_blanket_order,
									"new_blanket_ord_name":self.new_blanket_order
								})
								# frappe.throw(str(updated_item_rate_li))
								self.append("item_details",{"item_code":str(j["item_code"]),"item_name":str(j["item_name"]),"old_rate":float(j["rate"]),"old_blanket_order":i.old_blanket_order,"new_rate":float(k.rate),"new_blanket_ord_name":self.new_blanket_order})
     
		
	#To get data into sales_invoice_details table      custom_open_order
	# @frappe.whitelist()
	# def get_sales_invoice_details(self):
	# 	for i in self.get("old_blanket_order"):
	# 		sales_order_dict=frappe.db.sql("""select distinct parent from `tabSales Order Item` where blanket_order='{0}' and docstatus = '1'""".format(i.old_blanket_order),as_dict=True)
	# 		if(sales_order_dict):
	# 			for sale_ord in sales_order_dict:
	# 				sales_invoice_data=frappe.db.sql("""select distinct parent,item_code,item_name,qty,rate,sales_order from `tabSales Invoice Item` where sales_order='{0}' and docstatus = '1'""".format(sale_ord.parent),as_dict=True)
	# 				if(sales_invoice_data):
	# 					for j in self.get("item_details"):
	# 						if(j.check):
	# 							if(j.old_blanket_order==i.old_blanket_order):
	# 								for k in sales_invoice_data:
	# 									# and k.custom_new_blanket_order!=self.new_blanket_order   
	# 									if(k.item_code==j.item_code):
	# 										rate_diff=j.new_rate-k.rate
	# 										total_amt=rate_diff*k.qty
	# 										sales_invoice_date = frappe.get_value("Sales Invoice", k.parent, "posting_date")
	# 										self.append("sales_invoice_details",{"item_code":k.item_code,"qty":k.qty,"item_name":k.item_name,"sales_invoice_rate":k.rate,"sales_invoice":k.parent,"blanket_order_ref":i.old_blanket_order,"sales_order_ref":k.sales_order,"rate_difference":float(rate_diff),
	# 													"sale_date":sales_invoice_date,"new_rate":j.new_rate,"total_amount":total_amt,"new_blanket_order_name":self.new_blanket_order})
	# 				else:
	# 					frappe.throw(f"Sales Invoice not found for the Blanket Order {i.old_blanket_order} \n. Please deselect that Order")
 
    #To get data into sales_invoice_details table      
	@frappe.whitelist()
	def get_sales_invoice_details(self):
		for i in self.get("old_blanket_order"):
			sales_order_dict=frappe.db.sql("""select distinct parent from `tabSales Order Item` where custom_open_order='{0}' and docstatus = '1'""".format(i.old_blanket_order),as_dict=True)
			if(sales_order_dict):
				for sale_ord in sales_order_dict:
					sales_invoice_data=frappe.db.sql("""select distinct parent,item_code,item_name,qty,rate,sales_order from `tabSales Invoice Item` where sales_order='{0}' and docstatus = '1'""".format(sale_ord.parent),as_dict=True)
					if(sales_invoice_data):
						for j in self.get("item_details"):
							if(j.check):
								if(j.old_blanket_order==i.old_blanket_order):
									for k in sales_invoice_data:
										# and k.custom_new_blanket_order!=self.new_blanket_order   
										if(k.item_code==j.item_code):
											rate_diff=j.new_rate-k.rate
											total_amt=rate_diff*k.qty
											sales_invoice_date = frappe.get_value("Sales Invoice", k.parent, "posting_date")
											self.append("sales_invoice_details",{"item_code":k.item_code,"qty":k.qty,"item_name":k.item_name,"sales_invoice_rate":k.rate,"sales_invoice":k.parent,"blanket_order_ref":i.old_blanket_order,"sales_order_ref":k.sales_order,"rate_difference":float(rate_diff),
														"sale_date":sales_invoice_date,"new_rate":j.new_rate,"total_amount":total_amt,"new_blanket_order_name":self.new_blanket_order})
					else:
						frappe.throw(f"Sales Invoice not found for the Open Order {i.old_blanket_order} \n. Please deselect that Order")

	#To generate sales invoice entry(Credit node and debit note)					
	def before_submit(self):
		sales_invoice_li=[]
		if(self.send_individual_invoice):
			for i in self.get("sales_invoice_details"):
				if(i.sales_invoice not in sales_invoice_li):
					sales_invoice_li.append(str(i.sales_invoice))
					doc1=frappe.new_doc("Sales Invoice")
					doc1.customer=self.customer
					doc1.company = self.company
					doc1.return_against=i.sales_invoice
					doc1.is_debit_note=True
					doc1_status=0
					tax_tem=frappe.get_value("Sales Invoice",i.sales_invoice,"taxes_and_charges")
					doc2=frappe.new_doc("Sales Invoice")
					doc2.customer=self.customer
					doc2.return_against=i.sales_invoice
					doc2.is_return=True
					doc2_status=0
					for j in self.get("sales_invoice_details"):
						if(j.sales_invoice==i.sales_invoice):
							if(j.total_amount>0):
								doc1_status=1
								table_data={
									"item_code":j.item_code,"item_name":j.item_name,"qty":j.qty,"rate":j.rate_difference,"unit4":"Prod-14-11-23-00142"
								}
								doc1.append("items",table_data)
							if(j.total_amount<0):
								doc2_status=1
								table_data={
									"item_code":j.item_code,"item_name":j.item_name,"qty":float(-abs(j.qty)),"rate":abs(j.rate_difference),"unit4":"Prod-14-11-23-00142"
								}
								doc2.append("items",table_data)
					if(doc1_status):
						doc1.custom_rate_change_req_reference=self.name
						doc1.run_method("set_missing_values")
						doc1.run_method("calculate_taxes_and_totals")
						doc1.custom_rate_adjustment_request = self.name
						doc1.save()
						doc1.submit()
											
	
					if(doc2_status):
						doc2.custom_rate_change_req_reference=self.name
						doc2.run_method("set_missing_values")
						doc2.run_method("calculate_taxes_and_totals")
						doc1.custom_rate_adjustment_request = self.name
						doc2.save()
						doc2.submit()

	#To cancel Sales invoive liked with Rate Adjustment Request
	def on_cancel(self):
		doc=frappe.get_all("Sales Invoice",{'custom_rate_change_req_reference':self.name,'docstatus':'1'},['name'])
		for i in doc:
			document=frappe.get_doc("Sales Invoice",i.name)
			document.cancel()
				

	