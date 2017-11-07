from app.services import hackatonproposalservice
from app.controllers.base_controller import BaseController


class HackatonProposalController(BaseController):
	
	@staticmethod
	def index(status):
		result = hackatonproposalservice.get(status)
		if result['error']:
			return BaseController.send_error_api(result['data'], result['message'])
		return BaseController.send_response_api(result['data'], result['message'])

	@staticmethod
	def deny(order_id):
		if order_id is None:
			return BaseController.send_error_api(None, 'invalid payload')
		payloads = {
			'order_id': order_id
		}
		result = hackatonproposalservice.deny(payloads)
		if result['error']:
			return BaseController.send_error_api(result['data'], result['message'])
		return BaseController.send_response_api(result['data'], result['message'])

	@staticmethod
	def verify(order_id):
		if order_id is None:
			return BaseController.send_error_api(None, 'invalid payload')
		payloads = {
			'order_id': order_id
		}
		result = hackatonproposalservice.verify(payloads)
		if result['error']:
			return BaseController.send_error_api(result['data'], result['message'])
		return BaseController.send_response_api(result['data'], result['message'])

