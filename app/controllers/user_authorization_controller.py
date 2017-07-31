# utils import
import datetime

from flask import request, jsonify, json, current_app

# parent class imports
from app.controllers.base_controller import BaseController
from app.models import db
from app.models.user import User
from app.models.access_token import AccessToken

class UserAuthorizationController(BaseController):

	@staticmethod
	def login(request):
		username = request.form['username'] if 'username' in request.form else None
		password = request.form['password'] if 'password' in request.form else None
		if username and password:
			# check if user exist
			user = db.session.query(User).filter_by(username = username).first()
			if user is not None:
				if user.verify_password(password):
					refresh_token = user.generate_refresh_token()
					access_token = user.generate_auth_token()
					UserAuthorizationController.save_token(access_token, refresh_token, user.id)
					return BaseController.send_response({'access_token': access_token.decode(), 'refresh_token': refresh_token}, 'User logged in successfully')
				else:
					return BaseController.send_response(None, 'wrong credentials')
			else:
				return BaseController.send_response(None, 'username not found')
		return BaseController.send_response({}, 'username and password required')

	@staticmethod
	def save_token(access_token, refresh_token, user_id):
		token_exist = db.session.query(AccessToken).filter_by(user_id=user_id).first()
		if not token_exist:
			payload = AccessToken(access_token, refresh_token, user_id)
			db.session.add(payload)
			db.session.commit()
			return
		token_exist.access_token = access_token
		token_exist.refresh_token = refresh_token
		db.session.commit()
		return