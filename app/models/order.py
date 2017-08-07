import datetime
# import classes
from app.models.base_model import BaseModel
from app.models import db


class Order(db.Model, BaseModel):
	# table name
	__tablename__ = 'orders'
	# displayed fields
	visible = ['id', 'user_id', 'status', 'created_at', 'updated_at']

	# columns definitions
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(
		db.String(40),
		db.ForeignKey('users.id'),
		nullable=False
	)
	user = db.relationship('User')
	status = db.Column(db.String)
	created_at = db.Column(db.DateTime)
	updated_at = db.Column(db.DateTime)

	def __init__(self):
		self.created_at = datetime.datetime.now()
		self.updated_at = datetime.datetime.now()
