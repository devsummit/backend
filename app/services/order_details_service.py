import datetime
from app.models import db
from sqlalchemy.exc import SQLAlchemyError
# import model class
from app.models.order_details import OrderDetails


class OrderDetailsService():

	def __init__(self, model_order_details):
		self.model_order_details = model_order_details

	def get(self, order_id):
		order_details = db.session.query(OrderDetails).filter_by(order_id=order_id).all()
		return order_details

	def show(self, order_id, detail_id):
		order_details = db.session.query(OrderDetails).filter_by(order_id=order_id).filter_by(id=detail_id).first()
		return order_details

	def create(self, payloads, order_id):
		self.model_order_details.ticket_id = payloads['ticket_id']
		self.model_order_details.count = payloads['count']
		self.model_order_details.order_id = order_id

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
