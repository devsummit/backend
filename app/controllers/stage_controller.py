from app.controllers.base_controller import BaseController
from app.models.base_model import BaseModel
from app.services import stageservice


class StageController(BaseController):

	@staticmethod
	def index():
		stages = stageservice.get()
		return BaseController.send_response_api(BaseModel.as_list(stages), 'stages retrieved successfully')

	@staticmethod
	def show(id):
		stage = stageservice.show(id)
		if stage is None:
			return BaseController.send_error_api(None, 'stage not found')
		return BaseController.send_response_api(stage.as_dict(), 'stage retrieved successfully')

	@staticmethod
	def create(request):
		name = request.json['name'] if 'name' in request.json else None
		stage_type = request.json['stage_type'] if 'stage_type' in request.json else None
		information = request.json['information'] if 'information' in request.json else ''

		if name and stage_type:
			payloads = {
				'name': name,
				'stage_type': stage_type,
				'information': information
			}
		else:
			return BaseController.send_error_api(None, 'field is not complete')

		result = stageservice.create(payloads)

		if not result['error']:
			return BaseController.send_response_api(result['data'], 'stage succesfully created')
		else:
			return BaseController.send_error_api(None, result['data'])

	@staticmethod
	def update(request, id):
		name = request.json['name'] if 'name' in request.json else None
		stage_type = request.json['stage_type'] if 'stage_type' in request.json else None
		information = request.json['information'] if 'information' in request.json else ''

		if name and stage_type:
			payloads = {
				'name': name,
				'stage_type': stage_type,
				'information': information
			}
		else:
			return BaseController.send_error_api(None, 'field is not complete')

		result = stageservice.update(payloads, id)

		if not result['error']:
			return BaseController.send_response_api(result['data'], 'stage succesfully updated')
		else:
			return BaseController.send_error_api(None, result['data'])

	@staticmethod
	def delete(id):
		stage = stageservice.delete(id)
		if stage['error']:
			return BaseController.send_response_api(None, 'stage not found')
		return BaseController.send_response_api(None, 'stage with id: ' + id + ' has been succesfully deleted')
