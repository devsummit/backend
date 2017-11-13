from app.services import boothcheckinservice
from app.controllers.base_controller import BaseController


class BoothCheckinController(BaseController):
	
	@staticmethod
	def checkin(request, user_id):
		booth_type = request.json['booth_type'] if 'booth_type' in request.json else None
		booth_id = request.json['booth_id'] if 'booth_id' in request.json else None
		speed_dating = request.json['speed_dating'] if 'speed_dating' in request.json else False
		# booth_type:
		# exhibitor -> booth
		# sponsor -> sponsor
		if booth_type and booth_id:
			payloads = {
				'booth_type': booth_type,
				'booth_id': booth_id,
				'speed_dating': speed_dating,
				'user_id': user_id
			}
		else:
			return BaseController.send_error_api(None, 'invalid payload')

		result = boothcheckinservice.checkin(payloads)
		if result['error']:
			return BaseController.send_error_api(result['data'], result['message'])
		return BaseController.send_response_api(result['data'], result['message'])
