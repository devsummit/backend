from app.controllers.base_controller import BaseController
from app.services import sourceservice


class SourceController(BaseController):

    @staticmethod
    def get(request):
        source = sourceservice.get(request)
        if source['error']:
            return BaseController.send_error(source['data'], source['message'])
        return BaseController.send_response_api(source['data'], source['message'], source['included'])

    @staticmethod
    def create(request):
        account_number = request.json['account_number'] if 'account_number' in request.json else None
        bank = request.json['bank'] if 'bank' in request.json else None
        alias = request.json['alias'] if 'alias' in request.json else None

        if account_number and bank and alias:
            payloads = {
                'account_number': account_number,
                'bank': bank,
                'alias': alias
            }
            result = sourceservice.create(payloads)
        else:
            return BaseController.send_error_api(None, 'field is not complete')

        if not result['error']:
            return BaseController.send_error_api(result['data'], 'source succesfully created', result['included'])
        else:
            return BaseController.send_error_api(None, result['data'])

    @staticmethod
    def update(request, id):
        account_number = request.json['account_number'] if 'account_number' in request.json else None
        bank = request.json['bank'] if 'bank' in request.json else None
        alias = request.json['alias'] if 'alias' in request.json else None

        if account_number and bank and alias:
            payloads = {
                'account_number': account_number,
                'bank': bank,
                'alias': alias
            }
            result = sourceservice.update(payloads, id)
        else:
            return BaseController.send_error_api(None, 'field is not complete')

        if not result['error']:
            return BaseController.send_response_api(result['data'], 'source succesfully updated', result['included'])
        else:
            return BaseController.send_error_api(None, result['data'])

    @staticmethod
    def show(id):
        source = sourceservice.show(id)
        if source['error']:
            return BaseController.send_error_api(source['data'], source['message'])
        return BaseController.send_response_api(source['data'], source['message'], source['included'])

    @staticmethod
    def delete(id):
        source = sourceservice.delete(id)
        if source['error']:
            return BaseController.send_response_api(None, 'source not found')
        return BaseController.send_response_api(None, 'source has been succesfully deleted')
