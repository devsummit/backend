from datetime import datetime, timedelta
from app.models.base_model import BaseModel
from app.models import db


class Feed(db.Model, BaseModel):

	__tablename__ = 'feeds'


	visible = ['id', 'message', 'user_id', 'attachment', 'created_at', 'updated_at', 'deleted_at']


	id = db.Column(db.Integer, primary_key=True)
	message = db.Column(db.Text)
	attachment = db.Column(db.String)
	user_id = db.Column(
		db.Integer,
		db.ForeignKey('users.id'),
		nullable=False
	)
	sponsor_id = db.Column(db.Integer)
	user = db.relationship('User')
	type = db.Column(db.String(40))
	redirect_url = db.Column(db.String)
	created_at = db.Column(db.DateTime)
	updated_at = db.Column(db.DateTime)
	deleted_at = db.Column(db.DateTime)

	def __init__(self):
<<<<<<< HEAD
		self.created_at = datetime.now()
		self.updated_at = datetime.now()
		self.deleted_at = datetime.now()
	
=======
		self.created_at = datetime.now() + timedelta(hours=7) 
		self.updated_at = datetime.now() + timedelta(hours=7)
		self.type = 'user'
>>>>>>> develop
