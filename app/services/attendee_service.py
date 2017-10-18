from app.models import db
# import model class
from app.models.attendee import Attendee
from app.services.base_service import BaseService
from app.builders.response_builder import ResponseBuilder


class AttendeeService(BaseService):

    def __init__(self, perpage): 
        self.perpage = perpage

    def get(self, request):
        self.total_items = Attendee.query.count()

        if request.args.get('page'):
            self.page = request.args.get('page')
        else:
            self.perpage = self.total_items
            self.page = 1
        self.base_url = request.base_url
        # paginate
        paginate = super().paginate(db.session.query(Attendee))
        paginate = super().include(['user'])
        response = ResponseBuilder()
        result = response.set_data(paginate['data']).set_links(paginate['links']).build()
        return result

    def show(self, id):
        attendee = db.session.query(Attendee).filter_by(id=id).first()
        data = attendee.as_dict()
        data['user'] = attendee.user.include_photos().as_dict()
        return data
