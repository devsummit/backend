from app.models import db
from sqlalchemy.exc import SQLAlchemyError
from app.models.access_token import AccessToken
from functools import wraps
from flask import jsonify, request, current_app, Response, json
from itsdangerous import (TimedJSONWebSignatureSerializer 
	as Serializer, BadSignature, SignatureExpired
	)

from app.models.user import User


def token_required(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		if 'Authorization' not in request.headers:
			return Response(json.dumps({'message': 'Authorization header is missing'}), status=401, mimetype='application/json')
		else:
			token = request.headers['Authorization']
		s = Serializer(current_app.config['SECRET_KEY'])
		try:
			s.loads(token)
		except SignatureExpired:
			return Response(json.dumps({'message': 'Token is missing'}), status=401, mimetype='application/json')
		except BadSignature:
			return Response(json.dumps({'message': 'Token is invalid'}), status=401, mimetype='application/json')
		kwargs['user'] = User.verify_auth_token(token)
		token = db.session.query(AccessToken).filter_by(access_token=token).first()
		if token is None:
			return Response(json.dumps({'message':'User is not logged in'}), status=401, mimetype='application/json')
		return f(*args, **kwargs)
	return decorated
