from app.controllers.base_controller import BaseController
from app.services import fcmservice


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
