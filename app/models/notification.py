from datetime import datetime, timedelta
from app.models.base_model import BaseModel
from app.models import db


class Notification(db.Model, BaseModel):

	__tablename__ = 'notifications'

	visible = ['id', 'message', 'sender_uid', 'receiver_uid', 'type', 'attachment', 'created_at', 'updated_at']

	id = db.Column(db.Integer, primary_key=True)
	message = db.Column(db.Text)
	attachment = db.Column(db.String)
	sender_uid = db.Column(
		db.Integer,
		db.ForeignKey('users.id'),
		nullable=False
	)
	sender = db.relationship("User", foreign_keys=[sender_uid])
	receiver_uid = db.Column(
		db.Integer,
		db.ForeignKey('users.id'),
		nullable=False
	)
	receiver = db.relationship('User', foreign_keys=[receiver_uid])
	type = db.Column(db.String)
	created_at = db.Column(db.DateTime)
	updated_at = db.Column(db.DateTime)

	def __init__(self):
		self.created_at = datetime.now() + timedelta(hours=7) 
		self.updated_at = datetime.now() + timedelta(hours=7) 
