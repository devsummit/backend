import datetime
# import classes
from app.models.base_model import BaseModel
from app.models import db
from app.models.user import User  # noqa
from app.models.hacker_team import HackerTeam  # noqa


class Hacker(db.Model, BaseModel):
	# table name
	__tablename__ = 'hackers'
	# displayed fields
	visible = ['id', 'user_id', 'team_id', 'points', 'lead', 'summary', 'created_at', 'updated_at']

	# columns definitions
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(
		db.String(40),
		db.ForeignKey('users.id'),
		nullable=False
	)
	user = db.relationship('User')
	team_id = db.Column(
		db.Integer,
		db.ForeignKey('hacker_teams.id')
	)
	team = db.relationship('HackerTeam')
	summary = db.Column(db.String)
	lead = db.Column(db.Boolean)
	points = db.Column(db.Integer)
	created_at = db.Column(db.DateTime)
	updated_at = db.Column(db.DateTime)

	def __init__(self):
		self.created_at = datetime.datetime.now()
		self.updated_at = datetime.datetime.now()
		self.summary = ''
		self.points = 0
		self.team_id = None