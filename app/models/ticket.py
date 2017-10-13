import datetime

from app.models import db
from app.models.base_model import BaseModel


class Ticket(db.Model, BaseModel):

	# table name
	__tablename__ = 'tickets'
	# displayed fields
	visible = ['id', 'ticket_type', 'price', 'usd_price', 'information', 'created_at', 'updated_at']

	# columns definitions
	id = db.Column(db.Integer, primary_key=True)
	ticket_type = db.Column(db.String)
	price = db.Column(db.Integer)
	usd_price = db.Column(db.Integer)
	information = db.Column(db.String)
	created_at = db.Column(db.DateTime)
	updated_at = db.Column(db.DateTime)

	def __init__(self):
		self.created_at = datetime.datetime.now()
		self.updated_at = datetime.datetime.now()
