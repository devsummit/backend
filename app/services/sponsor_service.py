import datetime
from app.models import db
from sqlalchemy.exc import SQLAlchemyError
from app.configs.constants import SPONSOR_STAGES, SPONSOR_TYPES
# import model class
from app.models.sponsor import Sponsor
from app.models.sponsor_interaction_log import SponsorInteractionLog
from app.services.base_service import BaseService
from app.models.base_model import BaseModel
from app.builders.response_builder import ResponseBuilder


class SponsorService(BaseService):

    def __init__(self, perpage): 
        self.perpage = perpage

    def get(self, request):
        self.total_items = Sponsor.query.count()

        if request.args.get('page'):
            self.page = request.args.get('page')
        else:
            self.perpage = self.total_items
            self.page = 1
        self.base_url = request.base_url
        # paginate
        paginate = super().paginate(db.session.query(Sponsor))
        paginate = super().transform()
        response = ResponseBuilder()
        result = response.set_data(paginate['data']).set_links(paginate['links']).build()
        return result

    def get_logs(self, id):
        response = ResponseBuilder()
        logs = db.session.query(SponsorInteractionLog).filter_by(sponsor_id=id).all()
        return response.set_data(BaseModel.as_list(logs)).build()

    def post_log(self, payload, id):
        response = ResponseBuilder()
        log = SponsorInteractionLog()
        log.description = payload['description']
        log.sponsor_id = id
        db.session.add(log)
        try:
            db.session.commit()
            return response.set_data(log.as_dict()).set_message('logged').build()
        except SQLAlchemyError as e:
            data = e.orig.args
            return response.set_data(data).set_error(True).build()

    def show(self, id):
        response = ResponseBuilder()
        sponsor = db.session.query(Sponsor).filter_by(id=id).first()
        data = sponsor.as_dict() if sponsor else None
        if data:
            return response.set_data(data).build()
        return response.set_error(True).set_message('data not found').set_data(None).build()

    def create(self, payload):
        response = ResponseBuilder()
        sponsor = Sponsor()
        sponsor.name = payload['name']
        sponsor.phone = payload['phone']
        sponsor.email = payload['email']
        sponsor.note = payload['note']
        sponsor.stage = payload['stage'] if payload['stage'] else 1 # default to one as lead
        sponsor.type = payload['type'] or 4 if sponsor.stage == 3 else None # default to four if stage is official
        db.session.add(sponsor)

        try:
            db.session.commit()
            return response.set_data(sponsor.as_dict()).set_message('Data created succesfully').build()
        except SQLAlchemyError as e:
            data = e.orig.args
            return response.set_data(data).set_error(True).build()

    def update(self, id, payload):
        response = ResponseBuilder()
        sponsor = db.session.query(Sponsor).filter_by(id=id)
        data = sponsor.first().as_dict() if sponsor.first() else None
        if data is None:
            return response.set_error(True).set_message('data not found').set_data(None).build()
        if data['stage'] != payload['stage']:
            log = SponsorInteractionLog()
            _from = SPONSOR_STAGES[data['stage']] if data['stage'] else 'None'
            _to = SPONSOR_STAGES[payload['stage']] if payload['stage'] else 'None'
            log.description = 'Admin move stage from: ' + _from + ' to: ' + _to
            log.sponsor_id = id
            db.session.add(log)
        
        if (data['type'] != payload['type']):
            log = SponsorInteractionLog()
            _from = SPONSOR_TYPES[data['type']] if data['type'] else 'None'
            _to = SPONSOR_TYPES[payload['type']] if payload['type'] else 'None'
            log.description = 'Admin move stage from: ' + _from + ' to: ' + _to
            log.sponsor_id = id
            db.session.add(log)

        new_data = super().filter_update_payload(payload)        
        new_data['updated_at'] = datetime.datetime.now()
        sponsor.update(new_data)

        try:
            db.session.commit()
            return response.set_data(sponsor.first().as_dict()).build()

        except SQLAlchemyError as e:
            data = e.orig.args
            return response.set_data(data).set_error(True).build()

    def delete(self, id):
        response = ResponseBuilder()
        sponsor = db.session.query(Sponsor).filter_by(id=id)
        if sponsor.first():
            sponsor.delete()
            db.session.commit()
            return response.set_message('data deleted').set_data(None).build()
        return response.set_message('data not found').set_error(True).build()
