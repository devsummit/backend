import datetime

from app.models import db
from app.models.base_model import BaseModel


class UserTicket(db.Model, BaseModel):

	# table name
	__tablename__ = 'user_tickets'
	# displayed fields
	visible = ['id', 'user_id', 'ticket_id']

	# columns definitions
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(
		db.Integer,
		db.ForeignKey('users.id'),
		nullable=False
	)
	user = db.relationship('User')
	ticket_id = db.Column(
		db.Integer,
		db.ForeignKey('tickets.id'),
		nullable=False)
	ticket = db.relationship('Ticket')
	created_at = db.Column(db.DateTime)
	updated_at = db.Column(db.DateTime)

	def __init__(self):
		self.created_at = datetime.datetime.now()
		self.updated_at = datetime.datetime.now()
