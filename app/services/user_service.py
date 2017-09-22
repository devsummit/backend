import oauth2 as oauth
import json
import requests
import datetime

from app.models import db
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import or_
from flask import request
from app.models.access_token import AccessToken
from app.models.user import User
from app.models.user_booth import UserBooth
from app.models.user_photo import UserPhoto
from app.models.booth import Booth  # noqa
from app.models.attendee import Attendee  # noqa
from app.models.speaker import Speaker  # noqa
from app.models.client import Client
from app.models.ambassador import Ambassador  # noqa
from app.models.redeem_code import RedeemCode  # noqa
from app.configs.constants import ROLE  # noqa
from werkzeug.security import generate_password_hash
from app.services.base_service import BaseService
from app.builders.response_builder import ResponseBuilder
from app.models.base_model import BaseModel
from app.services.user_ticket_service import UserTicketService
from app.services.fcm_service import FCMService


class UserService(BaseService):

	def __init__(self, perpage):
		self.perpage = perpage


	def get_booth_by_uid(self, user_id):
		response = ResponseBuilder()

		user_booth = db.session.query(UserBooth).filter_by(user_id=user_id).first()
		data = user_booth.booth.as_dict()
		members = db.session.query(UserBooth).filter_by(booth_id=data['id']).all()
		data['members'] = []

		for member in members:
			data['members'].append(member.user.include_photos().as_dict())

		return response.set_data(data).build()

	def register(self, payloads):
		response = ResponseBuilder()
		# payloads validation
		if payloads is None:
			return response.set_error(True).set_message('Payload not valid').build()

		# check if social or email
		if payloads['social_id'] is not None:
			check_user = db.session.query(User).filter_by(
				social_id=payloads['social_id']).first()
		else:
			check_user = db.session.query(User).filter_by(
				email=payloads['email']).first()

		# check if user already exist
		if(check_user is not None):
			return response.set_data(None).set_message('User already registered').set_error(True).build()

		# check referal limit
		check_referer = db.session.query(User).filter_by(
				referer=payloads['referer']).all()
		if check_referer is not None and len(BaseModel.as_list(check_referer)) >= 10:
			return response.set_data(None).set_message('Referal code already exceed the limit').set_error(True).build()

		if payloads['email'] is not None:
			try:
				self.model_user = User()
				self.model_user.first_name = payloads['first_name']
				self.model_user.last_name = payloads['last_name']
				self.model_user.email = payloads['email']
				self.model_user.username = payloads['username']
				self.model_user.role_id = payloads['role']
				self.model_user.social_id = payloads['social_id']
				self.model_user.referer = payloads['referer'] if check_referer else None
				if payloads['provider'] == 'email': 
					self.model_user.hash_password(payloads['password'])
				db.session.add(self.model_user)
				db.session.commit()
				data = self.model_user.as_dict()

				# checking referer add full day ticket if reach 10 counts
				if payloads['referer'] is not None:
					check_referer_count = db.session.query(User).filter_by(referer=payloads['referer']).all()
					if check_referer_count is not None and len(check_referer_count) > 0:
						referer_detail = db.session.query(User).filter_by(username=payloads['referer']).first().as_dict()
						count = len(check_referer_count)
						payload = {}
						payload['user_id'] = referer_detail['id']
						payload['ticket_id'] = 1						
						receiver_id = referer_detail['id']
						sender_id = 1
						# only send notification if count less than 10
						if count < 10:
							type = "Referral Notification"
							message = "%s has registered referring you, your total referals count is: %d" % (payloads['username'], count)
							FCMService().send_single_notification(type, message, receiver_id, sender_id)
						# else count==10, send notif and create new ticket
						else:
							type = "Free Ticket Notification"
							message = "Congratulation! You have been referred 10 times! You've got one free ticket, please check it on 'my ticket' menu"
							FCMService().send_single_notification(type, message, receiver_id, sender_id)
							UserTicketService().create(payload)

				return response.set_error(False).set_data(data).set_message('User created successfully').build()

			except SQLAlchemyError as e:
				data = e.orig.args
				return response.set_error(True).set_message('SQL error').set_data(data).build()

	def list_user(self, request, admin=False):
		self.total_items = User.query.count()
		if request.args.get('page'):
			self.page = request.args.get('page')
		else:
			self.perpage = self.total_items
			self.page = 1
		self.base_url = request.base_url if not admin else request.url_root + 'users'
		paginate = super().paginate(db.session.query(User))
		paginate = super().include(['role'])
		response = ResponseBuilder()
		result = response.set_data(paginate['data']).set_links(
			paginate['links']).build()
		return result

	def get_user_by_id(self, id):
		response = ResponseBuilder()
		user = db.session.query(
			User).filter_by(id=id).first()
		user = user.include_photos().as_dict()
		# add relation includes
		includes = ''
		if user['role_id'] != 1:
			for role, role_id in ROLE.items():
				if role_id == user['role_id']:
					includes = role.title()
		user = super().outer_include(user, [includes])
		return response.set_data(user).build()

	def get_user(self, param):
		self.model_user = db.session.query(
			User).filter(or_(User.username.like(param), User.email.like(param))).first()
		
		return self.model_user

	def get_user_photo(self, id):
		self.model_user_photo = db.session.query(
			UserPhoto).filter_by(user_id=id).first()
		url = ''
		if self.model_user_photo:
			url = request.url_root + 'static/' + \
				self.model_user_photo.as_dict()['url']
		return url

	def social_sign_in(self, provider, social_token, token_secret=''):
		if (provider == 'google'):
			# check token integrity
			try:
				# get client id
				google_endpoint = 'https://www.googleapis.com/oauth2/v3/tokeninfo?id_token=' + social_token
				result = requests.get(google_endpoint)
				payload = result.json()
				if 'error_description' in payload:
					return None
				else:
					return payload['sub']
			except:
				# Invalid token
				return None

		elif(provider == 'facebook'):
			# check token integrity
			try:
				CLIENT_ID = db.session.query(Client).filter_by(
					app_name=provider).first()
				facebook_endpoint = 'https://graph.facebook.com/debug_token?input_token=' + \
					social_token + '&access_token=' + \
					CLIENT_ID.client_id + '|' + CLIENT_ID.client_secret
				result = requests.get(facebook_endpoint)
				payload = result.json()
				if(payload['data']['is_valid']):
					userid = payload['data']['user_id']
				return userid
			except:
				return None
		elif(provider == 'twitter'):
			# check token integrity
			try:
				CLIENT_ID = db.session.query(Client).filter_by(
					app_name=provider).first()
				consumer = oauth.Consumer(
					key=CLIENT_ID.client_id, secret=CLIENT_ID.client_secret)
				access_token = oauth.Token(
					key=social_token, secret=token_secret)

				client = oauth.Client(consumer, access_token)
				account_endpoint = "https://api.twitter.com/1.1/account/verify_credentials.json"
				response, data = client.request(account_endpoint)
				payload = json.loads(data)
				if('id' in payload):
					userid = payload['id_str']
				else:
					return None
				# check if error exist in data
			except:
				return None
			return userid

		elif(provider == 'mobile'):
			# check token to grap fb server
			try:
				CLIENT_ID = db.session.query(Client).filter_by(
					app_name=provider).first()
				url = 'https://graph.accountkit.com/v1.2/me/?access_token=' + social_token
				result = requests.get(url)
				payload = result.json()
				accountId = None
				if 'error' not in payload:
					accountId = payload['id'] if 'id' in payload else None
				return accountId
			except:
				return None

	def check_social_account(self, provider, social_id):
		# check if social id exist in user table
		self.model_user = db.session.query(
			User).filter_by(social_id=social_id).first()
		if self.model_user is not None:
			# user with social_id exist
			# return the user
			return self.model_user
		else:
			return None

	def save_token(self, provider='password_grant'):
		token_exist = db.session.query(AccessToken).filter_by(
			user_id=self.model_user.id).first()
		if not token_exist:
			self.model_access_token = AccessToken()
			payload = self.model_access_token.init_token(self.model_user.generate_auth_token(
			), self.model_user.generate_refresh_token(), self.model_user.id)
			db.session.add(payload)
			db.session.commit()
			return {
				'error': False,
				'data': payload
			}
		token_exist.access_token = self.model_user.generate_auth_token()
		token_exist.refresh_token = self.model_user.generate_refresh_token()
		# get id of client app
		client = db.session.query(Client).filter_by(app_name=provider).first()
		token_exist.client_id = client.id

		db.session.commit()
		return{
			'error': True,
			'data': token_exist
		}

	def change_name(self, payloads):
		response = ResponseBuilder()
		try:
			self.model_user = db.session.query(
				User).filter_by(id=payloads['user']['id'])
			self.model_user.update({
				'first_name': payloads['first_name'],
				'last_name': payloads['last_name'],
				'updated_at': datetime.datetime.now()
			})
			db.session.commit()
			data = self.model_user.first().as_dict()
			if (data['role_id'] is ROLE['booth']):
				booth = db.session.query(Booth).filter_by(user_id=payloads['user']['id'])
				if payloads['booth_info'] is not None:
					booth.update({
						'summary': payloads['booth_info']
					})
					db.session.commit()
				data['booth'] = booth.first().as_dict()
			elif data['role_id'] is ROLE['speaker']:
				speaker = db.session.query(Speaker).filter_by(user_id=payloads['user']['id'])
				if payloads['speaker_job'] is not None and payloads['speaker_summary'] is not None:
					speaker.update({
						'job': payloads['speaker_job'],
						'summary': payloads['speaker_summary']	
					})
					db.session.commit()
				data['speaker'] = speaker.first().as_dict()

			return response.set_data(data).build()
		except SQLAlchemyError as e:
			data = e.orig.args
			return response.set_error(True).set_message(data).build()

	def change_password(self, payloads):
		user = self.get_user(payloads['user']['username'])
		try:
			if user.verify_password(payloads['old_password']):
				self.model_user = db.session.query(
					User).filter_by(id=payloads['user']['id'])
				self.model_user.update({
					'password': generate_password_hash(payloads['new_password']),
					'updated_at': datetime.datetime.now()
				})
				db.session.commit()
				data = self.model_user.first().as_dict()
				return {
					'error': False,
					'data': data
				}
			return {
				'error': True,
				'data': "Invalid password"
			}
		except SQLAlchemyError as e:
			data = e.orig.args
			return {
				'error': True,
				'data': data
			}

	def check_refresh_token(self, refresh_token):
		refresh_token_exist = db.session.query(AccessToken).filter_by(
			refresh_token=refresh_token).first()
		if refresh_token_exist:
			id = refresh_token_exist.as_dict()['id']
			return id
		return None

	def get_new_token(self, id):
		try:
			self.model_access_token = db.session.query(
				AccessToken).filter_by(id=id)
			users = db.session.query(User).filter_by(
				id=self.model_access_token.first().as_dict()['user_id']).first()
			self.model_access_token.update({
				'access_token': users.generate_auth_token().decode(),
				'refresh_token': users.generate_refresh_token(),
				'updated_at': datetime.datetime.now()
			})
			db.session.commit()
			data = self.model_access_token.first().as_dict()
			return {
				'error': False,
				'data': data
			}
		except SQLAlchemyError as e:
			data = e.orig.args
			return {
				'error': True,
				'data': data
			}

	def delete(self, id):
		self.model_user = db.session.query(User).filter_by(id=id)
		temp_model = self.model_user.first().as_dict() if self.model_user.first() else None

		error = True
		data = ''

		if temp_model is not None:
			if temp_model['role_id'] in [ROLE['admin'], ROLE['speaker'], ROLE['booth']]:
				self.model_user.delete()
				db.session.commit()
				error = False
				data = 'The account has been deleted!'
			else:
				data = 'Attendee account, cannot be deleted!'
		else:
			data = 'User account not found'

		return {
			'error': error,
			'data': data
		}

	def update(self, payloads, id):
		try:
			self.model_user = db.session.query(
				User).filter_by(id=id)
			self.model_user.update({
				'first_name': payloads['first_name'],
				'last_name': payloads['last_name'],
				'email': payloads['email'],
				'username': payloads['username'],
				'role_id': payloads['role_id']
			})
			db.session.commit()
			data = self.model_user.first().as_dict()

			# apply includes data
			if 'admin' not in payloads.values():
				includes = payloads['includes']
				self.editIncludes(includes)

			return {
				'error': False,
				'data': data
			}
		except SQLAlchemyError as e:
			data = e.orig.args
			return {
				'error': True,
				'data': data
			}

	def add(self, payloads):
		response = ResponseBuilder()
		try:
			self.model_user = User()
			self.model_user.first_name = payloads['first_name']
			self.model_user.last_name = payloads['last_name']
			self.model_user.email = payloads['email']
			self.model_user.username = payloads['username']
			self.model_user.role_id = payloads['role_id']
			db.session.add(self.model_user)
			db.session.commit()
			data = self.model_user.as_dict()

			# apply includes data if not admin (role_id != 1)
			if 'role_id' in payloads and payloads['role_id'] != 1:
				includes = payloads['includes']
				data = self.postIncludes(includes)
				return data

		except SQLAlchemyError as e:
			data = e.args
			return response.set_message(data).set_error(True).build()

	def include_role_data(self, user):
		if (user['role_id'] is ROLE['speaker']):
			user = super().outer_include(user, ['Speaker'])
		elif (user['role_id'] is ROLE['booth']):
			user = super().outer_include(user, ['Booth'])
		return user

	def postIncludes(self, includes):
		response = ResponseBuilder()
		user_id = self.model_user.as_dict()['id']
	
		entityModel = eval(includes['name'])()
		entityModel.user_id = user_id
		for key in includes:
			if key is not 'name':
				setattr(entityModel, key, includes[key])
		db.session.add(entityModel)
		try:
			db.session.commit()
			return response.set_data(None).build()
		except SQLAlchemyError as e:
			data = e.args
			return response.set_message(data).set_error(True).set_data(None).build()

	def editIncludes(self, includes):
		user_id = self.model_user.first().as_dict()['id']
		entityModel = db.session.query(eval(includes['name'])).filter_by(user_id=user_id)
		del includes['name']
		entity = entityModel.first()

		if (entity):
			entityModel.update(includes)
		else:
			entityModel = Model()
			entityModel.user_id = user_id
			for key in includes:
				setattr(entityModel, key, includes[key])
			db.session.add(entityModel)
		db.session.commit()

	def updatefcmtoken(self, token, user):
		response = ResponseBuilder()
		user = db.session.query(User).filter_by(id=user['id'])
		user.update({
			'fcmtoken': token
		})
		try:
			db.session.commit()
			return response.set_data(user.first().include_photos().as_dict()).build()
		except SQLAlchemyError as e:
			data = e.args
			return response.set_error(True).set_message(data).build()