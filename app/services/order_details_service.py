import datetime
from flask import current_app
from app.models import db
from sqlalchemy.exc import SQLAlchemyError
from app.services.helper import Helper 
# import model class
from app.models.order_details import OrderDetails
from app.models.payment import Payment
from app.models.ticket import Ticket
from app.models.order import Order
from app.models.order_verification import OrderVerification


class OrderDetailsService():

	def get(self, order_id):
		_results = []
		order_details = db.session.query(OrderDetails).filter_by(order_id=order_id).all()
		order = db.session.query(Order).filter_by(id=order_id).first()
		order_verification = db.session.query(OrderVerification).filter_by(order_id=order_id).first()
		payment = db.session.query(Payment).filter_by(order_id=order_id).first()
		payment = payment.as_dict() if payment is not None else None
		included = {}
		included['user'] = order.user.as_dict()
		included['referal'] = order.referal.as_dict() if order.referal else None
		included['payment'] = payment
		if order_verification:
			included['verification'] = order_verification.as_dict()
			included['verification']['payment_proof'] =  Helper().url_helper(order_verification.payment_proof , current_app.config['GET_DEST']) if order_verification.payment_proof else "https://museum.wales/media/40374/thumb_480/empty-profile-grey.jpg"
		else:
			included['verification'] = None
		for detail in order_details:
			order = detail.order.as_dict()
			data = detail.as_dict()
			data['ticket'] = detail.ticket.as_dict()
			_results.append(data)
		return {
			'error': False,
			'data': _results,
			'included': included
		}
		# return order_details

	def show(self, order_id, detail_id):
		order_details = db.session.query(OrderDetails).filter_by(order_id=order_id).filter_by(id=detail_id).first()
		data = order_details.as_dict()
		data['ticket_type'] = order_details.ticket.as_dict()
		return data

	def create(self, payloads, order_id):
		self.model_order_details = OrderDetails()
		self.model_order_details.ticket_id = payloads['ticket_id']
		self.model_order_details.count = payloads['count']
		self.model_order_details.order_id = order_id
		# get ticket data
		ticket = self.get_ticket(payloads['ticket_id'])
		self.model_order_details.price = ticket.price
		db.session.add(self.model_order_details)
		try:
			db.session.commit()
			data = self.model_order_details.as_dict()

			return {
				'error': False,
				'data': data
			}
		except SQLAlchemyError as e:
			data = e.orig.args
			return {
				'error': True,
				'data': data
			}

	def update(self, payloads, detail_id):
		try:
			self.model_order_details = db.session.query(OrderDetails).filter_by(id=detail_id)
			self.model_order_details.update({
				'count': payloads['count'],
				'updated_at': datetime.datetime.now()
			})
			db.session.commit()
			data = self.model_order_details.first().as_dict()
			return {
				'error': False,
				'data': data
			}
		except SQLAlchemyError as e:
			data = e.orig.args
			return {
				'error': True,
				'data': data
			}

	def delete(self, order_id, detail_id):
		self.model_order_details = db.session.query(OrderDetails).filter_by(order_id=order_id).filter_by(id=detail_id)
		if self.model_order_details.first() is not None:
			# delete row
			self.model_order_details.delete()
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
