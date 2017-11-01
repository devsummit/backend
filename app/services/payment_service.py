import datetime
import base64
import requests
import paypalrestsdk
from sqlalchemy.exc import SQLAlchemyError
from app.models import db, mail
# import model class
from app.models.payment import Payment
from app.models.order_details import OrderDetails
from app.models.user import User
from app.models.order import Order
from app.models.booth import Booth
from app.models.redeem_code import RedeemCode
from app.models.hacker_team import HackerTeam
from app.models.user_hacker import UserHacker
from app.models.user_booth import UserBooth
from app.models.user_ticket import UserTicket
from app.services.user_ticket_service import UserTicketService
from app.services.redeem_code_service import RedeemCodeService
from app.builders.response_builder import ResponseBuilder
from app.services.fcm_service import FCMService
from app.services.email_service import EmailService
from app.configs.constants import MIDTRANS_API_BASE_URL as url, SERVER_KEY
from app.configs.constants import VA_NUMBER
from app.configs.constants import TICKET_TYPES, ROLE


class PaymentService():

	def __init__(self):
		self.authorization = base64.b64encode(bytes(SERVER_KEY, 'utf-8')).decode()
		self.headers = {
			'Accept': 'application/json',
			'Content-Type': 'application/json',
			'Authorization': 'Basic ' + self.authorization
		}

	def admin_get(self):
		response = ResponseBuilder()
		results = db.session.query(Payment).all()
		_results = []
		for result in results:
			data = result.as_dict()
			data['user'] = result.order.user.as_dict()
			_results.append(data)
		return response.set_data(_results).build()

	def admin_filter(self, param):
		response = ResponseBuilder()
		results = self.admin_get()['data']
		_results = []
		for result in results:
			if 'fraud_status' in param:
				if result['fraud_status'] is not None and result['fraud_status'] == param['fraud_status']:
					_results.append(result)
			elif 'transaction_status' in param:
				if result['transaction_status'] is not None and result['transaction_status'] == param['transaction_status']:
					_results.append(result)
			else:
				_results.append(result)
		return response.set_data(_results).build()

	def get(self, user_id):
		response = ResponseBuilder()
		# get the orders
		orders = db.session.query(Order).filter_by(user_id=user_id).all()
		_results = []
		for order in orders:
			data = db.session.query(Payment).filter_by(order_id=order.id).first()
			data = data.as_dict() if data else None
			_results.append(data)
		return response.set_data(_results).build()

	def admin_show(self, payment_id):
		response = ResponseBuilder()
		result = db.session.query(Payment).filter_by(id=payment_id).first()
		data = result.as_dict()
		data['user'] = result.order.user.as_dict()
		return response.set_data(data).build()

	def show(self, payment_id):
		response = ResponseBuilder()
		result = db.session.query(Payment).filter_by(id=payment_id).first()
		result = result.as_dict() if result else None
		return response.set_data(result).build()

	def get_order_referal(self, order_id):
		order = db.session.query(Order).filter_by(id=order_id).first()
		if (order is not None and order.referal):
			return order.referal.as_dict()
		return None

	def bank_transfer(self, payloads):
		response = ResponseBuilder()
		payloads['gross_amount'] = int(payloads['gross_amount'])
		# check for referal discount
		ref = self.get_order_referal(payloads['order_id'])
		# generate order details payload
		details = self.get_order_details(payloads['order_id'], ref)

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
						# payloads['va_number']
				]
			) and not isinstance(payloads['gross_amount'], int):
				return response.build_invalid_payload_response()

			# todo create payload for BCA virtual account
			data = {}
			data['payment_type'] = payloads['payment_type']
			data['transaction_details'] = {}
			data['transaction_details']['gross_amount'] = payloads['gross_amount']
			data['transaction_details']['order_id'] = payloads['order_id']
			data['customer_details'] = {}
			data['customer_details']['email'] = payloads['email']
			data['customer_details']['first_name'] = payloads['first_name']
			data['customer_details']['last_name'] = payloads['last_name']
			data['customer_details']['phone'] = payloads['phone']
			data['item_details'] = details
			data['bank_transfer'] = {}
			data['bank_transfer']['bank'] = payloads['bank']
			data['bank_transfer']['va_number'] = VA_NUMBER[payloads['bank']]
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
			if not all(
				isinstance(string, str) for string in [
					payloads['payment_type'],
					payloads['order_id']
				]
			) and not isinstance(payloads['gross_amount'], int):
				return response.build_invalid_payload_response()

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
			if not all(
				isinstance(string, str) for string in [
					payloads['payment_type'],
					payloads['email'],
					payloads['first_name'],
					payloads['last_name'],
					payloads['phone']
				]
			) and not isinstance(payloads['gross_amount'], int):
				return response.build_invalid_payload_response()

			# create payload for midtrans
			data = {}
			data['payment_type'] = payloads['payment_type']
			data['bank_transfer'] = {}
			data['bank_transfer']['bank'] = payloads['bank']
			data['bank_transfer']['va_number'] = VA_NUMBER[payloads['bank']]
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
			# payload validation for mandiri
			if not all(
				isinstance(string, str) for string in [
					payloads['payment_type'],
				]
			) and not isinstance(payloads['gross_amount'], int):
				return response.build_invalid_payload_response()

			# create payload for midtrans
			data = {}
			data['payment_type'] = payloads['payment_type']
			data['item_details'] = details
			data['transaction_details'] = {}
			data['transaction_details']['order_id'] = payloads['order_id']
			data['transaction_details']['gross_amount'] = payloads['gross_amount']
			data['echannel'] = {}
			data['echannel']['bill_info1'] = 'Payment for:'
			data['echannel']['bill_info2'] = 'DevSummit Indonesia'

		midtrans_api_response = self.send_to_midtrans_api(data)

		return midtrans_api_response

	def credit_payment(self, payloads):
		response = ResponseBuilder()
		if not all(
			isinstance(string, str) for string in [
				payloads['order_id'],
				payloads['email'],
				payloads['first_name'],
				payloads['last_name'],
				payloads['phone'],
				payloads['card_number'],
				payloads['card_exp_month'],
				payloads['card_exp_year'],
				payloads['card_cvv'],
				payloads['client_key']
			]
		) and not isinstance(payloads['gross_amount'], int):
			return response.build_invalid_payload_response()

		# get the token id first
		token_id = requests.get(url + 'card/register?' + 'card_number=' + payloads['card_number'] + '&card_exp_month=' + payloads['card_exp_month'] + '&card_exp_year=' + payloads['card_exp_year'] + '&card_cvv=' + payloads['card_cvv'] + '&bank=' + payloads['bank'] + '&secure=' + 'true' + '&gross_amount=' + str(payloads['gross_amount']) + '&client_key=' + payloads['client_key'], headers=self.headers)
		token_id = token_id.json()
		# prepare data
		data = {}
		if 'status_code' in token_id and token_id['status_code'] == '200':
			data['saved_token_id'] = token_id['saved_token_id']
			data['masked_card'] = token_id['masked_card']
		else:
			return response.set_message(token_id['validation_messages'][0]).set_error(True).build()

		# check for referal discount
		ref = self.get_order_referal(payloads['order_id'])
		# generate order details payload
		item_details = self.get_order_details(payloads['order_id'], ref)

		data['payment_type'] = payloads['payment_type']
		data['transaction_details'] = {}
		data['transaction_details']['order_id'] = payloads['order_id']
		data['transaction_details']['gross_amount'] = payloads['gross_amount']
		data['credit_card'] = {}
		data['credit_card']['token_id'] = token_id['saved_token_id']
		data['item_details'] = item_details
		data['customer_details'] = {}
		data['customer_details']['first_name'] = payloads['first_name']
		data['customer_details']['last_name'] = payloads['last_name']
		data['customer_details']['email'] = payloads['email']
		data['customer_details']['phone'] = payloads['phone']

		return self.send_to_midtrans_api(data)

	def authorize(self, payloads):
		response = ResponseBuilder()
		if not all(isinstance(string, str) for string in [
			payloads['payment_type'],
			payloads['type'],
			payloads['order_id']
		]) and not isinstance(payloads['gross_amount'], int):
			return response.build_invalid_payload_response()

		token = db.session.query(Payment).filter_by(order_id=payloads['order_id']).first()
		token = token.as_dict()

		data = {}
		data['payment_type'] = payloads['payment_type']
		data['transaction_details'] = {}
		data['transaction_details']['order_id'] = payloads['order_id']
		data['transaction_details']['gross_amount'] = payloads['gross_amount']
		data['credit_card'] = {}
		data['credit_card']['token_id'] = token['saved_token_id']
		data['credit_card']['type'] = payloads['type']

		endpoint = url + str(payloads['order_id']) + '/approve'
		transaction_status = requests.post(
			endpoint,
			headers=self.headers,
			json=data
		)
		transaction_status = transaction_status.json()

		if 'status_code' in transaction_status and transaction_status['status_code'] in ['200', '201']:
			payment = db.session.query(Payment).filter_by(order_id=transaction_status['order_id'])
			payment.update({
				'updated_at': datetime.datetime.now(),
				'fraud_status': transaction_status['fraud_status']
			})

			db.session.commit()

			return response.set_data(transaction_status).set_message('Authorization success').build()

		else:
			return response.set_error(True).set_data(transaction_status).set_message('change fraud status is failed').build()

	def internet_banking(self, payloads):
		response = ResponseBuilder()
		if not all(isinstance(string, str) for string in [
			payloads['order_id'],
			payloads['first_name'],
			payloads['last_name'],
			payloads['email'],
			payloads['phone']
		]) and not isinstance(payloads['gross_amount'], int):
			return response.build_invalid_payload_response()

		# check for referal discount
		ref = self.get_order_referal(payloads['order_id'])
		details = self.get_order_details(payloads['order_id'], ref)

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
			data['bank'] = 'cimb'

		if (payloads['payment_type'] == 'bca_klikpay'):
			data['bca_klikpay'] = {}
			data['bca_klikpay']['type'] = 1
			data['bca_klikpay']['description'] = 'Devsummit tickets purchase'
			data['bank'] = 'bca'

		if (payloads['payment_type'] == 'bca_klikbca'):
			data['bca_klikbca'] = {}
			data['bca_klikbca']['user_id'] = payloads['user_id']
			data['bca_klikbca']['description'] = payloads['description']
			data['bank'] = 'bca'

		if (payloads['payment_type'] == 'mandiri_clickpay'):
			data['mandiri_clickpay'] = {}
			data['mandiri_clickpay']['card_number'] = payloads['card_number']
			data['mandiri_clickpay']['input1'] = payloads['card_number'][6:]
			data['mandiri_clickpay']['input2'] = payloads['gross_amount']
			data['mandiri_clickpay']['input3'] = payloads['input3']
			data['mandiri_clickpay']['token'] = payloads['token']
			data['bank'] = 'mandiri'

		return self.send_to_midtrans_api(data)

	def cstore(self, payloads):
		response = ResponseBuilder()
		if not all(isinstance(string, str) for string in [
			payloads['order_id'],
			payloads['first_name'],
			payloads['last_name'],
			payloads['email'],
			payloads['phone'],
		]) and not isinstance(payloads['gross_amount'], int):
			return response.build_invalid_payload_response()

		# get referral by order id
		ref = self.get_order_referal(payloads['order_id'])

		details = self.get_order_details(payloads['order_id'], ref)

		data = {}
		data['payment_type'] = payloads['payment_type']
		data['transaction_details'] = {}
		data['transaction_details']['gross_amount'] = payloads['gross_amount']
		data['transaction_details']['order_id'] = payloads['order_id']
		data['cstore'] = {}
		data['cstore']['store'] = 'Indomaret'
		data['cstore']['message'] = 'dev summit ticket transaction'
		data['customer_details'] = {}
		data['customer_details']['first_name'] = payloads['first_name']
		data['customer_details']['last_name'] = payloads['last_name']
		data['customer_details']['email'] = payloads['email']
		data['customer_details']['phone'] = payloads['phone']
		data['details'] = details

		return self.send_to_midtrans_api(data)

	def get_midtrans_va_number(self, payload):
		# Permata = "permata_va_number" = "8562000087926752"
		# BCA = "va_numbers": [{"bank": "bca", "va_number": "91019021579"}]
		# Mandiri Bill = no va number (use bill_key and biller_code instead)
		# BNI = "va_numbers": [{"bank": "bni", "va_number": "8578000000111111"}]

		if 'va_numbers' in payload:
			va_number = payload['va_numbers'][0]['va_number']
		elif 'permata_va_number' in payload:
			va_number = payload['permata_va_number']
		elif 'bill_key' in payload and 'biller_code' in payload:
			va_number = payload['bill_key'] + '-' + payload['biller_code']
		else:
			va_number = None

		return va_number

	# this will send the all payment methods payload to midtrand api
	def send_to_midtrans_api(self, payloads):
		response = ResponseBuilder()
		endpoint = url + 'charge'
		result = requests.post(
				endpoint,
				headers=self.headers,
				json=payloads
		)
		payload = result.json()
		if(str(payload['status_code']) in ['400', '202']):

			if 'validation_messages' in payload and payload['validation_messages'][0]:
				messages = payload['validation_messages'][0] 
			elif 'status_message' in payload:
				messages = payload['status_message']
			else:
				messages = 'unknown error occured'

			return response.set_error(True).set_status_code(payload['status_code']).set_message(messages).build()
		else:
			if 'bank' in payloads and payloads['payment_type'] != 'credit_card':
				payload['bank'] = payloads['bank']
			elif payloads['payment_type'] == 'echannel':
				payload['bank'] = 'mandiri_bill'
				payload['va_number'] = self.get_midtrans_va_number(payload)
			
			else:
				if 'bank_transfer' in payloads:
					payload['bank'] = payloads['bank_transfer']['bank']
					payload['va_number'] = self.get_midtrans_va_number(payload)
				else:
					payload['bank'] = None

			if payloads['payment_type'] in ['bca_klikbca', 'bca_klikpay', 'cimb_clicks', 'danamon_online', 'bri_epay']:
				payload['va_number'] = payload['redirect_url']

			if 'status_code' in payload and payload['status_code'] == '406':
				return response.set_data(payload).set_error(True).set_message('Duplicate order ID. Order ID has already been utilized previously').build()

			# handle indomaret payment
			if payloads['payment_type'] == 'cstore':
				payload['bank'] = 'indomaret'
				payload['fraud_status'] = payload['payment_code']

			if ('status_code' in payload and str(payload['status_code']) in ['201', '200']):
				self.save_payload(payload, payloads)

			# if  not fraud and captured save ticket to user_ticket table
			if('fraud_status' in payload and payload['fraud_status'] == 'accept' and payload['transaction_status'] == 'capture'):
				order = db.session.query(Order).filter_by(id=payload['order_id']).first()
				self.save_paid_ticket(order.as_dict())
		message = payload['status_message'] if 'status_message' in payload else 'No message from payload' 
		return response.set_data(payload).set_message(message).build()

	def update(self, id):
		response = ResponseBuilder()
		# get the transaction id from payment table
		payment = db.session.query(Payment).filter_by(id=id).first()
		if payment is not None:
			order = payment.order.as_dict()
			payment = payment.as_dict()
		else:
			return response.set_error(True).set_message('payment not found').build()

		payment_status = requests.get(
			url + str(payment['order_id']) + '/status',
			headers=self.headers
		)

		status = payment_status.json()

		if status['status_code'] in ['200', '201', '407', '412']:

			if (payment['transaction_status'] != status['transaction_status']):
				payment = db.session.query(Payment).filter_by(id=id)
				payment.update({
					'updated_at': datetime.datetime.now(),
					'transaction_status': status['transaction_status']
				})

				db.session.commit()
				if (payment.first().as_dict()['transaction_status'] == 'expire'):
					# on payment success
					self.save_paid_ticket(order)
			return response.set_data(status).build()

		return response.build_invalid_payload_response()

	def save_paid_ticket(self, order):
		item_details = db.session.query(OrderDetails).filter_by(order_id=order['id']).all()
		for item in item_details:
			data = item.as_dict()
			for i in range(0, item.count):
				user_ticket = UserTicket()
				user_ticket.user_id = order['user_id']
				user_ticket.ticket_id = data['ticket_id']
				db.session.add(user_ticket)
			db.session.commit()

	def get_order_details(self, order_id, referal=None):
		# using order_id to get ticket_id, price, quantity, ticket_type(name) in payment service
		item_details = db.session.query(OrderDetails).filter_by(order_id=order_id).all()
		result = []
		total = 0
		last_id = 0
		for item in item_details:
			ticket = item.ticket.as_dict()
			item = item.as_dict()
			temp = {}
			temp['name'] = ticket['ticket_type']
			temp['price'] = item['price']
			temp['quantity'] = item['count']
			temp['id'] = item['id']
			total = total + (item['price'] * item['count'])
			last_id = temp['id']
			result.append(temp)
		if referal is not None:
			temp = {}
			temp['name'] = referal['owner']
			temp['price'] = -(total * referal['discount_amount'])
			temp['quantity'] = 1
			temp['id'] = last_id + 1
			result.append(temp)
		return result

	def save_payload(self, data, payloads):
		new_payment = Payment()
		new_payment.transaction_id = data['transaction_id']
		new_payment.order_id = data['order_id']
		new_payment.gross_amount = data['gross_amount']
		new_payment.payment_type = data['payment_type']
		new_payment.transaction_time = data['transaction_time']
		new_payment.transaction_status = data['transaction_status']
		new_payment.bank = data['bank']
		new_payment.fraud_status = data['fraud_status'] if 'fraud_status' in data else None
		new_payment.masked_card = payloads['masked_card'] if 'masked_card' in payloads else None
		new_payment.saved_token_id = payloads['saved_token_id'] if 'saved_token_id' in payloads else None
		new_payment.va_number = data['va_number'] if 'va_number' in data else None

		db.session.add(new_payment)
		db.session.commit()

	def get_paypal_detail(self, id):
		try:
			payment = paypalrestsdk.Payment.find(id)
			print(payment)
		except paypalrestsdk.ResourceNotFound as error:
			payment = False
		return payment

	def confirm(self, payload, user_id):
		response = ResponseBuilder()
		emailservice = EmailService()
		transaction_exist = db.session.query(Payment).filter_by(transaction_id=payload['transaction_id']).first()
		if transaction_exist:
			return response.set_error(True).set_message('this transaction have been used before').set_data(None).build()
		paypal_details = self.get_paypal_detail(payload['transaction_id'])
		if paypal_details == False:
			return response.set_error(True).set_message('Transaction id not found').set_data(None).build()
		paypal_details_amount = int(paypal_details['transactions'][0]['amount']['total'].split('.')[0])
		order_ = db.session.query(Order).filter_by(id=payload['order_id']).first()
		if order_ is None:
			return response.set_error(True).set_data(None).set_message('Order not found').build()
		user = order_.user
		order_details = db.session.query(OrderDetails).filter_by(order_id=payload['order_id']).all()
		check_total = 0
		discount = 0
		for order in order_details:
			check_total += order.price * order.count	
		if order_.referal_id is not None:
			discount = check_total * order_.referal.discount_amount 
		if check_total - discount <= paypal_details_amount:
			payment_exist = db.session.query(Payment).filter_by(transaction_id=payload['transaction_id']).first()
			if payment_exist:
				return response.set_data(None).set_message('Payment had been completed!').set_error(True).build()
			payment = Payment()
			payment.order_id = payload['order_id']
			payment.transaction_id = payload['transaction_id']
			payment.gross_amount = paypal_details_amount
			payment.payment_type = 'paypal'
			payment.transaction_status = "captured"			
			try:				
				db.session.add(payment)
				db.session.commit()
			except SQLAlchemyError as e:
				data = e.orig.args
				return response.set_data(None).set_message(data).set_error(True).build()
			items = db.session.query(OrderDetails).filter_by(order_id=payment.order_id).first()
			if items.ticket.type == TICKET_TYPES['exhibitor']:
				payload = {}
				payload['user_id'] = user.id
				payload['ticket_id'] = items.ticket_id
				UserTicketService().create(payload)
				self.create_booth(user)
				user_query = db.session.query(User).filter_by(id=user.id)
				user_query.update({
					'role_id': ROLE['booth']
				})
				redeem_payload = {}
				redeem_payload['ticket_id'] = items.ticket_id
				redeem_payload['codeable_id'] = user.id
				RedeemCodeService().purchase_user_redeems(redeem_payload)
				get_codes = db.session.query(RedeemCode).filter_by(codeable_type='user', codeable_id=user.id).all()
				code = []
				for get_code in get_codes:
					code.append("<li>%s</li>" %(get_code.code))
				li = ''.join(code)
				template = "<h3>You have complete the payment with order_id = %s</h3><h4>Here are the redeem codes for claiming full 3 days ticket at devsummit event as described in the package information : </h4>%s<h3>Use the above code to claim your ticket</h3><h3>Thank you for your purchase</h3>" %(order_.id, li)
				template += "<h4>And here is your Invoice:</h4>"
				template += '<a href="https://api.devsummit.io/invoices/'+ order_.id +'">Klik here to show the invoice</a>'
				email = emailservice.set_recipient(user.email).set_subject('Congratulations !! you received exhibitor code').set_sender('noreply@devsummit.io').set_html(template).build()
				mail.send(email)
			if items.ticket.type == TICKET_TYPES['hackaton']:
				payload = {}
				payload['user_id'] = user.id
				payload['ticket_id'] = items.ticket_id
				UserTicketService.create(payload)
				self.create_hackaton_team(user, items.ticket_id)
				user_query = db.session.query(User).filter_by(id=user.id)
				user_query.update({
					'role_id': ROLE['hackaton']
				})
				hacker_team = db.session.query(HackerTeam).order_by(HackerTeam.created_at.desc()).first()
				redeem_payload = {}
				redeem_payload['codeable_type'] = TICKET_TYPES['hackaton']
				redeem_payload['codeable_id'] = hacker_team.id,
				redeem_payload['count'] = items.ticket.quota
				RedeemCodeService().create(redeem_payload)
				get_codes = db.session.query(RedeemCode).filter_by(codeable_type='hackaton', codeable_id=hacker_team.id).all()
				code = []
				for get_code in get_codes:
					code.append("<li>%s</li>" %(get_code.code))
				li = ''.join(code)
				template = "<h3>You have complete the payment with order_id = %s</h3><h4>Here your redeem codes : </h4>%s<h3>Share the above code to your teammate, and put it into redeem code menu to let them join your team and claim their ticket</h3><h3>Thank you for your purchase</h3>" %(order_.id, li)
				template += "<h4>And here is your Invoice:</h4>"
				template += '<a href="https://api.devsummit.io/invoices/'+ order_.id +'">Klik here to show the invoice</a>'
				email = emailservice.set_recipient(user.email).set_subject('Congratulations !! you received hackaton code').set_sender('noreply@devsummit.io').set_html(template).build()
				mail.send(email)
			else:				
				result = None
				for order in order_details:
					for i in range(0, order.count):
						payload = {}
						payload['user_id'] = user.id
						payload['ticket_id'] = order.ticket_id
						result = UserTicketService().create(payload)
				if (result and (not result['error'])):
					template = "<h3>Congratulation! you have the previlege to attend Indonesia Developer Summit</h3>"
					template += "<h4>Here is your Invoice:</h4>"
					template += '<a href="https://api.devsummit.io/invoices/'+ order_.id +'">Klik here to show the invoice</a>'
					template += "<h5>Thank you.</h5>"
					email = emailservice.set_recipient(user.email).set_subject('Devsummit Ticket Invoice').set_sender('noreply@devsummit.io').set_html(template).build()
					mail.send(email)
			confirmed_order = db.session.query(Order).filter_by(id=payment.order_id)
			confirmed_order.update({
				'status': 'paid'
			})
			db.session.commit()
			send_notification = FCMService().send_single_notification('Payment Status', 'Your payment has been confirmed', user.id, ROLE['admin'])
			return response.set_data(None).set_message('Purchase Completed').build()
		else:
			return response.set_error(True).set_message('Paypal amount did not match').build()

	def create_booth(self, user):
		booth = Booth()
		booth.name = 'Your booth name here'
		booth.user_id = user.id
		booth.points = 0
		booth.summary = ''
		booth.logo_url = None
		booth.stage_id = None
		db.session.add(booth)
		db.session.commit()
		userbooth = UserBooth()
		userbooth.user_id = user.id
		userbooth.booth_id = booth.id
		db.session.add(userbooth)
		db.session.commit()

	def create_hackaton_team(self, user, ticket_id):
		hacker_team = HackerTeam()
		hacker_team.name = 'Your Hacker Team name'
		hacker_team.logo = ''
		hacker_team.project_name = 'Project Name'
		hacker_team.project_url = 'Project Link'
		hacker_team.theme = ''
		hacker_team.ticket_id = ticket_id
		db.session.add(hacker_team)
		db.session.commit()
		hackteam = db.session.query(HackerTeam).order_by(HackerTeam.created_at.desc()).first()
		userhacker = UserHacker()
		userhacker.user_id = user.id
		userhacker.hacker_team_id = hackteam.id
		db.session.add(userhacker)
		db.session.commit()
		
