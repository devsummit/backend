import os
import datetime
from app.models import db
from sqlalchemy.exc import SQLAlchemyError
from flask import current_app
from PIL import Image
from app.configs.constants import IMAGE_QUALITY
from app.services.helper import Helper 
from werkzeug import secure_filename
from app.models.prize_list import PrizeList
from app.services.base_service import BaseService
from app.builders.response_builder import ResponseBuilder

class PrizeListService(BaseService):

	def get(self, request):
		prizelists = db.session.query(PrizeList).all()
		results = []
		for prizelist in prizelists:
			data = prizelist.as_dict()
			results.append(data)
		response = ResponseBuilder()
		result = response.set_data(results).build()
		return result

	def create(self, payloads):
		response = ResponseBuilder()
		prizelist = PrizeList()
		prizelist.name = payloads['name']
		prizelist.count = payloads['count']
		attachment = self.save_file(payloads['attachment']) if payloads['attachment'] is not None else None
		prizelist.attachment = attachment
		prizelist.point_cost = payloads['point_cost']
		db.session.add(prizelist)
		try:
			db.session.commit()
			data = prizelist.as_dict()
			data['attachment'] = Helper().url_helper(data['attachment'], current_app.config['GET_DEST']) if data['attachment'] is not None else None
			return response.set_data(data).build()
		except SQLAlchemyError as e:
			data = e.orig.args
			return response.set_data(data).set_error(True).build()

	def show(self, id):
		response = ResponseBuilder()
		prizelist = db.session.query(PrizeList).filter_by(id=id).first()
		data = prizelist.as_dict() if prizelist else None
		if data:
			return response.set_data(data).build()
		return response.set_error(True).set_message('data not found').set_data(None).build()

	def update(self, id, payloads):
		response = ResponseBuilder()
		if payloads['attachment'] is not None:
			prizelist_dict = db.session.query(PrizeList).filter_by(id=id).first()
			if prizelist_dict.attachment is not None:
				os.remove(current_app.config['STATIC_DEST'] + prizelist_dict.attachment)
		attachment = self.save_file(payloads['attachment']) if payloads['attachment'] is not None else None
		try:
			prizelist = db.session.query(PrizeList).filter_by(id=id)			
			prizelist.update({
				'name': payloads['name'],
				'point_cost': payloads['point_cost'],
				'attachment': attachment,
				'count': payloads['count'],
				'updated_at': datetime.datetime.now()
			})
			db.session.commit()
			data = prizelist.first()
			return response.set_data(data.as_dict()).build()
		except SQLAlchemyError as e:
			data = e.orig.args
			return response.set_error(True).set_data(data).build()

	def delete(self, id):
		response = ResponseBuilder()
		prizelist_dict = db.session.query(PrizeList).filter_by(id=id).first()
		if prizelist_dict.attachment is not None:
			os.remove(current_app.config['STATIC_DEST'] + prizelist_dict.attachment)
		prizelist = db.session.query(PrizeList).filter_by(id=id)
		if prizelist.first() is not None:
			prizelist.delete()
			db.session.commit()
			return response.set_message('Prize list entry was deleted').build()
		else:
			data = 'Entry not found'
			return response.set_data(None).set_message(data).set_error(True).build()

	def save_file(self, file, id=None):
		image = Image.open(file, 'r')
		if file and Helper().allowed_file(file.filename, current_app.config['ALLOWED_EXTENSIONS']):
			if (Helper().allowed_file(file.filename, ['jpg', 'jpeg'])):
				image = image.convert("RGB")
			filename = secure_filename(file.filename)
			filename = Helper().time_string() + "_" + file.filename.replace(" ", "_")
			image.save(os.path.join(current_app.config['POST_PRIZE_LIST_DEST'], filename), quality=IMAGE_QUALITY, optimize=True)
			return current_app.config['SAVE_PRIZE_LIST_DEST'] + filename
		else:
			return None