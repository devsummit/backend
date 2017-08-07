import datetime

from app.models import db
from app.models.base_model import BaseModel


class Stage(db.Model, BaseModel):

	# table name
	__tablename__ = 'stages'
	# displayed fields
	visible = ['id', 'name', 'stage_type', 'information', 'created_at', 'updated_at']

	# columns definitions
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String)
	stage_type = db.Column(db.String)
	information = db.Column(db.String)
	created_at = db.Column(db.DateTime)
	updated_at = db.Column(db.DateTime)

	def __init__(self):
		self.created_at = datetime.datetime.now()
		self.updated_at = datetime.datetime.now()
