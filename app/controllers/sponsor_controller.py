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
        name = request.form['name'] if 'name' in request.form else None
        email = request.form['email'] if 'email' in request.form else None
        phone = request.form['phone'] if 'phone' in request.form else None
        note = request.form['note'] if 'note' in request.form else ''
        type = request.form['type'] if 'type' in request.form else None
        stage = request.form['stage'] if 'stage' in request.form else None
        attachment = request.files['attachment'] if 'attachment' in request.files else None
        url = request.form['url'] if 'url' in request.form else ''
        callback_url = request.form['callback_url'] if 'callback_url' in request.form else ''

        if name and (email or phone):
            payloads = {
                'name': name,
                'email': email,
                'phone': phone,
                'note': note,
                'type': type,
                'stage': stage,
                'attachment': attachment,
                'callback_url': callback_url,
                'url': url
            }
        else:
            BaseController.send_error_api(None, 'payload is invalid')

        result = sponsorservice.create(payloads)

        if result['error']:
            return BaseController.send_error_api(result['data'], result['message'])

        return BaseController.send_response_api(result['data'], result['message'])

    @staticmethod
    def update(id, request):
        name = request.form['name'] if 'name' in request.form else None
        email = request.form['email'] if 'email' in request.form else None
        phone = request.form['phone'] if 'phone' in request.form else None
        note = request.form['note'] if 'note' in request.form else None
        type = request.form['type'] if 'type' in request.form else None
        stage = request.form['stage'] if 'stage' in request.form else None
        attachment = request.files['attachment'] if 'attachment' in request.files else None
        url = request.form['url'] if 'url' in request.form else None
        callback_url = request.form['callback_url'] if 'callback_url' in request.form else None

        payloads = {
            'name': name,
            'email': email,
            'phone': phone,
            'note': note,
            'type': type,
            'stage': stage,
            'attachment': attachment,
            'callback_url': callback_url,
            'url': url
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
