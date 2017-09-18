from app.controllers.base_controller import BaseController
from app.services import feedservice


class FeedController(BaseController):

	@staticmethod
	def index(request):
		feeds = feedservice.get(request)
		return BaseController.send_response_api(feeds['data'], feeds['message'])

	@staticmethod
	def create(request, user_id):
		message = request.form['message'] if 'message' in request.form else None
		attachment = request.files['attachment'] if request.files['attachment'] else None
		if message:
			payloads = {
				'message': message,
				'user_id': user_id,
				'attachment': attachment
			}
		else:
			return BaseController.send_error_api(None, 'field is not complete')

		result = feedservice.create(payloads)

		if result['error']:
			return BaseController.send_error_api(result['data'], result['message'])
		else:
			return BaseController.send_response_api(result['data'], result['message'], {}. result['links'])

	@staticmethod
	def show(id):
		feed = feedservice.show(id)
		if feed['error']:
			return BaseController.send_error_api(feed['data'], feed['message'])
		return BaseController.send_response_api(feed['data'], feed['message'])

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
