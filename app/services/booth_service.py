from app.models import db
from sqlalchemy.exc import SQLAlchemyError
from app.models.booth import Booth
from app.models.user_booth import UserBooth
from app.models.user import User
from app.services.base_service import BaseService
from app.builders.response_builder import ResponseBuilder
from flask import request, current_app
from app.services.helper import Helper 
import os
import datetime


class BoothService(BaseService):

	def __init__(self, perpage): 
		self.perpage = perpage

	def get(self, request):
		self.total_items = Booth.query.count()
		if request.args.get('page'):
			self.page = request.args.get('page')
		else:
			self.perpage = self.total_items
			self.page = 1
		self.base_url = request.base_url
		paginate = super().paginate(db.session.query(Booth))
		paginate = super().include(['user', 'stage']) 
		for row in paginate['data']:
			row['logo_url'] = Helper().url_helper(row['logo_url'], current_app.config['GET_DEST']) if row['logo_url'] else None
		response = ResponseBuilder()
		result = response.set_data(paginate['data']).set_links(paginate['links']).build()
		return result

	def show(self, id):
		# get the booth id
		response = ResponseBuilder()
		booth = db.session.query(Booth).filter_by(id=id).first()
		if booth is None:
			data = {
				'user_exist': True
			}
			return response.set_data(data).set_error(True).set_message('booth not found').build()
		data = booth.as_dict()
		data['user'] = booth.user.include_photos().as_dict()
		data['logo_url'] = Helper().url_helper(data['logo_url'], current_app.config['GET_DEST'])

		user_booth = db.session.query(UserBooth).filter_by(booth_id=id).all()

		data['members'] = []

		for user in user_booth:
			user_id = user.as_dict()['user_id']
			user = db.session.query(User).filter_by(id=user_id).first()
			data['members'].append(user.include_photos().as_dict())

		data['stage'] = booth.stage.as_dict() if booth.stage else None
		return response.set_data(data).build()

	def update(self, payloads, booth_id):
		response = ResponseBuilder()
		try:
			self.model_booth = db.session.query(Booth).filter_by(id=booth_id)
			self.model_booth.update({
				'stage_id': payloads['stage_id'],
				'points': payloads['points'],
				'summary': payloads['summary']
			})
			db.session.commit()
			data = self.model_booth.first().as_dict()
			data['user'] = self.model_booth.first().user.include_photos().as_dict()
			data['stage'] = self.model_booth.first().stage.as_dict() if payloads['stage_id'] is not None else None
			return response.set_data(data).build()
		except SQLAlchemyError as e:
			data = e.orig.args
			return response.set_error(True).set_data(data).set_message('sql error').build()

	def update_logo(self, payloads, booth_id):
		response = ResponseBuilder()

		file = request.files['image_data']

		if file and Helper().allowed_file(file.filename, current_app.config['ALLOWED_EXTENSIONS']):
			try:
				if not os.path.exists(current_app.config['POST_BOOTH_PHOTO_DEST']):
					os.makedirs(current_app.config['POST_BOOTH_PHOTO_DEST'])

				filename = Helper().time_string() + "_" + file.filename.replace(" ", "_")
				file.save(os.path.join(current_app.config['POST_BOOTH_PHOTO_DEST'], filename))
				newUrl = current_app.config['SAVE_BOOTH_PHOTO_DEST'] + filename
				self.model_booth = db.session.query(Booth).filter_by(id=booth_id)
				self.booth_logo = db.session.query(Booth).filter_by(id=booth_id).first()
				# check in case current profile don't have any logo picture, so need to remove
				if self.booth_logo is not None and self.booth_logo.as_dict()['logo_url'] is not None:
					Helper().silent_remove(current_app.config['STATIC_DEST'] + self.booth_logo.as_dict()['logo_url'])

				self.model_booth.update({
					'logo_url': newUrl,
					'updated_at': datetime.datetime.now()
				})

				db.session.commit()
				data = self.model_booth.first().as_dict()
				data['logo_url'] = Helper().url_helper(data['logo_url'], current_app.config['GET_DEST'])

				return response.set_data(data).set_message('Booth logo updated successfully').build()
			except SQLAlchemyError as e:
				data = e.orig.args
				return response.set_error(True).set_data(None).set_message(data).build()

	def create(self, payloads):
		response = ResponseBuilder()
		self.model_booth = Booth()
		self.model_booth.user_id = payloads['user_id']
		self.model_booth.stage_id = payloads['stage_id']
		self.model_booth.points = payloads['points']
		self.model_booth.summary = payloads['summary']
		db.session.add(self.model_booth)
		try:
			db.session.commit()
			data = self.model_booth.as_dict()
			return response.set_data(data).build()
		except SQLAlchemyError as e:
			data = e.orig.args
			return response.set_data(data).set_error(True).build()
