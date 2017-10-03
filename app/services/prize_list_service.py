import datetime
from app.models import db
from sqlalchemy.exc import SQLAlchemyError
from app.models.prize_list import PrizeList
from app.services.base_service import BaseService
from app.builders.response_builder import ResponseBuilder

class PrizeListService(BaseService):

	def get(request):
		prizelists = db.session.query(PrizeList).all()
		results = []
		for prizelist in prizelists:
			data = prizelist.as_dict()
			results.append(data)
		response = ResponseBuilder()
		result = response.set_data(results).build()
		return result

	def create(payloads):
		response = ResponseBuilder()
		prizelist = PrizeList()
		prizelist.name = payloads['name']
		prizelist.point_cost = payloads['point_cost']
		prizelist.attachment = payloads['attachment']
		prizelist.count = payloads['count']
		db.session.add(prizelist)
		try:
			db.session.commit()
			return response.set_data(prizelist.as_dict()).set_message('Data created succesfully').build()
		except SQLAlchemyError as e:
			data = e.orig.args
			return response.set_data(data).set_error(True).build()

	def show(id):
		response = ResponseBuilder()
		prizelist = db.session.query(PrizeList).filter_by(id=id).first()
		data = prizelist.as_dict() if prizelist else None
		if data:
			return response.set_data(data).build()
		return response.set_error(True).set_message('data not found').set_data(None).build()

	def update(id, payloads):
		response = ResponseBuilder()
		if payloads is not None:
			try:
				prizelist = db.session.query(PrizeList).filter_by(id=id)
				prizelist.update({
					'name': payloads['name'],
					'point_cost': payloads['point_cost'],
					'attachment': payloads['attachment'],
					'count': payloads['count'],
					'updated_at': datetime.datetime.now()
				})
				db.session.commit()
				data = prizelist.first()
				return response.set_data(data.as_dict()).build()
			except SQLAlchemyError as e:
				data = e.orig.args
				return response.set_error(True).set_data(data).build()

	def delete(id):
		response = ResponseBuilder()
		prizelist = db.session.query(PrizeList).filter_by(id=id)
		if prizelist.first() is not None:
			prizelist.delete()
			db.session.commit()
			return response.set_message('Prize list entry was deleted').build()
		else:
			data = 'Entry not found'
			return response.set_data(None).set_message(data).set_error(True).build()