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
		name = request.form['name'] if 'name' in request.form else None
		point_cost = request.form['point_cost'] if 'point_cost' in request.form else None
		attachment = request.files['attachment'] if 'attachment' in request.files else None
		count = request.form['count'] if 'count' in request.form else None
		if name and point_cost and count and attachment:
			payloads = {
				'name': name,
				'point_cost': point_cost,
				'attachment': attachment,
				'count': count
			}
			result = prizelistservice.create(payloads)
			if result['error']:
				return BaseController.send_error_api(result['data'], result['message'])
			else:
				return BaseController.send_response_api(result['data'], result['message'])
		else:
			return BaseController.send_error_api(None, 'payload is invalid')

	@staticmethod
	def show(id):
		prizelist = prizelistservice.show(id)
		return BaseController.send_response_api(prizelist['data'], prizelist['message'])

	@staticmethod
	def update(id, request):
		name = request.form['name'] if 'name' in request.form else None
		point_cost = request.form['point_cost'] if 'point_cost' in request.form else None
		attachment = request.files['attachment'] if 'attachment' in request.files else None
		count = request.form['count'] if 'count' in request.form else None
		if name or point_cost or count or attachment:
			payloads = {
				'name': name,
				'point_cost': point_cost,
				'attachment': attachment,
				'count': count
			}
			result = prizelistservice.update(id, payloads)
			if result['error']:
				return BaseController.send_error_api(result['data'], result['message'])
			else:
				return BaseController.send_response_api(result['data'], result['message'])
		else:
			return BaseController.send_error_api({}, 'payload is invalid')

	@staticmethod
	def delete(id):
		data = prizelistservice.delete(id)
		if data['error']:
			return BaseController.send_error_api(data['data'], data['message'])
		return BaseController.send_response_api(data['data'], data['message'])			