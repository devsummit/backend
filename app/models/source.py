import datetime
# import classes
from app.models.base_model import BaseModel
from app.models import db


class Source(db.Model, BaseModel):
	# table name
	__tablename__ = 'sources'
	# displayed fields
	visible = ['id', 'account_number', 'bank',
			'alias', 'created_at', 'updated_at']

	# columns definitions
	id = db.Column(db.Integer, primary_key=True)
	account_number = db.Column(db.String(20))
	bank = db.Column(db.String(40))
	alias = db.Column(db.String(60))
	created_at = db.Column(db.DateTime)
	updated_at = db.Column(db.DateTime)

	def __init__(self):
		self.created_at = datetime.datetime.now()
		self.updated_at = datetime.datetime.now()
