from app.controllers.base_controller import BaseController
from app.services import packagemanagementservice
from app.services import boothservice
from app.services import redeemcodeservice
class PackageManagementController(BaseController):
	
	@staticmethod
	def get(request):
		package_managements = packagemanagementservice.get(request)
		if package_managements['error']:
			return BaseController.send_error(package_managements['data'], package_managements['message'])
		return BaseController.send_response_api(package_managements['data'], package_managements['message'], package_managements['included'])

	@staticmethod
	def create(request):
		name = request.json['name'] if 'name' in request.json else None
		price = request.json['price'] if 'price' in request.json else None
		quota = request.json['quota'] if 'quota' in request.json else None
		if name and price and quota:
			payloads = {
				'name': name,
				'price': price,
				'quota': quota
			}
			result = packagemanagementservice.create(payloads)
			if result['error']:
				return BaseController.send_error_api(result['data'], result['message'])
			else:
				return BaseController.send_response_api(result['data'], result['message'])
		else:
			return BaseController.send_error_api(None, 'payload is invalid')

	@staticmethod
	def show(id):
		packagemanagement = packagemanagementservice.show(id)
		return BaseController.send_response_api(packagemanagement['data'], packagemanagement['message'])

	@staticmethod
	def update(id, request):
		name = request.json['name'] if 'name' in request.json else None
		price = request.json['price'] if 'price' in request.json else None
		quota = request.json['quota'] if 'quota' in request.json else None
		if name or price or quota:
			payloads = {
				'name': name,
				'price': price,
				'quota': quota
			}
			result = packagemanagementservice.update(id, payloads)
			if result['error']:
				return BaseController.send_error_api(result['data'], result['message'])
			else:
				return BaseController.send_response_api(result['data'], result['message'])
		else:
			return BaseController.send_error_api({}, 'payload is invalid')

	@staticmethod
	def package_purchase(request):
		package_id = request.json['package_id'] if 'package_id' in request.json else None
		partner_id = request.json['partner_id'] if 'partner_id' in request.json else None
		name = request.json['name'] if 'name' in request.json else None
		logo_url = request.json['logo_url'] if 'logo_url' in request.json else None

		payloads = {
			'codeable_type': 'partner',
			'codeable_id': partner_id,
			'count': package_id
		}
		data = redeemcodeservice.create(payloads)

		payloads={
			'user_id': None,
			'stage_id': None,
			'points': 0,
			'summary': None,
			'name': name,
			'logo_url': logo_url
		}
		data = boothservice.create(payloads)
		
		if data['error']:
			return BaseController.send_error_api(data['data'], data['message'])
		return BaseController.send_response_api(data['data'], data['message'])

		
	@staticmethod
	def delete(id):
		data = packagemanagementservice.delete(id)
		if data['error']:
			return BaseController.send_error_api(data['data'], data['message'])
		return BaseController.send_response_api(data['data'], data['message'])			
	