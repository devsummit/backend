import datetime
# import classes
from app.models.base_model import BaseModel
from app.models import db


class HackerTeam(db.Model, BaseModel):
	# table name
	__tablename__ = 'hacker_teams'
	# displayed fields
	visible = ['id', 'team_name', 'city', 'project_name', 'points', 'created_at', 'updated_at']

	# columns definitions
	id = db.Column(db.Integer, primary_key=True)
	team_name = db.Column(db.String)
	project_name = db.Column(db.String)
	city = db.Column(db.String)
	points = db.Column(db.Integer)
	created_at = db.Column(db.DateTime)
	updated_at = db.Column(db.DateTime)

	def __init__(self):
		self.created_at = datetime.datetime.now()
		self.updated_at = datetime.datetime.now()
		self.project_name = ''
		self.points = 0
		self.city = '-'