// Copyright (c) 2023, Quantbit and contributors
// For license information, please see license.txt
frappe.ui.form.on('Rate Adjustment Request', {
    refresh: function(frm) {
        frm.fields_dict.old_blanket_order.get_query = function(doc, cdt, cdn) {
            return {
                filters: [
                    ['Blanket Order', 'customer', '=', frm.doc.customer]
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
						]
			};
		});

    },
	new_blanket_order:function(frm){
		frm.call({
			method:"get_item_details",
			doc:frm.doc
		});
	}
});
