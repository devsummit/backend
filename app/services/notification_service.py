import os
import datetime
from flask import current_app
from app.models import db
from app.services.helper import Helper 
from werkzeug import secure_filename
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import or_
from app.models.notification import Notification
from app.services.base_service import BaseService
from app.builders.response_builder import ResponseBuilder


class NotificationService(BaseService):

	def __init__(self, perpage):
		self.perpage = perpage

	def get(self, request, user_id):
		self.total_items = Notification.query.filter(or_(Notification.receiver_uid == user_id, Notification.receiver_uid == None)).count()
		if request.args.get('page'):
			self.page = request.args.get('page')
		else:
			self.perpage = self.total_items
			self.page = 1
		self.base_url = request.base_url
        # paginate
		paginate = super().paginate(db.session.query(Notification).filter(or_(Notification.receiver_uid == user_id, Notification.receiver_uid == None)).order_by(Notification.created_at.desc()))
		paginate = super().include(['sender', 'receiver'])
		response = ResponseBuilder()
		return response.set_data(paginate['data']).set_links(paginate['links']).build()

	def show(self, id):
		response = ResponseBuilder()
		notification = db.session.query(Notification).filter_by(id=id).first()
		data = {}
		data = notification.as_dict() if notification else None
		data['receiver'] = notification.receiver.include_photos().as_dict()
		data['sender'] = notification.sender.include_photos().as_dict()
		return response.set_data(data).build()

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
			data['receiver'] = notification.receiver.include_photos().as_dict()
			data['sender'] = notification.sender.include_photos().as_dict()
			return response.set_data(data).build()
		except SQLAlchemyError as e:
			data = e.orig.args
			return response.set_data(data).set_error(True).build()
