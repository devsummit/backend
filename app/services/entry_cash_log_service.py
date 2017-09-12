from app.models import db
from sqlalchemy.exc import SQLAlchemyError
from app.models.entry_cash_log import EntryCashLog
from app.services.base_service import BaseService
from app.builders.response_builder import ResponseBuilder


class EntryCashLogService(BaseService):

    def index(self, request):
        entry_cash_logs = db.session.query(EntryCashLog).all()
        return entry_cash_logs