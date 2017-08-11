import datetime

# import classes
from app.models.base_model import BaseModel
from app.models import db
from app.models.user import User

class Speaker(db.Model, BaseModel):
	# table name
	__tablename__ = 'speakers'
	# displayed fields
	visible = ['id', 'user_id', 'summary', 'information', 'job', 'created_at', 'updated_at']

	# columns definitions
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(
		db.String(40),
		db.ForeignKey('users.id'),
		nullable=False
	)
	user = db.relationship('User')
	information = db.Column(db.Text)
	summary = db.Column(db.String)
	job = db.Column(db.String)
	created_at = db.Column(db.DateTime)
	updated_at = db.Column(db.DateTime)

	def __init__(self):
		self.created_at = datetime.datetime.now()
		self.updated_at = datetime.datetime.now()
