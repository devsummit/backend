import datetime
from app.models import db
from sqlalchemy.exc import SQLAlchemyError
# import model class
from app.models.attendee import Attendee


class AttendeeService():
    def get(self):
        attendees = db.session.query(Attendee).all()
        return attendees
    
    def show(self, id):
        attendee = db.session.query(Attendee).filter_by(id=id).first()
        return attendee
