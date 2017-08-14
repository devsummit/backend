import datetime

from app.models import db
from app.models.base_model import BaseModel


class TicketTransferLog(db.Model, BaseModel):

	# table name
	__tablename__ = 'ticket_transfer_logs'
	# displayed fields
	visible = ['user_ticket_id', 'sender_user_id', 'receiver_user_id']

	# columns definitions
	id = db.Column(db.Integer, primary_key=True)
	user_ticket_id = db.Column(db.Integer)
	sender_user_id = db.Column(db.Integer)
	receiver_user_id = db.Column(db.Integer)
	created_at = db.Column(db.DateTime)
	updated_at = db.Column(db.DateTime)

	def __init__(self):
		self.created_at = datetime.datetime.now()
		self.updated_at = datetime.datetime.now()
