from app.models import db
from sqlalchemy.exc import SQLAlchemyError
from app.models.access_token import AccessToken
from app.models.user import User


class UserService:
    def __init__(self, model_user, model_access_token):
        self.model_user = model_user
        self.model_access_token = model_access_token

    def register(self, payloads):
        self.model_user.first_name = payloads['first_name']
        self.model_user.last_name = payloads['last_name']
        self.model_user.email = payloads['email']
        self.model_user.username = payloads['username']
        self.model_user.role = payloads['role']
        self.model_user.hash_password(payloads['password'])
        db.session.add(self.model_user)
        try:
            db.session.commit()
            return {
                'error': False,
                'data': self.model_user
            }
        except SQLAlchemyError as e:
            return {
                'error': True,
                'data': e.orig.args
            }

    def get_user(self, username):
        self.model_user = db.session.query(User).filter_by(username=username).first()
        return self.model_user

    def save_token(self):
        token_exist = db.session.query(AccessToken).filter_by(user_id=self.model_user.id).first()
        if not token_exist:
            payload = self.model_access_token.init_token(self.model_user.generate_auth_token(), self.model_user.generate_refresh_token(), self.model_user.id)            
            db.session.add(payload)
            db.session.commit()
            return {
                'error': False,
                'data': payload
            }
        token_exist.access_token = self.model_user.generate_auth_token()
        token_exist.refresh_token = self.model_user.generate_refresh_token()
        db.session.commit()
        return{
            'error': False,
            'data': token_exist
        }
