from app.models import db
from sqlalchemy.exc import SQLAlchemyError
from app.models.entry_cash_log import EntryCashLog
from app.services.base_service import BaseService
from app.builders.response_builder import ResponseBuilder


class EntryCashLogService(BaseService):

    def __init__(self, perpage): 
        self.perpage = perpage

    def get(self, request):
        self.total_items = EntryCashLog.query.count()
        if request.args.get('page'):
            self.page = request.args.get('page')
        else:
            self.perpage = self.total_items
            self.page = 1
        self.base_url = request.base_url
        paginate = super().paginate(db.session.query(EntryCashLog))
        response = ResponseBuilder()
        result = response.set_data(paginate['data']).set_links(paginate['links']).build()
        return result

    def show(self, id):
        return db.session.query(EntryCashLog).filter_by(id=id).first()

    def update(self, payloads, entrycashlog_id):
        response = ResponseBuilder()
        if not isinstance(payloads['amount'], int) and not isinstance(payloads['description'], str):
            return response.set_error(True).set_status_code(400).set_message('payloads is invalid').build()

        try:
            self.model_entrycashlog = db.session.query(EntryCashLog).filter_by(id=entrycashlog_id)
            self.model_entrycashlog.update({
                'amount': payloads['amount'],
                'description': payloads['description']
            })
            db.session.commit()
            data = self.model_entrycashlog.first().as_dict()
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
        response = ResponseBuilder()
        if not isinstance(payloads['amount'], int) and not isinstance(payloads['description'], str):
            return response.set_error(True).set_status_code(400).set_data('payloads is invalid').build()

        self.model_entrycashlog = EntryCashLog()
        self.model_entrycashlog.amount = payloads['amount']
        self.model_entrycashlog.description = payloads['description']
        db.session.add(self.model_entrycashlog)

        try:
            db.session.commit()
            data = self.model_entrycashlog.as_dict()
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

    def delete(self, entrycashlog_id):
        self.model_entrycashlog = db.session.query(EntryCashLog).filter_by(id=entrycashlog_id)
        if self.model_entrycashlog.first() is not None:
            self.model_entrycashlog.delete()
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
