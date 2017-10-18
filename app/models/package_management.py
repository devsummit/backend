import datetime
# import classes
from app.models.base_model import BaseModel
from app.models import db


class PackageManagement(db.Model, BaseModel):
	# table name
	__tablename__ = 'packages_management'
	# displayed fields
	visible = ['id', 'name', 'price', 'quota', 'created_at', 'updated_at']

	# columns definitions
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String)
	price = db.Column(db.Numeric)
	quota = db.Column(db.Integer)
	created_at = db.Column(db.DateTime)
	updated_at = db.Column(db.DateTime)

	def __init__(self):
		self.created_at = datetime.datetime.now()
		self.updated_at = datetime.datetime.now()