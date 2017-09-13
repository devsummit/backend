import datetime

from app.models import db
from app.models.base_model import BaseModel


class SponsorInteractionLog(db.Model, BaseModel):
	# table name
	__tablename__ = 'sponsor_interaction_log'

	# visible fields
	visible = ['id', 'sponsor_id', 'description', 'created_at', 'updated_at']

	# columns definitions
	id = db.Column(db.Integer, primary_key=True)
	sponsor_id = db.Column(
		db.Integer,
		db.ForeignKey('sponsors.id'),
		nullable=False
	)
	sponsor = db.relationship('Sponsor')
	description = db.Column(db.Text)
	created_at = db.Column(db.DateTime)
	updated_at = db.Column(db.DateTime)

	def __init__(self):
		self.created_at = datetime.datetime.now()
		self.updated_at = datetime.datetime.now()
