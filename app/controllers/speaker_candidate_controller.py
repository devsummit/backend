from app.controllers.base_controller import BaseController
from app.services import speakercandidateservice


class SpeakerCandidateController(BaseController):

    @staticmethod
    def show(id):
        result = speakercandidateservice.show(id)
        if not result['error']:
            return BaseController.send_response_api(result['data'], result['message'], [])
        else:
            return BaseController.send_error_api(None, result['data'])

    @staticmethod
    def update(request, id):
        result = speakercandidateservice.update(request.json, id)

        if not result['error']:
            return BaseController.send_response_api(
                result['data'],
                'candidate succesfully updated',
                result['included']
            )
        else:
            return BaseController.send_error_api(None, result['data'])

    @staticmethod
    def create(request):
        result = speakercandidateservice.create(request.json)

        if not result['error']:
            return BaseController.send_response_api(
                result['data'],
                'candidate succesfully added',
                result['included']
            )
        else:
            return BaseController.send_error_api(None, result['data'])
