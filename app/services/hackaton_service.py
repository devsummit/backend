from app.models import db
from app.models.hacker_team import HackerTeam
from app.models.user_hacker import UserHacker
from sqlalchemy.exc import SQLAlchemyError
from app.configs.constants import ROLE
from app.services.base_service import BaseService
from app.builders.response_builder import ResponseBuilder

class HackatonService(BaseService):

    def get_team(self, user):
        response = ResponseBuilder()
        if user['role_id'] == ROLE['hackaton']:
            get_hacker_user = db.session.query(UserHacker).filter_by(user_id=user['id']).first()
            hackerteam = db.session.query(HackerTeam).filter_by(id=get_hacker_user.hacker_team_id).first()
            hackerusers = db.session.query(UserHacker).filter_by(hacker_team_id=hackerteam.id).all()
            data = hackerteam.as_dict()
            data['user'] = []
            for hackeruser in hackerusers:
                user = hackeruser.user.include_photos().as_dict()
                data['user'].append(user)
            return response.set_data(data).set_message('Data retrieved successfully').build()
        if user['role_id'] == ROLE['admin']:
            hackerteams = db.session.query(HackerTeam).all()
            results = []
            for hackerteam in hackerteams:
                hackerusers = db.session.query(UserHacker).filter_by(hacker_team_id=hackerteam.id).all()
                data = hackerteam.as_dict()
                data['user'] = []
                for hackeruser in hackerusers:
                    user = hackeruser.user.include_photos().as_dict()
                    data['user'].append(user)
                results.append(data)
            return response.set_data(results).set_message('Data retrieved successfully').build()
        else:
            return response.set_data(None).set_message('Unauthorized').set_error(True).build()

