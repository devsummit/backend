import datetime
from app.models import db
from sqlalchemy.exc import SQLAlchemyError
from app.models.user_feedback import UserFeedback
from app.services.base_service import BaseService
from app.builders.response_builder import ResponseBuilder


class UserFeedbackService(BaseService):

    def index(self):
        response = ResponseBuilder()
        user_feedbacks = db.session.query(UserFeedback).all()
        results = []
        if user_feedbacks:
            for feedback in user_feedbacks:
                data = feedback.as_dict()
                results.append(data)
        return response.set_data(results).set_message('User feedback entries retrieved successfully').build()

    def create(self, payloads):
        response = ResponseBuilder()
        userfeedback = UserFeedback()
        userfeedback.user_id = payloads['user_id']
        userfeedback.content = payloads['content']
        db.session.add(userfeedback)
        try:
            db.session.commit()
            data = userfeedback.as_dict()
            return response.set_data(data).build()
        except SQLAlchemyError as e:
            data = e.orig.args
            return response.set_data(data).set_error(True).build()
    
    def show(self, id):
        response = ResponseBuilder()
        result = db.session.query(UserFeedback).filter_by(id=id).first()
        result = result.as_dict()
        return response.set_data(result).set_message('User feedback retrieved successfully').build()

