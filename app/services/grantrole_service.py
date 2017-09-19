import datetime
import secrets
from app.models import db
from sqlalchemy.exc import SQLAlchemyError
from app.builders.response_builder import ResponseBuilder

from app.models.user import User
from app.models.attendee import Attendee
from app.models.booth import Booth
from app.models.speaker import Speaker
from app.models.ambassador import Ambassador
from app.models.base_model import BaseModel


class GrantroleService():
    
    def update(self, payloads, id):
        response = ResponseBuilder()
        try:
            self.model_grant_role = db.session.query(User).filter_by(id=id)
            self.model_grant_role.update({
                'role_id': payloads['role_id']
            })
            db.session.commit()
            data = self.model_grant_role.first().as_dict()
            return response.set_data(data).set_message('User updated successfully').set_error(False).build()

        except SQLAlchemyError as e:
            return response.set_data(e.orig.args).set_message('SQL error').set_error(True).build()
    
    
    def add_attendee(self, payloads):
        response = ResponseBuilder()
        self.attendee = Attendee()
        self.attendee.user_id = payloads['user_id']
        self.attendee.points = payloads['points']
        db.session.add(self.attendee)
        try:
            db.session.commit()
            data = self.attendee.as_dict()
            return response.set_data(data).build()
        except SQLAlchemyError as e:
            data = e.orig.args
            return response.set_data(data).set_error(True).build()
    
    def add_booth(self, payloads):
        response = ResponseBuilder()
        self.booth = Booth()
        self.booth.user_id = payloads['user_id']
        self.booth.stage_id = payloads['stage_id']
        self.booth.points = payloads['points']
        self.booth.summary = payloads['summary']
        db.session.add(self.booth)
        try:
            db.session.commit()
            data = self.booth.as_dict()
            return response.set_data(data).build()
        except SQLAlchemyError as e:
            data = e.orig.args
            return response.set_data(data).set_error(True).build()

    def add_speaker(self, payloads):
        response = ResponseBuilder()
        self.speaker = Speaker()
        self.speaker.user_id = payloads['user_id']
        self.speaker.job = payloads['job']
        self.speaker.summary = payloads['summary']
        self.speaker.information = payloads['information']
        db.session.add(self.speaker)
        try:
            db.session.commit()
            data = self.speaker.as_dict()
            return response.set_data(data).build()
        except SQLAlchemyError as e:
            data = e.orig.args
            return response.set_data(data).set_error(True).build()

    def add_ambassador(self, payloads):
        response = ResponseBuilder()
        self.ambassador = Ambassador()
        self.ambassador.user_id = payloads['user_id']
        self.ambassador.informations = payloads['infrormation']
        self.ambassador.institution = payloads['institution']
        db.session.add(self.ambassador)
        try:
            db.session.commit()
            data = self.ambassador.as_dict()
            return response.set_data(data).build()
        except SQLAlchemyError as e:
            data = e.orig.args
            return response.set_data(data).set_error(True).build()
            