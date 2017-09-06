import datetime
# import classes
from app.models.base_model import BaseModel
from app.models import db
from app.models.event import Event  # noqa
from app.models.stage import Stage  # noqa


class Schedule(db.Model, BaseModel):
	# table name
	__tablename__ = 'schedules'
	# displayed fields
	visible = ['id', 'user_id', 'event_id', 'time_start', 'time_end', 'created_at', 'updated_at']

	# columns definitions
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(
		db.String(40),
		db.ForeignKey('users.id'),
		nullable=True
	)
	user = db.relationship('User')
	event_id = db.Column(
		db.String(40),
		db.ForeignKey('events.id'),
		nullable=False
	)
	event = db.relationship('Event')

	stage_id = db.Column(
		db.String(40),
		db.ForeignKey('stages.id'),
		nullable=False
	)
	stage = db.relationship('Stage')
	time_start = db.Column(db.DateTime)
	time_end = db.Column(db.DateTime)
	created_at = db.Column(db.DateTime)
	updated_at = db.Column(db.DateTime)

	def __init__(self):
		self.created_at = datetime.datetime.now()
		self.updated_at = datetime.datetime.now()
