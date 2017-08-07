import datetime
# import classes
from app.models.base_model import BaseModel
from app.models import db


class Events(db.Model, BaseModel):
	# table name
	__tablename__ = 'events'
	# displayed fields
	visible = ['id', 'information', 'time_start', 'time_end', 'created_at', 'updated_at']

	# columns definitions
	id = db.Column(db.Integer, primary_key=True)
	information = db.Column(db.String)
	time_start = db.Column(db.DateTime)
	time_end = db.Column(db.DateTime)
	created_at = db.Column(db.DateTime)
	updated_at = db.Column(db.DateTime)

	def __init__(self):
		self.created_at = datetime.datetime.now()
		self.updated_at = datetime.datetime.now()
