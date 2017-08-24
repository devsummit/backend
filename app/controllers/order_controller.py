from app.controllers.base_controller import BaseController
from app.models.base_model import BaseModel
from app.services import orderservice


class OrderController(BaseController):

	@staticmethod
	def index():
		orders = orderservice.get()
		return BaseController.send_response_api(orders, 'orders retrieved successfully')

	@staticmethod
	def show(id):
		order = orderservice.show(id)
		if order is None:
			return BaseController.send_error_api(None, 'order not found')
		return BaseController.send_response_api(order.as_dict(), 'order retrieved successfully')

	@staticmethod
	def create(request, user_id):
		order_details = request.json['order_details'] if 'order_details' in request.json else []

		payloads = {
			'user_id': user_id,
			'order_details': order_details
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
