from app.controllers.base_controller import BaseController
from app.models.base_model import BaseModel
from app.services import referalservice


class ReferalController(BaseController):

	@staticmethod
	def index():
		referals = referalservice.get()
		return BaseController.send_response_api(referals, 'referals retrieved successfully')

	@staticmethod
	def show(id):
		referal = referalservice.show(id)
		if referal is None:
			return BaseController.send_error_api(None, 'referal not found')
		return BaseController.send_response_api(referal, 'referal retrieved successfully')

	@staticmethod
	def create(request):
		owner_type = request.json['owner_type'] if 'owner_type' in request.json else None
		owner_id = request.json['owner_id'] if 'owner_id' in request.json else None
		discount_amount = 0.1 # 10% discount fix
		referal_code = request.json['referal_code'] if 'referal_code' in request.json else ''
		quota = request.json['quota'] if 'quota' in request.json else 1

		if discount_amount and referal_code and quota and owner_type and owner_id:
			payloads = {
				'owner_type': owner_type,
				'owner_id': owner_id,
				'discount_amount': discount_amount,
				'referal_code': referal_code,
				'quota': quota
			}
		else:
			return BaseController.send_error_api({'payload_invalid': True}, 'field is not complete')

		result = referalservice.create(payloads)

		if not result['error']:
			return BaseController.send_response_api(result['data'], result['message'])
		else:
			return BaseController.send_error_api(result['data'], result['message'])

	@staticmethod
	def update(request, id):
		quota = request.json['quota'] if 'quota' in request.json else 1

		if quota:
			payloads = {
				'quota': quota
			}
		else:
			return BaseController.send_error_api({'payload_invalid': True}, 'field is not complete')

		result = referalservice.update(payloads, id)

		if not result['error']:
			return BaseController.send_response_api(result['data'], result['message'])
		else:
			return BaseController.send_error_api(result['data'], result['message'])

	@staticmethod
	def reward_referal(user):
		referal = referalservice.reward_referal(user)
		if referal['error']:
			return BaseController.send_error_api(referal['data'], referal['message'])
		return BaseController.send_response_api(referal['data'], referal['message'])

	@staticmethod
	def delete(id):
		referal = referalservice.delete(id)
		if referal['error']:
			return BaseController.send_response_api(None, 'referal not found')
		return BaseController.send_response_api(None, 'referal with id: ' + id + ' has been succesfully deleted')

	@staticmethod
	def check(request, user):
		referal_code = request.json['referal_code'] if 'referal_code' in request.json else None
		if referal_code:
			# process
			referal = referalservice.check_referal_code(referal_code, user)
			if referal['error']:
				return BaseController.send_error_api(referal['data'], referal['message'])
			return BaseController.send_response_api(referal['data'], referal['message'])

		return BaseController.send_error_api({'payload_invalid': True}, 'payload is not valid')
