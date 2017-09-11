from app.models import db
from sqlalchemy.exc import SQLAlchemyError
from app.models.booth import Booth
from app.services.base_service import BaseService
from app.builders.response_builder import ResponseBuilder


class BoothService(BaseService):

    def __init__(self, perpage): 
        self.perpage = perpage

    def get(self, request):
        self.total_items = Booth.query.count()
        if request.args.get('page'):
            self.page = request.args.get('page')
        else:
            self.perpage = self.total_items
            self.page = 1
        self.base_url = request.base_url
        paginate = super().paginate(db.session.query(Booth))
        response = ResponseBuilder()
        result = response.set_data(paginate['data']).set_links(paginate['links']).build()
        return result

    def show(self, id):
        # get the booth id
        booth = db.session.query(Booth).filter_by(id=id).first()
        if booth is None:
            data = {
                'user_exist': True
            }
            return {
                'data': data,
                'error': True,
                'message': 'booth not found'
            }
        data = booth.as_dict()
        data['user'] = booth.user.include_photos().as_dict()
        data['stage'] = booth.stage.as_dict() if booth.stage else None
        return {
            'error': False,
            'data': data,
            'message': 'booth retrieved'
        }

    def update(self, payloads, booth_id):
        try:
            self.model_booth = db.session.query(Booth).filter_by(id=booth_id)
            self.model_booth.update({
                'stage_id': payloads['stage_id'],
                'points': payloads['points'],
                'summary': payloads['summary']
            })
            db.session.commit()
            data = self.model_booth.first().as_dict()
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

    def create(self, payloads):
        self.model_booth = Booth()
        self.model_booth.user_id = payloads['user_id']
        self.model_booth.stage_id = payloads['stage_id']
        self.model_booth.points = payloads['points']
        self.model_booth.summary = payloads['summary']
        db.session.add(self.model_booth)
        try:
            db.session.commit()
            data = self.model_booth.as_dict()
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

    def get_includes(self, booths):
        included = []
        if isinstance(booths, list):
            for booth in booths:
                temp = {}
                temp['user'] = booth.user.as_dict()
                temp['stage'] = booth.stage.as_dict()
                included.append(temp)

        else:
            temp = {}
            temp['user'] = booths.user.as_dict()
            temp['stage'] = booths.stage.as_dict()
            included.append(temp)
        return included
