from app.controllers.base_controller import BaseController
from app.services import partnerservice


class PartnerController(BaseController):

	@staticmethod
	def index(request):
		partners = partnerservice.get(request)
		return BaseController.send_response_api(partners['data'], partners['message'])

	@staticmethod
	def create(request):
		name = request.form['name'] if 'name' in request.form else None
		email = request.form['email'] if 'email' in request.form else None
		website = request.form['website'] if 'website' in request.form else None
		types = request.form['type'] if 'type' in request.form else None
		photo = request.files['image_file'] if 'image_file' in request.files else None
		if name and website and email:
			payloads = {
				'name': name,
				'email': email,
				'website': website,
				'photo': photo,
				'type': types
			}
		else:
			return BaseController.send_error_api(None, 'field is not complete')

		result = partnerservice.create(payloads)

		if not result['error']:
			return BaseController.send_response_api(result['data'], result['message'])
		else:
			return BaseController.send_error_api(result['data'], result['message'])

	@staticmethod
	def show(id):
		partner = partnerservice.show(id)
		if partner['error']:
			return BaseController.send_error_api(partner['data'], partner['message'])
		return BaseController.send_response_api(partner['data'], partner['message'])

	@staticmethod
	def update(id, request):
		name = request.form['name'] if 'name' in request.form else None
		email = request.form['email'] if 'email' in request.form else None
		website = request.form['website'] if 'website' in request.form else None
		type = request.form['type'] if 'type' in request.form else None
		photo = request.files['image_file'] if request.files['image_file'] else None
		if name and website and type:
			payloads = {
				'name': name,
				'email': email,
				'website': website,
				'photo': photo,
				'type': type
			}
		else:
			return BaseController.send_error_api(None, 'field is not complete')
		result = partnerservice.update(payloads, id)

		if not result['error']:
			return BaseController.send_response_api(result['data'], result['message'])
		else:
			return BaseController.send_error_api(result['data'], result['message'])

	@staticmethod
	def delete(id):
		partner = partnerservice.delete(id)
		if partner['error']:
			return BaseController.send_response_api(partner['data'], partner['message'])
		return BaseController.send_response_api(partner['data'], partner['message'])
