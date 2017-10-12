import sys
from flask import current_app
from app.models import db
from app.models.attendee import Attendee  # noqa
from app.models.booth import Booth  # noqa
from app.models.speaker import Speaker  # noqa
from app.models.ambassador import Ambassador  # noqa
from app.models.user import User  #noqa
from app.models.sponsor import Sponsor #noqa
from app.models.panel_event import PanelEvent 
from app.services.helper import Helper 


class BaseService():

    def __init__(self, page=0, base_url='', total_items=0):
        self.page = page
        self.base_url = base_url
        self.total_items = total_items

    def paginate(self, query):
        results = query.paginate(int(self.page), int(self.perpage), False)
        self.paginated = {}
        links = {}

        links['prev'] = (self.base_url + '?page=' + str(results.prev_num)) if results.prev_num else None
        links['next'] = (self.base_url + '?page=' + str(results.next_num)) if results.next_num else None
        links['curr'] = self.base_url + '?page=' + str(self.page)
        links['total_items'] = self.total_items

        self.paginated['data'] = results.items
        self.paginated['links'] = links

        return self.paginated

    def include(self, fields):
        _results = []
        for item in self.paginated['data']:
            data = item.as_dict()
            for field in fields:
                data[field] = getattr(item, field).as_dict() if getattr(item, field) else None
            _results.append(data)
        self.paginated['data'] = _results
        return self.paginated

    def include_user(self):
        _results = []
        for item in self.paginated['data']:
            data = item.as_dict()
            data['user'] = item.user.include_photos().as_dict()
            _results.append(data)
        self.paginated['data'] = _results
        return self.paginated

    def include_sponsor(self):
        _results = []
        for item in self.paginated['data']:
            data = item.as_dict()
            if item.type is None or 'user' in item.type:
                data['user'] = item.user.include_photos().as_dict()
            elif 'sponsor' in item.type:
                sponsor = db.session.query(Sponsor).filter_by(id=item.sponsor_id).first()        
                data['user'] = sponsor.as_dict()
                if data['user']['attachment'] is not None:
                    data['user']['attachment'] = Helper().url_helper(data['user']['attachment'], current_app.config['GET_DEST'])
                else:
                    data['user']['attachment'] = 'https://museum.wales/media/40374/thumb_480/empty-profile-grey.jpg'
            _results.append(data)
        self.paginated['data'] = _results
        return self.paginated

    def include_events(self):
        _results = []
        for item in self.paginated['data']:
            data = item.as_dict()
            if item.type is None or 'discuss panel' in item.type:
                users = []
                panel_event = db.session.query(PanelEvent).filter_by(event_id=data['id']).all()
                for pe in panel_event:
                    users.append(pe.user.include_photos().as_dict())
                data['user'] = users
            else:
                data['user'] = item.user.include_photos().as_dict()
            _results.append(data)
        self.paginated['data'] = _results
        return self.paginated

    def outer_include(self, data, fields):
        entity_name = self.__class__.__name__.lower().replace('service', '')
        for field in fields:
            if field:
                base_model = getattr(sys.modules[__name__], field.title())
                Model = type(field, (base_model,), {})
                # since filter_by need an explicit keyword not an expression
                # we cannot do like this:
                # filter_by(eval(entity_name)=data['id'])
                # so we still have to apply it with condition
                if entity_name in ['user', 'userphoto']:
                    prep = db.session.query(Model).filter_by(user_id=data['id']).first()
                    data[field.lower()] = prep.as_dict() if prep else None
                # add other enitity filtering here like above if needed
                # if ...
        return data

    def transform(self):
        _results = []
        for item in self.paginated['data']:
            item = item.as_dict()
            _results.append(item)
        self.paginated['data'] = _results
        return self.paginated

    def filter_update_payload(self, payload):
        new_data = {}
        for key in payload:
            if payload[key] is not None:
                new_data[key] = payload[key]
        return new_data
