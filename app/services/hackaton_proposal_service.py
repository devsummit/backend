import datetime
from flask import current_app, request
from app.models import db, mail
from app.models.email_templates.email_hackaton import EmailHackaton
from sqlalchemy.exc import SQLAlchemyError
from app.configs.constants import ROLE
from app.configs.settings import LOCAL_TIME_ZONE
from app.services.helper import Helper
from app.services.fcm_service import FCMService
from app.services.order_verification_service import OrderVerificationService
from app.services.base_service import BaseService
from app.services.email_service import EmailService
from app.builders.response_builder import ResponseBuilder
from app.models.hackaton_proposals import HackatonProposal
from app.models.order import Order


class HackatonProposalService(BaseService):

	def __init__(self):
		self.orderverificationservice = OrderVerificationService()

	def get(self, status):
		response = ResponseBuilder()
		results = db.session.query(HackatonProposal).filter_by(status=status).all()
		_results = []
		for result in results:
			data = result.as_dict()
			data = self.transformTimeZone(data)
			data['order'] = result.order.as_dict()
			data['user'] = result.order.user.include_photos().as_dict()
			_results.append(data)
		return response.set_data(_results).build()

	def get_except(self, status):
		response = ResponseBuilder()
		results = db.session.query(HackatonProposal).filter(HackatonProposal.status!=status).all()
		_results = []
		for result in results:
			data = result.as_dict()
			data = self.transformTimeZone(data)
			data['order'] = result.order.as_dict()
			data['user'] = result.order.user.include_photos().as_dict()
			_results.append(data)
		return response.set_data(_results).build()

	def create(self, payloads):
		response = ResponseBuilder()
		emailservice = EmailService()
		hackaton_proposal = HackatonProposal()
		hackaton_proposal.github_link = payloads['github_link']
		hackaton_proposal.order_id = payloads['order_id']
		hackaton_proposal.status = 'pending'
		db.session.add(hackaton_proposal)
		try:
			db.session.commit()
			mail_template = EmailHackaton()
			user = hackaton_proposal.order.user
			template = mail_template.build(user.first_name + ' ' + user.last_name)
			email = emailservice.set_recipient(hackaton_proposal.order.user.email).set_subject('Indonesia Developer Summit 2017 Hackathon').set_sender('noreply@devsummit.io').set_html(template).build()
			mail.send(email)
			return response.set_data(hackaton_proposal.as_dict()).set_message('proposal succesfully created').build()
		except SQLAlchemyError as e:
			data = e.orig.args
			return response.set_data(data).set_error(True).build()		

	def check_hackaton_proposal_exist(self, user_id):
		hackaton_proposal = db.session.query(HackatonProposal).join(Order).filter(Order.user_id == user_id).first()
		if hackaton_proposal:
			return True
		return False

	def deny(self, payloads):
		response = ResponseBuilder()
		hackaton_proposal = db.session.query(HackatonProposal).filter_by(order_id=payloads['order_id'])
		if hackaton_proposal.first() is None:
			return response.set_error(True).set_data(None).set_message('proposal not found').build()
		hackaton_proposal.update({
			'updated_at': datetime.datetime.now(),
			'status': 'denied'
		})
		try:
			db.session.commit()
			hackatonprop = hackaton_proposal.first()
			receiver = hackatonprop.order.user_id
			send_notification = FCMService().send_single_notification('Hackaton Status', 'Your proposal to join our hackaton has just been rejected, as this may be dissapointing to you, you can still purchase our ticket as attendee. See you there.', receiver, ROLE['admin'])
			return response.set_data(None).set_message('proposal succesfully denied').build()
		except SQLAlchemyError as e:
			data = e.orig.args
			return response.set_data(data).set_error(True).build()

	def verify(self, payloads):
		response = ResponseBuilder()
		hackaton_proposal = db.session.query(HackatonProposal).filter_by(order_id=payloads['order_id'])
		if hackaton_proposal.first() is None:
			return response.set_error(True).set_data(None).set_message('proposal not found').build()
		hackaton_proposal.update({
			'updated_at': datetime.datetime.now(),
			'status': 'verified'
		})
		try:
			db.session.commit()
			self.orderverificationservice.admin_verify(payloads['order_id'], request)
			return response.set_data(None).set_message('hackaton proposal succesfully accepted').build()
		except SQLAlchemyError as e:
			data = e.orig.args
			return response.set_data(data).set_error(True).build()

	def resend_email(self, payloads):
		response = ResponseBuilder()
		emailservice = EmailService()
		hackaton_proposal = db.session.query(HackatonProposal).filter(HackatonProposal.order_id == payloads['order_id']).first()
		if hackaton_proposal is None:
			return response.set_error(True).set_data(None).set_message('proposal not found').build()
		mail_template = EmailHackaton()
		user = hackaton_proposal.order.user
		template = mail_template.build(user.first_name + ' ' + user.last_name)
		email = emailservice.set_recipient(user.email).set_subject('Indonesia Developer Summit 2017 Hackathon').set_sender('noreply@devsummit.io').set_html(template).build()
		mail.send(email)
		return response.set_data(None).set_message('email has been sent to: ' + user.email).build()

	def transformTimeZone(self, obj):
		entry = obj
		created_at_timezoned = datetime.datetime.strptime(entry['created_at'], "%Y-%m-%d %H:%M:%S") + datetime.timedelta(hours=LOCAL_TIME_ZONE)
		entry['created_at'] = str(created_at_timezoned).rsplit('.', maxsplit=1)[0] + " WIB"
		updated_at_timezoned = datetime.datetime.strptime(entry['updated_at'], "%Y-%m-%d %H:%M:%S") + datetime.timedelta(hours=LOCAL_TIME_ZONE)
		entry['updated_at'] = str(updated_at_timezoned).rsplit('.', maxsplit=1)[0] + " WIB"
		return entry
