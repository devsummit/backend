import os
import datetime
from app.models import db, mail
from sqlalchemy.exc import SQLAlchemyError
# import model class
from app.models.order import Order
from app.models.email_templates.email_purchase import EmailPurchase
from app.models.order_details import OrderDetails
from app.models.user import User
from app.models.payment import Payment
from app.models.order_verification import OrderVerification
from app.models.ticket import Ticket
from app.models.base_model import BaseModel
from app.models.booth import Booth
from app.models.user_booth import UserBooth
from app.models.hacker_team import HackerTeam
from app.models.user_hacker import UserHacker
from app.models.redeem_code import RedeemCode
from app.services.base_service import BaseService
from app.services.email_service import EmailService
from app.builders.response_builder import ResponseBuilder
from app.services.user_ticket_service import UserTicketService
from app.services.redeem_code_service import RedeemCodeService
from app.services.fcm_service import FCMService
from flask import current_app
from PIL import Image
from app.configs.constants import IMAGE_QUALITY, ROLE
from app.services.helper import Helper
from app.configs.constants import TICKET_TYPES
from app.configs.settings import LOCAL_TIME_ZONE
from werkzeug import secure_filename


class OrderVerificationService(BaseService):
	
	def get(self):
		result = db.session.query(OrderVerification, Order, Payment).join(Order).join(Payment).filter(OrderVerification.is_used==0, Order.status != 'paid').all()
		_result = []
		for orderverification, order, payment in result:
			data = orderverification.as_dict()
			data = self.transformTimeZone(data)
			if data['payment_proof']:
				data['payment_proof'] = Helper().url_helper(data['payment_proof'], current_app.config['GET_DEST'])
			else:
				data['payment_proof'] = ""
			data['payment'] = payment.as_dict()
			data['user'] = orderverification.user.include_photos().as_dict()
			_result.append(data)
		return _result

	def create(self, payload):
		response = ResponseBuilder()
		orderverification_query = db.session.query(OrderVerification).filter_by(order_id=payload['order_id'])
		orderverification = orderverification_query.first()
		payment_proof = self.save_file(payload['payment_proof']) if payload['payment_proof'] is not None else None
		if orderverification:
			if orderverification.payment_proof is not None:
				Helper().silent_remove(current_app.config['STATIC_DEST'] + orderverification.payment_proof)
			orderverification_query.update({
				'payment_proof': payment_proof,
				'updated_at': datetime.datetime.now()
			})
			order = orderverification.order
		else:
			orderverification = OrderVerification()
			order_query = db.session.query(Order).filter_by(id=payload['order_id'])
			payment_query = db.session.query(Payment).filter_by(order_id=payload['order_id'])
			order = order_query.first()
			orderverification.user_id = order.user_id
			orderverification.order_id = payload['order_id']
			orderverification.payment_proof = payment_proof
			order_query.update({
				'status': 'in progress',
				'updated_at': datetime.datetime.now()
			})
			payment_query.update({
				'transaction_status': 'in progress',
				'updated_at': datetime.datetime.now()
			})
			db.session.add(orderverification)
		try:
			db.session.commit()
			result = orderverification.as_dict()
			result['payment_proof'] = Helper().url_helper(result['payment_proof'], current_app.config['GET_DEST'])
			if orderverification:
				send_notification = FCMService().send_single_notification('Payment Status', 'Payment proof have been uploaded, your payment is being processed', order.user_id, ROLE['admin'])
			return response.set_data(result).set_message('Data created succesfully').build()
		except SQLAlchemyError as e:
			data = e.orig.args
			return response.set_data(data).set_error(True).build()

	def show(self, id):
		response = ResponseBuilder()
		orderverification = db.session.query(OrderVerification).filter_by(order_id=id).first()
		data = orderverification.as_dict() if orderverification else None
		if data:
			if data['payment_proof']:
				data['payment_proof'] = Helper().url_helper(data['payment_proof'], current_app.config['GET_DEST'])
			else:
				data['payment_proof'] = ""
			return response.set_data(data).build()
		return response.set_error(True).set_message('data not found').set_data(None).build()


	def update(self, id, payload):
		response = ResponseBuilder()
		orderverification = db.session.query(OrderVerification).filter_by(id=id)
		data = orderverification.first().as_dict() if orderverification.first() else None
		if data['payment_proof'] is not None and payload['payment_proof']:
			Helper().silent_remove(current_app.config['STATIC_DEST'] + data['payment_proof'])
		if data is None:
			return response.set_error(True).set_message('data not found').set_data(None).build()
		payment_proof = self.save_file(payload['payment_proof']) if payload['payment_proof'] is not None else None
		try:
			orderverification = db.session.query(OrderVerification).filter_by(id=id)			
			orderverification.update({
				'user_id': payload['user_id'],
				'order_id': payload['order_id'],
				'payment_proof': payment_proof,
				'updated_at': datetime.datetime.now()
			})
			db.session.commit()
			data = orderverification.first()
			return response.set_data(data.as_dict()).build()
		except SQLAlchemyError as e:
			data = e.orig.args
			return response.set_error(True).set_data(data).build()

	def delete(self, id):
		response = ResponseBuilder()
		orderverification = db.session.query(OrderVerification).filter_by(id=id).first()
		if orderverification.payment_proof is not None:
			Helper().silent_remove(current_app.config['STATIC_DEST'] + orderverification.payment_proof)
		orderverification = db.session.query(OrderVerification).filter_by(id=id)
		if orderverification.first() is not None:
			orderverification.delete()
			db.session.commit()
			return response.set_message('Order Verification entry was deleted').build()
		else:
			data = 'Entry not found'
			return response.set_data(None).set_message(data).set_error(True).build()

	def save_file(self, file, id=None):
		image = Image.open(file, 'r')
		if file and Helper().allowed_file(file.filename, current_app.config['ALLOWED_EXTENSIONS']):
			if (Helper().allowed_file(file.filename, ['jpg', 'jpeg', 'png'])):
				image = image.convert("RGB")
			filename = secure_filename(file.filename)
			filename = Helper().time_string() + "_" + file.filename.replace(" ", "_")
			image.save(os.path.join(current_app.config['POST_PAYMENT_PROOF_DEST'], filename), quality=IMAGE_QUALITY, optimize=True)
			return current_app.config['SAVE_PAYMENT_PROOF_DEST'] + filename
		else:
			return None

	def create_booth(self, user, type):
		booth = Booth()
		booth.name = 'Your booth name here'
		booth.user_id = user.id
		booth.points = 0
		booth.summary = ''
		booth.type = type
		booth.logo_url = None
		booth.stage_id = None
		db.session.add(booth)
		db.session.commit()
		userbooth = UserBooth()
		userbooth.user_id = user.id
		userbooth.booth_id = booth.id
		db.session.add(userbooth)
		db.session.commit()

	def create_hackaton (self, user, ticket_id, hacker_team_name=''):
		hacker_team = HackerTeam()
		hacker_team.name = hacker_team_name
		hacker_team.logo = None
		hacker_team.project_name = 'Your project name here'
		hacker_team.project_url = 'Project name'
		hacker_team.theme = 'Project link'
		hacker_team.ticket_id = ticket_id
		db.session.add(hacker_team)
		db.session.commit()
		userhacker = UserHacker()
		userhacker.user_id = user.id
		userhacker.hacker_team_id = hacker_team.id
		db.session.add(userhacker)
		db.session.commit()
		return hacker_team.id

	def admin_verify(self, order_id, request, hacker_team_name=None):
		response = ResponseBuilder()
		emailservice = EmailService()
		order_query = db.session.query(Order).filter_by(id=order_id)
		order = order_query.first()
		if order.status != 'paid':
			user_query = db.session.query(User).filter_by(id=order.user_id)
			user = user_query.first()
			items = db.session.query(OrderDetails).filter_by(order_id=order.id).all()
			url_invoice = request.url_root + '/invoices/'+ order.id
			if items[0].ticket.type == TICKET_TYPES['exhibitor']:
				payload = {}
				payload['user_id'] = user.id
				payload['ticket_id'] = items[0].ticket_id

				UserTicketService().create(payload)
				self.create_booth(user, items[0].ticket.ticket_type)
				user_query.update({
					'role_id': ROLE['booth'],
					'updated_at': datetime.datetime.now()
				})
				redeem_payload = {}
				redeem_payload['ticket_id'] = items[0].ticket_id
				redeem_payload['codeable_id'] = user.id
				RedeemCodeService().purchase_user_redeems(redeem_payload)
				get_codes = db.session.query(RedeemCode).filter_by(codeable_type='user', codeable_id=user.id).all()
				mail_template = EmailPurchase()
				template = mail_template.set_invoice_path(order.id).set_redeem_code(get_codes).build()
				email = emailservice.set_recipient(user.email).set_subject('Congratulations !! you received exhibitor code').set_sender('noreply@devsummit.io').set_html(template).build()
				mail.send(email)
			elif items[0].ticket.type == TICKET_TYPES['hackaton']:
				payload = {}
				payload['user_id'] = user.id
				payload['ticket_id'] = items[0].ticket_id
				UserTicketService().create(payload)
				user_query.update({
					'role_id': ROLE['hackaton'],
					'updated_at': datetime.datetime.now()
				})
				send_notification = FCMService().send_single_notification('Hackaton Status', 'Congratulations you are accepted to join our hackaton. Further information can be seen at your registered email.', user.id, ROLE['admin'])
				mail_template = EmailPurchase()
				template = mail_template.set_invoice_path(order.id).build()
				email = emailservice.set_recipient(user.email).set_subject('Congratulations!! you are accepted to join Indonesia Developer Summit 2017 hackaton').set_sender('noreply@devsummit.io').set_html(template).build()
				mail.send(email)
			else:
				result = None
				for item in items:
					for i in range(0, item.count):
						payload = {}
						payload['user_id'] = user.id
						payload['ticket_id'] = item.ticket_id
						result = UserTicketService().create(payload)
				if (result and (not result['error'])):
					mail_template = EmailPurchase()
					template = mail_template.set_invoice_path(order.id).build()
					email = emailservice.set_recipient(user.email).set_subject('Devsummit Ticket Invoice').set_sender('noreply@devsummit.io').set_html(template).build()
					mail.send(email)

			order_query.update({
				'updated_at': datetime.datetime.now(),
				'status': 'paid'
			})
			payment_query = db.session.query(Payment).filter_by(order_id=order.id)
			payment_query.update({
				'transaction_status': 'captured'
			})
			db.session.commit()
			send_notification = FCMService().send_single_notification('Payment Status', 'Your payment has been verified', user.id, ROLE['admin'])
			
			return response.set_data(None).set_message('ticket purchased').build()
		else:
			return response.set_data(None).set_error(True).set_message('This payment has already verified').build()


	def verify(self, id, request, hacker_team_name=None):
		response = ResponseBuilder()
		emailservice = EmailService()		
		orderverification_query = db.session.query(OrderVerification).filter_by(id=id)
		orderverification = orderverification_query.first()
		order = orderverification.order
		if orderverification.is_used is not 1:
			user_query = db.session.query(User).filter_by(id=orderverification.user_id)
			user = user_query.first()
			items = db.session.query(OrderDetails).filter_by(order_id=orderverification.order_id).all()
			url_invoice = request.url_root + '/invoices/'+ orderverification.order_id
			if items[0].ticket.type == TICKET_TYPES['exhibitor']:
				payload = {}
				payload['user_id'] = user.id
				payload['ticket_id'] = items[0].ticket_id
				UserTicketService().create(payload)
				self.create_booth(user, items[0].ticket.ticket_type)
				user_query.update({
					'role_id': ROLE['booth'],
					'updated_at': datetime.datetime.now()
				})
				redeem_payload = {}
				redeem_payload['ticket_id'] = items[0].ticket_id
				redeem_payload['codeable_id'] = user.id
				RedeemCodeService().purchase_user_redeems(redeem_payload)
				get_codes = db.session.query(RedeemCode).filter_by(codeable_type='user', codeable_id=user.id).all()
				mail_template = EmailPurchase()
				template = mail_template.set_invoice_path(order.id).set_redeem_code(get_codes).build()
				email = emailservice.set_recipient(user.email).set_subject('Congratulations !! you received exhibitor code').set_sender('noreply@devsummit.io').set_html(template).build()
				mail.send(email)
			elif items[0].ticket.type == TICKET_TYPES['hackaton']:
				payload = {}
				payload['user_id'] = user.id
				payload['ticket_id'] = items[0].ticket_id
				UserTicketService().create(payload)
				user_query.update({
					'role_id': ROLE['hackaton'],
					'updated_at': datetime.datetime.now()
				})
				send_notification = FCMService().send_single_notification('Hackaton Status', 'Congratulations you are accepted to join our hackaton. Further information can be seen at your registered email.', user.id, ROLE['admin'])
				mail_template = EmailPurchase()
				template = mail_template.set_invoice_path(order.id).build()
				email = emailservice.set_recipient(user.email).set_subject('Congratulations!! you are accepted to join Indonesia Developer Summit 2017 hackaton').set_sender('noreply@devsummit.io').set_html(template).build()
				mail.send(email)
			else:
				result = None
				for item in items:
					for i in range(0, item.count):
						payload = {}
						payload['user_id'] = user.id
						payload['ticket_id'] = item.ticket_id
						result = UserTicketService().create(payload)
				if (result and (not result['error'])):
					mail_template = EmailPurchase()
					template = mail_template.set_invoice_path(order.id).build()
					email = emailservice.set_recipient(user.email).set_subject('Devsummit Ticket Invoice').set_sender('noreply@devsummit.io').set_html(template).build()
					mail.send(email)

			orderverification_query.update({
				'is_used': 1,
				'updated_at': datetime.datetime.now()
			})
			payment_query = db.session.query(Payment).filter_by(order_id=orderverification.order_id)
			payment_query.update({
				'updated_at': datetime.datetime.now(),
				'transaction_status': 'captured'
			})
			completed_order = db.session.query(Order).filter_by(id=orderverification.order_id)
			completed_order.update({
				'updated_at': datetime.datetime.now(),
				'status': 'paid'
			})
			db.session.commit()
			send_notification = FCMService().send_single_notification('Payment Status', 'Your payment has been verified', user.id, ROLE['admin'])
			
			return response.set_data(None).set_message('ticket purchased').build()
		else:
			return response.set_data(None).set_error(True).set_message('This payment has already verified').build()

	def transformTimeZone(self, obj):
		entry = obj
		created_at_timezoned = datetime.datetime.strptime(entry['created_at'], "%Y-%m-%d %H:%M:%S") + datetime.timedelta(hours=LOCAL_TIME_ZONE)
		entry['created_at'] = str(created_at_timezoned).rsplit('.', maxsplit=1)[0] + " WIB"
		updated_at_timezoned = datetime.datetime.strptime(entry['updated_at'], "%Y-%m-%d %H:%M:%S") + datetime.timedelta(hours=LOCAL_TIME_ZONE)
		entry['updated_at'] = str(updated_at_timezoned).rsplit('.', maxsplit=1)[0] + " WIB"
		return entry

	def resend_order_email(self, payload):
		response = ResponseBuilder()
		emailservice = EmailService()
		mail_template = EmailPurchase()
		order = db.session.query(Order).filter_by(id=payload['order_id']).first()
		if order is None:
			return response.set_data(None).set_error(True).set_message('Order not found').build()
		# send email
		template = mail_template.set_invoice_path(order.id).build()
		email = emailservice.set_recipient(order.user.email).set_subject('Congratulations !! you received hackaton code').set_sender('noreply@devsummit.io').set_html(template).build()
		mail.send(email)
		return response.set_data(None).set_message('Email sent').build()