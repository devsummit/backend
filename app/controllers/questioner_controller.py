from app.controllers.base_controller import BaseController
from app.models.base_model import BaseModel
from app.services import questionerservice


class QuestionerController(BaseController):

	@staticmethod
	def index():
		questioners = questionerservice.get()
		return BaseController.send_response_api(BaseModel.as_list(questioners), 'questioners retrieved successfully')

	@staticmethod
	def show(id):
		questioner = questionerservice.show(id)
		return BaseController.send_response_api(questioner)
	
	@staticmethod
	def patch(id, request):
		if request.json['questions']:
			payload = {
				'questions': request.json['questions']
			}
			questioner = questionerservice.patch(id, payload)
			return BaseController.send_response_api(questioner)
		else:
			return BaseController.send_error_api('payload not valid')
