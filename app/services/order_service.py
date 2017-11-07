from app.models import db
from flask import current_app, request
from app.services.helper import Helper 
from app.services.order_verification_service import OrderVerificationService 
import paypalrestsdk
import datetime
from sqlalchemy.exc import SQLAlchemyError
# import model class
from app.models.order import Order
from app.builders.response_builder import ResponseBuilder
from app.models.ticket import Ticket
from app.models.payment import Payment
from app.models.referal import Referal
from app.services.hackaton_proposal_service import HackatonProposalService
from app.configs.constants import PAYPAL, ROLE  # noqa
from app.models.order_details import OrderDetails
from app.models.order_verification import OrderVerification


class OrderService():

	def __init__(self):
		self.hackatonproposalservice = HackatonProposalService()
		paypalrestsdk.configure({
			  "mode": PAYPAL['mode'], # sandbox or live
			  "client_id": PAYPAL['client_id'],
			  "client_secret": PAYPAL['client_secret']
		})


	def get_paypal_detail(self, id):
		payment = paypalrestsdk.Payment.find(id)
		return payment

	def get(self, user_id):
		orders = db.session.query(Order).filter_by(user_id=user_id).order_by(Order.created_at.desc()).all()
		type = 'user'
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
				type = item.ticket.type
				amount += item.price * item.count 
			order['amount'] = amount
			order['referal'] = referal
			order['type'] = type
			results.append(order)
		return results

	def unverified_order(self):
		response = ResponseBuilder()
		orders = db.session.query(Order).filter(Order.status != 'paid').all()
		results = []
		for order in orders:
			data = order.as_dict()
			data['user'] = order.user.as_dict()
			if order.referal is not None:
				data['referal'] = order.referal.as_dict()
			else:
				data['referal'] = None
			results.append(data)
		return response.set_data(results).build()

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

	def create(self, payloads, user):
		response = ResponseBuilder()
		if user['role_id'] == ROLE['hackaton']:
			return response.set_data(None).set_message('Hackaton attendee cannot buy ticket').set_error(True).build()
		order_details = payloads['order_details']
		# check if it's hackaton
		if order_details[0]['ticket_id'] == 10:
			# check if proposal already submited
			if self.hackatonproposalservice.check_hackaton_proposal_exist(user['id']):
				return response.set_error(True).set_message('Hackaton cannot be submitted twice, our admin is in the process of verifying it, you will receive notification once it is done').set_data(None).build()
			
		self.model_order = Order()
		self.model_order.user_id = payloads['user_id']
		self.model_order.status = 'pending'
		# Referal code checking
		referal = db.session.query(Referal).filter_by(referal_code=payloads['referal_code'])
		if referal.first() is not None:
			# verify quota and update quota
			if referal.first().quota > 0:
				referal.update({
					'quota': referal.first().quota - 1
				})
				self.model_order.referal_id = referal.first().as_dict()['id']
			else:
				# handle for referal code exceed limit / quota
				return response.set_error(True).set_data(None).set_message('quota for specified code have exceeded the limit').build()
		# place order
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
				if payloads['payment_type'] == 'paypal':
					order_item.price = ticket.usd_price
				else:
					order_item.price = ticket.price
				db.session.add(order_item)
				db.session.commit()
				order_item_dict = order_item.as_dict()
				order_item_dict['ticket'] = order_item.ticket.as_dict() 
				order_items.append(order_item_dict)
			if payloads['payment_type'] == 'offline':
				gross_amount = (item['count'] * ticket.price) 
				if referal.first() is not None:
					# discount on gross amount
					gross_amount -= gross_amount * referal.first().discount_amount 
				payment = Payment()
				payment.order_id = order_id
				payment.payment_type = 'offline'
				payment.gross_amount = gross_amount
				payment.transaction_time = datetime.datetime.now()
				payment.transaction_status = 'pending'

				db.session.add(payment)
				db.session.commit()	
				# check if ticket is free
				if order_details[0]['ticket_id'] == 10:
					# hackaton proposal
					hackatonproposal = {
						'github_link': payloads['hacker_team_name'],
						'order_id': order_id
					}
					hack_result = self.hackatonproposalservice.create(hackatonproposal)

				elif gross_amount == 0 or (referal.first() and referal.first().discount_amount == 1):
					# call verify service
					ov_service = OrderVerificationService()
					ov_service.admin_verify(self.model_order.id, request, payloads['hacker_team_name'])

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
