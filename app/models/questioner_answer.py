import datetime

# import classes
from app.models.base_model import BaseModel
from app.models import db


class QuestionerAnswer(db.Model, BaseModel):
	# table name
	__tablename__ = 'questioner_answers'
	# displayed fields
	visible = ['id', 'user_id', 'questioner_id', 'answers', 'created_at', 'updated_at']

	# columns definitions
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(
		db.Integer,
		db.ForeignKey('users.id'),
		nullable=False
	)
	questioner_id = db.Column(
		db.Integer,
		db.ForeignKey('questioners.id'),
		nullable=False
	)
	answers = db.Column(db.Text)
	created_at = db.Column(db.DateTime)
	updated_at = db.Column(db.DateTime)

	def __init__(self):
		self.created_at = datetime.datetime.now()
		self.updated_at = datetime.datetime.now()
		self.answers = ''
