import datetime

from app.models import db
from app.models.base_model import BaseModel


class PartnerPj(db.Model, BaseModel):
	# table name
	__tablename__ = 'partner_pj'

	# visible fields
	visible = ['id', 'partner_id', 'user_id', 'created_at', 'updated_at']

	# columns definitions
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	partner_id = db.Column(db.Integer, db.ForeignKey('partners.id'))
	created_at = db.Column(db.DateTime)
	updated_at = db.Column(db.DateTime)
	partner = db.relationship('Partner')
	user = db.relationship('User')

	def __init__(self):
		self.created_at = datetime.datetime.now()
		self.updated_at = datetime.datetime.now()
