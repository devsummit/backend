import datetime
from flask import current_app
from app.models import db
from sqlalchemy.exc import SQLAlchemyError
from app.models.feed_report import FeedReport
from app.services.base_service import BaseService
from app.builders.response_builder import ResponseBuilder


class FeedReportService(BaseService):

    def __init__(self, perpage):
        self.perpage = perpage

    def get(self, request, page):
        self.total_items = FeedReport.query.count()
        if page is not None:
            self.page = request.args.get('page')
        else:
            self.perpage = 10
            self.page = 1
        self.base_url = request.base_url
        # paginate
        paginate = super().paginate(db.session.query(
            FeedReport).order_by(FeedReport.created_at.desc()))
        paginate = super().include_user()
        response = ResponseBuilder()
        return response.set_data(paginate['data']).set_links(paginate['links']).build()

    def show(self, id):
        response = ResponseBuilder()
        feed_report = db.session.query(FeedReport).filter_by(id=id).first()
        data = {}
        data = feed_report.as_dict() if feed_report else None
        data['user'] = feed_report.user.include_photos().as_dict()
        return response.set_data(data).build()

    def create(self, payloads):
        response = ResponseBuilder()
        feed_report = FeedReport()
        for key in payloads:
            setattr(feed_report, key, payloads[key])
        db.session.add(feed_report)
        try:
            db.session.commit()
            user = feed_report.user.include_photos().as_dict()
            del user['fcmtoken']
            data = feed_report.as_dict()
            data['user'] = user
            return response.set_data(data).build()
        except SQLAlchemyError as e:
            data = e.orig.args
            return response.set_data(data).set_error(True).build()
