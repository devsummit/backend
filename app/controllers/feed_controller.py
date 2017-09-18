from app.controllers.base_controller import BaseController
from app.services import feedservice


class FeedController(BaseController):

	@staticmethod
	def index(request):
		feeds = feedservice.get(request)
		return BaseController.send_response_api(feeds['data'], feeds['message'], {}, feeds['links'])

	@staticmethod
	def create(request, user_id):
		message = request.form['message'] if 'message' in request.form else None
		attachment = request.files['attachment'] if 'attachment' in request.files else None
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
			return BaseController.send_response_api(result['data'], result['message'])

	@staticmethod
	def show(id):
		feed = feedservice.show(id)
		if feed['error']:
			return BaseController.send_error_api(feed['data'], feed['message'])
		return BaseController.send_response_api(feed['data'], feed['message'])
