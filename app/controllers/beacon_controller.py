from app.controllers.base_controller import BaseController
from app.models.base_model import BaseModel
from app.services import beaconservice

class BeaconController(BaseController):

	@staticmethod
	def index():
		beacons = beaconservice.get()
		return BaseController.send_response_api(BaseModel.as_list(beacons), 'stages retrieved successfully')

	@staticmethod
	def create(request):
		code = request.json['code'] if 'code' in request.json else None

		if code:
			payloads = {
				'code': code,
			}
		else:
			return BaseController.send_error_api(None, 'field is not complete')

		result = beaconservice.create(payloads)

		if not result['error']:
			return BaseController.send_response_api(result['data'], 'beacon succesfully created')
		else:
			return BaseController.send_error_api(None, result['data'])

	@staticmethod
	def update(request, id):
		code = request.json['code'] if 'code' in request.json else None

		if code:
			payloads = {
				'code': code,
			}
		else:
			return BaseController.send_error_api(None, 'field is not complete')

		result = beaconservice.update(payloads, id)

		if not result['error']:
			return BaseController.send_response_api(result['data'], 'beacon succesfully updated')
		else:
			return BaseController.send_error_api(None, result['data'])

	@staticmethod
	def delete(id):
		beacon = beaconservice.delete(id)
		if beacon['error']:
			return BaseController.send_response_api(None, 'beacon not found')
		return BaseController.send_response_api(None, 'beacon with id: ' + id + ' has been succesfully deleted')
