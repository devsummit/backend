import datetime
from app.models import db
from sqlalchemy.exc import SQLAlchemyError
from app.models.rundown_list import RundownList
from app.configs.constants import EVENT_DATES

class RundownListService():

	def get(self):
		
		return {
				'error': True,
				'data': data
			}
	
	# def create(self, payloads):
	# 	self.model_schedule = Schedule()
	# 	self.model_schedule.stage_id = payloads['stage_id']
	# 	self.model_schedule.event_id = payloads['event_id']
	# 	self.model_schedule.time_start = datetime.datetime.strptime(payloads['time_start'], "%Y-%m-%d %H:%M:%S.%f") 
	# 	self.model_schedule.time_end = datetime.datetime.strptime(payloads['time_end'], "%Y-%m-%d %H:%M:%S.%f") 
	# 	db.session.add(self.model_schedule)
	# 	try:
	# 		db.session.commit()
	# 		data = self.model_schedule
	# 		included = self.get_includes(data)
	# 		return {
	# 			'error': False,
	# 			'data': data.as_dict(),
	# 			'included': included
	# 		}
	# 	except SQLAlchemyError as e:
	# 		data = e.orig.args
	# 		return {
	# 			'error': True,
	# 			'data': data
	# 		}

	# def update(self, payloads, id):
	# 	try:
	# 		self.model_schedule = db.session.query(Schedule).filter_by(id=id)
	# 		self.model_schedule.update({
	# 			'event_id': payloads['event_id'],
	# 			'stage_id': payloads['stage_id'],
	# 			'time_start': datetime.datetime.strptime(payloads['time_start'], "%Y-%m-%d %H:%M:%S.%f"),
	# 			'time_end': datetime.datetime.strptime(payloads['time_end'], "%Y-%m-%d %H:%M:%S.%f"),
	# 			'updated_at': datetime.datetime.now()
	# 		})
	# 		db.session.commit()
	# 		data = self.model_schedule.first()
	# 		included = self.get_includes(data)
	# 		return {
	# 			'error': False,
	# 			'data': data.as_dict(), 
	# 			'included': included
	# 		}
	# 	except SQLAlchemyError as e:
	# 		data = e.orig.args
	# 		return {
	# 			'error': True,
	# 			'data': data
	# 		}

	# def delete(self, id):
	# 	self.model_schedule = db.session.query(Schedule).filter_by(id=id)
	# 	if self.model_schedule.first() is not None:
	# 		# delete row
	# 		self.model_schedule.delete()
	# 		db.session.commit()
	# 		return {
	# 			'error': False,
	# 			'data': None
	# 		}
	# 	else:
	# 		data = 'data not found'
	# 		return {
	# 			'error': True,
	# 			'data': data
	# 		}
	