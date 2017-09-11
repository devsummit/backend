from app.controllers.base_controller import BaseController
from app.services import boothservice
from app.models.booth import Booth
from app.models import db


class BoothController(BaseController):

    @staticmethod
    def index(request):
        booths = boothservice.get(request)
        return BaseController.send_response_api(
            booths['data'],
            booths['message'],
            {},
            booths['links']
        )

    @staticmethod
    def show(id):
        booth = boothservice.show(id)
        if booth['error']:
            return BaseController.send_error_api(
                booth['data'],
                booth['message']
            )
        return BaseController.send_response_api(
            booth['data'], 
            booth['message']
        )

    @staticmethod
    def update(request, user_id=None, booth_id=None):
        if user_id is not None:
            booth_id = db.session.query(Booth).filter_by(user_id=user_id).first().as_dict()['id']

        stage_id = request.json['stage_id'] if 'stage_id' in request.json else None
        stage_id = None if stage_id < 0 else stage_id
        points = request.json['points'] if 'points' in request.json else None
        summary = request.json['summary'] if 'summary' in request.json else None

        if points and summary:
            payloads = {
                'stage_id': stage_id,
                'points': points,
                'summary': summary
            }
        else:
            return BaseController.send_error_api(None, 'field is not complete')

        result = boothservice.update(payloads, booth_id)

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
