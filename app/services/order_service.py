from app.models import db
from flask import current_app
from app.services.helper import Helper 
import paypalrestsdk
import datetime
from sqlalchemy.exc import SQLAlchemyError
# import model class
from app.models.order import Order
from app.builders.response_builder import ResponseBuilder
from app.models.ticket import Ticket
from app.models.payment import Payment
from app.models.referal import Referal
from app.configs.constants import PAYPAL  # noqa
from app.models.order_details import OrderDetails
from app.models.order_verification import OrderVerification


class OrderService():

	def __init__(self):
		paypalrestsdk.configure({
			  "mode": PAYPAL['mode'], # sandbox or live
			  "client_id": PAYPAL['client_id'],
			  "client_secret": PAYPAL['client_secret']
		})


	# def paypalorder(self, payload):
	# 	order_details = payload['order_details']
	# 	ord_det = []
	# 	for order in order_details:
	# 		item = {}
	# 		ticket = db.session.query(Ticket).filter_by(id=order['ticket_id']).first().as_dict()
	# 		item['name'] = ticket['ticket_type']
	# 		item['quantity'] = str(order['count'])
	# 		item['currency'] = payload['currency']
	# 		item['price'] = ticket['price']

	# 		ord_det.append(item)

	# 	payment = paypalrestsdk.Payment({
	# 		"intent": "order",
	# 		"payer": {
	# 			"payment_method": "paypal"
	# 		},
	# 		"transactions": [{
	# 			"amount": {
	# 				"currency":payload['currency'],
	# 				"total": payload['gross_amount']
	# 			},
	# 			"payee": {
	# 				"email": PAYPAL['payee']
	# 			},
	# 			"description": "Devsummit ticket purchase.",
	# 			"item_list": {
	# 				"items": ord_det
	# 			}, 
	# 		}],
	# 		"redirect_urls": {
	# 			"return_url": PAYPAL['return_url'],
	# 	        "cancel_url": PAYPAL['cancel_url']
	# 	    }})
	# 	result = payment.create()
	# 	if result:
	# 		self.get_paypal_detail(payment.id)
	# 	else:
	# 		print(payment.error)
	# 	return payment

	def get_paypal_detail(self, id):
		payment = paypalrestsdk.Payment.find(id)
		return payment

	def get(self, user_id):
		orders = db.session.query(Order).filter_by(user_id=user_id).order_by(Order.created_at.desc()).all()
		results = []
		for order in orders:
			items = db.session.query(OrderDetails).filter_by(order_id=order.id).all()
			payment = db.session.query(Payment).filter_by(order_id=order.id).first()
			referal = order.referal.as_dict() if order.referal else None
			order = order.as_dict()
			if payment is not None:
				payment = payment.as_dict()
				order['payment'] = payment
			else: 
				order['payment'] = None
			amount = 0
			for item in items:
				amount += item.price * item.count 
			order['amount'] = amount
			order['referal'] = referal
			results.append(order)

		return results

	def show(self, id):
		response = ResponseBuilder()
		order_raw = db.session.query(Order).filter_by(id=id).first()
		if order_raw is None:
			return response.set_error(True).set_message('Order not found').set_data(None).build()
		order = order_raw.as_dict()
		order_verification = db.session.query(OrderVerification).filter_by(order_id=id).first()
		if order_verification:
			order['verification'] = order_verification.as_dict()
			order['verification']['payment_proof'] =  Helper().url_helper(order_verification.payment_proof , current_app.config['GET_DEST']) if order_verification.payment_proof else "https://museum.wales/media/40374/thumb_480/empty-profile-grey.jpg"
		else:
			order['verification'] = None
		return response.set_data(order).set_message('Order retrieved').build()

	def create(self, payloads):
		self.model_order = Order()
		order_details = payloads['order_details']
		self.model_order.user_id = payloads['user_id']
		self.model_order.status = 'pending'
		referal = db.session.query(Referal).filter_by(referal_code=payloads['referal_code'])
		if(referal.first() is not None):
			self.model_order.referal_id = referal.first().as_dict()['id']
		db.session.add(self.model_order)
		try:
			db.session.commit()
			data = self.model_order.as_dict()
			# insert the order details
			order_id = data['id']
			order_items = []
			for item in order_details:
				order_item = OrderDetails()
				order_item.ticket_id = item['ticket_id']
				order_item.count = item['count']
				order_item.order_id = order_id
				# get ticket data
				ticket = self.get_ticket(item['ticket_id'])
				if payloads['payment_type'] == 'offline':
					order_item.price = ticket.price
				elif payloads['payment_type'] == 'paypal':
					order_item.price = ticket.usd_price
				else:
					order_item.price = ticket.price
				db.session.add(order_item)
				db.session.commit()
				order_items.append(order_item.as_dict())
			if payloads['payment_type'] == 'offline':
				gross_amount = (item['count'] * ticket.price)
				payment = Payment()
				payment.order_id = order_id
				payment.payment_type = 'offline'
				payment.gross_amount = gross_amount
				payment.transaction_time = datetime.datetime.now()
				payment.transaction_status = 'pending'
				db.session.add(payment)
				db.session.commit()	
			
				# if payloads['payment_type'] == 'paypal':
					# self.paypalorder(payloads)
			# save all items
			return {
				'error': False,
				'data': data,
				'included': order_items
			}
		except SQLAlchemyError as e:
			data = e.orig.args
			return {
				'error': True,
				'data': data
			}

	def delete(self, id):
		self.model_order = db.session.query(Order).filter_by(id=id)
		if self.model_order.first() is not None:
			self.model_order_details = db.session.query(OrderDetails).filter_by(order_id=self.model_order.first().id)
			self.model_order_payment = db.session.query(Payment).filter_by(order_id=self.model_order.first().id)
			self.model_order_details.delete()
			self.model_order_payment.delete()
			db.session.commit()

			# delete row
			self.model_order.delete()
			db.session.commit()
			return {
				'error': False,
				'data': None
			}
		else:
			data = 'data not found'
			return {
				'error': True,
				'data': data
			}

	def get_ticket(self, id):
		return db.session.query(Ticket).filter_by(id=id).first()
