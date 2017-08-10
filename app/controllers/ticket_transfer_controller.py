from app.controllers.base_controller import BaseController
from app.models.base_model import BaseModel
from app.services import tickettransferservice
from app.configs.constants import ROLE


class TicketTransferController(BaseController):
    
    @staticmethod
    def ticket_transfer_logs(request, user):
        if user['role_id'] == ROLE['admin']:
			# admin
			result = tickettransferservice.get_admin_log()
		elif user['role_id'] == ROLE['attendee']:
			# attendee
			result = tickettransferservice.get_attendee_log(user['id'])
		elif user['role_id'] == ROLE['booth']:
			# booth
			result = tickettransferservice.get_booth_log(user['id'])

		return BaseController.send_response_api(BaseModel.as_list(result), 'logs retrieved succesfully')

