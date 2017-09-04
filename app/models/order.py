import datetime
# import classes
from app.models.base_model import BaseModel
from app.models.referal import Referal
from app.models import db


class Order(db.Model, BaseModel):
	# table name
	__tablename__ = 'orders'
	# displayed fields
	visible = ['id', 'user_id', 'referal_id', 'status', 'created_at', 'updated_at']

	# columns definitions
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(
		db.Integer,
		db.ForeignKey('users.id'),
		nullable=False
	)
	user = db.relationship('User')
	referal_id = db.Column(
		db.Integer,
		db.ForeignKey('referals.id'),
		nullable=False
	)
	referal = db.relationship('Referal')
	status = db.Column(db.String)
	created_at = db.Column(db.DateTime)
	updated_at = db.Column(db.DateTime)

	def __init__(self):
		self.created_at = datetime.datetime.now()
		self.updated_at = datetime.datetime.now()
