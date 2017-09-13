import datetime
from app.models.base_model import BaseModel
from app.models import db


class Partner(db.Model, BaseModel):

	__tablename__ = 'partners'

	visible = ['id', 'name', 'email', 'type', 'website', 'photo', 'created_at', 'updated_at']

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String)
	email = db.Column(db.String)
	website = db.Column(db.String)
	type = db.Column(db.String)
	photo = db.Column(db.String)
	created_at = db.Column(db.DateTime)
	updated_at = db.Column(db.DateTime)

	def __init__(self):
		self.created_at = datetime.datetime.now()
		self.updated_at = datetime.datetime.now()
