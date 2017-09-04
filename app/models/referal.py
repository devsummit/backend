import datetime

from app.models import db
from app.models.base_model import BaseModel


class Referal(db.Model, BaseModel):
	# table name
	__tablename__ = 'referals'

	# visible fields
	visible = ['id', 'owner', 'discount_amount', 'created_at', 'updated_at']

	# columns definitions
	id = db.Column(db.Integer, primary_key=True)
	owner = db.Column(db.String)
	discount_amount = db.Column(db.Float(precision=2))
	created_at = db.Column(db.DateTime)
	updated_at = db.Column(db.DateTime)

	def __init__(self):
		self.created_at = datetime.datetime.now()
		self.updated_at = datetime.datetime.now()
