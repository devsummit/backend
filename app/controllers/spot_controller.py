from app.controllers.base_controller import BaseController
from app.models.base_model import BaseModel
from app.services import spotservice


class SpotController(BaseController):

	@staticmethod
	def index():
		spots = spotservice.get()
		return BaseController.send_response_api(BaseModel.as_list(spots), 'spots retrieved successfully')

	@staticmethod
	def update(request, id):
		beacon_id = request.json['beacon_id'] if 'beacon_id' in request.json else None
		stage_id = request.json['stage_id'] if 'stage_id' in request.json else None

		payloads = {
			'beacon_id': beacon_id,
			'stage_id': stage_id,
		}

		result = spotservice.update(payloads, id)

		if not result['error']:
			return BaseController.send_response_api(result['data'], 'spot succesfully updated')
		else:
			return BaseController.send_error_api(None, result['data'])		
