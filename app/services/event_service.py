from app.models import db
from sqlalchemy.exc import SQLAlchemyError
from app.models.event import Event


class EventService:
    def __init__(self, events_model):
        self.events_model = events_model

    def index(self):
        events = db.session.query(Event).all()
        return self.events_model.as_list(events)

    def show(self, id):
        self.events_model = db.session.query(Event).filter_by(id=id).first()
        return self.events_model.as_dict()

    def create(self, payloads):
        try:
            information = payloads['information'] if 'information' in payloads else None
            title = payloads['title'] if 'title' in payloads else None

            self.events_model.information = information
            self.events_model.title = title

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

            new_event = {}
            if information:
                new_event["information"] = information
            if title:
                new_event["title"] = title

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
