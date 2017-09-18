import datetime
import secrets
from app.models import db
from sqlalchemy.exc import SQLAlchemyError
from app.builders.response_builder import ResponseBuilder

from app.models.redeem_code import RedeemCode
from app.models.base_model import BaseModel


class RedeemCodeService():

    def get(self):
        redeem_codes = db.session.query(RedeemCode).all()
        return redeem_codes

    def show(self, id):
        redeem_code = db.session.query(RedeemCode).filter_by(id=id).first()
        return redeem_code

    def create(self, payloads):
        response = ResponseBuilder()

        code = secrets.token_hex(3)
        codes = BaseModel.as_list(db.session.query(RedeemCode).all())
        while (code in codes):
            code = secrets.token_hex(3)

        self.model_redeem_code = RedeemCode()
        self.model_redeem_code.codeable_type = payloads['codeable_type']
        self.model_redeem_code.codeable_id = payloads['codeable_id']
        self.model_redeem_code.code = code
        self.model_redeem_code.count = payloads['count']
        db.session.add(self.model_redeem_code)

        try: 
            db.session.commit()
            data = self.model_redeem_code.as_dict()
            return response.set_message('Redeem code created successfully').set_data(data).set_error(False).build()
        except SQLAlchemyError as e:
            return response.set_data(e.orig.args).set_message('SQL error').set_error(True).build()

    def update(self, payloads, id):
        response = ResponseBuilder()
        try:
            self.model_redeem_code = db.session.query(RedeemCode).filter_by(id=id)
            self.model_redeem_code.update({
                'codeable_type': payloads['codeable_type'],
                'codeable_id': payloads['codeable_id'],
                'code': payloads['code'],
                'count': payloads['count'],
                'updated_at': datetime.datetime.now()
            })
            db.session.commit()
            data = self.model_redeem_code.first().as_dict()
            return response.set_data(data).set_message('Redeem code updated successfully').set_error(False).build()

        except SQLAlchemyError as e:
            return response.set_data(e.orig.args).set_message('SQL error').set_error(True).build()

    def delete(self, id):
        response = ResponseBuilder()
        self.model_redeem_code = db.session.query(RedeemCode).filter_by(id=id)
        if self.model_redeem_code.first() is not None:
            # delete row
            self.model_redeem_code.delete()
            db.session.commit()
            return response.set_data(None).set_message('redeem code delete successfully').set_error(False).build()
        else:
            return response.set_data(None).set_message('data not found').set_error(True).build()
