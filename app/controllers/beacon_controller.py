from app.controllers.base_controller import BaseController
from app.models.base_model import BaseModel
from app.services import beaconservice


class BeaconController(BaseController):

	@staticmethod
	def index():
		beacons = beaconservice.get()
		if beacons['error']:
			return BaseController.send_error_api(beacons['data'], beacons['message'])
		return BaseController.send_response_api(beacons['data'], beacons['message'])

	@staticmethod
	def show(id):
		beacon = beaconservice.show(id)
		if beacon['error']:
			return BaseController.send_error_api(beacon['data'], beacon['message'])
		return BaseController.send_response_api(beacon['data'], beacon['message'])

	@staticmethod
	def create(request):
		uuid = request.json['uuid'] if 'uuid' in request.json else None
		type = request.json['type'] if 'type' in request.json else None
		type_id = request.json['type_id'] if 'type_id' in request.json else None
		description = request.json['description'] if 'description' in request.json else ''
		if uuid and type and type_id:
			payloads = {
				'uuid': uuid,
				'type': type,
				'type_id': type_id,
				'description': description,
			}
		else:
			return BaseController.send_error_api(None, 'invalid payload')

		result = beaconservice.create(payloads)

		if not result['error']:
			return BaseController.send_response_api(result['data'], result['message'])
		else:
			return BaseController.send_error_api(result['data'], result['message'])

	@staticmethod
	def update(request, id):
		uuid = request.json['uuid'] if 'uuid' in request.json else None
		type = request.json['type'] if 'type' in request.json else None
		type_id = request.json['type_id'] if 'type_id' in request.json else None
		description = request.json['description'] if 'description' in request.json else ''
		
		if uuid and type and type_id:
			payloads = {
				'uuid': uuid,
				'type': type,
				'type_id': type_id,
				'description': description,
			}
		else:
			return BaseController.send_error_api(None, 'invalid payload')

		result = beaconservice.update(payloads, id)

		if result['error']:
			return BaseController.send_error_api(result['data'], result['message'])
		return BaseController.send_response_api(result['data'], result['message'])

	@staticmethod
	def delete(id):
		beacon = beaconservice.delete(id)
		if beacon['error']:
			return BaseController.send_response_api(None, 'beacon not found')
		return BaseController.send_response_api(None, 'beacon with id: ' + id + ' has been succesfully deleted')
