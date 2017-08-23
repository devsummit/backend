from app.controllers.base_controller import BaseController
from app.models.base_model import BaseModel
from app.services import paymentservice


class PaymentController(BaseController):

    @staticmethod
    def create(request):

        payment_type = request.json['payment_type'] if 'payment_type' in request.json else None
        gross_amount = request.json['gross_amount'] if 'gross_amount' in request.json else None
        bank = request.json['bank'] if 'bank' in request.json else None
        order_id = request.json['order_id'] if 'order_id' in request.json else None

        if (bank == 'permata'):
            if payment_type and gross_amount and bank and order_id: 
                payloads = {
                    'payment_type': payment_type,
                    'gross_amount': gross_amount,
                    'bank': bank,
                    'order_id': order_id
                }
            else:
                return BaseController.send_error_api(None, 'field is not complete')

            result = paymentservice.bank_transfer(payloads)

            if result['status_code'] == '201':
                return BaseController.send_response_api(result, 'Succesfully')
            else:
                return BaseController.send_error_api(None, result)

        if (bank == 'bca'):
            email = request.json['email'] if 'email' in request.json else None
            first_name = request.json['first_name'] if 'first_name' in request.json else None
            last_name = request.json['last_name'] if 'last_name' in request.json else None
            phone = request.json['phone'] if 'phone' in request.json else None
            va_number = request.json['va_number'] if 'va_number' in request.json else None
            # using order_id to get ticket_id, price, quantity, ticket_type(name) in payment service

            if payment_type and gross_amount and order_id and email and first_name and last_name and phone and bank and va_number:
                payloads = {
                    'payment_type': payment_type,
                    'gross_amount': gross_amount,
                    'order_id': order_id,
                    'email': email,
                    'first_name': first_name,
                    'last_name': last_name,
                    'phone': phone,
                    'name': name,
                    'bank': bank,
                    'va_number': va_number
                }
            else:
                return BaseController.send_error_api(None, 'field is not complete')

            result = paymentservice.bank_transfer(payloads)

            if result['status_code'] == '201':
                return BaseController.send_response_api(result, 'Succesfully')
            else:
                return BaseController.send_error_api(None, result)



