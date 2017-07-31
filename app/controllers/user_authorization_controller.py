# utils import
import datetime

from flask import request, jsonify, json, current_app

# parent class imports
from app.controllers.base_controller import BaseController
from app.models import db
from app.models.user import User

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
					token = user.generate_auth_token()
					return BaseController.send_response({'access_token': token.decode()}, 'User logged in successfully')
				else:
					return BaseController.send_response(None, 'wrong credentials')
			else:
				return BaseController.send_response(None, 'username not found')
		return BaseController.send_response({}, 'username and password required')
