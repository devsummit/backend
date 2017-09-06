import datetime
from app.models import db
from sqlalchemy.exc import SQLAlchemyError
# import model class
from app.models.schedule import Schedule
from app.models.user import User
from app.models.event import Event
from app.models.booth import Booth
from app.models.speaker import Speaker


class ScheduleService():

	def get(self):
		schedules = db.session.query(Schedule).all()
		results = []
		for schedule in schedules:
			user = db.session.query(User).filter_by(id=schedule.user_id).first()
			event = db.session.query(Event).filter_by(id=schedule.event_id).first()
			schedule = schedule.as_dict()
			schedule['user'] = user.as_dict() if user else None
			schedule['event'] = event.as_dict() if event else None

			if schedule['user']['role_id'] == 3:
				booth = db.session.query(Booth).filter_by(user_id=schedule['user_id']).first()
				schedule['booth'] = booth.as_dict() if booth else None
			elif schedule['user']['role_id'] == 4:
				speaker = db.session.query(Speaker).filter_by(user_id=schedule['user_id']).first()
				schedule['speaker'] = speaker.as_dict() if speaker else None

			results.append(schedule)
			
		# # add includes
		# included = self.get_includes(results)
		return {
			'data': results,
			'included': {}
		}

	def filter(self, param):
		schedules = self.get()['data'];
		results = []
		for schedule in schedules:
			if schedule['event'] is not None and schedule['event']['type'] == param:
				results.append(schedule)
		return {
			'data': results,
			'included': {}
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
		self.model_schedule = Schedule()
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
				'time_start': datetime.datetime.strptime(payloads['time_start'], '%b %d %Y %I:%M%p'),
				'time_end': datetime.datetime.strptime(payloads['time_end'], '%b %d %Y %I:%M%p'),
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

	def get_includes(self, schedules):
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
