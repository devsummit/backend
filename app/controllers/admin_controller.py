from app.controllers.base_controller import BaseController
from app.services import fcmservice
from flask_mail import Message
from app.models import mail


class AdminController(BaseController):

    @staticmethod
    def send_single_notification(requests, user):
        message = requests.json['message'] if 'message' in requests.json else None
        receiver_id = requests.json['receiver_id'] if 'receiver_id' in requests.json else None
        attachment = requests.json['attachment'] if 'attachment' in requests.json else None
        type = requests.json['type'] if 'type' in requests.json else None
        if message and receiver_id and type:
            result = fcmservice.send_single_notification(type, message, receiver_id, user['id'])
        else:
            return BaseController.send_error_api(None, 'payload not valid')
        if result['error']:
            return BaseController.send_error_api(result['data'], result['message'])
        return BaseController.send_response_api(result['data'], result['message'])


    @staticmethod
    def broadcast_notification(requests, user):
        message = requests.json['message'] if 'message' in requests.json else None
        attachment = requests.json['attachment'] if 'attachment' in requests.json else None
        type = requests.json['type'] if 'type' in requests.json else None
        if message and type:
            result = fcmservice.broadcast_notification(type, message, user['id'])
        else:
            return BaseController.send_error_api(None, 'payload not valid')
        if result['error']:
            return BaseController.send_error_api(result['data'], result['message'])
        return BaseController.send_response_api(result['data'], result['message'])


    @staticmethod
    def send_email(request, user):
        body = request.json['body'] if 'body' in request.json else None
        recipient = request.json['recipient'] if 'recipient' in request.json else None
        title = request.json['title'] if 'title' in request.json else None
        email = Message(subject=title + '-' + user['first_name'] + ' ' + user['last_name'])
        email.recipients = [recipient]
        email.html = body
        try:
            mail.send(email)
            return BaseController.send_response_api({'email_sent': True}, 'email sent successfully to: ' + recipient)
        except Exception as e:
            return BaseController.send_error_api({'email_sent': False}, 'some error occured when sending email')
