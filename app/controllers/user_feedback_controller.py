# parent class imports
from app.controllers.base_controller import BaseController
from app.services import userfeedbackservice


class UserFeedbackController(BaseController):

    @staticmethod
    def index():
        result = userfeedbackservice.index()            
        return BaseController.send_response_api(result['data'], result['message'])

    @staticmethod
    def create(request):
        user_id = request.json['user_id'] if 'user_id' in request.json else None
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
            return BaseController.send_response_api(result['data'], 'user feedback created successfully', result['included'])
        else:
            return BaseController.send_error_api(None, result['data'])

    @staticmethod
    def show(id):
        result = userfeedbackservice.show(id)
        return BaseController.send_response_api(result['data'], result['message'])