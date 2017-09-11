from app.controllers.base_controller import BaseController
from app.services import attendeeservice


class AttendeeController(BaseController):
    @staticmethod
    def index(request):
        attendees = attendeeservice.get(request)
        return BaseController.send_response_api(attendees['data'], 'attendees retrieved successfully', {}, attendees['links'])

    @staticmethod
    def show(id):
        attendee = attendeeservice.show(id)
        if attendee is None:
            return BaseController.send_error_api(None, 'attendee not found')
        return BaseController.send_response_api(attendee, 'attendee retrieved succesfully')
