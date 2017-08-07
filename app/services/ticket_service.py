import datetime
from app.models import db
from sqlalchemy.exc import SQLAlchemyError
# import model class
from app.models.ticket import Ticket


class TicketService():

	def __init__(self, model_ticket):
		self.model_ticket = model_ticket

	def get(self):
		tickets = db.session.query(Ticket).all()
		return tickets

	def show(self, id):
		ticket = db.session.query(Ticket).filter_by(id=id).first()
		return ticket

	def create(self, payloads):
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
