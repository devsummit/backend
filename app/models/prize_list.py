import datetime
# import classes
from app.models.base_model import BaseModel
from app.models import db


class PrizeList(db.Model, BaseModel):
	# table name
	__tablename__ = 'prize_lists'
	# displayed fields
	visible = ['id', 'point_cost', 'name', 'attachment', 'count', 'created_at', 'updated_at']

	# columns definitions
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String)
	point_cost = db.Column(db.Integer)
	attachment = db.Column(db.String)
	count = db.Column(db.Integer)
	created_at = db.Column(db.DateTime)
	updated_at = db.Column(db.DateTime)

	def __init__(self):
		self.created_at = datetime.datetime.now()
		self.updated_at = datetime.datetime.now()