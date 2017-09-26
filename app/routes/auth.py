from flask import Blueprint, request
from app.middlewares.authentication import token_required


# import controller
from app.controllers.user_authorization_controller import UserAuthorizationController
from app.controllers.admin_controller import AdminController
from app.controllers.user_controller import UserController

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['POST'])
def login():
	return UserAuthorizationController.login(request)


@auth.route('/register', methods=['POST'])
def register():
	return UserAuthorizationController.register(request)

@auth.route('/user/authorize', methods=['POST'])
@token_required
def user_authorize():
	return UserController.password_require(request)

@auth.route('/admin/authorize', methods=['POST'])
def admin_authorize():
    return AdminController.password_require(request)


@auth.route('/refreshtoken', methods=['POST'])
def refreshtoken():
	return UserAuthorizationController.refreshtoken(request)


@auth.route('/me/changesetting', methods=['PATCH', 'PUT'])
@token_required
def change_setting(*args, **kwargs):
	user = kwargs['user'].as_dict()
	return UserAuthorizationController.change_name(request, user)

@auth.route('/me/updatefcmtoken', methods=['PUT', 'PATCH'])
@token_required
def update_fcm_token(*args, **kwargs):
	user = kwargs['user'].as_dict()
	return UserAuthorizationController.updatefcmtoken(request, user)


@auth.route('/me/booth', methods=['GET'])
@token_required
def get_booth(*args, **kwargs):
	user = kwargs['user'].as_dict()
	return UserAuthorizationController.get_booth_info(user)


@auth.route('/me/changepassword', methods=['PATCH', 'PUT'])
@token_required
def change_password(*args, **kwargs):
	user = kwargs['user'].as_dict()
	return UserAuthorizationController.change_password(request, user)
