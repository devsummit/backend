from app.models import db
import os
from flask import current_app
from app.models.hacker_team import HackerTeam
from app.models.user_hacker import UserHacker
from sqlalchemy.exc import SQLAlchemyError
from werkzeug import secure_filename
from app.configs.constants import ROLE
from app.services.base_service import BaseService
from app.builders.response_builder import ResponseBuilder
from app.services.helper import Helper 

class HackatonService(BaseService):

    def get_team(self, user):
        response = ResponseBuilder()
        if user['role_id'] == ROLE['hackaton']:
            get_hacker_user = db.session.query(UserHacker).filter_by(user_id=user['id']).first()
            hackerteam = db.session.query(HackerTeam).filter_by(id=get_hacker_user.hacker_team_id).first()
            hackerusers = db.session.query(UserHacker).filter_by(hacker_team_id=hackerteam.id).all()
            data = hackerteam.as_dict()
            data['user'] = []
            if data['logo'] is not None:
                data['logo'] = Helper().url_helper(data['logo'], current_app.config['GET_DEST'])
            for hackeruser in hackerusers:
                user = hackeruser.user.include_photos().as_dict()
                data['user'].append(user)
            return response.set_data(data).set_message('Data retrieved successfully').build()

        
    def show(self, id):
        response = ResponseBuilder()
        hackerteam = db.session.query(HackerTeam).filter_by(id=id).first()
        hackerusers = db.session.query(UserHacker).filter_by(hacker_team_id=hackerteam.id).all()
        data = hackerteam.as_dict()
        data['user'] = []
        if data['logo'] is not None:
            data['logo'] = Helper().url_helper(data['logo'], current_app.config['GET_DEST'])
        for hackeruser in hackerusers:
             user = hackeruser.user.include_photos().as_dict()
             data['user'].append(user)
        return response.set_data(data).set_message('Data retrieved successfully').build()

    def get_all(Self):
        response = ResponseBuilder()
        hackerteams = db.session.query(HackerTeam).all()
        results = []
        for hackerteam in hackerteams:
            hackerusers = db.session.query(UserHacker).filter_by(hacker_team_id=hackerteam.id).all()
            data = hackerteam.as_dict()
            data['user'] = []
            if data['logo'] is not None:
                data['logo'] = Helper().url_helper(data['logo'], current_app.config['GET_DEST'])
            for hackeruser in hackerusers:
                user = hackeruser.user.include_photos().as_dict()
                data['user'].append(user)
            results.append(data)
        return response.set_data(results).set_message('Data retrieved successfully').build()
        
    def update_team(self, payloads, id):
        response = ResponseBuilder()
        try:
            hackatonteam = db.session.query(HackerTeam).filter_by(id=id)
            hackatonteam.update({
                'name': payloads['name'],
                'project_name': payloads['project_name'],
                'project_url': payloads['project_url'],
                'theme': payloads['theme']
            })
            db.session.commit()
            data = hackatonteam.first().as_dict()
            if data['logo'] is not None:
                data['logo'] = Helper().url_helper(data['logo'], current_app.config['GET_DEST'])
            return response.set_data(data).set_message('Update data team success').build()
        except SQLAlchemyError as e:
            data = e.orig.args
            return response.set_error(True).set_data(data).set_message('Update Failed').build()

    def update_team_logo(self, payloads, id):
        response = ResponseBuilder()
        logo = self.save_file(payloads['logo']) if payloads['logo'] is not None else None
        try:
            hackatonteam = db.session.query(HackerTeam).filter_by(id=id)
            hackatonteam.update({
                'logo': logo
            })
            db.session.commit()
            data = hackatonteam.first().as_dict()
            return response.set_data(data).set_message('Update logo team success').build()
        except SQLAlchemyError as e:
            data = e.orig.args
            return response.set_error(True).set_data(data).set_message('Update Failed').build()
        
    def save_file(self, file, id=None):
        if file and Helper().allowed_file(file.filename, current_app.config['ALLOWED_EXTENSIONS']):
            filename = secure_filename(file.filename)
            filename = Helper().time_string() + "_" + file.filename.replace(" ", "_")
            file.save(os.path.join(current_app.config['POST_HACKER_TEAM_PIC_DEST'], filename))
            if id:
                temp_partner = db.session.query(Partner).filter_by(id=id).first()
                partner_photo = temp_partner.as_dict() if temp_partner else None
                if partner_photo is not None and partner_photo['photo'] is not None:
                    Helper().silent_remove(current_app.config['STATIC_DEST'] + partner_photo['photo'])
            return current_app.config['SAVE_HACKER_TEAM_PIC_DEST'] + filename
        else:
            return None