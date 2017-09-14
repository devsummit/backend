import os
import datetime
from flask import current_app
from app.models import db
from app.services.helper import Helper 
from sqlalchemy.exc import SQLAlchemyError
from app.models.rundown_list import RundownList
from app.builders.response_builder import ResponseBuilder
from app.configs.constants import EVENT_DATES

class RundownListService():

	def get(self, request):
		rundownlists = db.session.query(RundownList).all()
		results = []		
		for rundownlist in rundownlists:
			data = rundownlist.as_dict()			
			results.append(data)
		return {
			'error': False,
			'data': results,
			'message': 'Schedules retrieved succesfully',
			'included': {}
		}
	
	def create(self, payloads):
		response = ResponseBuilder()
		rundownlist = RundownList()		
		rundownlist.description = payloads['description']
		rundownlist.time_start = datetime.datetime.strptime(payloads['time_start'], "%Y-%m-%d %H:%M:%S.%f")
		rundownlist.time_end = datetime.datetime.strptime(payloads['time_end'], "%Y-%m-%d %H:%M:%S.%f")
		rundownlist.location = payloads['location']
		db.session.add(rundownlist)			
		try:
			db.session.commit()
			data = rundownlist.as_dict()
			return response.set_data(data).build()
		except SQLAlchemyError as e:
			data = e.orig.args
			return response.set_data(data).set_error(True).build()

	def update(self, payloads, id):		
		response = ResponseBuilder()
		try:
			rundownlist = db.session.query(RundownList).filter_by(id=id)
			print (rundownlist)		
			rundownlist.update({
				'description': payloads['description'],
				'time_start': datetime.datetime.strptime(payloads['time_start'], "%Y-%m-%d %H:%M:%S.%f"),
				'time_end': datetime.datetime.strptime(payloads['time_end'], "%Y-%m-%d %H:%M:%S.%f"),				
				'location': payloads['location'],
				'updated_at': datetime.datetime.now()
			})
			db.session.commit()
			data = rundownlist.first()
			return response.set_data(data.as_dict()).build()
		except SQLAlchemyError as e:
			data = e.orig.args
			return response.set_error(True).set_data(data).build()
	
	def show(self, id):
		response = ResponseBuilder()
		result = db.session.query(RundownList).filter_by(id=id).first()
		result = result.as_dict() if result else None
		return response.set_data(result).build()

	def delete(self, id):
		response = ResponseBuilder()
		rundown = db.session.query(RundownList).filter_by(id=id)
		if rundown.first() is not None:
			# delete row
			rundown.delete()
			db.session.commit()
			return response.set_message('data deleted').build()
		else:
			data = 'data not found'
			return response.set_data(None).set_message(data).set_error(True).build()