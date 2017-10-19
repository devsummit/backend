from app.controllers.base_controller import BaseController
from app.services import orderservice

class OrderController(BaseController):

	@staticmethod
	def index(user_id):
		orders = orderservice.get(user_id)
		if(len(orders) != 0):
			return BaseController.send_response_api(orders, 'orders retrieved successfully')
		else:
			return BaseController.send_response_api([], 'orders is empty')

	@staticmethod
	def show(id):
		order = orderservice.show(id)
		if order['error']:
			return BaseController.send_error_api(order['data'], order['message'])
		return BaseController.send_response_api(order['data'], order['message'])

	@staticmethod
	def create(request, user):
		order_details = request.json['order_details'] if 'order_details' in request.json else None
		referal_code = request.json['referal_code'] if 'referal_code' in request.json else None
		payment_type = request.json['payment_type'] if 'payment_type' in request.json else None

		if order_details is None or len(order_details) < 1:
			return BaseController.send_error_api({'payload_invalid': True}, 'payload is invalid')

		payloads = {
			'user_id': user['id'],
			'order_details': order_details,
			'referal_code': referal_code,
			'payment_type': payment_type
		}
		
		result = orderservice.create(payloads, user)

		if not result['error']:
			return BaseController.send_response_api(result['data'], 'order succesfully created', result['included'])
		else:
			return BaseController.send_error_api(None, result['message'])

	@staticmethod
	def delete(id, user):
		order = orderservice.delete(id, user)
		if order['error']:
			return BaseController.send_response_api(None, 'order not found')
		return BaseController.send_response_api(None, 'order with id: ' + id + ' has been succesfully deleted')

