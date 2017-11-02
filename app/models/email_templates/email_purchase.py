from flask import request


class EmailPurchase():
	"""docstring for EmailPurchase"""

	def __init__(self):
		self.template = "<h3>Congratulation! you have the privillege to attend Indonesia Developer Summit</h3>"
	
	def set_invoice_path(self, order_id):
		url_invoice = request.url_root + '/invoices/' + order_id
		self.template += "<h4>Here is your Invoice:</h4>"
		self.template += '<a href="'+ url_invoice +'">Click here to show the invoice</a>'
		return self

	def set_redeem_code(self, redeem_codes):
		codes = []
		for code in redeem_codes:
			codes.append("<li>%s</li>" %(code.code))
		li = ''.join(codes)
		self.template += '<h4>Here your redeem codes: </h4>%s<h3>Share the above code to your teammate, and put it into redeem code menu to let them join your team and claim their ticket</h3>' %(codes)
		return self

	def build(self):
		self.template += "<h5>Thank you for your purchased.</h5>"
		return self.template
