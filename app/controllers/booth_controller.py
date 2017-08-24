from app.controllers.base_controller import BaseController
from app.models.base_model import BaseModel
from app.services import boothservice


class BoothController(BaseController):

    @staticmethod
    def index():
        booths = boothservice.get()
        return BaseController.send_response_api(
            BaseModel.as_list(booths['data']),
            'booths retrieved succesfully',
            booths['included']
        )

    @staticmethod
    def show(id):
        booth = boothservice.show(id)
        if booth is None:
            return BaseController.send_error_api(None, 'booth not found')
        return BaseController.send_response_api(booth.as_dict(), 'booth retrieved succesfully')

    @staticmethod
    def update(request, id):
        user_id = request.json['user_id'] if 'user_id' in request.json else None
        stage_id = request.json['stage_id'] if 'stage_id' in request.json else None
        points = request.json['points'] if 'points' in request.json else None
        summary = request.json['summary'] if 'summary' in request.json else None

        if user_id and stage_id and points and summary:
            payloads = {
                'user_id': user_id,
                'stage_id': stage_id,
                'points': points,
                'summary': summary
            }
        else:
            return BaseController.send_error_api(None, 'field is not complete')

        result = boothservice.update(id)

        if not result['error']:
            return BaseController.send_response_api(result['data'], 'booth succesfully updated')
        else:
            return BaseController.send_error_api(None, result['data'])

    @staticmethod
    def create(request):
        user_id = request.json['user_id'] if 'user_id' in request.json else None
        stage_id = request.json['stage_id'] if 'stage_id' in request.json else None
        points = request.json['points'] if 'points' in request.json else None
        summary = request.json['summary'] if 'summary' in request.json else None

        if user_id and stage_id and points and summary:
            payloads = {
                'user_id': user_id,
                'stage_id': stage_id,
                'points': points,
                'summary': summary
            }
        else:
            return BaseController.send_error_api(None, 'field is not complete')

        result = boothservice.create(payloads)

        if not result['error']:
            return BaseController.send_response_api(result['data'], 'booth succesfully created')
        else:
            return BaseController.send_error_api(None, result['data'])
