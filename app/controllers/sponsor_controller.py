from app.controllers.base_controller import BaseController
from app.services import sponsorservice


class SponsorController(BaseController):

    @staticmethod
    def index(request):
        sponsors = sponsorservice.get(request0)
        return BaseController.send_response_api(sponsors['data'], sponsors['message'], {}, sponsors['links'])
    
    @staticmethod
    def show(id):
        sponsor = sponsorservice.show(id)
        return BaseController.send_response_api(sponsor['data'], sponsor['message'])


    @staticmethod
    def create(request):
        name = request.json['name'] if 'name' in request.json else None
        email = request.json['email'] if 'email' in request.json else None
        phone = request.json['phone'] if 'phone' in request.json else None
        note = request.json['note'] if 'note' in request.json else ''
        if name and (email or phone):
            payloads = {
                'name': name,
                'email': email,
                'phone': phone,
                'note': note
            }
        else:
            BaseController.send_error_api(None, 'payload is invalid')

        result = sponsorservice.create(payloads)

        if result['error']:
            return BaseController.send_error_api(result['data'], result['message'])

        return BaseController.send_response_api(result['data'], result['message'])
