import datetime

from app.models import db
from app.models.base_model import BaseModel


class TicketTransferLog(db.Model, BaseModel):

	# table name
	__tablename__ = 'ticket_transfer_log'
	# displayed fields
	visible = ['ticket_id', 'sender_user_id', 'receiver_user']

	# columns definitions
	id = db.Column(db.Integer, primary_key=True)
	ticket_type = db.Column(db.String)
	price = db.Column(db.Integer)
	information = db.Column(db.String)
	created_at = db.Column(db.DateTime)
	updated_at = db.Column(db.DateTime)

	def __init__(self):
		self.created_at = datetime.datetime.now()
		self.updated_at = datetime.datetime.now()