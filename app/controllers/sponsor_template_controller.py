from app.controllers.base_controller import BaseController
from app.services import sponsortemplateservice

class SponsorTemplateController(BaseController):

    @staticmethod
    def index(request):
        sponsor_templates = sponsortemplateservice.get(request)
        if sponsor_templates['error']:
            return BaseController.send_error(sponsor_templates['data'], sponsor_templates['message'])
        return BaseController.send_response_api(sponsor_templates['data'], sponsor_templates['message'], sponsor_templates['included'])

    @staticmethod
    def create(request):
        sponsor_id = request.form['sponsor_id'] if 'sponsor_id' in request.form else None
        message = request.form['message'] if 'message' in request.form else None
        attachment = request.files['attachment'] if 'attachment' in request.files else None
        redirect_url = request.form['redirect_url'] if 'redirect_url' in request.form else None

        payloads = {
            'sponsor_id': sponsor_id,
            'message': message,
            'attachment': attachment,
            'redirect_url': redirect_url
        }

        result = sponsortemplateservice.create(payloads)

        if result['error']:
            return BaseController.send_error_api(result['data'], result['message'])
        else:
            return BaseController.send_response_api(result['data'], result['message'])
        
    @staticmethod
    def show(request, sponsor_id):
        sponsor_template = sponsortemplateservice.show(sponsor_id)
        if sponsor_template['error']:
            return BaseController.send_error_api(sponsor_template['data'], sponsor_template['message'])
        return BaseController.send_response_api(sponsor_template['data'], sponsor_template['message'])

    @staticmethod
    def update(request, sponsor_id):
        message = request.form['message'] if 'message' in request.form else None
        attachment = request.files['attachment'] if 'attachment' in request.files else None
        redirect_url = request.form['redirect_url'] if 'redirect_url' in request.form else None

        payloads = {
            'message': message,
            'attachment': attachment,
            'redirect_url': redirect_url
        }

        result = sponsortemplateservice.update(payloads, sponsor_id)

        if result['error']:
            return BaseController.send_error_api(result['data'], result['message'])
        else:
            return BaseController.send_response_api(result['data'], result['message'])
