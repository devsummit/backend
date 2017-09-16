from app.models import db
from sqlalchemy.exc import SQLAlchemyError
from app.builders.response_builder import ResponseBuilder
# import model class
from app.models.user import User
from app.models.notification import Notification

class NotificationService():

	def get(self):
		response = ResponseBuilder()
		notifications = db.session.query(Notification).all()
		results = []
		for notification in notifications:
			data = notification.as_dict()
			user = notification.user 
			data['user'] = user.as_dict()
			results.append(data)
		return response.set_data(results).build()

	def show(self, id):
		response = ResponseBuilder()
		notification = db.session.query(Notification).filter_by(id=id).first()
		data = notification.as_dict() if notification else None
		if data is not None:
			data['user'] = {}
			data['user'] = notification.user.as_dict()
		return response.set_data(data).build()

	def create(self, payload):
		# check if have team
		response = ResponseBuilder()
		notification = Notification()
		notification.receiver_user_id = payload['receiver_user_id']
		notification.sender_user_id = payload['sender_user_id']
		notification.message = payload['message']
		notification.status = payload['status']
		notification.type = payload['type']
		db.session.add(notification)
		db.session.commit()
		return response.set_data(notification.as_dict()).set_message('notification created').build()

	# def delete(self, id):
	# 	response = ResponseBuilder()
	# 	hacker = db.session.query(Hacker).filter_by(team_id=id)
	# 	hacker.update({
	# 		'team_id': None
	# 	})
	# 	db.session.commit()
	# 	hackerteam = db.session.query(HackerTeam).filter_by(id=id)
	# 	hackerteam.delete()
	# 	try:
	# 		db.session.commit()
	# 		return response.set_data(None).set_message('data deleted successfully').build()			
	# 	except SQLAlchemyError as e:
	# 		message = e.orig.args
	# 		return response.set_error(True).set_data(None).set_message(data).build()
