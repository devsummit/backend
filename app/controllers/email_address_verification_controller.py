# parent class imports
from app.controllers.base_controller import BaseController
from app.services import userservice

class EmailAddressVerificationController(BaseController):

    @staticmethod
    def verify(token):
        result = userservice.email_address_verification(token)
        if result['error']:
                return BaseController.send_error_api(result['data'], result['message'])
        return BaseController.send_response_api(result['data'], result['message'], {}, result['links'])
