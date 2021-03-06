from app.controllers.base_controller import BaseController
from app.services import orderservice, slackservice, orderverificationservice
from app.models.slack.slack_order import SlackOrder
from app.services.fcm_service import FCMService
from app.configs.constants import SLACK, ROLE

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
		hacker_team_name = request.json['hacker_team_name'] if 'hacker_team_name' in request.json else None

		if order_details is None or len(order_details) < 1:
			return BaseController.send_error_api({'payload_invalid': True}, 'payload is invalid')

		payloads = {
			'user_id': user['id'],
			'order_details': order_details,
			'referal_code': referal_code,
			'payment_type': payment_type,
			'hacker_team_name': hacker_team_name
		}
		
		result = orderservice.create(payloads, user)

		if not result['error']:
			send_notification = FCMService().send_single_notification('Order Status', 'Your order have been succesfully placed.', user['id'], ROLE['admin'])
			if SLACK['notification']:
				slackorder = SlackOrder(user, result, payment_type)
				slackservice.send_message(slackorder.build())
			return BaseController.send_response_api(result['data'], 'order succesfully created', result['included'])
		else:
			return BaseController.send_error_api(None, result['message'])

	@staticmethod
	def delete(id):
		order = orderservice.delete(id)
		if order['error']:
			return BaseController.send_response_api(None, 'order not found')
		return BaseController.send_response_api(None, 'order with id: ' + id + ' has been succesfully deleted')
	
	@staticmethod
	def unverified_order():
		orders = orderservice.unverified_order()
		if orders['error']:
			return BaseController.send_error_api(orders['data'], orders['message'])
		return BaseController.send_response_api(orders['data'], orders['message'])

	@staticmethod
	def verify_order(id, request):
		result = orderverificationservice.admin_verify(id, request)
		if result['error']:
			return BaseController.send_error_api(result['data'], result['message'])
		return BaseController.send_response_api(None, result['message'])
