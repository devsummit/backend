import datetime

# import classes
from app.models.base_model import BaseModel
from app.models import db


class Booth(db.Model, BaseModel):
	# table name
	__tablename__ = 'booths'
	# displayed fields
	visible = ['id', 'user_id', 'stage_id', 'points', 'summary', 'created_at', 'updated_at']

	# columns definitions
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(
		db.String(40),
		db.ForeignKey('users.id'),
		nullable=False
	)
	user = db.relationship('User')
	stage_id = db.Column(
		db.String(40),
		db.ForeignKey('stages.id'),
		nullable=False
	)
	stage = db.relationship('Stage')
	summary = db.Column(db.Text)
	points = db.Column(db.Integer)
	created_at = db.Column(db.DateTime)
	updated_at = db.Column(db.DateTime)

	def __init__(self):
		self.created_at = datetime.datetime.now()
		self.updated_at = datetime.datetime.now()
		self.summary = ''
		self.points = 0
