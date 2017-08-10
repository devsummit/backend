from app.controllers.base_controller import BaseController
from app.models.base_model import BaseModel
from app.services import tickettransferservice
from app.configs.constants import ROLE


class TicketTransferController(BaseController):

	@staticmethod
	def ticket_transfer_logs(user):
		if user['role_id'] == ROLE['admin']:
			# admin
			result = tickettransferservice.get_logs()
		elif user['role_id'] == ROLE['attendee']:
			# attendee
			result = tickettransferservice.get_logs(user['id'])
		else:
			return BaseController.send_error_api(None, 'resource not accessible for this type of user')

		return BaseController.send_response_api(BaseModel.as_list(result), 'logs retrieved succesfully')

	def ticket_transfer(request, user):
		receiver_user_id = request.json['receiver_user_id']
		user_ticket_id = request.json['user_ticket_id']

		if user['role_id'] == ROLE['attendee']:
			result = tickettransferservice.transfer(user['id'], user_ticket_id, receiver_user_id)
		else:
			return BaseController.send_error_api(None, 'this operation is not valid for this type of user')

		if result['error']:
			return BaseController.send_error_api(result['data'], 'transfer failed')
		else:			
			return BaseController.send_response_api(result['data'], 'ticket transfered successfully')
