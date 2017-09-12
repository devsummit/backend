from app.models import db
from sqlalchemy.exc import SQLAlchemyError
# import model class
from app.models.sponsor import Sponsor
from app.services.base_service import BaseService
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

    def show(self, id):
        response = ResponseBuilder()
        sponsor = db.session.query(Sponsor).filter_by(id=id).first()
        data = sponsor.as_dict()
        return response.set_data(data).build()

    def create(self, payload):
        response = ResponseBuilder()
        sponsor = Sponsor()
        sponsor.name = payload['name']
        sponsor.phone = payload['phone']
        sponsor.email = payload['email']
        sponsor.note = payload['note']
        sponsor.stage = 1 # default to one as lead
        db.session.add(sponsor)

        try:
            db.session.commit()
            return response.set_data(sponsor.as_dict()).set_message('Data created succesfully').build()
        except SQLAlchemyError as e:
            data = e.orig.args
            return response.set_data(data).set_error(True).build()
