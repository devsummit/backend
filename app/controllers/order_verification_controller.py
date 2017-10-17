from app.controllers.base_controller import BaseController
from app.services import orderverificationservice
from app.configs.constants import ROLE


class OrderVerificationController(BaseController):

	@staticmethod
	def index(request, user):
		if (user['role_id'] != ROLE['admin']):
			return 'Unauthorized User'
		else:
			order_verification_details = orderverificationservice.get()
		return BaseController.send_response_api(order_verification_details, 'order verification details retrieved successfully')

	@staticmethod
	def create(request):
		payment_proof = request.files['payment_proof'] if 'payment_proof' in request.files else ''
		order_id = request.form['order_id'] if 'order_id' in request.form else ''
		if payment_proof and order_id:
			payloads = {
				'order_id': order_id,
				'payment_proof': payment_proof
			}
		else:
			return BaseController.send_error_api(None, 'field is not complete')
		result = orderverificationservice.create(payloads)
		if not result['error']:
			return BaseController.send_response_api(result['data'], result['message'])
		else:
			return BaseController.send_error_api(result['data'], result['message'])

	@staticmethod
	def show(id, request):
		orderverification = orderverificationservice.show(id)
		return BaseController.send_response_api(orderverification['data'], orderverification['message'])	

	
	@staticmethod
	def update(id, request):
		user_id = request.form['user_id'] if 'user_id' in request.form else None
		order_id = request.form['order_id'] if 'order_id' in request.form else None
		payment_proof = request.files['payment_proof'] if 'payment_proof' in request.files else None
		if user_id or order_id or payment_proof:
			payloads = {
				'user_id': user_id,
				'order_id': order_id,
				'payment_proof': payment_proof
			}
		else:
			return BaseController.send_error_api(None, 'field is not complete')
		result = orderverificationservice.update(id, payloads)
		if not result['error']:
			return BaseController.send_response_api(result['data'], result['message'])
		else:
			return BaseController.send_error_api(result['data'], result['message'])

	@staticmethod
	def delete(id):
		data = orderverificationservice.delete(id)
		if data['error']:
			return BaseController.send_error_api(data['data'], data['message'])
		return BaseController.send_response_api(data['data'], data['message'])


	@staticmethod
	def verify(id, request, user_id):
		data = orderverificationservice.verify(id, user_id)
		if data['error']:
			return BaseController.send_error_api(data['data'], data['message'])
		return BaseController.send_response_api(data['data'], data['message'])
