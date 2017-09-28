import datetime

# import classes
from app.models.base_model import BaseModel
from app.models import db


class PointTransactionLog(db.Model, BaseModel):
	# table name
	__tablename__ = 'point_transaction_log'
	# displayed fields
	visible = ['id', 'booth_id', 'user_id', 'amount', 'created_at', 'updated_at']

	# columns definitions
	id = db.Column(db.Integer, primary_key=True)
	booth_id = db.Column(
		db.String(40),
		db.ForeignKey('booths.id'),
		nullable=False
	)
	booth = db.relationship('Booth')
	user_id = db.Column(
		db.String(40),
		db.ForeignKey('users.id'),
		nullable=False
	)
	user = db.relationship('User')
	amount = db.Column(db.Integer)
	created_at = db.Column(db.DateTime)
	updated_at = db.Column(db.DateTime)

	def __init__(self):
		self.created_at = datetime.datetime.now()
		self.updated_at = datetime.datetime.now()
