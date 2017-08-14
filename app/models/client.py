import datetime

from app.models import db
from app.models.base_model import BaseModel


class Client(db.Model, BaseModel):
	# table name
	__tablename__ = 'clients'

	# visible fields
	visible = ['id', 'app_name', 'client_secret', 'created_at', 'updated_at']

	# columns definitions
	id = db.Column(db.Integer, primary_key=True)
	app_name = db.Column(db.String)
	client_secret = db.Column(db.String)
	client_id = db.Column(db.String)
	created_at = db.Column(db.DateTime)
	updated_at = db.Column(db.DateTime)

	def __init__(self):
		self.created_at = datetime.datetime.now()
		self.updated_at = datetime.datetime.now()
