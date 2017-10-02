import datetime
from flask import current_app
from app.models import db
from sqlalchemy.exc import SQLAlchemyError
from app.models.feed_report import FeedReport
from app.models.feed import Feed
from app.models.user import User
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

    def admin_get(self, request):
        report_feeds = db.session.query(Feed,User).filter(Feed.user_id == User.id).all()
        spam = db.session.query(Feed,FeedReport,User).filter(FeedReport.feed_id == Feed.id).filter(FeedReport.user_id == User.id).filter(FeedReport.report_type == 'Spam').count()
        racism = db.session.query(Feed,FeedReport,User).filter(FeedReport.feed_id == Feed.id).filter(FeedReport.user_id == User.id).filter(FeedReport.report_type == 'Racism').count()
        results = []
        for feed, user in report_feeds:
            data = {
                'id': feed.id,
                'username': user.username,
                'message': feed.message,
                'report_type': {
                    'racism': racism,
                    'spam': spam,
                    'pornography': 0,
                    'violence': 1
                }
            }
            print(data)
            results.append(data)
        response = ResponseBuilder()
        result = response.set_data(results).build()
        return result

        # report_feeds = db.session.query(FeedReport,Feed,User).all()
        # report_feeds = db.session.query(Feed, FeedReport, User).join(FeedReport).join(Feed).join(User)
        # results = []
        # for report in report_feeds:
        #     # data = report.as_dict()
        #     print(report)
        #     results.append(report)
        # response = ResponseBuilder()
        # result = response.set_data(results).build()
        # return result
