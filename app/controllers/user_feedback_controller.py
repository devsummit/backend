# parent class imports
from app.controllers.base_controller import BaseController
from app.services import userfeedbackservice
from app.configs.constants import ROLE


class UserFeedbackController(BaseController):

    @staticmethod
    def index(user):
        if user['role_id'] == ROLE['admin']:
            result = userfeedbackservice.index()            
            return BaseController.send_response_api(result['data'], result['message'])
        return BaseController.send_error_api(None, 'user is not authorized')


    @staticmethod
    def create(user, request):
        user_id = user['id']
        content = request.json['content'] if 'content' in request.json else None
        if user_id and content:
            payloads = {
                'user_id': user_id,
                'content': content
            }
            result = userfeedbackservice.create(payloads)
        else:
            return BaseController.send_error_api(None, 'field is not complete')
        if not result['error']:
            return BaseController.send_response_api(result['data'], result['message'])
        return BaseController.send_error_api(None, result['data'])

    @staticmethod
    def show(id, user):
        result = userfeedbackservice.show(id, user)
        if result['error']:
                return BaseController.send_error_api(result['data'], result['message'])
        return BaseController.send_response_api(result['data'], result['message'])
