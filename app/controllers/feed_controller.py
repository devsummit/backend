from app.controllers.base_controller import BaseController
from app.services import feedservice


class FeedController(BaseController):

	@staticmethod
	def index(request, page=None):
		feeds = feedservice.get(request, page=page)
		return BaseController.send_response_api(feeds['data'], feeds['message'], {}, feeds['links'])

	@staticmethod
	def create(request, user_id):
		message = request.form['message'] if 'message' in request.form else None
		attachment = request.files['attachment'] if 'attachment' in request.files else None
		payloads = {
			'message': message,
			'user_id': user_id,
			'attachment': attachment
		}

		result = feedservice.create(payloads)

		if result['error']:
			return BaseController.send_error_api(result['data'], result['message'])
		else:
			return BaseController.send_response_api(result['data'], result['message'])

	@staticmethod
	def show(id):
		feed = feedservice.show(id)
		if feed['error']:
			return BaseController.send_error_api(feed['data'], feed['message'])
		return BaseController.send_response_api(feed['data'], feed['message'])

	@staticmethod
	def delete(user, id):
		result = feedservice.delete(user, id)
		if result['error']:
			return BaseController.send_error_api(result['data'], result['message'])
		return BaseController.send_response_api(result['data'], result['message'])