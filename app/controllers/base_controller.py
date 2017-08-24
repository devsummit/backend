from flask import jsonify


class BaseController:

	@staticmethod
	def send_response(data, message=''):
		return jsonify(
			message=message,
			result=data,
			success=True
		)

	@staticmethod
	def send_error(self, error):
		return jsonify(
			message=error,
			result=[],
			success=False
		)

	@staticmethod
	def send_response_api(data, message='', included={}, links={}):
		meta = {
			'message': message,
			'success': True
		}
		data = data if isinstance(data, list) else [data]
		return jsonify(
			meta=meta,
			data=data,
			included=included,
			links=links
		)

	@staticmethod
	def send_error_api(data, message='', included={}, links={}):
		meta = {
			'message': message,
			'success': False
		}
		return jsonify(
			meta=meta,
			data=data,
			included=included,
			links=links
		)
