from datetime import datetime
from app.models.base_model import BaseModel
from app.models import db


class HackatonProposal(db.Model, BaseModel):

	__tablename__ = 'hackaton_proposals'

	visible = ['id', 'github_link', 'order_id', 'status', 'created_at', 'updated_at']

	id = db.Column(db.Integer, primary_key=True)
	github_link = db.Column(db.String)
	order_id = db.Column(
		db.Integer,
		db.ForeignKey('orders.id'),
		nullable=False
	)
	order = db.relationship('Order')
	status = db.Column(db.String)
	created_at = db.Column(db.DateTime)
	updated_at = db.Column(db.DateTime)

	def __init__(self):
		self.created_at = datetime.now()
		self.updated_at = datetime.now()
