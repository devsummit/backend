from flask import Blueprint, request
from app.middlewares.authentication import token_required


# import controller
from app.controllers.user_authorization_controller import UserAuthorizationController

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['POST'])
def login():
	return UserAuthorizationController.login(request)


@auth.route('/register', methods=['POST'])
def register():
	return UserAuthorizationController.register(request)


@auth.route('/me/changesetting', methods=['PATCH', 'PUT'])
@token_required
def change_setting(*args, **kwargs):
	user = kwargs['user'].as_dict()
	return UserAuthorizationController.change_name(request, user)


@auth.route('/me/changepassword', methods=['PATCH', 'PUT'])
@token_required
def change_password(*args, **kwargs):
	user = kwargs['user'].as_dict()
	return UserAuthorizationController.change_password(request, user)
