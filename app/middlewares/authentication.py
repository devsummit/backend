from flask import jsonify, request, current_app
from itsdangerous import (TimedJSONWebSignatureSerializer 
	as Serializer, BadSignature, SignatureExpired
	)

from app.models.user import User

def token_required(f):
	def decorated(*args, **kwargs):
		if 'Authorization' not in request.headers :
			return jsonify({'message': 'token is missing'})
		else:
			token = request.headers['Authorization']
		s = Serializer(current_app.config['SECRET_KEY'])
		try:
			s.loads(token)
		except SignatureExpired:
			return jsonify({'message': 'token is expired'})
		except BadSignature:
			return jsonify({'message': 'token is invalid'})
		kwargs['user'] = User.verify_auth_token(token)
		return f(*args, **kwargs)
	return decorated