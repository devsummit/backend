import oauth2 as oauth
import json
import requests
import datetime
from app.models import db
from sqlalchemy.exc import SQLAlchemyError
from flask import request

from app.models.access_token import AccessToken
from app.models.user import User
from app.models.user_photo import UserPhoto
from app.models.booth import Booth  # noqa
from app.models.attendee import Attendee  # noqa
from app.models.speaker import Speaker  # noqa
from app.models.client import Client
from app.configs.constants import ROLE  # noqa
from werkzeug.security import generate_password_hash
from app.services.base_service import BaseService
from app.builders.response_builder import ResponseBuilder


class UserService(BaseService):

    def __init__(self, perpage): 
        self.perpage = perpage

    def register(self, payloads):
        role = int(payloads['role'])
        # payloads validation
        if (payloads is None) or (not isinstance(role, int)):
            return {
                'error': True,
                'data': 'payload not valid'
            }

        # check if social or email
        if payloads['social_id'] is not None:
            check_user = db.session.query(User).filter_by(
                social_id=payloads['social_id']).first()
        else:
            check_user = db.session.query(User).filter_by(
                email=payloads['email']).first()

        # check if user already exist
        if(check_user is not None):
            data = {
                'registered': True
            }
            return {
                'data': data,
                'message': 'User already registered',
                'error': True
            }

        self.model_user = User()
        self.model_user.first_name = payloads['first_name']
        self.model_user.last_name = payloads['last_name']
        self.model_user.email = payloads['email']
        self.model_user.username = payloads['username']
        self.model_user.role_id = role
        self.model_user.social_id = payloads['social_id']
        self.model_user.hash_password(payloads['password'])
        db.session.add(self.model_user)

        try:
            db.session.commit()
            data = self.model_user.as_dict()

            # insert role model
            if(role == ROLE['attendee']):
                attendee = Attendee()
                attendee.user_id = data['id']
                db.session.add(attendee)
                db.session.commit()
            elif(role == ROLE['booth']):
                booth = Booth()
                booth.user_id = data['id']
                db.session.add(booth)
                db.session.commit()
            elif(role == ROLE['speaker']):
                speaker = Speaker()
                speaker.user_id = data['id']
                db.session.add(speaker)
                db.session.commit()

            return {
                'error': False,
                'data': data,
                'message': 'user registered successfully'
            }
        except SQLAlchemyError as e:
            data = e.orig.args
            return {
                'error': True,
                'data': {'sql_error': True},
                'message': data
            }

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
        result = response.set_data(paginate['data']).set_links(paginate['links']).build()
        return result

    def get_user_by_id(self, id):
        user = db.session.query(
            User).filter_by(id=id).first()
        return user.include_photos().as_dict()

    def get_user(self, username):
        self.model_user = db.session.query(
            User).filter_by(username=username).first()
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
