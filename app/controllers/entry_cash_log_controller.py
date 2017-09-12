# parent class imports
from app.controllers.base_controller import BaseController
from app.services import entrycashlogservice


class EntryCashLogController(BaseController):

    @staticmethod
    def index(request):
        result = entrycashlogservice.index()
        if result['error']:
            return BaseController.send_error_api(result['data'], result['message'])
        return BaseController.send_response_api(
            result['data'],
            result['message'],
            {},
            result['links']
        )