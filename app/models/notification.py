import datetime
# import classes
from app.models.base_model import BaseModel
from app.models import db
from app.models.user import User  # noqa


class Notification(db.Model, BaseModel):
	# table name
	__tablename__ = 'notifications'
	# displayed fields
	visible = ['id', 'sender_user_id', 'receiver_user_id', 'message', 'attachment', 'type', 'status', 'created_at', 'updated_at']

	# columns definitions
	id = db.Column(db.Integer, primary_key=True)
	sender_user_id = db.Column(
		db.String(40),
		db.ForeignKey('users.id'),
		nullable=False
	)
	sender_user = db.relationship('User')
	receiver_user_id = db.Column(
		db.String(40),
		db.ForeignKey('users.id'),
		nullable=False
	)
	receiver_user = db.relationship('User')
	message = db.Column(db.String)
	attachment = db.Column(db.String)
	type = db.Column(db.String)
	status = db.Column(db.String)
	created_at = db.Column(db.DateTime)
	updated_at = db.Column(db.DateTime)

	def __init__(self):
		self.created_at = datetime.datetime.now()
		self.updated_at = datetime.datetime.now()
		self.summary = ''
