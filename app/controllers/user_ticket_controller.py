from app.controllers.base_controller import BaseController
from app.services import userticketservice


class UserTicketController(BaseController):

    @staticmethod
    def show(user_id):
        user_ticket = userticketservice.show(user_id)
        if user_ticket is None:
            return BaseController.send_error_api(None, 'ticket not found')
        return BaseController.send_response_api(user_ticket, 'tickets retrieved successfully')

    @staticmethod
    def update(user_id, request):
        ticket_id = request.json['ticket_id'] if 'ticket_id' in request.json else None
        receiver_id = request.json['receiver_id'] if 'receiver_id' in request.json else None
        if ticket_id and receiver_id:
            payloads = {
                'ticket_id': ticket_id,
                'receiver_id': receiver_id
            }
            result = userticketservice.update(user_id, payloads)
            if not result['error']:
                return BaseController.send_response_api(result['data'], 'user ticket succesfully updated')
            else:
                return BaseController.send_error_api(None, result['data'])
        else:
            return BaseController.send_error_api(None, "fields are not complete")
