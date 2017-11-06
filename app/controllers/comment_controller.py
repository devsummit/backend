from app.services import commentservice
from app.controllers.base_controller import BaseController


class CommentController(BaseController):
	
	@staticmethod
	def index(request, feed_id, page):
		# implement your get method
		result = commentservice.get_by_post_id(request, feed_id, page)
		if result['error']:
			return BaseController.send_error_api(result['data'], result['message'])
		return BaseController.send_response_api(result['data'], result['message'], {}, result['links'])

	@staticmethod
	def create(request, feed_id, user):
		# implement your create method
		content = request.json['content'] if 'content' in request.json else None
		if content:
			payload = {
				'content': content,
				'user_id': user.id,
				'feed_id': feed_id
			}
		else:
			return BaseController.send_error_api(None, 'invalid payload')

		result = commentservice.create(payload)
		if result['error']:
			return BaseController.send_error_api(result['data'], result['message'])
		return BaseController.send_response_api(result['data'], result['message'])
