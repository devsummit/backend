import datetime

# import classes
from app.models.base_model import BaseModel
from app.models import db


class Questioner(db.Model, BaseModel):
	# table name
	__tablename__ = 'questioners'
	# displayed fields
	visible = ['id', 'booth_id', 'questions', 'created_at', 'updated_at']

	# columns definitions
	id = db.Column(db.Integer, primary_key=True)
	booth_id = db.Column(
		db.String(40),
		db.ForeignKey('booths.id'),
		nullable=False
	)
	questions = db.Column(db.Text)
	created_at = db.Column(db.DateTime)
	updated_at = db.Column(db.DateTime)

	def __init__(self):
		self.created_at = datetime.datetime.now()
		self.updated_at = datetime.datetime.now()
		self.questions = ''
