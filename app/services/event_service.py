from app.models import db
from sqlalchemy.exc import SQLAlchemyError
from app.models.event import Event
from app.services.base_service import BaseService
from app.builders.response_builder import ResponseBuilder


class EventService(BaseService):

    def __init__(self, perpage): 
        self.perpage = perpage

    def index(self, request):
        self.total_items = Event.query.count()
        if request.args.get('page'):
            self.page = request.args.get('page')
        else:
            self.perpage = self.total_items
            self.page = 1
        self.base_url = request.base_url
        paginate = super().paginate(db.session.query(Event))
        response = ResponseBuilder()
        result = response.set_data(paginate['data']).set_links(paginate['links']).build()
        return result

    def show(self, id):
        self.events_model = db.session.query(Event).filter_by(id=id)
        if self.events_model.first() is None:
            return {
                'error': True, 
                'data': None,
                'message': 'event not found'
            }
        data = self.events_model.first().as_dict()
        data['user'] = self.events_model.first().user.as_dict() if self.events_model.first().user else None
        return {
            'error': False,
            'data': data,
            'message': 'event retrieved succesfully'
        }

    def create(self, payloads):
        try:
            information = payloads['information'] if 'information' in payloads else None
            title = payloads['title'] if 'title' in payloads else None
            type = payloads['type'] if 'type' in payloads else None
            user_id = payloads['user_id'] if 'user_id' in payloads else None
            self.events_model = Event()
            self.events_model.information = information
            self.events_model.title = title
            self.events_model.type = type
            self.events_model.user_id = user_id

            db.session.add(self.events_model)
            db.session.commit()

            data = self.events_model.as_dict()

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

    def update(self, id, payloads):
        try:
            self.events_model = db.session.query(Event).filter_by(id=id)
            information = payloads['information'] if 'information' in payloads else None
            title = payloads['title'] if 'title' in payloads else None
            type = payloads['type'] if 'type' in payloads else None
            user_id = payloads['user_id'] if 'user_id' in payloads else None
            new_event = {}
            if information:
                new_event['information'] = information
            if title:
                new_event['title'] = title
            if type:
                new_event['type'] = type
            if user_id:
                new_event['user_id'] = user_id
            self.events_model.update(new_event)

            db.session.commit()
            data = self.events_model.first().as_dict()
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

    def delete(self, id):
        self.events_model = db.session.query(Event).filter_by(id=id)
        if self.events_model.first() is not None:
            # delete row
            self.events_model.delete()
            db.session.commit()
            return {
                'error': False,
                'data': None
            }
        else:
            data = 'data not found'
            return {
                'error': True,
                'data': data
            }
