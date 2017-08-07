from app.models import db
from sqlalchemy.exc import SQLAlchemyError
# import model class
from app.models.order import Order
from app.models.ticket import Ticket

from app.models.order_details import OrderDetails

class OrderService():

	def __init__(self, model_order):
		self.model_order = model_order

	def get(self):
		orders = db.session.query(Order).all()
		return orders

	def show(self, id):
		order = db.session.query(Order).filter_by(id=id).first()
		return order

	def create(self, payloads):
		order_details = payloads['order_details']
		self.model_order.user_id = payloads['user_id']
		self.model_order.status = 'pending'
		db.session.add(self.model_order)
		try:
			db.session.commit()
			data = self.model_order.as_dict()
			# insert the order details
			order_id = data['id']
			for item in order_details:
				order_item = OrderDetails()
				order_item.ticket_id = item['ticket_id']
				order_item.count = item['count']
				order_item.order_id = order_id
				# get ticket data
				ticket = self.get_ticket(item['ticket_id'])
				order_item.price = ticket.price
				db.session.add(order_item)
			# save all items
			db.session.commit()
			data['details'] = order_details
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

	def delete(self, id):
		self.model_order = db.session.query(Order).filter_by(id=id)
		if self.model_order.first() is not None:
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