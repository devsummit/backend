# parent class imports
from app.controllers.base_controller import BaseController
from app.services import entrycashlogservice


class EntryCashLogController(BaseController):

    @staticmethod
    def index(request):
        result = entrycashlogservice.get(request)
        if result['error']:
            return BaseController.send_error_api(
                result['data'], 
                result['message']
            )
        return BaseController.send_response_api(
            result['data'],
            result['message'],
            {},
            result['links']
        )

    @staticmethod
    def show(id):
        result = entrycashlogservice.show(id)
        if result is None:
            return BaseController.send_error_api(None, 'entry cash log not found')
        return BaseController.send_response_api(result.as_dict(), 'entry cash log retrieved succesfully')

    @staticmethod
    def update(request, id):
        debit = request.json['debit'] if 'debit' in request.json else None
        credit = request.json['credit'] if 'credit' in request.json else None
        description = request.json['description'] if 'description' in request.json else None
        source_id = request.json['source_id'] if 'source_id' in request.json else None
        if source_id and description:
            payloads = {
                'debit': debit,
                'credit': credit,
                'source_id' : source_id,
                'description': description
            }
        else:
            return BaseController.send_error_api(None, 'field is not complete')

        result = entrycashlogservice.update(payloads, id)

        if not result['error']:
            return BaseController.send_response_api(result['data'], 'entry cash log updated succesfully')
        else:
            return BaseController.send_error_api(None, result['data'])

    @staticmethod
    def create(request):
        debit = request.json['debit'] if 'debit' in request.json else None
        credit = request.json['credit'] if 'credit' in request.json else None
        description = request.json['description'] if 'description' in request.json else None
        source_id = request.json['source_id'] if 'source_id' in request.json else None
        if source_id and description:
            payloads = {
                'source_id': source_id,
                'debit': debit,
                'credit': credit,
                'description': description
            }
        else:
            return BaseController.send_error_api(None, 'request is no complete')

        result = entrycashlogservice.create(payloads)

        if not result['error']:
            return BaseController.send_response_api(result['data'], 'entry cash log created succesfully')
        else:
            return BaseController.send_error_api(None, result['data'])

    @staticmethod
    def delete(id):
        entry_cash = entrycashlogservice.delete(id)
        if entry_cash['error']:
            return BaseController.send_response_api(None, 'entry cash log not found')
        return BaseController.send_response_api(None, 'entry with id: ' + id + ' has been deleted succesfully')
