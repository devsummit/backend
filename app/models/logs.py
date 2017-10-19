import datetime

from app.models import db
from app.models.base_model import BaseModel


class Logs(db.Model, BaseModel):
	# table name
	__tablename__ = 'logs'

	# visible fields
	visible = ['id', 'description', 'created_at']

	# columns definitions
	id = db.Column(db.Integer, primary_key=True)
	description = db.Column(db.Text)
	created_at = db.Column(db.DateTime)

	def __init__(self):
		self.created_at = datetime.datetime.now()
