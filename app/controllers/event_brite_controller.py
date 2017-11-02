from app.controllers.base_controller import BaseController
from app.services import eventbriteservice

class EventBriteController(BaseController):
	
	@staticmethod
	def hook(request):
		result = eventbriteservice.hook(request)
		if result['error']:
			return BaseController.send_error_api(result['data'], result['error'])
		return BaseController.send_response_api(result['data'], result['message'])
