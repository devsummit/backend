from app.controllers.base_controller import BaseController
from app.services import hackatonservice
from app.builders.response_builder import ResponseBuilder


class HackatonController(BaseController):

    @staticmethod
    def get_team(request, user):
        result = hackatonservice.get_team(user)
        if result['error']:
            return BaseController.send_error_api(result['data'], result['message'])
        return BaseController.send_response_api(result['data'], result['message'])

    @staticmethod
    def get_all(request):
        result = hackatonservice.get_all()
        if result['error']:
            return BaseController.send_error_api(result['data'], result['message'])
        return BaseController.send_response_api(result['data'], result['message'])

    @staticmethod
    def show(request, id):
        result = hackatonservice.show(id)
        if result['error']:
            return BaseController.send_error_api(result['data'], result['message'])
        return BaseController.send_response_api(result['data'], result['message'])

    @staticmethod
    def update_team(request, id):
        name = request.json['name'] if 'name' in request.json else None
        project_name = request.json['project_name'] if 'project_name' in request.json else None
        project_url = request.json['project_url'] if 'project_url' in request.json else None
        theme = request.json['theme'] if 'theme' in request.json else None

        payloads = {
            'name': name,
            'project_name': project_name,
            'project_url': project_url,
            'theme': theme
        }
        result = hackatonservice.update_team(payloads, id)

        if result['error']:
            return BaseController.send_error_api(result['data'], result['message'])
        return BaseController.send_response_api(result['data'], result['message'])

    @staticmethod
    def update_team_logo(request, id):
        logo = request.files['logo'] if 'logo' in request.files else None

        if logo:
            payloads = {
                'logo': logo
            }
        else:
            return BaseController.send_error_api(None, 'field is not complete')

        result = hackatonservice.update_team_logo(payloads, id)

        if result['error']:
            return BaseController.send_error_api(result['data'], result['message'])
        return BaseController.send_response_api(result['data'], result['message'])