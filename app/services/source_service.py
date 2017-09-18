import datetime
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
    
    def update(self, payloads, id):
        response = ResponseBuilder()
        try:
            source = db.session.query(Source).filter_by(id=id)
            source.update({
                'account_number': payloads['account_number'],
                'bank': payloads['bank'],
                'alias': payloads['alias'],                
                'updated_at': datetime.datetime.now()
            })
            db.session.commit()
            data = source.first()
            return response.set_data(data.as_dict()).build()
        except SQLAlchemyError as e:
            data = e.orig.args
            return response.set_error(True).set_data(data).build()

    def show(self, id):
        response = ResponseBuilder()
        result = db.session.query(Source).filter_by(id=id).first()
        result = result.as_dict() if result else None
        return response.set_data(result).build()

    def delete(self, id):
        response = ResponseBuilder()
        source = db.session.query(Source).filter_by(id=id)
        if source.first() is not None:
            # delete row
            source.delete()
            db.session.commit()
            return response.set_message('data deleted').build()
        else:
            data = 'data not found'
            return response.set_data(None).set_message(data).set_error(True).build()