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
		if order is None:
			return BaseController.send_error_api(None, 'order not found')
		return BaseController.send_response_api(order.as_dict(), 'order retrieved successfully')

	@staticmethod
	def create(request, user_id):
		order_details = request.json['order_details'] if 'order_details' in request.json else None
		referal_code = request.json['referal_code'] if 'referal_code' in request.json else None
		payment_type = request.json['payment_type'] if 'payment_type' in request.json else None
		currency = request.json['currency'] if 'currency' in request.json else None
		gross_amount = request.json['gross_amount'] if 'gross_amount' in request.json else None

		if order_details is None or len(order_details) < 1:
			return BaseController.send_error_api({'payload_invalid': True}, 'payload is invalid')

		payloads = {
			'user_id': user_id,
			'order_details': order_details,
			'referal_code': referal_code 
		}
		
		result = orderservice.create(payloads)

		if not result['error']:
			return BaseController.send_response_api(result['data'], 'order succesfully created', result['included'])
		else:
			return BaseController.send_error_api(None, result['data'])

	@staticmethod
	def delete(id):
		order = orderservice.delete(id)
		if order['error']:
			return BaseController.send_response_api(None, 'order not found')
		return BaseController.send_response_api(None, 'order with id: ' + id + ' has been succesfully deleted')

