from app.controllers.base_controller import BaseController
from app.models.base_model import BaseModel
from app.services import stageservice


class StageController(BaseController):

	@staticmethod
	def index():
		stages = stageservice.get()
		return BaseController.send_response_api(BaseModel.as_list(stages), 'stages retrieved successfully')

	@staticmethod
	def indexPicture(stage_id):
		stage_pictures = stageservice.getPictures(stage_id)
		return BaseController.send_response_api(stage_pictures, 'stage pictures retrieved successfully')

	@staticmethod
	def show(id):
		stage = stageservice.show(id)
		if stage is None:
			return BaseController.send_error_api(None, 'stage not found')
		return BaseController.send_response_api(stage.as_dict(), 'stage retrieved successfully')

	@staticmethod
	def showPicture(stage_id, id):
		stage_picture = stageservice.showPicture(stage_id, id)
		if stage_picture is None:
			return BaseController.send_error_api(None, 'stage picture not found')
		return BaseController.send_response_api(stage_picture, 'stage picture retrieved successfully')

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
	def createPicture(request, stage_id):
		image_file = request.files
		payloads = {
			'stage_id': stage_id,
			'image_file': image_file
		}

		result = stageservice.createPicture(payloads)

		if not result['error']:
			return BaseController.send_response_api(result['data'], 'stage picture succesfully created')
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
	def updatePicture(request, stage_id, id):
		image_file = request.files

		payloads = {
			'image_file': image_file
		}

		result = stageservice.updatePicture(payloads, stage_id, id)

		if not result['error']:
			return BaseController.send_response_api(result['data'], 'stage picture succesfully updated')
		else:
			return BaseController.send_error_api(None, result['data'])

	@staticmethod
	def delete(id):
		stage = stageservice.delete(id)
		if stage['error']:
			return BaseController.send_response_api(None, 'stage not found')
		return BaseController.send_response_api(None, 'stage with id: ' + id + ' has been succesfully deleted')

	@staticmethod
	def deletePicture(stage_id, id):
		stage_picture = stageservice.deletePicture(stage_id, id)
		if stage_picture['error']:
			return BaseController.send_response_api(None, 'stage picture not found')
		return BaseController.send_response_api(None, 'stage picture with id: ' + id + ' has been succesfully deleted')
