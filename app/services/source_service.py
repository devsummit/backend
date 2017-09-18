from app.models import db
from sqlalchemy.exc import SQLAlchemyError
from app.models.source import Source
from app.services.base_service import BaseService
from app.builders.response_builder import ResponseBuilder


class SourceService(BaseService):

    def get(self, request):
        sources = db.session.query(Source).all()
        results = []
        for source in sources:
            data = source.as_dict()
            results.append(data)
        response = ResponseBuilder()
        result = response.set_data(results).build()
        return result
    
    def create(self, payloads):
        response = ResponseBuilder()
        source = Source()
        source.account_number = payloads['account_number']
        source.bank = payloads['bank']
        source.alias = payloads['alias']
        db.session.add(source)
        try:
            db.session.commit()
            data = source.as_dict()
            return response.set_data(data).build()
        except SQLAlchemyError as e:
            data = e.orig.args
            return response.set_data(data).set_error(True).build()