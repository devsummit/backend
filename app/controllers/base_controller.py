from flask import jsonify

class BaseController:

	@staticmethod
	def send_response(data, message=''):
		return jsonify(
			message = message,
			result = data,
			success = True
			)

	@staticmethod
	def send_error(self, error):
		return jsonify(
			message = error,
			result = [],
			success = False
			)
