import datetime
import json
import base64
import requests
from app.models import db
from sqlalchemy.exc import SQLAlchemyError
#import model class
from app.models.payment import Payment
from app.models.order import Order
from app.models.order_details import OrderDetails
from app.configs.constants import MIDTRANS_API_BASE_URL as url, MERCHANT_ID as merchant_id, CLIENT_KEY, SERVER_KEY
from app.models.base_model import BaseModel

class PaymentService():
    
    def __init__(self):
        self.authorization = base64.b64encode(bytes(SERVER_KEY, 'utf-8')).decode()

    def bank_transfer(self, payloads):
        
        payloads['gross_amount'] = int(payloads['gross_amount'])


        headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization': self.authorization}

        # generate order details payload
        details = self.get_order_details(payloads['order_id'])

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
                        payloads['va_number']
                ]) and not isinstance(payloads['gross_amount'], int):
                    return {
                        'error': True,
                        'data': 'payload not valid'
                    }
            # todo create payload for BCA virtual account
            data = {}
            data['payment_type'] = payloads['payment_type']
            data['transaction_details'] = {}
            data['transaction_details']['gross_amount'] = payloads['gross_amount']
            data['transaction_details']['order_id'] = payloads['order_id']
            data['customer_details'] = {}
            data['customer_details']['email ']= payloads['email']
            data['customer_details']['first_name '] = payloads['first_name']
            data['customer_details']['last_name '] = payloads['last_name']
            data['customer_details']['phone '] = payloads['phone']
            data['item_details'] = details
            data['bank_transfer'] = {}
            data['bank_transfer']['bank'] = payloads['bank']
            data['bank_transfer']['va_number'] = payloads['va_number']
            data['bank_transfer']['free_text'] = {}
            data['bank_transfer']['free_text']['inquiry'] = [
                {
                    "id": "Free Text ID Free Text ID Free Text ID",
                    "en": "Free Text EN Free Text EN Free Text EN"
                }
            ]
            data['bank_transfer']['free_text']['payment'] = [
                {
                    "id": "Free Text ID Free Text ID Free Text ID",
                    "en": "Free Text EN Free Text EN Free Text EN"
                }
            ]

        if (payloads['bank'] == 'permata'):

            # payload validation for permata
            if not all(isinstance(string, str) for string in [
                    payloads['payment_type'],
                    payloads['order_id'],
                ]
            ) and not isinstance(payloads['gross_amount'], int):
                return {
                    'error': True,
                    'data': 'payloads is not valid'
                }
            # create paylod for midtrans
            data = {}
            data['payment_type'] = payloads['payment_type']
            data['bank_transfer'] = {}
            data['bank_transfer']['bank'] = payloads['bank']
            data['transaction_details'] = {}
            data['transaction_details']['order_id'] = payloads['order_id']
            data['transaction_details']['gross_amount'] = payloads['gross_amount']


        if(payloads['bank'] == 'bni'):
            # payload validation for bni
            if not all(isinstance(string, str) for string in [
                    payloads['payment_type'],
                    payloads['email'],
                    payloads['first_name'],
                    payloads['last_name'],
                    payloads['phone'],
                    payloads['va_number']
                ]
            ) and not isinstance(payloads['gross_amount'], int):
                return {
                    'error': True,
                    'data': 'payloads is not valid'
                }

            # create payload for midtrans
            data = {}
            data['payment_type'] = payloads['payment_type']
            data['bank_transfer'] = {}
            data['bank_transfer']['bank'] = payloads['bank']
            data['bank_transfer']['va_number'] = payloads['va_number']
            data['customer_details'] = {}
            data['customer_details']['email'] = payloads['email']
            data['customer_details']['first_name'] = payloads['first_name']
            data['customer_details']['last_name'] = payloads['last_name']
            data['customer_details']['phone'] = payloads['phone']
            data['item_details'] = details
            data['transaction_details'] = {}
            data['transaction_details']['order_id'] = payloads['order_id']
            data['transaction_details']['gross_amount'] = payloads['gross_amount']
       
        if(payloads['bank'] == 'mandiri_bill'):
            # payload validation for bni
            if not all(isinstance(string, str) for string in [
                    payloads['payment_type'],
                ]
            ) and not isinstance(payloads['gross_amount'], int):
                return {
                    'error': True,
                    'data': 'payloads is not valid'
                }

            # create payload for midtrans
            data = {}
            data['payment_type'] = payloads['payment_type']
            data['item_details'] = details
            data['transaction_details'] = {}
            data['transaction_details']['order_id'] = payloads['order_id']
            data['transaction_details']['gross_amount'] = payloads['gross_amount']

    def internet_banking(self, payloads):
        if not all(isinstance(string, str) for string in [
            payloads['order_id'],
            payloads['first_name'],
            payloads['last_name'],
            payloads['email'],
            payloads['phone']
        ]) and not isinstance(payloads['gross_amount', int]):
            return {
                'error': True,
                'message': 'payloads is not valid'
            }

        details = self.get_order_details(payloads['order_id'])
            
        data = {}
        data['payment_type'] = payloads['payment_type']
        data['transaction_details'] = {}
        data['transaction_details']['order_id'] = payloads['order_id']
        data['transaction_details']['gross_amount'] = payloads['gross_amount']
        data['item_details'] = details
        data['customer_details'] = {}
        data['customer_details']['first_name'] = payloads['first_name']
        data['customer_details']['last_name'] = payloads['last_name']
        data['customer_details']['email'] = payloads['email']
        data['customer_details']['phone'] = payloads['phone']        

        if (payloads['payment_type'] == 'cimb_clicks'):
            data['cimb_clicks'] = {}
            data['cimb_clicks']['description'] = payloads['description']

        # this will send the all payment methods payload to midtrand api
        try:
            endpoint = url + 'charge'
            result = requests.post(
                    endpoint,
                    headers={
                        'Accept': 'application/json',
                        'Content-Type':'application/json', 
                        'Authorization': 'Basic ' + self.authorization
                    }, json=data
            )

            payload = result.json()

            if (payload['status_code'] == '201'):
                self.save_payload(payload)

            return payload

        except Exception as e:
            # Invalid payloads
            return None
            data['transaction_details'] = {}
            data['transaction_details']['order_id'] = payloads['order_id']
            data['transaction_details']['gross_amount'] = payloads['gross_amount']

    def update(self, id):
        payment_status = requests.get(
            url + str(id) + '/status',
            headers={
                'Accept': 'application/json',
                'Content-Type':'application/json', 
                'Authorization': 'Basic ' + self.authorization
            }
        ) 

        status = payment_status.json()

        if (status['status_code'] == '201'):
            payment = db.session.query(Payment).filter_by(id=id).first().as_dict()

            if (payment['transaction_status'] != status['transaction_status']):

                payment.update({
                    'updated_at': datetime.datetime.now(),
                    'transaction_status': status['transaction_status']
                })

                db.session.commit()

        return status

    def get_order_details(self, order_id):
        # using order_id to get ticket_id, price, quantity, ticket_type(name) in payment service
        item_details = db.session.query(OrderDetails).filter_by(order_id=order_id).all()
        result = []
        for item in item_details:
            ticket = item.ticket.as_dict()
            item = item.as_dict()
            temp = {}
            temp['name'] = ticket['ticket_type']
            temp['price'] = item['price']
            temp['quantity'] = item['count']
            temp['id'] = item['id']
            result.append(temp)
        return result

    def save_payload(self, data):

        new_payment = Payment()
        new_payment.transaction_id = data['transaction_id']
        new_payment.order_id = data['order_id']
        new_payment.gross_amount = data['gross_amount']
        new_payment.payment_type = data['payment_type']
        new_payment.transaction_time = data['transaction_time']
        new_payment.transaction_status = data['transaction_status']
        new_payment.fraud_status = data['fraud_status'] if 'fraud_status' in data else None

        db.session.add(new_payment)
        db.session.commit()



