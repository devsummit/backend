from app.controllers.base_controller import BaseController
from app.models.base_model import BaseModel
from app.services import attendeeservice


class AttendeeController(BaseController):
    @staticmethod
    def index():
        attendees = attendeeservice.get()
        return BaseController.send_response_api(BaseModel.as_list(attendees), 'attendees retrieved successfully')
    
    @staticmethod
    def show(id):
        attendee = attendeeservice.show(id)
        if attendee is None:
            return BaseController.send_error_api(None, 'attendee not found')
        return BaseController.send_response_api(attendee.as_dict(), 'attendee retrieved succesfully')
