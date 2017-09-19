import datetime
import secrets
from app.models import db
from sqlalchemy.exc import SQLAlchemyError
from app.builders.response_builder import ResponseBuilder

from app.models.user import User
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