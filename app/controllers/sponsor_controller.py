from app.controllers.base_controller import BaseController
from app.services import sponsorservice


class SponsorController(BaseController):

    @staticmethod
    def index(request):
        sponsors = sponsorservice.get(request)
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
        type = request.json['type'] if 'type' in request.json else None
        stage = request.json['stage'] if 'stage' in request.json else None
        if name and (email or phone):
            payloads = {
                'name': name,
                'email': email,
                'phone': phone,
                'note': note,
                'type': type,
                'stage': stage
            }
        else:
            BaseController.send_error_api(None, 'payload is invalid')

        result = sponsorservice.create(payloads)

        if result['error']:
            return BaseController.send_error_api(result['data'], result['message'])

        return BaseController.send_response_api(result['data'], result['message'])

    @staticmethod
    def update(id, request):
        name = request.json['name'] if 'name' in request.json else None
        email = request.json['email'] if 'email' in request.json else None
        phone = request.json['phone'] if 'phone' in request.json else None
        note = request.json['note'] if 'note' in request.json else None
        type = request.json['type'] if 'type' in request.json else None
        stage = request.json['stage'] if 'stage' in request.json else None

        payloads = {
            'name': name,
            'email': email,
            'phone': phone,
            'note': note,
            'type': type,
            'stage': stage
        }
        
        result = sponsorservice.update(id, payloads)

        if result['error']:
            return BaseController.send_error_api(result['data'], result['message'])
        return BaseController.send_response_api(result['data'], result['message'])        

    @staticmethod
    def delete(id):
        data = sponsorservice.delete(id)
        if data['error']:
            return BaseController.send_error_api(data['data'], data['message'])
        return BaseController.send_response_api(data['data'], data['message'])

    @staticmethod
    def get_logs(id):
        logs = sponsorservice.get_logs(id)
        return BaseController.send_response_api(logs['data'], logs['message'])

    @staticmethod
    def create_log(request, id):
        description = request.json['description'] if 'description' in request.json else None

        if description:
            payload = {
                'description': description,
            }
        else:
            return BaseController.send_error_api(None, 'payload invalid')

        result = sponsorservice.post_log(payload, id)

        if result['error']:
            return BaseController.send_error_api(result['data'], result['message'])
        return BaseController.send_response_api(result['data'], result['message'])