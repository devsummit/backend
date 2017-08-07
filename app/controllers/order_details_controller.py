from app.controllers.base_controller import BaseController
from app.models.base_model import BaseModel
from app.services import orderdetailservice


class OrderDetailsController(BaseController):

	@staticmethod
	def index(order_id):
		order_details = orderdetailservice.get(order_id)
		return BaseController.send_response_api(BaseModel.as_list(order_details), 'order details retrieved successfully')

	@staticmethod
	def show(order_id, detail_id):
		orderdetail = orderdetailservice.show(order_id, detail_id)
		if orderdetail is None:
			return BaseController.send_error_api(None, 'order item not found')
		return BaseController.send_response_api(orderdetail.as_dict(), 'order item retrieved successfully')

	@staticmethod
	def update(detail_id, request):
		count = request.json['count'] if 'count' in request.json else None

		if count and count > 0:
			payloads = {
				'count': count
			}
		else:
			return BaseController.send_error_api(None, 'item count cannot be 0')

		result = orderdetailservice.update(payloads, detail_id)

		if not result['error']:
			return BaseController.send_response_api(result['data'], 'order item succesfully updated')
		else:
			return BaseController.send_error_api(None, result['data'])

	@staticmethod
	def create(order_id, request):
		ticket_id = request.json['ticket_id'] if 'ticket_id' in request.json else None
		count = request.json['count'] if 'count' in request.json else None

		if ticket_id and count and count > 0:
			payloads = {
				'ticket_id': ticket_id,
				'count': count
			}
		else:
			return BaseController.send_error_api(None, 'wrong payload sent!')

		result = orderdetailservice.create(payloads, order_id)

		if not result['error']:
			return BaseController.send_response_api(result['data'], 'item succesfully added to order')
		else:
			return BaseController.send_error_api(None, result['data'])

	@staticmethod
	def delete(order_id, detail_id):
		orderdetail = orderdetailservice.delete(order_id, detail_id)
		if orderdetail['error']:
			return BaseController.send_response_api(None, 'item not found')
		return BaseController.send_response_api(None, 'order item has been succesfully deleted')
