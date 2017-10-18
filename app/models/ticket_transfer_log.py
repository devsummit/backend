import datetime

from app.models import db
from app.models.base_model import BaseModel


class TicketTransferLog(db.Model, BaseModel):

	# table name
	__tablename__ = 'ticket_transfer_logs'
	# displayed fields
	visible = ['user_ticket_id', 'sender_user_id', 'receiver_user_id', 'sender', 'receiver', 'created_at', 'updated_at']

	# columns definitions
	id = db.Column(db.Integer, primary_key=True)
	user_ticket_id = db.Column(db.Integer)
	sender_user_id = db.Column(
		db.Integer, 
		db.ForeignKey('users.id'),
		nullable=False)
	receiver_user_id = db.Column(
		db.Integer, 
		db.ForeignKey('users.id'),
		nullable=False)
	sender = db.relationship("User", foreign_keys=[sender_user_id])
	receiver = db.relationship("User", foreign_keys=[receiver_user_id])
	created_at = db.Column(db.DateTime)
	updated_at = db.Column(db.DateTime)

	def __init__(self):
		self.created_at = datetime.datetime.now()
		self.updated_at = datetime.datetime.now()
