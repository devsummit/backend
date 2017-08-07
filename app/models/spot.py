import datetime

from app.models import db
from app.models.base_model import BaseModel


class Spot(db.Model, BaseModel):

	# table name
	__tablename__ = 'spots'
	# displayed fields
	visible = ['id', 'beacon_id', 'stage_id', 'coordinate_x', 'coordinate_y', 'created_at', 'updated_at']

	# columns definitions
	id = db.Column(db.Integer, primary_key=True)
	beacon_id = db.Column(
		db.String(40),
		db.ForeignKey('beacons.id'),
		nullable=True
	)
	beacon = db.relationship('Beacon')
	stage_id = db.Column(
		db.String(40),
		db.ForeignKey('stages.id'),
		nullable=True
	)
	stage = db.relationship('Stage')
	coordinate_x = db.Column(db.Integer)
	coordinate_y = db.Column(db.Integer)
	created_at = db.Column(db.DateTime)
	updated_at = db.Column(db.DateTime)

	def __init__(self):
		self.created_at = datetime.datetime.now()
		self.updated_at = datetime.datetime.now()
