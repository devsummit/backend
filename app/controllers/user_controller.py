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
