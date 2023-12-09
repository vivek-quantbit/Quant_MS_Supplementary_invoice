// Copyright (c) 2023, Quantbit and contributors
// For license information, please see license.txt
frappe.ui.form.on('Rate Adjustment Request', {
    setup: function(frm) {
		$('.layout-side-section').hide();
		$('.layout-main-section-wrapper').css('margin-left', '0');
        frm.fields_dict.old_blanket_order.get_query = function(doc, cdt, cdn) {
            return {
                filters: [
                    ['Blanket Order', 'customer', '=', frm.doc.customer],
					['Blanket Order', 'docstatus', '=', '1'],
					['Blanket Order', 'blanket_order_type', '=', 'Selling']
                ]
            }; 
        };
		frm.set_query("new_blanket_order", function(doc) {
			var old_blanket_order_li= [];	
			frm.doc.old_blanket_order.forEach(function(row) {
				old_blanket_order_li.push(row.old_blanket_order);
			});
			return{
					filters: [    
						['Blanket Order', 'customer', '=', frm.doc.customer],
						['Blanket Order', 'name','not in', old_blanket_order_li],
						['Blanket Order', 'docstatus', '=', '1'],
						['Blanket Order', 'from_date', '>=', frm.doc.from_date_rate_update],
						['Blanket Order', 'blanket_order_type', '=', 'Selling']
						]
			};
		});

    },
	new_blanket_order:function(frm){
		frm.clear_table("item_details");
        frm.refresh_field("item_details");
		frm.clear_table("sales_invoice_details");
        frm.refresh_field("sales_invoice_details");
        clearTableAndRefreshField(frm, 'sales_invoice_details', 2);
		frm.call({
			method:"get_item_details",
			doc:frm.doc
		});
	},
	get_invoice_details:function(frm){
		frm.clear_table("sales_invoice_details")
		frm.call({
			method:"get_sales_invoice_details",
			doc:frm.doc
		});
	},
	check_all:function(frm){
		frm.call({
			method:"checkall",
			doc:frm.doc
		});
	},
	send_individual_invoice: function(frm) {
        frm.doc.send_bulk_invoice = false;
        frm.refresh_field('send_bulk_invoice');
    },

    send_bulk_invoice: function(frm) {
        frm.doc.send_individual_invoice = false;
        frm.refresh_field('send_individual_invoice');
    },
	customer:function(frm){
		clearTableAndRefreshField(frm, 'item_details', 2);
        clearTableAndRefreshField(frm, 'sales_invoice_details', 2);
		frm.clear_table("old_blanket_order")
		frm.refresh_field("old_blanket_order")
		if(frm.doc.new_blanket_order)
		{
			frappe.model.set_value(frm.doctype, frm.docname, 'new_blanket_order', null);
			frm.refresh_field('new_blanket_order');
		}
	},
	old_blanket_order:function(frm){
		clearTableAndRefreshField(frm, 'item_details', 2);
        clearTableAndRefreshField(frm, 'sales_invoice_details', 2);
		if(frm.doc.new_blanket_order)
		{
			frappe.model.set_value(frm.doctype, frm.docname, 'new_blanket_order', null);
			frm.refresh_field('new_blanket_order');
		}
	},
});

//To clear and refresh the table content
function clearTableAndRefreshField(frm, tableField, condition) {
    var tableData = frm.doc[tableField] || [];
    var tableLength = tableData.length;

    if (tableLength > condition) {
        frm.clear_table(tableField);
        frm.refresh_field(tableField);
    }
}