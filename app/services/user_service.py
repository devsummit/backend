from app.models import db
from sqlalchemy.exc import SQLAlchemyError


class UserService:
    def __init__(self, model):
        self.model = model

    def register(self, payloads):
        self.model.first_name = payloads['first_name']
        self.model.last_name = payloads['last_name']
        self.model.email = payloads['email']
        self.model.username = payloads['username']
        self.model.role = payloads['role']
        self.model.password = payloads['password']
        db.session.add(self.model)
        try:
            db.session.commit()
            return {
                'error': None,
                'data': self.model
            }
        except SQLAlchemyError as e:
            return {
                'error': True,
                'data': e.orig.args
            }
