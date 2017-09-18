import os
import datetime
from flask import current_app
from app.models import db
from app.services.helper import Helper 
from werkzeug import secure_filename
from sqlalchemy.exc import SQLAlchemyError
from app.models.notification import Notification
from app.services.base_service import BaseService
from app.builders.response_builder import ResponseBuilder


class NotificationService(BaseService):

	def __init__(self, perpage):
		self.perpage = perpage

	def get(self, request, user_id):
		self.total_items = Notification.query.filter_by(receiver_uid=user_id).count()
		if request.args.get('page'):
			self.page = request.args.get('page')
		else:
			self.perpage = self.total_items
			self.page = 1
		self.base_url = request.base_url
        # paginate
		paginate = super().paginate(db.session.query(Notification).filter_by(receiver_uid=user_id).order_by(Notification.created_at.desc()))
		paginate = super().include(['sender', 'receiver'])
		response = ResponseBuilder()
		return response.set_data(paginate['data']).set_links(paginate['links']).build()

	# def show(self, id):
	# 	response = ResponseBuilder()
	# 	feed = db.session.query(Feed).filter_by(id=id).first()
	# 	data = {}
	# 	data = feed.as_dict() if feed else None
	# 	data['user'] = feed.user.include_photos().as_dict()
	# 	return response.set_data(data).build()

	def create(self, payloads):
		response = ResponseBuilder()
		notification = Notification()
		notification.message = payloads['message']
		notification.receiver_uid = payloads['receiver']
		notification.type = payloads['type']
		notification.sender_uid = payloads['user']['id']
		db.session.add(notification)
		try:
			db.session.commit()
			data = notification.as_dict()
			return response.set_data(data).build()
		except SQLAlchemyError as e:
			data = e.orig.args
			return response.set_data(data).set_error(True).build()

	# def save_file(self, file, id=None):
	# 	if file and Helper().allowed_file(file.filename, current_app.config['ALLOWED_EXTENSIONS']):
	# 			filename = secure_filename(file.filename)
	# 			filename = Helper().time_string() + "_" + file.filename.replace(" ", "_")
	# 			file.save(os.path.join(current_app.config['POST_FEED_PHOTO_DEST'], filename))
	# 			return current_app.config['SAVE_FEED_PHOTO_DEST'] + filename
	# 	else:
	# 		return None

	# def update(self, payloads, id):
	# 	response = ResponseBuilder()
	# 	try:
	# 		partner = db.session.query(Partner).filter_by(id=id)
	# 		file = payloads['photo']
	# 		photo = None
	# 		photo = self.save_file(file, id)
	# 		partner.update({
	# 			'name': payloads['name'],
	# 			'email': payloads['email'],
	# 			'website': payloads['website'],
	# 			'photo': photo,
	# 			'type': payloads['type'],
	# 			'updated_at': datetime.datetime.now()
	# 		})
	# 		db.session.commit()
	# 		data = partner.first().as_dict()
	# 		return response.set_data(data).build()
	# 	except SQLAlchemyError as e:
	# 		data = e.orig.args
	# 		return response.set_error(True).set_data(data).build()

	# def delete(self, id):
	# 	response = ResponseBuilder()
	# 	partner = db.session.query(Partner).filter_by(id=id)
	# 	if partner.first() is not None:
	# 		# delete row
	# 		partner.delete()
	# 		db.session.commit()
	# 		return response.set_message('data deleted').build()
	# 	else:
	# 		data = 'data not found'
	# 		return response.set_data(None).set_message(data).set_error(True).build()
