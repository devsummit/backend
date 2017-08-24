from app.models import db
# import model class
from app.models.attendee import Attendee
from app.models.user import User


class AttendeeService():
    def get(self):
        attendees = db.session.query(Attendee).all()
        _attendees = []
        for attendee in attendees:
            data = attendee.as_dict()
            data['user'] = attendee.user.as_dict()
            _attendees.append(data)
        return _attendees

    def show(self, id):
        attendee = db.session.query(Attendee).filter_by(id=id).first()
        if attendee:
            attendee = attendee.as_dict()
            attendee['user'] = db.session.query(User).filter_by(
                id=attendee['user_id']).first().as_dict()
        else:
            attendee = {}
        return attendee
