from app.controllers.base_controller import BaseController
from app.models.base_model import BaseModel
from app.services import tickettransferservice
from app.configs.constants import ROLE


class TicketTransferController(BaseController):

	@staticmethod
	def ticket_transfer_logs(request, user):
		if user['role_id'] == ROLE['admin']:
			# admin
			result = tickettransferservice.get_logs()
		elif user['role_id'] == ROLE['attendee']:
			# attendee
			result = tickettransferservice.get_logs(user['id'])
		else:
			return BaseController.send_error_api(None, 'resource not accessible for this type of user')

		return BaseController.send_response_api(BaseModel.as_list(result), 'logs retrieved succesfully')

