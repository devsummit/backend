from app.controllers.base_controller import BaseController
from app.services import paymentservice


class PaymentController(BaseController):

    @staticmethod
    def admin_get_payments():
        payments = paymentservice.admin_get()
        if(payments['error']):
            return BaseController.send_error_api(payments['data'], payments['message'])
        return BaseController.send_response_api(payments['data'], payments['message'])

    @staticmethod
    def admin_filter_payments(transaction_status):
        param = {}
        param['transaction_status'] = transaction_status
        payment = paymentservice.admin_filter(param)
        if payment['error']:
            return BaseController.send_error_api(payment['data'], payment['message'])
        else:
            return BaseController.send_response_api(payment['data'], payment['message'], payment['included'])

    @staticmethod
    def get_payments(user_id):
        payments = paymentservice.get(user_id)
        if(payments['error']):
            return BaseController.send_error_api(payments['data'], payments['message'])
        return BaseController.send_response_api(payments['data'], payments['message'])

    @staticmethod
    def admin_show_payment(payment_id):
        payment = paymentservice.admin_show(payment_id)
        if payment['error']:
            return BaseController.send_error_api(payment['data'], payment['message'])
        return BaseController.send_response_api(payment['data'], payment['message'])

    @staticmethod
    def show_payment(payment_id):
        payment = paymentservice.show(payment_id)
        if payment['error']:
            return BaseController.send_error_api(payment['data'], payment['message'])
        return BaseController.send_response_api(payment['data'], payment['message'])

    @staticmethod
    def create(request, user_id):
        payment_type = request.json['payment_type'] if 'payment_type' in request.json else None
        gross_amount = request.json['gross_amount'] if 'gross_amount' in request.json else None
        bank = request.json['bank'] if 'bank' in request.json else None
        order_id = request.json['order_id'] if 'order_id' in request.json else None
        if(payment_type and payment_type == 'bank_transfer'):

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

                if result['error']:
                    return BaseController.send_error_api(result['data'], result['message'])
                else:
                    return BaseController.send_response_api(result['data'], result['message'])

            if (bank == 'bca'):
                email = request.json['email'] if 'email' in request.json else None
                first_name = request.json['first_name'] if 'first_name' in request.json else None
                last_name = request.json['last_name'] if 'last_name' in request.json else ''
                phone = request.json['phone'] if 'phone' in request.json else None
                # va_number = request.json['va_number'] if 'va_number' in request.json else None

                if payment_type and gross_amount and order_id and email and first_name and phone and bank:
                    payloads = {
                        'payment_type': payment_type,
                        'gross_amount': gross_amount,
                        'order_id': order_id,
                        'email': email,
                        'first_name': first_name,
                        'last_name': last_name,
                        'phone': phone,
                        'bank': bank
                        # 'va_number': va_number
                    }
                else:
                    return BaseController.send_error_api(None, 'field is not complete')

                result = paymentservice.bank_transfer(payloads)

                if result['error']:
                    return BaseController.send_error_api(result['data'], result['message'])
                else:
                    return BaseController.send_response_api(result['data'], result['message'])

            if(bank == 'bni'):
                email = request.json['email'] if 'email' in request.json else None
                first_name = request.json['first_name'] if 'first_name' in request.json else None
                last_name = request.json['last_name'] if 'last_name' in request.json else ''
                phone = request.json['phone'] if 'phone' in request.json else None
                if email and first_name and last_name and phone:
                    payloads = {
                        'payment_type': payment_type,
                        'gross_amount': gross_amount,
                        'order_id': order_id,
                        'email': email,
                        'first_name': first_name,
                        'last_name': last_name,
                        'phone': phone,
                        'bank': bank
                    }
                else:
                    return BaseController.send_error_api(None, 'field is not complete')

                result = paymentservice.bank_transfer(payloads)

                if result['error']:
                    return BaseController.send_error_api(result['data'], result['message'])
                else:
                    return BaseController.send_response_api(result['data'], result['message'])

            if(bank == 'mandiri_bill'):
                payloads = {
                    'payment_type': 'echannel',
                    'bank': bank,
                    'gross_amount': gross_amount,
                    'order_id': order_id,
                }

                result = paymentservice.bank_transfer(payloads)

                if 'status_code' in result and str(result['status_code']) in ['201', '200']:
                    return BaseController.send_response_api(result, 'bank transfer transaction is created')
                else:
                    return BaseController.send_error_api(None, result)

        elif payment_type == 'credit_card':
            payloads = {
                'payment_type': payment_type,
                'gross_amount': PaymentController.is_field_exist(request, 'gross_amount'),
                'order_id': PaymentController.is_field_exist(request, 'order_id'),
                'email': PaymentController.is_field_exist(request, 'email'),
                'first_name': PaymentController.is_field_exist(request, 'first_name'),
                'last_name': PaymentController.is_field_exist(request, 'last_name'),
                'phone': PaymentController.is_field_exist(request, 'phone'),
                'bank': PaymentController.is_field_exist(request, 'bank'),
                'card_number': PaymentController.is_field_exist(request, 'card_number'),
                'card_exp_month': PaymentController.is_field_exist(request, 'card_exp_month'),
                'card_exp_year': PaymentController.is_field_exist(request, 'card_exp_year'),
                'card_cvv': PaymentController.is_field_exist(request, 'card_cvv'),
                'client_key': PaymentController.is_field_exist(request, 'client_key')
            }

            if None in payloads.values():
                return BaseController.send_error_api(None, 'field is not complete')

            if PaymentController.card_number_validation(payloads['card_number']) is False:
                return BaseController.send_error_api(None, 'Credit Card not valid')

            result = paymentservice.credit_payment(payloads)

            if result['error']:
                return BaseController.send_error_api(result['data'], result['message'])
            return BaseController.send_response_api(result['data'], result['message']) 

        else:
            payloads = {
                'order_id': PaymentController.is_field_exist(request, 'order_id'),
                'gross_amount': PaymentController.is_field_exist(request, 'gross_amount'),
                'first_name': PaymentController.is_field_exist(request, 'first_name'),
                'last_name': PaymentController.is_field_exist(request, 'last_name'),
                'email': PaymentController.is_field_exist(request, 'email'),
                'phone': PaymentController.is_field_exist(request, 'phone')
            }

            if None in payloads.values():
                return BaseController.send_error_api(None, 'Field is not complete')

            if (payment_type == 'bca_klikpay'):

                payloads['payment_type'] = payment_type

                result = paymentservice.internet_banking(payloads)
                if result['error']:
                    return BaseController.send_error_api(result['data'], result['message'])
                else:
                    return BaseController.send_response_api(result['data'], result['message'])

            if (payment_type == 'bca_klikbca'):

                payloads['payment_type'] = payment_type
                payloads['description'] = PaymentController.is_field_exist(
                    request, 'description')
                payloads['user_id'] = user_id

                result = paymentservice.internet_banking(payloads)

                if result['error']:
                    return BaseController.send_error_api(result['data'], result['message'])
                else:
                    return BaseController.send_response_api(result['data'], result['message'])

            if (payment_type == 'mandiri_clickpay'):

                payloads['payment_type'] = payment_type
                payloads['card_number'] = PaymentController.is_field_exist(
                    request, 'card_number')
                payloads['token'] = PaymentController.is_field_exist(
                    request, 'token')
                payloads['input1'] = PaymentController.is_field_exist(
                    request, 'input1')
                payloads['input3'] = PaymentController.is_field_exist(
                    request, 'random')

                if PaymentController.card_number_validation(payloads['card_number']) is False:
                    return BaseController.send_error_api(None, 'Card number is not valid')

                result = paymentservice.internet_banking(payloads)
                if result['error']:
                    return BaseController.send_error_api(result['data'], result['message'])
                else:
                    return BaseController.send_response_api(result['data'], result['message'])

            if (payment_type == 'bri_epay'):

                payloads['payment_type'] = payment_type

                result = paymentservice.internet_banking(payloads)

                if result['error']:
                    return BaseController.send_error_api(result['data'], result['message'])
                else:
                    return BaseController.send_response_api(result['data'], result['message'])

            if (payment_type == 'cimb_clicks'):

                payloads['payment_type'] = payment_type

                payloads['description'] = PaymentController.is_field_exist(
                    request, 'description')

                result = paymentservice.internet_banking(payloads)

                if result['error']:
                    return BaseController.send_error_api(result['data'], result['message'])
                else:
                    return BaseController.send_response_api(result['data'], result['message'])

            if (payment_type == 'danamon_online'):
                payloads['payment_type'] = payment_type

                result = paymentservice.internet_banking(payloads)

                if result['error']:
                    return BaseController.send_response_api(result['data'], result['message'])
                else:
                    return BaseController.send_error_api(result['data'], result['message'])

            if (payment_type == 'cstore'):
                payloads['payment_type'] = payment_type

                result = paymentservice.cstore(payloads)

                if result['error']:
                    return BaseController.send_response_api(result['data'], result['message'])
                else:
                    return BaseController.send_error_api(result['data'], result['message'])

    @staticmethod
    def authorize(request):
        payloads = {
            'payment_type': PaymentController.is_field_exist(request, 'payment_type'),
            'type': PaymentController.is_field_exist(request, 'type'),
            'order_id': PaymentController.is_field_exist(request, 'order_id'),
            'gross_amount': PaymentController.is_field_exist(request, 'gross_amount')
        }

        if None in payloads.values():
            return BaseController.send_error_api(None, 'field is not complete')

        result = paymentservice.authorize(payloads)

        if result['error']:
            return BaseController.send_error_api(result['data'], result['message'])

        return BaseController.send_response_api(result['data'], result['message'])

    @staticmethod
    def status(id):

        payment = paymentservice.update(id)

        if not payment['status_code'] == '404':
            return BaseController.send_response_api(payment, payment['data'], payment['message'])
        else:
            return BaseController.send_error_api(payment['data'], payment['message'])

    @staticmethod
    def is_field_exist(request, field_name):
        if field_name in request.json:
            return request.json[field_name]
        else:
            return None

    def card_number_validation(card_number):
        card_number = card_number.replace(" ", "")
        sum = 0
        num_digits = len(card_number)
        oddeven = num_digits & 1
        for count in range(0, num_digits):
            digit = int(card_number[count])
            if not ((count & 1) ^ oddeven):
                digit = digit * 2
            if digit > 9:
                digit = digit - 9
            sum = sum + digit
        return ((sum % 10) == 0)

    @staticmethod
    def confirm(request):
        transaction_id = request.json['transaction_id'] if 'transaction_id' in request.json else None
        order_id = request.json['order_id'] if 'order_id' in request.json else None
        if transaction_id and order_id:
            payload = {
                'transaction_id' : transaction_id,
                'order_id' : order_id
            }
            result = paymentservice.confirm(payload)
            if result['error']:
                return BaseController.send_error_api(result['data'], result['message'])
            return BaseController.send_response_api(result['data'], result['message'])
        else:
            return BaseController.send_error_api(None, 'payload is invalid')
