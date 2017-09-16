from app.controllers.base_controller import BaseController
from app.services import notificationservice
from app.services import orderservice


class NotificationController(BaseController):
    @staticmethod
    def index():
        notifications = notificationservice.get()
        return BaseController.send_response_api(notifications['data'], notifications['message'])

    @staticmethod
    def show(id):
        notification = notificationservice.show(id)
        if notification['error']:
            return BaseController.send_error_api(notification['data'], notification['message'])
        return BaseController.send_response_api(notification['data'], notification['message'])

    @staticmethod
    def create(request, user_id):
        message = request.json['message'] if 'message' in request.json else None
        receiver_user_id = request.json['receiver_user_id'] if 'receiver_user_id' in request.json else 1
        sender_user_id = request.json['sender_user_id'] if 'sender_user_id' in request.json else None
        attachment = request.json['attachment'] if 'attachment' in request.json else None
        status = request.json['status'] if 'status' in request.json else None
        type = request.json['type'] if 'type' in request.json else None

        if receiver_user_id and sender_user_id and message and status and type:
            payload = {
                'message': message,
                'receiver_user_id': receiver_user_id,
                'sender_user_id': sender_user_id,
                'attachment': attachment,
                'status': status,
                'type': type
            }

        else:
            return BaseController.send_error_api(None, 'field is not complete')

        result = notificationservice.create(payload)

        if not result['error']:
            # orders
            return BaseController.send_response_api(result['data'], result['message'])
        else:
            return BaseController.send_error_api(result['data'], result['message'])
