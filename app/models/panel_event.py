import datetime

from app.models import db
from app.models.base_model import BaseModel


class PanelEvent(db.Model, BaseModel):
	# table name
	__tablename__ = 'panel_event'

	# visible fields
	visible = ['id', 'user_id', 'event_id']

	# columns definitions
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(
		db.Integer,
		db.ForeignKey('users.id'),
		nullable=False
	)
	user = db.relationship('User')
	event_id = db.Column(
		db.Integer,
		db.ForeignKey('events.id'),
		nullable=False
	)
	event = db.relationship('Event')

	def __init__(self):
		pass
