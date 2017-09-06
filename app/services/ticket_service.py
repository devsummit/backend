import datetime
from app.models import db
from sqlalchemy.exc import SQLAlchemyError
# import model class
from app.models.ticket import Ticket
from app.models.payment import Payment
from app.models.order_details import OrderDetails
from app.configs.constants import SLOT


class TicketService():

	def get_items(self, payment):
		result = [0, 0, 0, 0, 0]
		order_details = db.session.query(OrderDetails).filter_by(order_id=payment['order_id']).all()
		for item in order_details:
			data = item.as_dict()
			result[data['ticket_id'] - 1] += data['count']
		return result

	def count_ticket_left(self, payments):
		reserved = [0, 0, 0, 0, 0]
		paid = [0, 0, 0, 0, 0]
		for payment in payments:
			data = payment.as_dict()
			if data['transaction_status'] is 'deny':
				continue

			count_data = self.get_items(data)
			for i in range(0, 5):
				if data['transaction_status'] == 'capture':
					paid[i] += count_data[i]
				else:
					reserved[i] += count_data[i]

		return {'reserved': reserved, 'paid': paid}

	def include_ticket_left(self, tickets):
		total_amount = [SLOT['commercial'], SLOT['commercial'], SLOT['commercial'], SLOT['commercial'], SLOT['community']]
		payments = db.session.query(Payment).all()
		data = self.count_ticket_left(payments)
		for i in range(0, 5):
			total_amount[i] -= data['reserved'][i]
			total_amount[i] -= data['paid'][i]
		return {
			'total_amount': total_amount, 
			'reserved': data['reserved'],
			'paid': data['paid']
		} 

	def get(self):
		tickets = db.session.query(Ticket).all()
		_results = []
		for ticket in tickets:
			data = ticket.as_dict()
			_results.append(data)
		count_data = self.include_ticket_left(_results)
		_results = self.include_count_data(count_data, _results)
		return {
			'error': False,
			'data': _results,
			'message': 'Ticket retrieved succesfully'
		}

	def include_count_data(self, count_data, results):
		for i in range(0, 5):
			results[i]['reserved'] = count_data['reserved'][i]
			results[i]['paid'] = count_data['paid'][i]
			results[i]['available'] = count_data['total_amount'][i]
		return results

	def show(self, id):
		ticket = db.session.query(Ticket).filter_by(id=id).first()
		return ticket

	def create(self, payloads):
		self.model_ticket = Ticket()
		self.model_ticket.ticket_type = payloads['ticket_type']
		self.model_ticket.price = payloads['price']
		self.model_ticket.information = payloads['information']
		db.session.add(self.model_ticket)
		try:
			db.session.commit()
			data = self.model_ticket.as_dict()
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

	def update(self, payloads, id):
		try:
			self.model_ticket = db.session.query(Ticket).filter_by(id=id)
			self.model_ticket.update({
				'ticket_type': payloads['ticket_type'],
				'price': payloads['price'],
				'information': payloads['information'],
				'updated_at': datetime.datetime.now()
			})
			db.session.commit()
			data = self.model_ticket.first().as_dict()
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
		self.model_ticket = db.session.query(Ticket).filter_by(id=id)
		if self.model_ticket.first() is not None:
			# delete row
			self.model_ticket.delete()
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
