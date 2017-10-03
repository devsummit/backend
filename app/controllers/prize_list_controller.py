from app.controllers.base_controller import BaseController
from app.services import prizelistservice


class PrizeListController(BaseController):

	@staticmethod
	def get(request):
		prizelist = prizelistservice.get(request)
		if prizelist['error']:
			return BaseController.send_error(prizelist['data'], prizelist['message'])
		return BaseController.send_response_api(prizelist['data'], prizelist['message'], prizelist['included'])

	@staticmethod
	def create(request):
		name = request.json['name'] if 'name' in request.json else None
		point_cost = request.json['point_cost'] if 'point_cost' in request.json else None
		attachment = request.json['attachment'] if 'attachment' in request.json else None
		count = request.json['count'] if 'count' in request.json else ''
		if name and point_cost and count and attachment:
			payloads = {
				'name': name,
				'point_cost': point_cost,
				'attachment': attachment,
				'count': count
			}
		else:
			BaseController.send_error_api(None, 'payload is invalid')

		result = prizelistservice.create(payloads)

		if result['error']:
			return BaseController.send_error_api(result['data'], result['message'])

		return BaseController.send_response_api(result['data'], result['message'])

	@staticmethod
	def show(id):
		prizelist = prizelistservice.show(id)
		return BaseController.send_response_api(prizelist['data'], prizelist['message'])

	@staticmethod
	def update(id, request):
		name = request.json['name'] if 'name' in request.json else None
		point_cost = request.json['point_cost'] if 'point_cost' in request.json else None
		attachment = request.json['attachment'] if 'attachment' in request.json else None
		count = request.json['count'] if 'count' in request.json else None

		payloads = {
			'name': name,
			'point_cost': point_cost,
			'attachment': attachment,
			'count': count
		}

		result = prizelistservice.update(id, payloads)

		if result['error']:
			return BaseController.send_error_api(result['data'], result['message'])
		return BaseController.send_response_api(result['data'], result['message'])

	@staticmethod
	def delete(id):
		data = prizelistservice.delete(id)
		if data['error']:
			return BaseController.send_error_api(data['data'], data['message'])
		return BaseController.send_response_api(data['data'], data['message'])			