import datetime
# import classes
from app.models.base_model import BaseModel
from app.models import db


class BeaconMapVersion(db.Model, BaseModel):
	# table name
	__tablename__ = 'beacon_map_version'
	# displayed fields
	visible = ['version']

	# columns definitions
	version = db.Column(db.Integer, primary_key=True)
