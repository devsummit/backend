# parent class imports
from app.controllers.base_controller import BaseController
from app.services import userservice
import requests


class UserAuthorizationController(BaseController):
    # dsjfkl
    @staticmethod
    def refreshtoken(request):
        refresh_token = request.json['refresh_token'] if 'refresh_token' in request.json else None
        if refresh_token:
            id = userservice.check_refresh_token(refresh_token)
            if id:
                new_token = userservice.get_new_token(id)
                return BaseController.send_response_api({'access_token': new_token['data']['access_token'], 'refresh_token': new_token['data']['refresh_token']}, 'token successfully refreshed')
            return BaseController.send_response_api({'exist': False}, 'refresh token not exist')
        return BaseController.send_error_api(None, 'refresh token required')

    @staticmethod
    def login(request):
        provider = request.json['provider'] if 'provider' in request.json else None

        admin = request.json['admin'] if 'admin' in request.json else None
        if provider is None:
            username = request.json['username'] if 'username' in request.json else None
            password = request.json['password'] if 'password' in request.json else None
            if username and password:
                # check if user exist
                user = userservice.get_user(username)                

                if user is not None:
                    if admin is not None and admin:
                        if user.as_dict()['role_id'] != 1:
                            return BaseController.send_error_api({'unauthorized': True}, 'unauthorized, must be admin to access this page.')
                    if user.verify_password(password):
                        token = userservice.save_token()
                        user = user.include_photos().as_dict()
                        return BaseController.send_response_api({'access_token': token['data'].access_token, 'refresh_token': token['data'].refresh_token}, 'User logged in successfully', user)
                    else:
                        return BaseController.send_error_api({'wrong_credential': True}, 'wrong credentials')
                else:
                    return BaseController.send_error_api({'not_registered': True}, 'username not found')
            return BaseController.send_error_api({'payload_invalid': True}, 'username and password required')
        else:
            # social sign in
            social_token = request.json['token'] if 'token' in request.json else None

            if (social_token is None):
                return BaseController.send_error_api({'payload_invalid': True}, 'social token is missing.')

            if(provider == 'twitter'):
                token_secret = request.json['token_secret'] if 'token_secret' in request.json else None
                if (token_secret is None):
                    return BaseController.send_error_api({'payload_invalid': True}, 'token secret is missing.')
                user_social_id = userservice.social_sign_in(provider, social_token, token_secret)
            else:
                user_social_id = userservice.social_sign_in(provider, social_token)

            if (user_social_id is not None):
                user = userservice.check_social_account(
                    provider, user_social_id)
                if user is not None:
                    token = userservice.save_token(provider)
                    user = user.include_photos().as_dict()
                    return BaseController.send_response_api({'access_token': token['data'].access_token, 'refresh_token': token['data'].refresh_token}, 'User logged in successfully', user)
                else:
                    return BaseController.send_error_api({'not_registered': True}, 'user is not registered')
            else:
                return BaseController.send_error_api({'wrong_credential': True}, 'token is invalid')

    @staticmethod
    def register(request):
        provider = request.json['provider'] if 'provider' in request.json else None

        firstname = request.json['first_name'] if 'first_name' in request.json else None
        lastname = request.json['last_name'] if 'last_name' in request.json else ''
        email = request.json['email'] if 'email' in request.json else None
        # For mobile/number verification, Phone number is sent as user name
        username = request.json['username'] if 'username' in request.json else None
        role = request.json['role'] if 'role' in request.json else None
        password = request.json['password'] if 'password' in request.json else None
        social_id = request.json['social_id'] if 'social_id' in request.json else None

        # if social_id = None then normal registration

        if (provider == 'mobile'):
            token = request.json['token'] if 'token' in request.json else None

            if token is None:
                return BaseController.send_error_api({'payload_invalid': True}, 'payload not valid')

            url = 'https://graph.accountkit.com/v1.2/me/?access_token=' + token
            result = requests.get(url)
            payload = result.json()
            accountId = None
            if 'error' not in payload:
                accountId = payload['id'] if 'id' in payload else None
            else:
                return BaseController.send_error_api(None, 'error while validating token.')
            verified = (social_id == accountId)
            if verified:
                payloads = {
                    'first_name': firstname,
                    'last_name': lastname,
                    'username': username,
                    'role': role,
                    'password': '',
                    'social_id': social_id,
                    'email': email,
                }
        elif firstname and email and username and role and password:
            payloads = {
                'first_name': firstname,
                'last_name': lastname,
                'email': email,
                'username': username,
                'role': role,
                'password': password,
                'social_id': social_id
            }
        else:
            return BaseController.send_response_api({'payload_invalid': True}, 'payloads not valid')

        result = userservice.register(payloads)
        if not result['error']:
            return BaseController.send_response_api(result['data'], 'user succesfully registered')
        else:
            return BaseController.send_error_api(result['data'], result['message'])

    @staticmethod
    def change_name(request, user):
        firstname = request.json['first_name'] if 'first_name' in request.json else None
        lastname = request.json['last_name'] if 'last_name' in request.json else ''
        booth_info = request.json['booth_info'] if 'booth_info' in request.json else None
        speaker_job = request.json['speaker_job'] if 'speaker_job' in request.json else None
        speaker_summary = request.json['speaker_summary'] if 'speaker_summary' in request.json else None
        if firstname:
            payloads = {
                'first_name': firstname,
                'last_name': lastname,
                'booth_info': booth_info,
                'speaker_job': speaker_job,
                'speaker_summary': speaker_summary,
                'user': user
            }

        else:
            return BaseController.send_response_api(None, 'payloads not valid')
        result = userservice.change_name(payloads)
        if result['error']:
            return BaseController.send_error_api(result['data'], result['message'])
        else:
            return BaseController.send_response_api(result['data'], result['message'])

    @staticmethod
    def change_password(request, user):
        oldpassword = request.json['old_password'] if 'old_password' in request.json else None
        newpassword = request.json['new_password'] if 'new_password' in request.json else None

        if oldpassword and newpassword:
            payloads = {
                'old_password': oldpassword,
                'new_password': newpassword,
                'user': user
            }
        else:
            return BaseController.send_response_api(None, 'payloads not valid')
        result = userservice.change_password(payloads)
        if not result['error']:
            return BaseController.send_response_api(result['data'], 'password succesfully changed')
        else:
            return BaseController.send_error_api(None, result['data'])
