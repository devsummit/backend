import datetime
import secrets
from app.models import db
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import and_
from app.builders.response_builder import ResponseBuilder

from app.models.redeem_code import RedeemCode
from app.models.base_model import BaseModel
from app.models.booth import Booth
from app.models.attendee import Attendee
from app.models.user_booth import UserBooth
from app.models.user_ticket import UserTicket
from app.models.partners import Partner
from app.models.user import User


class RedeemCodeService():

    def get(self):
        response = ResponseBuilder()
        entities = db.session.query(RedeemCode.codeable_id, RedeemCode.codeable_type).group_by(RedeemCode.codeable_id, RedeemCode.codeable_type).all()
        # redeem_codes = db.session.query(RedeemCode.codeable_type, RedeemCode.codeable_id).group_by(RedeemCode.codeable_type, RedeemCode.codeable_id).all()
        # print(redeem_codes)
        results = []
        for entity in entities:
            data = db.session.query(RedeemCode).filter(and_(RedeemCode.codeable_id.like(entity[0]), RedeemCode.codeable_type.like(entity[1]))).first()
            results.append(data)
        
        final_results = self.include_type_detail(results)

        return response.set_data(final_results).set_message("Redeem codes retrieved successfully").build()
    
    def include_type_detail(self, redeem_codes):
        results = []
        for redeem_code in redeem_codes:
            data = redeem_code.as_dict()
            if data['codeable_type'] == 'booth':
                booth = db.session.query(Booth).filter_by(id=data['codeable_id']).first()
                booth = booth.as_dict()
                data['booth'] = booth
                user = db.session.query(User).filter_by(id=data['booth']['user_id']).first()
                if user is not None:
                    user = user.as_dict()
                    data['user'] = user
            elif data['codeable_type'] == 'partner':
                partner = db.session.query(Partner).filter_by(id=data['codeable_id']).first()
                partner = partner.as_dict()
                data['partner'] = partner
            results.append(data)
        return results


    def filter(self, param):
        response = ResponseBuilder()
        redeem_codes = db.session.query(RedeemCode).filter(and_(RedeemCode.codeable_id.like(param['codeable_id']), RedeemCode.codeable_type.like(param['codeable_type']), RedeemCode.used.like(0))).all()
        results = self.include_type_detail(redeem_codes)

        return response.set_data(results).set_message("Redeem codes retrieved successfully").build()

    def show(self, id):
        response = ResponseBuilder()
        redeem_code = db.session.query(RedeemCode).filter_by(id=id).first()
        data = redeem_code.as_dict()
        if data['codeable_type'] == 'booth':
            booth = db.session.query(Booth).filter_by(id=data['codeable_id']).first()
            booth = booth.as_dict()
            data['booth'] = booth
            user = db.session.query(User).filter_by(id=data['booth']['user_id']).first()
            if user is not None:
                user = user.as_dict()
                data['user'] = user
        elif data['codeable_type'] == 'partner':
            partner = db.session.query(Partner).filter_by(id=data['codeable_id']).first()
            partner = partner.as_dict()
            data['partner'] = partner
        return response.set_data(data).set_message('Data retrieved successfully').build()

    def create(self, payloads):
        response = ResponseBuilder()
        codes = [r.code for r in db.session.query(RedeemCode.code).all()]
        for i in range(0, int(payloads['count'])):
            code = secrets.token_hex(3)
            while (code in codes):
                code = secrets.token_hex(3)
            self.model_redeem_code = RedeemCode()
            self.model_redeem_code.codeable_type = payloads['codeable_type']
            self.model_redeem_code.codeable_id = payloads['codeable_id']
            self.model_redeem_code.code = code
            self.model_redeem_code.used = False

            db.session.add(self.model_redeem_code)
            db.session.commit()
        return response.set_message('Redeem code created successfully').set_data(None).set_error(False).build()

    def update(self, code, user):
        response = ResponseBuilder()
        _result = {}
        _result['user'] = user
        raw_user = db.session.query(User).filter_by(id=user['id'])
        raw_redeem_code = db.session.query(RedeemCode).filter_by(code=code)
        if raw_redeem_code.first() is None:
            return response.set_data(None).set_error(True).set_message('code not found').build()
        redeem_code = raw_redeem_code.first().as_dict()
        if raw_user.first() is None:
            return response.set_data(None).set_error(True).set_message('user not found').build()
        if redeem_code['used'] == 1:
            return response.set_data(None).set_error(True).set_message('code already used').build()

        try:
            if redeem_code['codeable_type'] == 'partner':
                # become attendee
                attendee = Attendee()
                attendee.user_id = user['id']
                userticket = UserTicket()
                userticket.user_id = user['id']
                userticket.ticket_id = 1
                db.session.add(attendee)
                db.session.add(userticket)
                user['role_id'] = 2
                db.session.commit()
                _result['attendee'] = attendee.as_dict()
            elif redeem_code['codeable_type'] == 'booth':
                # get booth of the code
                booth = db.session.query(Booth).filter_by(id=redeem_code['codeable_id']).first().as_dict()
                # become member of booth
                user_booth = UserBooth()
                user_booth.user_id = user['id']
                user_booth.booth_id = booth['id']
                db.session.add(user_booth)
                user['role_id'] = 3
                db.session.commit()
                _result['booth'] = booth
            raw_redeem_code.update({
                'used': True
            })
            raw_user.update({
                'role_id': user['role_id']
            })
            db.session.commit()
            return response.set_data(_result).set_message('Redeem code updated successfully').set_error(False).build()
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
