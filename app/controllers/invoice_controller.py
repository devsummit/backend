from app.controllers.base_controller import BaseController
from app.services import invoiceservice


class InvoiceController(BaseController):

    @staticmethod
    def index():
        result = invoiceservice.get()
        if result['error']:
            return BaseController.send_error_api(result['data'], result['message'])
        return BaseController.send_response_api(result['data'], result['message'])

    @staticmethod
    def show(id):
        result = invoiceservice.show(id)
        if result['error']:
            return BaseController.send_error_api(None, 'invoice not found')
        return BaseController.send_response_api(result['data'], result['message'], result['included'])


    @staticmethod
    def create(request):
        description = request.json['description'] if 'description' in request.json else ''
        total = request.json['total'] if 'total' in request.json else None
        address = request.json['address'] if 'address' in request.json else ''
        invoiceable_type = request.json['invoiceable_type'] if 'invoiceable_type' in request.json else None
        invoiceable_id = request.json['invoiceable_id'] if 'invoiceable_id' in request.json else None

        payload = {
            'description': description,
            'total': total,
            'address': address,
            'invoiceable_type': invoiceable_type,
            'invoiceable_id': invoiceable_id
        }
        if None in payload:
            return BaseController.send_error_api(None, 'payload invalid')
        
        result = invoiceservice.create(payload)
        if result['error']:
            return BaseController.send_error_api(None, result['message'])
        return BaseController.send_response_api(result['data'], result['message'])
