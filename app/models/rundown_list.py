import datetime
# import classes
from app.models.base_model import BaseModel
from app.models import db

class RundownList(db.Model, BaseModel):
	# table name
	__tablename__ = 'rundown_lists'
	# displayed fields
	visible = ['id', 'description', 'time_start', 'time_end', 'location','created_at', 'updated_at']

	# columns definitions
	id = db.Column(db.Integer, primary_key=True)
	description = db.Column(
		db.String(40),
		nullable=False
	)
	time_start = db.Column(db.DateTime)	
	time_end = db.Column(db.DateTime)
	location = db.Column(
		db.String(40)
	)
	created_at = db.Column(db.DateTime)
	updated_at = db.Column(db.DateTime)

	def __init__(self):
		self.created_at = datetime.datetime.now()
		self.updated_at = datetime.datetime.now()
