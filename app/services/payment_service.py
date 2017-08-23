import datetime
import json
import base64
import requests
from app.models import db
from sqlalchemy.exc import SQLAlchemyError
#import model class
from app.models.payment import Payment
from app.models.order import Order
from app.configs.constants import MIDTRANS_API_BASE_URL as url, MERCHANT_ID as merchant_id, CLIENT_KEY, SERVER_KEY

class PaymentService():

    def bank_transfer(self, payloads):
        
        payloads['gross_amount'] = int(payloads['gross_amount'])

        self.authorization = str(base64.b64encode(bytes(SERVER_KEY, 'utf-8')))[1:]

        headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization': self.authorization}

        if (payloads['bank'] == 'bca'):

            # payloads validation for BCA virtual account
            if not all(
                isinstance(string, str) for string in [
                        payloads['payment_type'], 
                        payloads['order_id'], 
                        payloads['email'],
                        payloads['first_name'],
                        payloads['last_name'],
                        payloads['phone'],
                        payloads['ticket_id'],
                        payloads['name'],
                        payloads['bank'],
                        payloads['va_number']
                ] and isinstance(number, int) for number in [
                        payloads['gross_amount'],
                        payloads['price'],
                        payloads['quantity']
                ]
            ):
                return {
                    'error': True,
                    'data': 'payload not valid'
                }
            # todo create payload for BCA virtual account

        if (payloads['bank'] == 'permata'):

            # payload validation for permata
            if not all(isinstance(string, str) for string in [
                    payloads['payment_type'],
                    payloads['bank'],
                    payloads['order_id'],
                ]
            ) and not isinstance(payloads['gross_amount'], int):
                return {
                    'error': True,
                    'data': 'payloads is not valid'
                }
            # get transaction_id and transaction_status from midtrans
            data = {}
            data['payment_type'] = payloads['payment_type']
            data['bank_transfer'] = {}
            data['bank_transfer']['bank'] = payloads['bank']
            data['transaction_details'] = {}
            data['transaction_details']['order_id'] = payloads['order_id']
            data['transaction_details']['gross_amount'] = payloads['gross_amount']

            try:
                result = requests.post(
                        'https://api.sandbox.midtrans.com/v2/charge', 
                        headers={
                            'Accept': 'application/json',
                            'Content-Type':'application/json', 
                            'Authorization': 'Basic VlQtc2VydmVyLW5qaHFnaG5GVVpidFpnT2c5bGROdFkwbDo='
                        }, json=data
                )
                payload = result.json()
                return payload
                # todo checkout the response from mid trans here
            except Exception as e:
                # Invalid payloads
                return None





