import datetime
# import classes
from app.models.base_model import BaseModel
from app.models import db


class Beacon(db.Model, BaseModel):
	# table name
	__tablename__ = 'beacons'
	# displayed fields
	visible = ['id', 'major', 'minor', 'type', 'type_id', 'description', 'created_at', 'updated_at']

	# columns definitions
	id = db.Column(db.Integer, primary_key=True)
	major = db.Column(db.String)
	minor = db.Column(db.String)
	type = db.Column(db.String)
	type_id = db.Column(db.String)
	description = db.Column(db.Text)
	created_at = db.Column(db.DateTime)
	updated_at = db.Column(db.DateTime)

	def __init__(self):
		self.created_at = datetime.datetime.now()
		self.updated_at = datetime.datetime.now()
