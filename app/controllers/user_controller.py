from app.controllers.base_controller import BaseController
from app.services import userservice
import requests


class UserController(BaseController):
    @staticmethod
    def index(request):
        users = userservice.list_user(request)
        return BaseController.send_response_api(users['data'], 'users retrieved successfully', {}, users['links'])

    @staticmethod
    def show(id):
        user = userservice.get_user_by_id(id)
        if user is None:
            return BaseController.send_error_api(user['data'], user['message'])
        return BaseController.send_response_api(user['data'], user['message'])

    @staticmethod
    def delete(id):
        result = userservice.delete(id)
        if result['error']:
            return BaseController.send_error_api([], result['data'])
        return BaseController.send_response_api([], result['data'])

    @staticmethod
    def update(request, id):
        first_name = request.json['first_name'] if 'first_name' in request.json else None
        last_name = request.json['last_name'] if 'last_name' in request.json else None
        email = request.json['email'] if 'email' in request.json else None
        username = request.json['username'] if 'username' in request.json else None
        role_id = request.json['role_id'] if 'role_id' in request.json else None
        includes = request.json['includes'] if 'includes' in request.json else None
        if first_name and last_name and email and username and role_id:
            payloads = {
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'username': username,
                'role_id': role_id,
                'includes': includes
            }
        else:
            return BaseController.send_error_api(None, 'field is not complete')

        result = userservice.update(payloads, id)

        if not result['error']:
            return BaseController.send_response_api(result['data'], 'user succesfully updated')
        else:
            return BaseController.send_error_api(None, result['data'])

    @staticmethod
    def add(request):
        first_name = request.json['first_name'] if 'first_name' in request.json else None
        last_name = request.json['last_name'] if 'last_name' in request.json else ''
        email = request.json['email'] if 'email' in request.json else None
        username = request.json['username'] if 'username' in request.json else None
        role_id = request.json['role_id'] if 'role_id' in request.json else None
        includes = request.json['includes'] if 'includes' in request.json else None
        referal = request.json['referal'] if 'referal' in request.json else None

        if first_name and email and username and role_id:
            payloads = {
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'username': username,
                'role_id': role_id,
                'includes': includes,
                'referal': referal
            }
        else:
            return BaseController.send_error_api(None, 'field is not complete')

        result = userservice.add(payloads)

        if not result['error']:
            return BaseController.send_response_api(result['data'], 'user succesfully added')
        else:
            return BaseController.send_error_api(None, result['data'])

    @staticmethod
    def redeemreferal(request, id):
        referal = request.json['referal'] if 'referal' in request.json else None
        if referal:
            payloads = {
                'referal': referal
            }
        else:
            return BaseController.send_error_api(None, 'field is not complete')

        result = userservice.redeemreferal(payloads, id)
        if result['error']:
            return BaseController.send_error_api(result['data'], result['message'])
        else:
            return BaseController.send_response_api(result['data'], result['message'])

    @staticmethod
    def redeemcode(request, user):
        code = request.json['redeem_code'] if 'redeem_code' in request.json else None
        if (user['role_id'] != 7):
            return BaseController.send_error_api(None, 'you can no longer use the redeem functionality')
        if code:
            result = userservice.redeemcode(code, user)
            if result['error']:
                return BaseController.send_error_api(result['data'], result['message'])
            return BaseController.send_response_api(result['data'], result['message'])
        else:
            return BaseController.send_error_api(None, 'invalid payload')

    @staticmethod
    def password_require(request):
        username = request.json['username'] if 'username' in request.json else None
        password = request.json['password'] if 'password' in request.json else None
        if username and password:
            user = userservice.get_user(username)
            if user.verify_password(password):
                return BaseController.send_response_api(None, "Password match")
            else:
                return BaseController.send_error_api(None, "Password did not match")
        else:
            return BaseController.send_error_api(None, 'Password required')

    @staticmethod
    def send_confirmation_email(request):
        email = request.json['email'] if 'email' in request.json else None
        if email:
            user = userservice.get_user(email)
            if user is None:
                return BaseController.send_error_api(None, 'User not found, register first')
            if user.confirmed:
                return BaseController.send_response_api(None, 'This account has been confirmed, you can login now')
            userservice.send_confirmation_email(user)
            return BaseController.send_response_api(None, 'Confirmation email has been sent to %s' %(email))
        else:
            return BaseController.send_error_api(None, 'Email required')

    @staticmethod
    def send_reset_password(request):
        email = request.json['email'] if 'email' in request.json else None
        if email:
            user = userservice.get_user(email)
            if user is not None:
                userservice.send_reset_password_email(user)
                return BaseController.send_response_api(None, 'Send Reset Password to %s success, you can check your email now' %(email))
            else:
                return BaseController.send_error_api(None, 'Email not found, Please send email which registered into your account before')

    @staticmethod
    def reset_password(request):
        newpassword = request.json['new_password'] if 'new_password' in request.json else None
        confirmpassword = request.json['confirm_password'] if 'confirm_password' in request.json else None
        token = request.json['token'] if 'token' in request.json else None

        if newpassword and confirmpassword:
            if newpassword == confirmpassword:
                payloads = {
                    'new_password': newpassword,
                    'token': token
                }
                result = userservice.password_reset(payloads)

                if result['error']:
                    return BaseController.send_error_api(None, result['message'])
                return BaseController.send_response_api(None, result['message'])
            else:
                return BaseController.send_error_api(None, 'new password and confirm password didnt match')
        else:
            return BaseController.send_error_api(None, 'Payloads not complete')