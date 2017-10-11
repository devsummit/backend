from app.controllers.base_controller import BaseController
from app.models.base_model import BaseModel
from app.services import tickettransferservice
from app.services import userservice
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
		password = request.json['password'] if 'password' in request.json else None
		username = user['username']
		if username and password:
			auth = userservice.get_user(username)
			if auth.verify_password(password):
				receiver = request.json['receiver'] if 'receiver' in request.json else None
				user_ticket_id = request.json['user_ticket_id'] if 'user_ticket_id' in request.json else None
				if None in [user, receiver, user_ticket_id]:
					return BaseController.send_error_api(None, 'payload is not valid')
				if str(user['role_id']) in str(ROLE['user']):
					result = tickettransferservice.transfer(user['id'], user_ticket_id, receiver)
				else:
					return BaseController.send_error_api(None, 'this operation is not valid for this type of user')

				if result['error']:
					return BaseController.send_error_api(result['data'], result['message'])
				else:			
					return BaseController.send_response_api(result['data'], result['message'])
			else:
				return BaseController.send_error_api(None, "Password did not match")
		else:
			return BaseController.send_error_api(None, "Password required")
