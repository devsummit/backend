from app.controllers.base_controller import BaseController
from app.services import notificationservice


class NotificationController(BaseController):

	@staticmethod
	def index(request, user_id):
		notifications = notificationservice.get(request, user_id)
		return BaseController.send_response_api(notifications['data'], notifications['message'], {}, notifications['links'])

	@staticmethod
	def create(request, user):
		message = request.json['message'] if 'message' in request.json else None
		type = request.json['type'] if 'type' in request.json else None
		attachment = request.json['attachment'] if 'attachment' in request.json else None
		receiver = request.json['receiver'] if 'receiver' in request.json else None
		if message and type:
			payloads = {
				'message': message,
				'type': type,
				'attachment': attachment,
				'user': user,
				'receiver': receiver
			}
		else:
			return BaseController.send_error_api(None, 'field is not complete')

		result = notificationservice.create(payloads)

		if result['error']:
			return BaseController.send_error_api(result['data'], result['message'])
		else:
			return BaseController.send_response_api(result['data'], result['message'])

	# @staticmethod
	# def show(id):
	# 	feed = feedservice.show(id)
	# 	if feed['error']:
	# 		return BaseController.send_error_api(feed['data'], feed['message'])
	# 	return BaseController.send_response_api(feed['data'], feed['message'])

	# @staticmethod
	# def update(id, request):
	# 	name = request.form['name'] if 'name' in request.form else None
	# 	email = request.form['email'] if 'email' in request.form else None
	# 	website = request.form['website'] if 'website' in request.form else None
	# 	type = request.form['type'] if 'type' in request.form else None
	# 	photo = request.files['image_file'] if request.files['image_file'] else None
	# 	if name and website and type:
	# 		payloads = {
	# 			'name': name,
	# 			'email': email,
	# 			'website': website,
	# 			'photo': photo,
	# 			'type': type
	# 		}
	# 	else:
	# 		return BaseController.send_error_api(None, 'field is not complete')
	# 	result = partnerservice.update(payloads, id)

	# 	if not result['error']:
	# 		return BaseController.send_response_api(result['data'], result['message'])
	# 	else:
	# 		return BaseController.send_error_api(result['data'], result['message'])

	# @staticmethod
	# def delete(id):
	# 	partner = partnerservice.delete(id)
	# 	if partner['error']:
	# 		return BaseController.send_response_api(partner['data'], partner['message'])
	# 	return BaseController.send_response_api(partner['data'], partner['message'])
