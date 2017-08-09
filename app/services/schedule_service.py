import datetime
from app.models import db
from sqlalchemy.exc import SQLAlchemyError
# import model class
from app.models.schedule import Schedule


class ScheduleService():

	def __init__(self, model_schedule):
		self.model_schedule = model_schedule

	def get(self):
		schedules = db.session.query(Schedule).all()
		# add includes
		included = self.get_includes(schedules)
		
		return {
			'data': schedules,
			'included': included
		}

	def show(self, id):
		schedule = db.session.query(Schedule).filter_by(id=id).first()
		#  add includes
		included = self.get_includes(schedule)
		print(schedule.as_dict())
		return {
			'data': schedule,
			'included': included
		}

	def create(self, payloads):
		self.model_schedule.user_id = payloads['user_id']
		self.model_schedule.stage_id = payloads['stage_id']
		self.model_schedule.event_id = payloads['event_id']
		self.model_schedule.time_start = datetime.datetime.strptime(payloads['time_start'], '%b %d %Y %I:%M%p')
		self.model_schedule.time_end = datetime.datetime.strptime(payloads['time_end'], '%b %d %Y %I:%M%p')
		db.session.add(self.model_schedule)
		try:
			db.session.commit()
			data = self.model_schedule
			included = self.get_includes(data)
			return {
				'error': False,
				'data': data.as_dict(),
				'included': included
			}
		except SQLAlchemyError as e:
			data = e.orig.args
			return {
				'error': True,
				'data': None
			}

	def update(self, payloads, id):
		try:
			self.model_schedule = db.session.query(Schedule).filter_by(id=id)
			self.model_schedule.update({
				'user_id': payloads['user_id'],
				'event_id': payloads['event_id'],
				'stage_id': payloads['stage_id'],
				'time_start':  datetime.datetime.strptime(payloads['time_start'], '%b %d %Y %I:%M%p'),
				'time_end':  datetime.datetime.strptime(payloads['time_end'], '%b %d %Y %I:%M%p'),
				'updated_at': datetime.datetime.now()
			})
			db.session.commit()
			data = self.model_schedule.first()
			included = self.get_includes(data)
			return {
				'error': False,
				'data': data.as_dict(), 
				'included': included
			}
		except SQLAlchemyError as e:
			data = e.orig.args
			return {
				'error': True,
				'data': data
			}

	def delete(self, id):
		self.model_schedule = db.session.query(Schedule).filter_by(id=id)
		if self.model_schedule.first() is not None:
			# delete row
			self.model_schedule.delete()
			db.session.commit()
			return {
				'error': False,
				'data': None
			}
		else:
			data = 'data not found'
			return {
				'error': True,
				'data': data
			}

	def get_includes(self, schedules) :
		included = []
		if isinstance(schedules, list):
			for schedule in schedules:
				temp = {}
				temp['event'] = schedule.event.as_dict()
				temp['stage'] = schedule.stage.as_dict()
				temp['user'] = schedule.user.as_dict()
				included.append(temp)
		else:
			temp = {}
			temp['event'] = schedules.event.as_dict()
			temp['stage'] = schedules.stage.as_dict()
			temp['user'] = schedules.user.as_dict()
			included.append(temp)
		return included