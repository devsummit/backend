from app.models import db
from sqlalchemy.exc import SQLAlchemyError
from app.models.access_token import AccessToken
from app.models.user import User


class UserService:

    def register(self, payloads):

        # payloads validation
        if not isinstance(payloads['role'], int):
            return {
                'error': True,
                'data': 'payload not valid'
            }

        self.model_user = User()
        self.model_user.first_name = payloads['first_name']
        self.model_user.last_name = payloads['last_name']
        self.model_user.email = payloads['email']
        self.model_user.username = payloads['username']
        self.model_user.role_id = payloads['role']
        self.model_user.hash_password(payloads['password'])
        db.session.add(self.model_user)

        try:
            db.session.commit()
            data = self.model_user.as_dict()
            return {
                'error': False,
                'data': data
            }
        except SQLAlchemyError as e:
            data = e.orig.args
            return {
                'error': True,
                'data': data
            }

    def get_user(self, username):
        self.model_user = db.session.query(
            User).filter_by(username=username).first()
        return self.model_user

    def save_token(self):
        token_exist = db.session.query(AccessToken).filter_by(
            user_id=self.model_user.id).first()
        if not token_exist:
            self.model_access_token = AccessToken()
            payload = self.model_access_token.init_token(self.model_user.generate_auth_token(
            ), self.model_user.generate_refresh_token(), self.model_user.id)
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
            'error': True,
            'data': token_exist
        }
