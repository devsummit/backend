from app.controllers.base_controller import BaseController
from app.services import hackatonservice


class HackatonController(BaseController):

    @staticmethod
    def get_team(request, user):
        result = hackatonservice.get_team(user)
        if result['error']:
            return BaseController.send_error_api(result['data'], result['message'])
        return BaseController.send_response_api(result['data'], result['message'])

