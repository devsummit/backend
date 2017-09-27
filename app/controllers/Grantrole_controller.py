from app.controllers.base_controller import BaseController
from app.models.base_model import BaseModel
from app.services import grantroleservice


class GrantroleController(BaseController):

    @staticmethod
    def update(request, id):
        role_id = request.json['role_id'] if 'role_id' in request.json else None
        user_id = id
        if role_id:
            payload = {
                'role_id': role_id
            }
            result = grantroleservice.update(payload, id)
        else:
            return BaseController.send_error_api(None, 'field is not complete')

        if role_id == "1":
            return BaseController.send_error(None, 'Admin cannot be grant')
        elif role_id == "2":
            points = request.json['includes']['points'] if 'points' in request.json['includes'] else 0
            if points:
                payloads = {
                    'user_id': user_id,
                    'points': points
                }
                result = grantroleservice.add_attendee(payloads)
            else:
                return BaseController.send_error_api(None, 'field is not complete')
        elif role_id == "3":
            stage_id = request.json['includes']['stage_id'] if 'stage_id' in request.json['includes'] else None
            points = request.json['includes']['points'] if 'points' in request.json['includes'] else None
            summary = request.json['includes']['summary'] if 'summary' in request.json['includes'] else None
            if points and summary:
                payloads = {
                    'user_id': user_id,
                    'stage_id': stage_id,
                    'points': points,
                    'summary': summary
                }
                result = grantroleservice.add_booth(payloads)
            else:
                return BaseController.send_error_api(None, 'field is not complete')
        elif role_id == "4":
            job = request.json['includes']['job'] if 'job' in request.json['includes'] else None
            summary = request.json['includes']['summary'] if 'job' in request.json['includes'] else None
            information = request.json['includes']['information'] if 'information' in request.json['includes'] else None
            type = request.json['includes']['type'] if 'type' in request.json['includes'] else None
            if job and summary and information:
                payloads = {
                    'user_id': user_id,
                    'job': job,
                    'summary': summary,
                    'information': information,
                    'type': type
                }
                result = grantroleservice.add_speaker(payloads)
            else:
                return BaseController.send_error_api(None, 'field is not complete')
        elif role_id == "6":
            information = request.json['includes']['information'] if 'information' in request.json['includes'] else None
            institution = request.json['includes']['institution'] if 'institution' in request.json['includes'] else None
            if information and institution:
                payloads = {
                    'user_id': user_id,
                    'information': information,
                    'institution': institution
                }
                result = grantroleservice.add_ambassador(payloads)
            else:
                return BaseController.send_error_api(None, 'field is not complete')

        if not result['error']:
            return BaseController.send_response_api(result['data'], 'User succesfully updated')
        else:
            return BaseController.send_error_api(None, result['data'])

    @staticmethod
    def get(request):
        return grantroleservice.get(request)
