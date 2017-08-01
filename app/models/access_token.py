import datetime

from app.models import db
from app.models.base_model import BaseModel


class AccessToken(db.Model, BaseModel):
	# table name
	__tablename__ = 'access_tokens'

	# visible fields
	visible = ['id', 'access_token', 'refresh_token', 'created_at', 'updated_at']

	# columns definitions
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(
		db.String(40),
		db.ForeignKey('users.id'),
		nullable=False
	)
	user = db.relationship('User')
	access_token = db.Column(db.String)
	refresh_token = db.Column(db.String)
	created_at = db.Column(db.DateTime)
	updated_at = db.Column(db.DateTime)

	def __init__(self):
		self.created_at = datetime.datetime.now()
		self.updated_at = datetime.datetime.now()

	def init_token(self, access_token, refresh_token, user_id):
		self.access_token = access_token
		self.refresh_token = refresh_token
		self.user_id = user_id
		return self
