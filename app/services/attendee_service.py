from app.models import db
# import model class
from app.models.attendee import Attendee


class AttendeeService():
    def get(self):
        attendees = db.session.query(Attendee).all()
        _attendees = []
        for attendee in attendees:
            data = attendee.as_dict()
            data['user'] = attendee.user.include_photos().as_dict()
            _attendees.append(data)
        return _attendees

    def show(self, id):
        attendee = db.session.query(Attendee).filter_by(id=id).first()
        data = attendee.as_dict()
        data['user'] = attendee.user.include_photos().as_dict()
        return data
