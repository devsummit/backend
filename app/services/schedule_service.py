import datetime
from app.models import db
from sqlalchemy.exc import SQLAlchemyError
# import model class
from app.models.schedule import Schedule
from app.models.booth import Booth
from app.models.speaker import Speaker
from app.models.panel_event import PanelEvent
from app.configs.constants import EVENT_DATES
from app.builders.response_builder import ResponseBuilder


class ScheduleService():

	def get(self):
		schedules = db.session.query(Schedule).order_by(Schedule.time_start.asc()).all()
		results = []
		for schedule in schedules:
			data = schedule.as_dict()
			event = schedule.event
			user = event.user
			stage = schedule.stage
			if event.type == 'discuss panel':
				_result = []
				_speaker = []
				pes = db.session.query(PanelEvent).filter_by(event_id=event.id).all()
				for pe in pes:
					_result.append(pe.user.include_photos().as_dict())
					speaker = db.session.query(Speaker).filter_by(user_id=pe.user_id).first()
					_speaker.append(speaker.as_dict())

				data['user'] = _result
				for n in range(0, len(data['user'])):
					data['user'][n]['speaker'] = _speaker[n]
			else:
				data['user'] = user.include_photos().as_dict() if user else {}

			data['event'] = event.as_dict() if event else {}
			data['stage'] = stage.as_dict() if stage else {}
			speaker = None
			if event.type != 'discuss panel':
				if data['user'] and data['user']['role_id'] == 4:
					speaker = db.session.query(Speaker).filter_by(user_id=data['user']['id']).first()
			
			data['speaker'] = speaker.as_dict() if speaker else {}

			results.append(data)
		return {
			'error': False,
			'data': results,
			'message': 'Schedules retrieved succesfully',
			'included': {}
		}

	def filter(self, param):
		schedules = self.get()['data']
		results = []
		day1 = []
		day2 = []
		day3 = []
		for schedule in schedules:
			if schedule['event'] is not None and EVENT_DATES['1'] in schedule['time_start']:
				day1.append(schedule)
			elif schedule['event'] is not None and EVENT_DATES['2'] in schedule['time_start']:
				day2.append(schedule)
			elif schedule['event'] is not None and EVENT_DATES['3'] in schedule['time_start']:
				day3.append(schedule)
		response = ResponseBuilder()

		if param == 'day-1': 
			results = day1
		elif param == 'day-2':
			results = day2
		elif param == 'day-3':
			results = day3
		else:
			results.append(day1)
			results.append(day2)
			results.append(day3)

		result = response.set_data(results).build()
		return result

	def show(self, id):
		schedule = db.session.query(Schedule).filter_by(id=id).first()
		data = schedule.as_dict()
		event = schedule.event
		data['event'] = event.as_dict()
		if event.type == 'discuss panel':
			_result_user = []
			_result_speaker = []
			pes = db.session.query(PanelEvent).filter_by(event_id=event.id).all()
			for pe in pes:
				user = pe.user.include_photos().as_dict()
				speaker = db.session.query(Speaker).filter_by(user_id=pe.user.id).first()
				user['speaker'] = speaker.as_dict()
				_result_user.append(user)
			data['user'] = _result_user
		else:
			data['user'] = event.user.include_photos().as_dict()

		#  add includes
		if schedule is None:
			return {
				'error': True,
				'data': None,
				'message': 'Schedule not found'
			}
		return {
			'error': False,
			'data': data,
			'message': 'Schedule retrieved successfully',
		}

	def create(self, payloads):
		self.model_schedule = Schedule()
		self.model_schedule.stage_id = payloads['stage_id']
		self.model_schedule.event_id = payloads['event_id']
		self.model_schedule.time_start = datetime.datetime.strptime(payloads['time_start'], "%Y-%m-%d %H:%M:%S.%f") 
		self.model_schedule.time_end = datetime.datetime.strptime(payloads['time_end'], "%Y-%m-%d %H:%M:%S.%f") 
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
				'data': data
			}

	def update(self, payloads, id):
		try:
			self.model_schedule = db.session.query(Schedule).filter_by(id=id)
			self.model_schedule.update({
				'event_id': payloads['event_id'],
				'stage_id': payloads['stage_id'],
				'time_start': datetime.datetime.strptime(payloads['time_start'], "%Y-%m-%d %H:%M:%S.%f"),
				'time_end': datetime.datetime.strptime(payloads['time_end'], "%Y-%m-%d %H:%M:%S.%f"),
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
				temp['user'] = schedule.event.user.as_dict() if schedule.event.user else None
				included.append(temp)
		else:
			temp = {}
			temp['event'] = schedules.event.as_dict()
			temp['stage'] = schedules.stage.as_dict()
			temp['user'] = schedules.event.user.as_dict() if schedules.event.user else None
			included.append(temp)
		return included
