from app.models import db
from sqlalchemy.exc import SQLAlchemyError
from app.models.entry_cash_log import EntryCashLog
from app.services.base_service import BaseService
from app.builders.response_builder import ResponseBuilder
from sqlalchemy.sql import func


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

    def get_by_filter(self, request):
        response = ResponseBuilder()
        data = []
        included = {}

        if 'filter' in request.args and request.args.get('filter') == 'source':
            cash_logs = db.session.query(EntryCashLog).all()

            for cash_log in cash_logs:
                cash_log_data = cash_log.as_dict()
                cash_log_data['source'] = cash_log.source.as_dict()
                data.append(cash_log_data)

            total_debit = int(EntryCashLog.query.with_entities(func.sum(EntryCashLog.debit)).scalar())
            total_credit = int(EntryCashLog.query.with_entities(func.sum(EntryCashLog.credit)).scalar())
            total = total_debit + total_credit
        elif 'filter' in request.args and request.args.get('filter') == 'date':
            date_from = request.json['date_from'] if 'date_from' in request.json else None
            date_to = request.json['date_to'] if 'date_to' in request.json else None
            total_debit = 0
            total_credit = 0

            cash_logs = db.session.query(EntryCashLog).filter(EntryCashLog.created_at.between(date_from, date_to)).all()

            for cash_log in cash_logs:
                cash_log_data = cash_log.as_dict()
                cash_log_data['source'] = cash_log.source.as_dict()
                data.append(cash_log_data)

                total_debit += cash_log_data['debit']
                total_credit += cash_log_data['credit']

            total = total_debit + total_credit
        else:
            return response.set_error(True).set_status_code(400).set_message('You need to specify filter').build()

        if data:
            included['total_debit'] = total_debit
            included['total_credit'] = total_credit
            included['total'] = total
        
        result = response.set_data(data).set_included(included).build()

        return result

    def show(self, id):
        return db.session.query(EntryCashLog).filter_by(id=id).first()
        
    def update(self, payloads, entrycashlog_id):
        response = ResponseBuilder()
        if not isinstance(payloads['debit'], int) and not isinstance(payloads['credit'], int) and not isinstance(payloads['description'], str):
            return response.set_error(True).set_status_code(400).set_message('payloads is invalid').build()

        try:
            self.model_entrycashlog = db.session.query(EntryCashLog).filter_by(id=entrycashlog_id)
            self.model_entrycashlog.update({
                'debit': payloads['debit'],
                'credit': payloads['credit'],
                'source_id': payloads['source_id'],
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
        if not isinstance(payloads['debit'], int) and not isinstance(payloads['credit'], int) and not isinstance(payloads['description'], str):
            return response.set_error(True).set_status_code(400).set_data('payloads is invalid').build()

        self.model_entrycashlog = EntryCashLog()
        self.model_entrycashlog.debit = payloads['debit']
        self.model_entrycashlog.credit = payloads['credit']
        self.model_entrycashlog.description = payloads['description']
        self.model_entrycashlog.source_id = payloads['source_id']
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
