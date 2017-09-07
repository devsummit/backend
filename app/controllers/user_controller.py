from app.controllers.base_controller import BaseController
from app.services import userservice


class UserController(BaseController):
    @staticmethod
    def index():
        users = userservice.list_user()
        return BaseController.send_response_api(users, 'users retrieved successfully')

    @staticmethod
    def show(id):
        user = userservice.get_user_by_id(id)
        if user is None:
            return BaseController.send_error_api(None, 'user not found')
        return BaseController.send_response_api(user, 'user retrieved succesfully')

    @staticmethod
    def delete(id):
        result = userservice.delete(id)
        if result['error']:
            return BaseController.send_error_api([], result['data'])
        return BaseController.send_response_api([], result['data'])

    @staticmethod
    def update(request, id):
        first_name = request.json['first_name'] if 'first_name' in request.json else None
        last_name = request.json['last_name'] if 'last_name' in request.json else None
        email = request.json['email'] if 'email' in request.json else None
        username = request.json['username'] if 'username' in request.json else None
        role_id = request.json['role_id'] if 'role_id' in request.json else None
        if first_name and last_name and email and username and role_id:
            payloads = {
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'username': username,
                'role_id': role_id

            }
        else:
            return BaseController.send_error_api(None, 'field is not complete')

        result = userservice.update(payloads, id)

        if not result['error']:
            return BaseController.send_response_api(result['data'], 'user succesfully updated')
        else:
            return BaseController.send_error_api(None, result['data'])

    @staticmethod
    def add(request):
        first_name = request.json['first_name'] if 'first_name' in request.json else None
        last_name = request.json['last_name'] if 'last_name' in request.json else None
        email = request.json['email'] if 'email' in request.json else None
        username = request.json['username'] if 'username' in request.json else None
        role_id = request.json['role_id'] if 'role_id' in request.json else None
        if first_name and last_name and email and username and role_id:
            payloads = {
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'username': username,
                'role_id': role_id

            }
        else:
            return BaseController.send_error_api(None, 'field is not complete')

        result = userservice.add(payloads)

        if not result['error']:
            return BaseController.send_response_api(result['data'], 'user succesfully added')
        else:
            return BaseController.send_error_api(None, result['data'])
