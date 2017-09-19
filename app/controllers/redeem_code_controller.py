from app.controllers.base_controller import BaseController
from app.services import redeemcodeservice


class RedeemCodeController(BaseController):

    @staticmethod
    def index():
        redeem_codes = redeemcodeservice.get()
        return BaseController.send_response_api(redeem_codes['data'], redeem_codes['message'])

    @staticmethod
    def show(id):
        redeem_code = redeemcodeservice.show(id)
        if redeem_code is None:
            return BaseController.send_error_api(None, 'redeem code not found')
        return BaseController.send_response_api(redeem_code['data'], redeem_code['message'])

    @staticmethod
    def create(request):
        codeable_type = request.json['codeable_type'] if 'codeable_type' in request.json else None
        codeable_id = request.json['codeable_id'] if 'codeable_id' in request.json else None
        count = request.json['count'] if 'count' in request.json else None

        if codeable_id and codeable_type and count:
            payloads = {
                'codeable_type': codeable_type,
                'codeable_id': codeable_id,
                'count': count
            }
        else:
            return BaseController.send_error_api({'payload_invalid': True}, 'field is not complete')

        result = redeemcodeservice.create(payloads)

        if not result['error']:
            return BaseController.send_response_api(result['data'], result['message'])
        else:
            return BaseController.send_error_api(result['data'], result['message'])

    @staticmethod
    def update(request, id):
        codeable_type = request.json['codeable_type'] if 'codeable_type' in request.json else None
        codeable_id = request.json['codeable_id'] if 'codeable_id' in request.json else None
        count = request.json['count'] if 'count' in request.json else None

        if codeable_id and codeable_type and count:
            payloads = {
                'codeable_type': codeable_type,
                'codeable_id': codeable_id,
                'count': count
            }
        else:
            return BaseController.send_error_api({'payload_invalid': True}, 'field is not complete')

        result = redeemcodeservice.update(payloads, id)

        if not result['error']:
            return BaseController.send_response_api(result['data'], result['message'])
        else:
            return BaseController.send_error_api(result['data'], result['message'])

    @staticmethod
    def delete(id):
        print(id)
        redeem_code = redeemcodeservice.delete(id)
        if redeem_code['error']:
            return BaseController.send_error_api(redeem_code['data'], redeem_code['message'])
        return BaseController.send_response_api(redeem_code['data'], redeem_code['message'])
