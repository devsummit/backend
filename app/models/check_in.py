import datetime

from app.models import db
from app.models.base_model import BaseModel


class CheckIn(db.Model, BaseModel):
	# table name
	__tablename__ = 'check_ins'

	# visible fields
	visible = ['id', 'user_ticket_id', 'created_at', 'updated_at']

	# columns definitions
	id = db.Column(db.Integer, primary_key=True)
	user_ticket_id = db.Column(
		db.Integer,
		db.ForeignKey('user_tickets.id'),
		nullable=False
	)
	user_ticket = db.relationship('UserTicket')
	created_at = db.Column(db.DateTime)
	updated_at = db.Column(db.DateTime)

	def __init__(self):
		self.created_at = datetime.datetime.now()
		self.updated_at = datetime.datetime.now()
