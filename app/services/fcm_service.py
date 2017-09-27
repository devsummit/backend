import datetime
import requests
from app.configs.constants import FCM_SERVER_KEY, FCM_GENERAL_TOPIC
from app.models import db
from sqlalchemy.exc import SQLAlchemyError
# import model class
from app.builders.response_builder import ResponseBuilder
from app.models.notification import Notification
from app.models.user import User


class FCMService():

	def __init__(self):
		self.fcm_url = 'https://fcm.googleapis.com/fcm/send'
		self.headers = {
			'Content-Type': 'application/json',
			'Authorization': FCM_SERVER_KEY
		}


	def send_single_notification(self, title, message, uid, sender_id):
		response = ResponseBuilder()
		user = db.session.query(User).filter_by(id=uid).first().as_dict()
		if not self.save_notification(title, message, uid, sender_id):
			return response.set_error(True).set_message('failed to save notification').set_data(None).build()
		fcmtoken = user['fcmtoken']
		result = self.send_message(fcmtoken, title, message)
		if 'success' in result.json() and result.json()['success'] == 1:
			return response.set_data(result.json()).set_message('notification sent').build()
		
	def save_notification(self, type, message, receiver_id, sender_id):
		notification = Notification()
		notification.sender_uid = sender_id
		notification.receiver_uid = receiver_id
		notification.message = message
		notification.type = type
		db.session.add(notification)
		try:
			db.session.commit()
			return True
		except SQLAlchemyError as e:
			data = e.orig.args
			return False

	def broadcast_notification(self, title, message, sender_id):
		response = ResponseBuilder()
		if not self.save_notification(title, message, None, sender_id):
			return response.set_error(True).set_message('failed to save notification').set_data(None).build()
		result = self.broadcast_message(title, message)
		if 'message_id' in result.json():
			return response.set_data(result.json()).set_message('notification broadcasted').build()
		return response.set_data(None).set_message('an error occured').set_error(True).build()
	
	def broadcast_message(self, title, message):
		data = {
			'to': FCM_GENERAL_TOPIC,
			'notification': {
				'body': message,
				'title': title,
				'icon': 'myicon'
			}
		}
		result = requests.post(self.fcm_url, headers=self.headers, json=data)
		return result

	def send_message(self, fcmtoken, title, message):
		data = {
			'to': fcmtoken,
			'notification': {
				'body': message,
				'title': title,
				'icon': 'myicon'
			}
		}
		result = requests.post(self.fcm_url, headers=self.headers, json=data)
		return result
