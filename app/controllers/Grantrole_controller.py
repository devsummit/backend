from app.controllers.base_controller import BaseController
from app.models.base_model import BaseModel
from app.services import grantroleservice


class GrantroleController(BaseController):

    @staticmethod
    def update(request, id):
        role_id = request.json['role_id'] if 'role_id' in request.json else None
        payload = request.json['includes'] if 'includes' in request.json else None
        if role_id:
            payload = {
                'role_id': role_id,
                'includes': payload
            }
            result = grantroleservice.update(payload, id)
        else:
            return BaseController.send_error_api(None, 'field is not complete')

        if not result['error']:
            return BaseController.send_response_api(result['data'], 'User succesfully updated')
        else:
            return BaseController.send_error_api(None, result['data'])

    @staticmethod
    def get(request):
        return grantroleservice.get(request)
