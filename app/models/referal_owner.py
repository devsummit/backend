import datetime

from app.models import db
from app.models.base_model import BaseModel


class ReferalOwner(db.Model, BaseModel):
	# table name
	__tablename__ = 'referal_owner'

	# visible fields
	visible = ['id', 'referalable_id', 'referalable_type', 'referal_id', 'created_at', 'updated_at']

	# columns definitions
	id = db.Column(db.Integer, primary_key=True)
	referalable_type = db.Column(db.String)
	referalable_id = db.Column(db.Integer)
	referal_id = db.Column(db.Integer)
	created_at = db.Column(db.DateTime)
	updated_at = db.Column(db.DateTime)

	def __init__(self):
		self.created_at = datetime.datetime.now()
		self.updated_at = datetime.datetime.now()
