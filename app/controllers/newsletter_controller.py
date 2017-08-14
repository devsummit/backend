from app.controllers.base_controller import BaseController
from app.models.base_model import BaseModel
from app.services import newsletterservice


class NewsletterController(BaseController):

	@staticmethod
	def index():
		newsletters = newsletterservice.get()
		return BaseController.send_response_api(BaseModel.as_list(newsletters), 'newsletters retrieved successfully')

	@staticmethod
	def create(request):
		email = request.json['email'] if 'email' in request.json else None

		if email:
			payloads = {
				'email': email,
			}
		else:
			return BaseController.send_error_api(None, 'field is not complete')

		result = newsletterservice.create(payloads)

		if not result['error']:
			return BaseController.send_response_api(result['data'], 'email succesfully added')
		else:
			return BaseController.send_error_api(None, result['data'])

	@staticmethod
	def update(request, id):
		email = request.json['email'] if 'email' in request.json else None

		if email:
			payloads = {
				'email': email,
			}
		else:
			return BaseController.send_error_api(None, 'field is not complete')

		result = newsletterservice.update(payloads, id)

		if not result['error']:
			return BaseController.send_response_api(result['data'], 'email succesfully updated')
		else:
			return BaseController.send_error_api(None, result['data'])

	@staticmethod
	def delete(id):
		newsletter = newsletterservice.delete(id)
		if newsletter['error']:
			return BaseController.send_response_api(None, 'newsletter not found')
		return BaseController.send_response_api(None, 'newsletter with id: ' + id + ' has been succesfully deleted')
