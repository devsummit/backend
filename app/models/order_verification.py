import datetime
# import classes
from app.models.base_model import BaseModel
from app.models import db


class OrderVerification(db.Model, BaseModel):
	# table name
	__tablename__ = 'order_verifications'
	# displayed fields
	visible = ['id', 'user_id', 'order_id', 'payment_proof', 'created_at', 'updated_at']

	# columns definitions
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(
		db.Integer,
		db.ForeignKey('users.id')
	)
	order_id = db.Column(
		db.String,
		db.ForeignKey('orders.id')
	)
	payment_proof = db.Column(
		db.String
	)
	created_at = db.Column(db.DateTime)
	updated_at = db.Column(db.DateTime)

	def __init__(self):
		self.created_at = datetime.datetime.now()
		self.updated_at = datetime.datetime.now()