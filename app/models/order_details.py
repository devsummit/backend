import datetime
# import classes
from app.models.base_model import BaseModel
from app.models import db


class OrderDetails(db.Model, BaseModel):
	# table name
	__tablename__ = 'order_details'
	# displayed fields
	visible = ['id', 'ticket_id', 'order_id', 'count', 'price', 'created_at', 'updated_at']

	# columns definitions
	id = db.Column(db.Integer, primary_key=True)
	ticket_id = db.Column(
		db.String(40),
		db.ForeignKey('tickets.id'),
		nullable=False
	)
	ticket = db.relationship('Ticket')
	order_id = db.Column(
		db.String(40),
		db.ForeignKey('orders.id'),
		nullable=False
	)
	order = db.relationship('Order')
	count = db.Column(db.Integer)
	price = db.Column(db.Integer)
	created_at = db.Column(db.DateTime)
	updated_at = db.Column(db.DateTime)

	def __init__(self):
		self.created_at = datetime.datetime.now()
		self.updated_at = datetime.datetime.now()
