from app.models import db
from sqlalchemy.exc import SQLAlchemyError
from app.models.access_token import AccessToken
from functools import wraps
from flask import jsonify, request, current_app
from itsdangerous import (TimedJSONWebSignatureSerializer 
	as Serializer, BadSignature, SignatureExpired
	)

from app.models.user import User


def token_required(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		if 'Authorization' not in request.headers:
			return jsonify({'message': 'token is missing'})
		else:
			token = request.headers['Authorization']
		s = Serializer(current_app.config['SECRET_KEY'])
		try:
			s.loads(token)
		except SignatureExpired:
			return jsonify({
				'message': 'token is expired',
				'expired': True
				})
		except BadSignature:
			return jsonify({
				'message': 'token is invalid',
				'invalid': True
				})
		kwargs['user'] = User.verify_auth_token(token)
		token = db.session.query(AccessToken).filter_by(access_token=token).first()
		if token is None:
			return jsonify({'message': 'user is not logged in, try loggin in again.'})
		return f(*args, **kwargs)
	return decorated
