class ResponseBuilder():

	def __init__(self):
		self.base_response_structure = {
			'status_code': 200,
			'error': False,
			'message': 'Data retrieved succesfully',
			'data': {},
			'included': {}
		}

	def build(self):
		return self.base_response_structure

	def set_error(self, error_status):
		self.base_response_structure['error'] = error_status
		return self

	def set_data(self, data):
		self.base_response_structure['data'] = data
		return self

	def set_included(self, included):
		self.base_response_structure['included'] = included
		return self

	def set_message(self, message):
		self.base_response_structure['message'] = message
		return self

	def set_status_code(self, status_code):
		self.base_response_structure['status_code'] = status_code
		return self

	def set_payload_invalid(self):
		self.base_response_structure['data']['payload_invalid'] = True

	def build_invalid_payload_response(self):
		return self.set_payload_invalid().set_error(True).set_status_code(400).set_message('payload is invalid').build()