import datetime

from app.models import db
from app.models.base_model import BaseModel


class Sponsor(db.Model, BaseModel):
	# table name
	__tablename__ = 'sponsors'

	# visible fields
	visible = ['id', 'name', 'email', 'phone', 'note', 'type', 'stage', 'attachment', 'created_at', 'updated_at']

	# columns definitions
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String)
	email = db.Column(db.String)
	phone = db.Column(db.String)
	note = db.Column(db.Text)
	type = db.Column(db.String)
	stage = db.Column(db.String)
	attachment = db.Column(db.String)
	created_at = db.Column(db.DateTime)
	updated_at = db.Column(db.DateTime)

	def __init__(self):
		self.created_at = datetime.datetime.now()
		self.updated_at = datetime.datetime.now()
