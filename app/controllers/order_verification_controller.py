from app.controllers.base_controller import BaseController
from app.services import orderverificationservice, slackservice
from app.configs.constants import ROLE, SLACK
from app.models import db
from app.models.order_verification import OrderVerification
from app.models.slack.slack_payment import SlackPayment
from app.models.slack.slack_verify import SlackVerify
from app.configs.constants import SLACK

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
			if SLACK['notification']:
				slackverify = SlackVerify(result)
				slackservice.send_message(slackverify.build())
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
	def verify(id, request):
		data = orderverificationservice.verify(id, request)
		if data['error']:
			return BaseController.send_error_api(data['data'], data['message'])
		order_verification = db.session.query(OrderVerification).filter_by(id=id).first()
		payload = {
			'order_id': order_verification.order.id
		}
		if SLACK['notification']:
			slackpayment = SlackPayment(order_verification.user, payload, False)
			slackservice.send_message(slackpayment.build())
		return BaseController.send_response_api(data['data'], data['message'])
