import datetime
from app.models import db
from sqlalchemy.exc import SQLAlchemyError
# import model class
from app.models.order_details import OrderDetails
from app.models.payment import Payment
from app.models.ticket import Ticket
from app.models.order import Order


class OrderDetailsService():

	def get(self, order_id):
		_results = []
		order_details = db.session.query(OrderDetails).filter_by(order_id=order_id).all()
		order = db.session.query(Order).filter_by(id=order_id).first()
		included = order.referal.as_dict() if order.referal else None
		for detail in order_details:
			order = detail.order.as_dict()
			payment = db.session.query(Payment).filter_by(order_id=order['id']).first()
			payment = payment.as_dict() if payment is not None else None
			data = detail.as_dict()
			data['ticket'] = detail.ticket.as_dict()
			data['payment'] = payment
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
